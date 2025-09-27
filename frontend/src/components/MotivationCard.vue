<template>
  <div class="card motivation-card">
    <div class="card-header">
      <h2 class="text-xl font-bold">来自鼠鼠的问候</h2>
    </div>
    <div class="p-6 flex flex-col items-center justify-center h-3/4">
      <p class="text-2xl font-bold mb-4 text-center">{{ greeting }}</p>
      <div class="text-purple-300">今日完成度: {{ todayCompletion }}% → 目标 65%</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MotivationCard',
  props: {
    greeting: {
      type: String,
      default: '加载中...'
    },
    todayCompletion: {
      type: Number,
      default: 0
    }
  }
}
</script>