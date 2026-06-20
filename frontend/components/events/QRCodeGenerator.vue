<template>
  <div class="qr-code-generator">
    <div v-if="loading" class="flex items-center justify-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-gold"></div>
    </div>
    
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <p class="text-red-600">{{ error }}</p>
    </div>
    
    <div v-else class="space-y-4">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-primary-navy">QR Code Ticket</h3>
        <Button variant="ghost" size="sm" @click="downloadQR">
          Download
        </Button>
      </div>
      
      <div class="bg-white p-6 rounded-xl border border-gray-200 flex flex-col items-center">
        <div ref="qrContainer" class="mb-4"></div>
        
        <div class="text-center">
          <p class="font-semibold text-primary-navy">{{ ticket.eventName }}</p>
          <p class="text-sm text-gray-600">{{ ticket.ticketHolder }}</p>
          <p class="text-xs text-gray-500 mt-1">{{ ticket.ticketType }} • ${{ ticket.price }}</p>
        </div>
      </div>
      
      <div class="bg-primary-gray p-4 rounded-lg">
        <p class="text-sm font-medium text-primary-navy mb-2">Ticket Details</p>
        <div class="space-y-1 text-sm">
          <div class="flex justify-between">
            <span class="text-gray-600">Event:</span>
            <span class="font-medium">{{ ticket.eventName }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600">Date:</span>
            <span class="font-medium">{{ ticket.eventDate }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600">Time:</span>
            <span class="font-medium">{{ ticket.eventTime }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600">Location:</span>
            <span class="font-medium">{{ ticket.location }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600">Ticket ID:</span>
            <span class="font-medium font-mono">{{ ticket.id }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import QRCode from 'qrcode'
import Button from '~/components/ui/Button.vue'

interface Props {
  ticket: {
    id: string
    eventName: string
    eventDate: string
    eventTime: string
    location: string
    ticketHolder: string
    ticketType: string
    price: number
  }
}

const props = defineProps<Props>()

const loading = ref(true)
const error = ref('')
const qrContainer = ref<HTMLElement | null>(null)
let qrCodeInstance: any = null

const generateQRCode = async () => {
  try {
    loading.value = true
    error.value = ''
    
    // Create ticket data for QR code
    const ticketData = JSON.stringify({
      ticketId: props.ticket.id,
      eventName: props.ticket.eventName,
      holder: props.ticket.ticketHolder,
      type: props.ticket.ticketType,
      timestamp: Date.now()
    })
    
    // Generate QR code
    const qrCanvas = await QRCode.toCanvas(ticketData, {
      width: 200,
      margin: 2,
      color: {
        dark: '#1b2a4a',
        light: '#ffffff'
      },
      errorCorrectionLevel: 'H'
    })
    
    if (qrContainer.value) {
      qrContainer.value.innerHTML = ''
      qrContainer.value.appendChild(qrCanvas)
    }
    
    loading.value = false
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to generate QR code'
    loading.value = false
  }
}

const downloadQR = async () => {
  try {
    const ticketData = JSON.stringify({
      ticketId: props.ticket.id,
      eventName: props.ticket.eventName,
      holder: props.ticket.ticketHolder,
      type: props.ticket.ticketType,
      timestamp: Date.now()
    })
    
    const qrDataURL = await QRCode.toDataURL(ticketData, {
      width: 400,
      margin: 2,
      color: {
        dark: '#1b2a4a',
        light: '#ffffff'
      },
      errorCorrectionLevel: 'H'
    })
    
    const link = document.createElement('a')
    link.download = `ticket-${props.ticket.id}.png`
    link.href = qrDataURL
    link.click()
  } catch (err) {
    console.error('Failed to download QR code:', err)
  }
}

onMounted(() => {
  generateQRCode()
})

onUnmounted(() => {
  if (qrContainer.value) {
    qrContainer.value.innerHTML = ''
  }
})
</script>
