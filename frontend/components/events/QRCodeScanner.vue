<template>
  <div class="qr-code-scanner">
    <div v-if="loading" class="flex items-center justify-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-gold"></div>
    </div>
    
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <p class="text-red-600">{{ error }}</p>
    </div>
    
    <div v-else class="space-y-4">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-primary-navy">Scan QR Code</h3>
        <Button variant="ghost" size="sm" @click="toggleCamera">
          {{ cameraActive ? 'Stop Camera' : 'Start Camera' }}
        </Button>
      </div>
      
      <div class="bg-black rounded-xl overflow-hidden relative">
        <video ref="videoElement" class="w-full h-64 object-cover"></video>
        <div v-if="cameraActive" class="absolute inset-0 flex items-center justify-center">
          <div class="w-48 h-48 border-4 border-primary-gold rounded-lg opacity-50"></div>
        </div>
        <div v-if="!cameraActive" class="absolute inset-0 flex items-center justify-center bg-gray-900">
          <p class="text-white text-center px-4">Camera inactive. Click "Start Camera" to begin scanning.</p>
        </div>
      </div>
      
      <div v-if="scannedTicket" class="bg-green-50 border border-green-200 rounded-lg p-4">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div>
            <p class="font-semibold text-green-800">Ticket Scanned Successfully</p>
            <p class="text-sm text-green-600">{{ scannedTicket.eventName }}</p>
          </div>
        </div>
        
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span class="text-gray-600">Ticket Holder:</span>
            <span class="font-medium">{{ scannedTicket.ticketHolder }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600">Ticket Type:</span>
            <span class="font-medium">{{ scannedTicket.ticketType }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600">Status:</span>
            <span :class="scannedTicket.status === 'valid' ? 'text-green-600' : 'text-red-600'" class="font-medium">
              {{ scannedTicket.status }}
            </span>
          </div>
        </div>
        
        <div class="mt-4 flex gap-2">
          <Button v-if="scannedTicket.status === 'valid'" variant="primary" size="sm" @click="checkInTicket">
            Check In
          </Button>
          <Button variant="ghost" size="sm" @click="resetScanner">
            Scan Another
          </Button>
        </div>
      </div>
      
      <div v-if="scanError" class="bg-red-50 border border-red-200 rounded-lg p-4">
        <p class="text-red-600">{{ scanError }}</p>
        <Button variant="ghost" size="sm" @click="resetScanner" class="mt-2">
          Try Again
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import Button from '~/components/ui/Button.vue'

interface Props {
  eventId: string
}

const props = defineProps<Props>()

const emit = defineEmits(['checkIn', 'error'])

const loading = ref(true)
const error = ref('')
const cameraActive = ref(false)
const videoElement = ref<HTMLVideoElement | null>(null)
const scannedTicket = ref<any>(null)
const scanError = ref('')

let stream: MediaStream | null = null
let scanInterval: any = null

const startCamera = async () => {
  try {
    loading.value = true
    error.value = ''
    
    if (!videoElement.value) {
      throw new Error('Video element not found')
    }
    
    stream = await navigator.mediaDevices.getUserMedia({ 
      video: { facingMode: 'environment' } 
    })
    
    videoElement.value.srcObject = stream
    await videoElement.value.play()
    
    cameraActive.value = true
    loading.value = false
    
    // Start scanning
    startScanning()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to start camera'
    loading.value = false
  }
}

const stopCamera = () => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
    stream = null
  }
  
  if (scanInterval) {
    clearInterval(scanInterval)
    scanInterval = null
  }
  
  cameraActive.value = false
}

const toggleCamera = () => {
  if (cameraActive.value) {
    stopCamera()
  } else {
    startCamera()
  }
}

const startScanning = () => {
  // In a real implementation, you would use a QR code scanning library
  // For now, we'll simulate scanning with a timeout
  scanInterval = setInterval(() => {
    // Simulate QR code detection
    // In production, use a library like @zxing/library or html5-qrcode
  }, 1000)
}

const simulateScan = (ticketData: any) => {
  scannedTicket.value = ticketData
  scanError.value = ''
}

const checkInTicket = () => {
  if (scannedTicket.value) {
    emit('checkIn', scannedTicket.value)
    resetScanner()
  }
}

const resetScanner = () => {
  scannedTicket.value = null
  scanError.value = ''
}

onMounted(() => {
  loading.value = false
})

onUnmounted(() => {
  stopCamera()
})
</script>
