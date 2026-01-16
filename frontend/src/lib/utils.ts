import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

/**
 * Merge Tailwind CSS classes with clsx for conditional classes
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Format a number as a percentage string
 */
export function formatPercent(value: number, decimals = 1): string {
  return `${value.toFixed(decimals)}%`
}

/**
 * Format a temperature value with unit
 */
export function formatTemperature(celsius: number): string {
  return `${celsius.toFixed(1)}°C`
}

/**
 * Format pH value with descriptive label
 */
export function formatPh(value: number): { value: string; label: string } {
  const formatted = value.toFixed(1)
  let label: string

  if (value < 4.5) {
    label = 'Very Acidic'
  } else if (value < 5.5) {
    label = 'Acidic'
  } else if (value < 6.5) {
    label = 'Slightly Acidic'
  } else if (value < 7.5) {
    label = 'Neutral'
  } else {
    label = 'Alkaline'
  }

  return { value: formatted, label }
}

/**
 * Get mood quadrant label from valence/arousal
 */
export function getMoodLabel(valence: number, arousal: number): string {
  if (valence > 0.15 && arousal > 0.15) return 'Excited / Joyful'
  if (valence > 0.15 && arousal < -0.15) return 'Calm / Content'
  if (valence < -0.15 && arousal > 0.15) return 'Tense / Anxious'
  if (valence < -0.15 && arousal < -0.15) return 'Melancholic / Sad'
  return 'Neutral / Balanced'
}

/**
 * Get scent family recommendations based on mood
 */
export function getScentFamilies(valence: number, arousal: number): string[] {
  if (valence > 0.15 && arousal > 0.15) {
    return ['Citrus', 'Fresh', 'Fruity', 'Sparkling']
  }
  if (valence > 0.15 && arousal < -0.15) {
    return ['Woody', 'Floral', 'Musky', 'Amber']
  }
  if (valence < -0.15 && arousal > 0.15) {
    return ['Herbal', 'Green', 'Aquatic', 'Aromatic']
  }
  if (valence < -0.15 && arousal < -0.15) {
    return ['Resinous', 'Ambery', 'Earthy', 'Smoky']
  }
  return ['Woody', 'Aromatic', 'Floral', 'Balanced']
}

/**
 * Delay execution for specified milliseconds
 */
export function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

/**
 * Generate a unique ID
 */
export function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}

/**
 * Clamp a number between min and max
 */
export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max)
}

/**
 * Linear interpolation between two values
 */
export function lerp(start: number, end: number, t: number): number {
  return start + (end - start) * t
}

/**
 * Map a value from one range to another
 */
export function mapRange(
  value: number,
  inMin: number,
  inMax: number,
  outMin: number,
  outMax: number
): number {
  return ((value - inMin) * (outMax - outMin)) / (inMax - inMin) + outMin
}

/**
 * Debounce a function
 */
export function debounce<T extends (...args: unknown[]) => unknown>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null

  return (...args: Parameters<T>) => {
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

/**
 * Throttle a function
 */
export function throttle<T extends (...args: unknown[]) => unknown>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle = false

  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}

/**
 * Check if running on client side
 */
export const isClient = typeof window !== 'undefined'

/**
 * Check if running on server side
 */
export const isServer = !isClient

/**
 * Safely access localStorage
 */
export function getLocalStorage<T>(key: string, defaultValue: T): T {
  if (isServer) return defaultValue

  try {
    const item = localStorage.getItem(key)
    return item ? JSON.parse(item) : defaultValue
  } catch {
    return defaultValue
  }
}

/**
 * Safely set localStorage
 */
export function setLocalStorage<T>(key: string, value: T): void {
  if (isServer) return

  try {
    localStorage.setItem(key, JSON.stringify(value))
  } catch {
    console.warn(`Failed to set localStorage key: ${key}`)
  }
}

/**
 * Remove localStorage item
 */
export function removeLocalStorage(key: string): void {
  if (isServer) return

  try {
    localStorage.removeItem(key)
  } catch {
    console.warn(`Failed to remove localStorage key: ${key}`)
  }
}
