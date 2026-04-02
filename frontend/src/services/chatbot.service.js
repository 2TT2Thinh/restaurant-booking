// src/services/chatbot.service.js
import apiClient from '@/api/axios'

export const chatbotService = {
  /**
   * Send message to chatbot
   * @param {Array} messages - Array of { role: 'user'|'assistant', content: string }
   * @returns {Promise<string>} Reply text
   */
  async sendMessage(messages) {
    // Endpoint: POST /api/v1/chat/
    const response = await apiClient.post('/chat/', { messages })
    
    // Response: { data: "reply text" }
    return response.data.data
  }
}