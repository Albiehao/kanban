import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: Date): string {
  const month = date.getMonth() + 1
  const day = date.getDate()
  const weekDays = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"]
  const weekDay = weekDays[date.getDay()]
  return `${month}月${day}日 ${weekDay}`
}

export function formatDateShort(date: Date): string {
  const month = date.getMonth() + 1
  const day = date.getDate()
  return `${month}月${day}日`
}
