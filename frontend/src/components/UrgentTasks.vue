<template>
  <div class="card tasks-card">
    <div class="card-header">
      <h2 class="text-xl font-bold">今日紧急任务</h2>
    </div>
    <div class="overflow-auto" style="height: calc(100% - 63px);">
      <div v-if="urgentTasks.length === 0" class="p-6 text-center text-gray-400">
        暂无紧急任务
      </div>
      <div 
        v-for="task in urgentTasks" 
        :key="task.id" 
        class="task-item p-4 mb-3 border border-gray-700 rounded-lg bg-gray-800/30"
      >
        <div class="flex justify-between">
          <span class="font-medium">{{ task.title }}</span>
          <span class="text-xs flex items-center">
            <div 
              class="status-dot mr-2"
              :class="{
                'status-gray': task.status === 'NO/*6T_STARTED',
                'status-blue': task.status === 'IN_PROGRESS',
                'status-gradient': task.status === 'DONE'
              }"
            ></div>
            {{ formatStatus(task.status) }}
          </span>
        </div>
        <div class="text-sm text-gray-400 flex items-center mt-2">
          <span class="mr-1">⏱️</span>
          <template v-if="task.deadline">
            截止: {{ formatDate(task.deadline) }}
          </template>
          <template v-else>
            截止: 未设置
          </template>
          <span 
            class="ml-3 text-xs pill-badge"
            :class="getPriorityClass(task)"
          >
            {{ getPriorityText(task) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UrgentTasks',
  props: {
    urgentTasks: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    formatStatus(status) {
      switch(status) {
        case 'NOT_STARTED': return '未开始'
        case 'IN_PROGRESS': return '进行中'
        case 'DONE': return '已完成'
        default: return status
      }
    },
    formatDate(dateString) {
      if (!dateString) return '未设置'
      const date = new Date(dateString)
      const today = new Date()
      const tomorrow = new Date(today)
      tomorrow.setDate(tomorrow.getDate() + 1)
      
      if (date.toDateString() === today.toDateString()) {
        return '今日'
      } else if (date.toDateString() === tomorrow.toDateString()) {
        return '明日'
      } else {
        return `${date.getMonth() + 1}月${date.getDate()}日`
      }
    },
    getPriorityText(task) {
      // 根据截止日期和任务级别确定优先级
      if (!task.deadline) return '待定'
      
      const deadline = new Date(task.deadline)
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      
      // 计算距离截止日期的天数
      const diffTime = deadline - today
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays < 0) {
        return '已过期'
      } else if (diffDays === 0) {
        return '紧急'
      } else if (diffDays <= 2) {
        return '高优先级'
      } else if (diffDays <= 7) {
        return '重要'
      } else {
        return '普通'
      }
    },
    getPriorityClass(task) {
      // 根据截止日期和任务级别确定优先级样式
      if (!task.deadline) return ''
      
      const deadline = new Date(task.deadline)
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      
      // 计算距离截止日期的天数
      const diffTime = deadline - today
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays < 0) {
        return 'tag-red' // 已过期
      } else if (diffDays === 0) {
        return 'tag-red' // 紧急
      } else if (diffDays <= 2) {
        return 'tag-orange' // 高优先级
      } else if (diffDays <= 7) {
        return 'tag-blue' // 重要
      } else {
        return 'tag-green' // 普通
      }
    }
  }
}
</script>