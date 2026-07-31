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
  // Backend AI chat endpoint
  apiEndpoint: `${apiConfig.baseURL}/api/ai/chat`
}
