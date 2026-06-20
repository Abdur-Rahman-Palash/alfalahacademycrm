/**
 * Composable for Hijri date operations
 */
import { computed } from 'vue'
import { 
  gregorianToHijri, 
  formatHijriDate, 
  formatHijriDateArabic,
  isRamadan,
  isDhulHijjah,
  getCurrentHijriDate
} from '~/utils/hijri'

export function useHijriDate(date: Date = new Date()) {
  const hijriDate = computed(() => gregorianToHijri(date))
  
  const formattedHijri = computed(() => formatHijriDate(hijriDate.value))
  
  const formattedHijriArabic = computed(() => formatHijriDateArabic(hijriDate.value))
  
  const inRamadan = computed(() => isRamadan(date))
  
  const inDhulHijjah = computed(() => isDhulHijjah(date))
  
  const gregorianDate = computed(() => 
    date.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  )
  
  const dualDate = computed(() => ({
    gregorian: gregorianDate.value,
    hijri: formattedHijri.value,
    hijriArabic: formattedHijriArabic.value
  }))
  
  return {
    hijriDate,
    formattedHijri,
    formattedHijriArabic,
    inRamadan,
    inDhulHijjah,
    gregorianDate,
    dualDate
  }
}
