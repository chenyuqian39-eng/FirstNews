<template>
  <div class="ai-chat-container">
    <van-nav-bar title="AI Q&A" fixed />
    
    <div class="chat-content">
      <div class="messages-container" ref="messagesContainer">
        <div 
          v-for="(message, index) in messages" 
          :key="index" 
          :class="['message', message.role === 'user' ? 'user-message' : 'ai-message']"
        >
          <div class="message-content">
            <div v-if="message.role === 'assistant' && message.content === ''" class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <div v-else v-html="formatMessage(message.content)"></div>
          </div>
        </div>
      </div>
      
      <div class="input-container">
        <van-field
          v-model="userInput"
          rows="1"
          autosize
          type="textarea"
          placeholder="Please enter a question..."
          class="chat-input"
          @keypress.enter.prevent="sendMessage"
        />
        <van-button 
          type="primary" 
          class="send-button" 
          :disabled="isLoading || !userInput.trim()" 
          @click="sendMessage"
        >
          Send
        </van-button>
      </div>
    </div>
    
    <tab-bar />
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';
import TabBar from '../components/TabBar.vue';
import { showToast } from 'vant';
import * as marked from 'marked';
import DOMPurify from 'dompurify';
import { aiChatConfig } from '../config/api';

// Chat messages
const messages = ref([
  { role: 'assistant', content: 'Hello! I am your AI assistant. How can I help?' }
]);
const userInput = ref('');
const messagesContainer = ref(null);
const isLoading = ref(false);

// Get API settings from the config file
const apiEndpoint = ref(aiChatConfig.apiEndpoint);
const apiKey = ref(aiChatConfig.apiKey);
const model = ref(aiChatConfig.model);

// Format message content with Markdown support
const formatMessage = (content) => {
  if (!content) return '';
  // Parse Markdown with marked and sanitize HTML with DOMPurify
  return DOMPurify.sanitize(marked.parse(content));
};

// Send message
const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return;
  
  // Check API settings
  if (!apiKey.value || apiKey.value === 'your-api-key-here') {
    showToast('API key is not configured. Please contact the administrator');
    return;
  }
  
  // Add user message
  const userMessage = userInput.value.trim();
  messages.value.push({ role: 'user', content: userMessage });
  userInput.value = '';
  
  // Add AI message placeholder
  messages.value.push({ role: 'assistant', content: '' });
  
  // Scroll to bottom
  await nextTick();
  scrollToBottom();
  
  // Send request
  isLoading.value = true;
  try {
    await fetchAIResponse(userMessage);
  } catch (error) {
    console.error('Error fetching AI response:', error);
    // Update the last message with an error message
    messages.value[messages.value.length - 1].content = `Error occurred: ${error.message || 'Please check the network connection and API settings'}`;
  } finally {
    isLoading.value = false;
    await nextTick();
    scrollToBottom();
  }
};

// Get AI response using SSE
const fetchAIResponse = async (userMessage) => {
  const allMessages = messages.value
    .slice(0, -1) // Exclude the last empty assistant message
    .map(msg => ({ role: msg.role, content: msg.content }));
  
  try {
    const response = await fetch(apiEndpoint.value, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey.value}`,
        'X-DashScope-SSE': 'enable' // Add the SSE header required by Alibaba Cloud DashScope
      },
      body: JSON.stringify({
        model: model.value,
        messages: allMessages,
        stream: true
      })
    });
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.error?.message || `HTTP error! status: ${response.status}`);
    }
    
    // Handle SSE stream
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let aiResponse = '';
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6);
        if (data === '[DONE]') continue;
        
        try {
          const json = JSON.parse(data);
          // Adapt to Alibaba Cloud DashScope response format
          const content = json.choices?.[0]?.delta?.content || 
                         json.output?.text || 
                         json.choices?.[0]?.message?.content || '';
          if (content) {
            aiResponse += content;
            // Update the last message
            messages.value[messages.value.length - 1].content = aiResponse;
            await nextTick();
            scrollToBottom();
          }
        } catch (e) {
          console.error('Error parsing SSE data:', e);
        }
      }
    }
  }
  
  // If no content is received
  if (!aiResponse) {
    messages.value[messages.value.length - 1].content = 'Sorry, I could not generate a response. Please check the API settings or try again later.';
  }
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
};

// Scroll to bottom
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

// Watch message changes and auto-scroll
watch(messages, () => {
  nextTick(scrollToBottom);
}, { deep: true });

// Scroll to bottom when the component mounts
onMounted(() => {
  scrollToBottom();
});
</script>

<style scoped>
.ai-chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding-top: 46px;
  padding-bottom: 50px;
  box-sizing: border-box;
}

.chat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.message {
  margin-bottom: 10px;
  max-width: 80%;
}

.user-message {
  margin-left: auto;
}

.ai-message {
  margin-right: auto;
}

.message-content {
  padding: 10px;
  border-radius: 10px;
  word-break: break-word;
}

.user-message .message-content {
  background-color: #007aff;
  color: white;
}

.ai-message .message-content {
  background-color: #f2f2f2;
  color: #333;
}

.input-container {
  display: flex;
  padding: 10px;
  border-top: 1px solid #eee;
  background-color: #fff;
}

.chat-input {
  flex: 1;
  margin-right: 10px;
}

.send-button {
  align-self: flex-end;
}

/* Markdown styles */
.message-content pre {
  background-color: #f8f8f8;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
}

.message-content code {
  background-color: rgba(0, 0, 0, 0.05);
  padding: 2px 4px;
  border-radius: 3px;
}

.message-content img {
  max-width: 100%;
}

/* Typing indicator */
.typing-indicator {
  display: flex;
  padding: 5px;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  background-color: #999;
  border-radius: 50%;
  margin: 0 2px;
  display: inline-block;
  animation: bounce 1.5s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-5px);
  }
}

/* Markdown styles */
:deep(pre) {
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
}

:deep(code) {
  font-family: monospace;
  background-color: #f0f0f0;
  padding: 2px 4px;
  border-radius: 4px;
}

:deep(p) {
  margin: 8px 0;
}

:deep(ul), :deep(ol) {
  padding-left: 20px;
}

:deep(a) {
  color: #1989fa;
  text-decoration: none;
}
</style>