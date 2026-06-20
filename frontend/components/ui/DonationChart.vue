<template>
  <div class="h-64">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import Chart from 'chart.js/auto'

const chartCanvas = ref<HTMLCanvasElement | null>(null)
let chartInstance: Chart | null = null

onMounted(() => {
  if (chartCanvas.value) {
    const ctx = chartCanvas.value.getContext('2d')
    if (ctx) {
      chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
          datasets: [
            {
              label: 'Donations',
              data: [12000, 19000, 15000, 25000, 22000, 30000],
              borderColor: '#D4AF37',
              backgroundColor: 'rgba(212, 175, 55, 0.1)',
              borderWidth: 3,
              fill: true,
              tension: 0.4,
              pointBackgroundColor: '#D4AF37',
              pointBorderColor: '#fff',
              pointBorderWidth: 2,
              pointRadius: 5,
              pointHoverRadius: 7
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              backgroundColor: '#1e3a5f',
              titleColor: '#fff',
              bodyColor: '#fff',
              padding: 12,
              cornerRadius: 8,
              displayColors: false,
              callbacks: {
                label: function(context) {
                  return '$' + context.parsed.y.toLocaleString()
                }
              }
            }
          },
          scales: {
            x: {
              grid: {
                display: false
              },
              ticks: {
                color: '#6b7280',
                font: {
                  size: 12
                }
              }
            },
            y: {
              grid: {
                color: 'rgba(0, 0, 0, 0.05)'
              },
              ticks: {
                color: '#6b7280',
                font: {
                  size: 12
                },
                callback: function(value) {
                  return '$' + (value / 1000) + 'k'
                }
              }
            }
          },
          interaction: {
            intersect: false,
            mode: 'index'
          }
        }
      })
    }
  }
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy()
  }
})
</script>
