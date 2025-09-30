<template>
  <div class="card tasks-card">
    <div class="card-header">
      <h2 class="text-xl font-bold">今日紧急任务</h2>
    </div>
    <div class="task-list-container">
      <div v-if="urgentTasks.length === 0" class="p-6 text-center text-gray-400">
        暂无紧急任务
      </div>
      <div 
        v-for="task in urgentTasks" 
        :key="task.id" 
        class="task-item"
      >
        <div class="task-content">
          <div class="task-header">
            <div class="task-title">{{ task.title }}</div>
            <div class="task-status">
              <div 
                class="status-dot"
                :class="{
                  'status-not-started': task.status === 'NOT_STARTED',
                  'status-in-progress': task.status === 'IN_PROGRESS',
                  'status-done': task.status === 'DONE'
                }"
              ></div>
              <span class="status-text">{{ formatStatus(task.status) }}</span>
            </div>
          </div>
          <div class="task-footer">
            <div class="task-deadline">
              <span class="deadline-icon">⏱️</span>
              <template v-if="task.deadline">
                <span>截止: {{ formatDate(task.deadline) }}</span>
              </template>
              <template v-else>
                <span>截止: 未设置</span>
              </template>
            </div>
            <span 
              class="priority-badge"
              :class="getPriorityClass(task)"
            >
              {{ getPriorityText(task) }}
            </span>
          </div>
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
        return '高'
      } else if (diffDays <= 7) {
        return '中'
      } else {
        return '低'
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
        return 'bg-red-100 text-red-800' // 已过期
      } else if (diffDays === 0) {
        return 'bg-red-100 text-red-800' // 紧急
      } else if (diffDays <= 2) {
        return 'bg-red-100 text-red-800' // 高
      } else if (diffDays <= 7) {
        return 'bg-yellow-100 text-yellow-800' // 中
      } else {
        return 'bg-green-100 text-green-800' // 低
      }
    }
  }
}
</script>

<style scoped>
.tasks-card {
  background: rgba(49, 43, 70, 0.6);
  border-radius: 24px;
  border: 1px solid rgba(113, 89, 193, 0.4);
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.tasks-card::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 24px;
  padding: 1px;
  background: linear-gradient(90deg, #E38EFF 0%, #7E57C2 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, 
                linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.card-header {
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 1;
}

.task-list-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px 20px;
  position: relative;
  z-index: 1;
}

/* 自定义滚动条样式 */
.task-list-container::-webkit-scrollbar {
  width: 6px;
}

.task-list-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.task-list-container::-webkit-scrollbar-thumb {
  background: rgba(227, 142, 255, 0.5);
  border-radius: 3px;
}

.task-list-container::-webkit-scrollbar-thumb:hover {
  background: rgba(227, 142, 255, 0.7);
}

.task-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 12px;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
}

.task-item:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(227, 142, 255, 0.3);
  transform: translateY(-1px);
}

.task-item:last-child {
  margin-bottom: 0;
}

.task-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.task-title {
  flex: 1;
  font-weight: 600;
  color: #EAE9F1;
  font-size: 14px;
  line-height: 1.4;
  word-break: break-word;
}

.task-status {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-not-started {
  background-color: #9CA3AF;
}

.status-in-progress {
  background-color: #3B82F6;
}

.status-done {
  background-color: #10B981;
}

.status-text {
  font-size: 12px;
  color: #9CA3AF;
  white-space: nowrap;
}

.task-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.task-deadline {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #9CA3AF;
}

.deadline-icon {
  font-size: 12px;
}

.priority-badge {
  font-size: 11px;
  padding: 4px 8px;
  border-radius: 12px;
  font-weight: 500;
  white-space: nowrap;
}

/* 优先级颜色 */
.priority-badge.bg-red-100 {
  background: rgba(239, 68, 68, 0.2);
  color: #F87171;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.priority-badge.bg-yellow-100 {
  background: rgba(245, 158, 11, 0.2);
  color: #FBBF24;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.priority-badge.bg-green-100 {
  background: rgba(16, 185, 129, 0.2);
  color: #34D399;
  border: 1px solid rgba(16, 185, 129, 0.3);
}
</style>