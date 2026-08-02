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

export const thirdPartyNewsConfig = {
  // Third-party news API used by the frontend news feed
  baseURL: 'https://newsapi.org/v2',
  apiKey: 'b19388cd2c284d549fb16a4220a3624e',
  country: 'au',
  pageSize: 10
}
