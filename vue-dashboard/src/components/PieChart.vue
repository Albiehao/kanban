<template>
  <div class="pie-chart-container">
    <div class="chart-wrapper">
      <svg :width="size" :height="size" class="pie-chart">
        <!-- 定义渐变 -->
        <defs>
          <linearGradient v-for="(item, index) in data" :key="`gradient-${index}`" :id="`gradient-${index}`" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" :style="`stop-color:${item.color};stop-opacity:1`" />
            <stop offset="100%" :style="`stop-color:${item.color};stop-opacity:0.7`" />
          </linearGradient>
        </defs>
        
        <g v-for="(segment, index) in segments" :key="index">
          <path
            v-if="segment.path"
            :d="segment.path"
            :fill="`url(#gradient-${index})`"
            :stroke="'white'"
            :stroke-width="3"
            class="pie-segment"
            :style="{ '--segment-index': index }"
          />
        </g>
        
        <!-- 中心圆 -->
        <circle
          :cx="center"
          :cy="center"
          :r="centerRadius"
          fill="white"
          stroke="#e5e7eb"
          stroke-width="2"
          class="center-circle"
        />
        
        <!-- 中心文字 -->
        <text
          :x="center"
          :y="center - 4"
          text-anchor="middle"
          class="center-text"
        >
          总支出
        </text>
        <text
          :x="center"
          :y="center + 12"
          text-anchor="middle"
          class="center-value"
        >
          ¥{{ formatAmount(totalAmount) }}
        </text>
      </svg>
    </div>
    
    <!-- 图例 -->
    <div class="chart-legend">
      <div
        v-for="(item, index) in dataWithPercentage"
        :key="index"
        class="legend-item"
      >
        <div class="legend-indicator">
          <div
            class="legend-color"
            :style="{ backgroundColor: item.color }"
          ></div>
          <div class="legend-percentage">{{ item.percentage }}%</div>
        </div>
        <div class="legend-text">
          <div class="legend-label">{{ item.label }}</div>
          <div class="legend-value">¥{{ item.value }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

interface ChartData {
  label: string
  value: number
  color: string
}

interface Props {
  data: ChartData[]
  size?: number
}

const props = withDefaults(defineProps<Props>(), {
  size: 200
})

// 格式化金额
const formatAmount = (amount: number) => {
  return amount.toLocaleString('zh-CN', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  })
}

const center = computed(() => props.size / 2)
const radius = computed(() => props.size / 2 - 25)
const centerRadius = computed(() => props.size / 6)

const totalAmount = computed(() => {
  return props.data.reduce((sum, item) => sum + item.value, 0)
})

const segments = computed(() => {
  // 如果没有数据，返回空数组
  if (!props.data || props.data.length === 0) {
    return []
  }
  
  const total = totalAmount.value
  // 如果总数为0，返回空数组
  if (total === 0) {
    return []
  }
  
  let currentAngle = -Math.PI / 2 // 从顶部开始（12点方向）
  
  return props.data.map(item => {
    const percentage = item.value / total
    const angle = percentage * 2 * Math.PI
    const startAngle = currentAngle
    const endAngle = currentAngle + angle
    
    // 计算扇形路径
    const x1 = center.value + radius.value * Math.cos(startAngle)
    const y1 = center.value + radius.value * Math.sin(startAngle)
    const x2 = center.value + radius.value * Math.cos(endAngle)
    const y2 = center.value + radius.value * Math.sin(endAngle)
    
    const largeArcFlag = angle > Math.PI ? 1 : 0
    
    // 特殊处理：如果是完整的圆（100%），需要确保闭合
    const path = angle >= 2 * Math.PI - 0.0001
      ? // 完整圆形 - 从顶部开始绘制完整圆
        [
          `M ${center.value} ${center.value}`,
          `L ${center.value} ${center.value - radius.value}`,
          `A ${radius.value} ${radius.value} 0 1 1 ${center.value} ${center.value + radius.value}`,
          `A ${radius.value} ${radius.value} 0 1 1 ${center.value} ${center.value - radius.value}`,
          'Z'
        ].join(' ')
      : angle < 0.0001
      ? // 角度太小，不绘制
        ''
      : // 普通扇形
        [
          `M ${center.value} ${center.value}`,
          `L ${x1} ${y1}`,
          `A ${radius.value} ${radius.value} 0 ${largeArcFlag} 1 ${x2} ${y2}`,
          'Z'
        ].join(' ')
    
    currentAngle += angle
    
    return {
      color: item.color,
      path
    }
  })
})

// 为数据添加百分比
const dataWithPercentage = computed(() => {
  if (!props.data || props.data.length === 0) {
    return []
  }
  
  const total = totalAmount.value
  if (total === 0) {
    return []
  }
  
  return props.data.map(item => ({
    ...item,
    percentage: Math.round((item.value / total) * 100)
  }))
})
</script>

<style scoped>
.pie-chart-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  width: 100%;
}

.chart-wrapper {
  position: relative;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
  display: flex;
  justify-content: center;
  align-items: center;
}

.pie-chart {
  display: block;
}

.pie-segment {
  cursor: pointer;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.center-circle {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.center-text {
  font-size: 10px;
  font-weight: 500;
  fill: hsl(var(--foreground));
}

.center-value {
  font-size: 14px;
  font-weight: 700;
  fill: hsl(var(--foreground));
}


.chart-legend {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
}

.legend-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  min-width: 60px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.legend-percentage {
  font-size: 11px;
  font-weight: 600;
  color: hsl(var(--foreground));
  min-width: 30px;
}

.legend-text {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex: 1;
}

.legend-label {
  font-size: 12px;
  font-weight: 500;
  color: hsl(var(--foreground));
}

.legend-value {
  font-size: 12px;
  font-weight: 600;
  color: hsl(var(--foreground));
}
</style>
