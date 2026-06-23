/**
 * API configuration file
 * Contains the base API URL and API parameters required by the AI Q&A feature
 */

// Base API URL configuration
export const apiConfig = {
  // Backend API base URL
  baseURL: 'http://127.0.0.1:8000',
}

export const aiChatConfig = {
  // OpenAI API endpoint
  apiEndpoint: 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
  
  // API Key (Specified by the developer)
  apiKey: 'sk-9c4d89982a6a4bd3b7494d94751fe81c',
  
  // Model to use
  model: 'qwen3-max-preview'
}
