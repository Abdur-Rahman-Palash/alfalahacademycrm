/**
 * Hijri date utilities for the frontend
 * Simplified version without external dependencies
 */

import dayjs from 'dayjs'

export interface HijriDate {
  year: number
  month: number
  day: number
  monthName: string
  monthNameArabic: string
}

export const ISLAMIC_MONTHS: Record<number, string> = {
  1: 'Muharram',
  2: 'Safar',
  3: 'Rabi al-Awwal',
  4: 'Rabi al-Thani',
  5: 'Jumada al-Awwal',
  6: 'Jumada al-Thani',
  7: 'Rajab',
  8: "Sha'ban",
  9: 'Ramadan',
  10: 'Shawwal',
  11: "Dhul Qa'dah",
  12: 'Dhul Hijjah'
}

export const ISLAMIC_MONTHS_ARABIC: Record<number, string> = {
  1: 'محرم',
  2: 'صفر',
  3: 'ربيع الأول',
  4: 'ربيع الآخر',
  5: 'جمادى الأولى',
  6: 'جمادى الآخرة',
  7: 'رجب',
  8: 'شعبان',
  9: 'رمضان',
  10: 'شوال',
  11: 'ذو القعدة',
  12: 'ذو الحجة'
}

/**
 * Simple Hijri date approximation (for demo purposes)
 * In production, use a proper Hijri library or API
 */
export function gregorianToHijri(date: Date): HijriDate {
  // This is a rough approximation - replace with proper library in production
  const gregorianYear = date.getFullYear()
  const gregorianMonth = date.getMonth() + 1
  const gregorianDay = date.getDate()
  
  // Approximate conversion (Hijri year ~ Gregorian year - 578)
  const hijriYear = gregorianYear - 578
  const hijriMonth = (gregorianMonth + 2) % 12 || 12
  const hijriDay = gregorianDay
  
  return {
    year: hijriYear,
    month: hijriMonth,
    day: hijriDay,
    monthName: ISLAMIC_MONTHS[hijriMonth],
    monthNameArabic: ISLAMIC_MONTHS_ARABIC[hijriMonth]
  }
}

/**
 * Format Hijri date as string
 */
export function formatHijriDate(hijri: HijriDate): string {
  return `${hijri.day} ${hijri.monthName} ${hijri.year}`
}

/**
 * Format Hijri date in Arabic
 */
export function formatHijriDateArabic(hijri: HijriDate): string {
  return `${hijri.day} ${hijri.monthNameArabic} ${hijri.year}`
}

/**
 * Get current Hijri date
 */
export function getCurrentHijriDate(): HijriDate {
  return gregorianToHijri(new Date())
}

/**
 * Check if current date is in Ramadan (month 9)
 */
export function isRamadan(date: Date = new Date()): boolean {
  const hijri = gregorianToHijri(date)
  return hijri.month === 9
}

/**
 * Check if current date is in Dhul Hijjah (month 12)
 */
export function isDhulHijjah(date: Date = new Date()): boolean {
  const hijri = gregorianToHijri(date)
  return hijri.month === 12
}

/**
 * Get donation presets with Islamic significance
 */
export const ISLAMIC_DONATION_PRESETS = [
  { amount: 5, label: 'Daily Sadaqah', description: 'Small daily charity' },
  { amount: 30, label: 'Iftar', description: 'Feed a fasting person' },
  { amount: 100, label: 'Zakat Fitrah', description: 'Charity before Eid' },
  { amount: 313, label: 'Prophetic Number', description: 'Blessed amount' },
  { amount: 500, label: 'Generous Gift', description: 'Significant contribution' },
  { amount: 1000, label: 'Zakat Eligible', description: '2.5% of $40,000 savings' },
  { amount: 5000, label: 'Major Gift', description: 'Transformative impact' },
  { amount: 10000, label: 'Visionary', description: 'Legacy contribution' }
]

/**
 * Get Islamic greeting based on time
 */
export function getIslamicGreeting(): string {
  const hour = new Date().getHours()
  
  if (isRamadan()) {
    return 'Ramadan Mubarak'
  }
  
  if (hour < 12) {
    return 'Sabah al-khair'
  } else if (hour < 17) {
    return 'Masa al-khair'
  } else {
    return 'Masa al-noor'
  }
}
