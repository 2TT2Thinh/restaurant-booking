<template>
  <v-card rounded="xl" elevation="0" border class="d-flex flex-column chatbot-card">

    <!-- Header -->
    <v-card-title class="d-flex align-center gap-2 pa-4 border-b">
      <v-avatar color="primary" size="32" rounded="lg">
        <v-icon color="white" size="18">mdi-robot-outline</v-icon>
      </v-avatar>
      <span class="text-body-1 font-weight-bold">Booking Assistant</span>
      <v-spacer></v-spacer>
      <v-chip size="x-small" color="success" variant="tonal">Online</v-chip>
    </v-card-title>

    <!-- Message list -->
    <v-card-text ref="scrollRef" class="flex-grow-1 overflow-y-auto pa-4 message-list">
      <!-- Empty state -->
      <div v-if="messages.length === 0" class="d-flex flex-column align-center justify-center h-100 text-grey">
        <v-icon size="48" color="grey-lighten-2" class="mb-2">mdi-chat-outline</v-icon>
        <p class="text-body-2">Ask me to help find or book a restaurant!</p>
      </div>

      <!-- Message bubbles -->
      <div
        v-for="(msg, i) in messages"
        :key="i"
        class="d-flex mb-3"
        :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
      >
        <!-- Bot avatar -->
        <v-avatar
          v-if="msg.role === 'assistant'"
          color="primary"
          size="28"
          rounded="lg"
          class="mt-1 mr-2 flex-shrink-0"
        >
          <v-icon color="white" size="16">mdi-robot-outline</v-icon>
        </v-avatar>

        <v-sheet
          :color="msg.role === 'user' ? 'primary' : 'grey-lighten-4'"
          rounded="xl"
          class="pa-3 message-bubble"
          :class="msg.role === 'user' ? 'text-white bubble-user' : 'bubble-bot'"
          style="max-width: 75%; white-space: pre-wrap; word-break: break-word;"
        >
          <span class="text-body-2">{{ msg.content }}</span>
        </v-sheet>
      </div>

      <!-- Typing indicator -->
      <div v-if="loading" class="d-flex align-center gap-2 mb-3">
        <v-avatar color="primary" size="28" rounded="lg">
          <v-icon color="white" size="16">mdi-robot-outline</v-icon>
        </v-avatar>
        <v-sheet color="grey-lighten-4" rounded="xl" class="pa-3">
          <div class="typing-dots">
            <span></span><span></span><span></span>
          </div>
        </v-sheet>
      </div>
    </v-card-text>

    <!-- Input area -->
    <v-divider></v-divider>
    <v-card-actions class="pa-3">
      <v-text-field
        v-model="input"
        placeholder="Type a message..."
        variant="outlined"
        density="compact"
        rounded="lg"
        hide-details
        color="primary"
        class="flex-grow-1 mr-2"
        :disabled="loading"
        @keydown.enter.prevent="sendMessage"
      ></v-text-field>
      <v-btn
        icon
        color="primary"
        variant="flat"
        rounded="lg"
        size="40"
        :loading="loading"
        :disabled="!input.trim()"
        @click="sendMessage"
      >
        <v-icon size="18">mdi-send</v-icon>
      </v-btn>
    </v-card-actions>

  </v-card>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { chatbotService } from '@/services/chatbot.service'

// State
const input = ref('')
const loading = ref(false)
const scrollRef = ref(null)
const messages = ref([])

// Scroll to bottom when new message arrives
const scrollToBottom = async () => {
  await nextTick()
  const el = scrollRef.value?.$el ?? scrollRef.value
  if (el) {
    el.scrollTop = el.scrollHeight
  }
}

// Send message to chatbot
const sendMessage = async () => {
  const text = input.value.trim()
  if (!text || loading.value) return

  // Add user message
  messages.value.push({ role: 'user', content: text })
  input.value = ''
  await scrollToBottom()

  loading.value = true

  try {
    // Gửi toàn bộ lịch sử hội thoại
    const history = messages.value.map(m => ({ 
      role: m.role, 
      content: m.content 
    }))
    
    const reply = await chatbotService.sendMessage(history)
    
    messages.value.push({ role: 'assistant', content: reply })
  } catch (err) {
    console.error('Chat error:', err.response?.data || err.message)
    messages.value.push({
      role: 'assistant',
      content: 'Xin lỗi, tôi đang gặp sự cố. Vui lòng thử lại sau.',
    })
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}
</script>

<style scoped>
.chatbot-card {
  height: 520px;
}

.message-list {
  min-height: 0;
}

.message-bubble {
  line-height: 1.5;
}

.bubble-user {
  border-bottom-right-radius: 4px !important;
}

.bubble-bot {
  border-bottom-left-radius: 4px !important;
}

/* Typing animation dots */
.typing-dots {
  display: flex;
  align-items: center;
  gap: 4px;
  height: 18px;
}

.typing-dots span {
  display: inline-block;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background-color: #9e9e9e;
  animation: bounce 1.2s infinite ease-in-out;
}

.typing-dots span:nth-child(1) { animation-delay: 0s; }
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.7); opacity: 0.5; }
  40%           { transform: scale(1);   opacity: 1; }
}
</style>