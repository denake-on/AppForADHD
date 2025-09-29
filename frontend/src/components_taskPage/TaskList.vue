<template>
  <div class="task-list">
    <div 
      v-for="task in tasks" 
      :key="task.id" 
      class="task-item card"
    >
      <div class="task-info">
        <div class="task-checkbox">
          <input 
            type="checkbox" 
            :id="'task-' + task.id"
            :checked="task.status === 'done'"
            @change="toggleTaskStatus(task)"
          />
          <label :for="'task-' + task.id"></label>
        </div>
        
        <div class="task-details">
          <div class="task-title-container">
            <h3 :class="['task-title', { completed: task.status === 'done' }]">
              {{ task.title }}
            </h3>
            <span class="task-status" :class="task.status">
              {{ getStatusText(task.status) }}
            </span>
          </div>
          <p class="task-description">{{ task.description }}</p>
          
          <div class="task-meta">
            <span class="task-priority" :class="task.priority">
              {{ task.priority }}
            </span>
            <span class="task-due">{{ formatDate(task.dueDate) }}</span>
          </div>
        </div>
        
        <div class="task-actions">
          <button class="action-btn edit-btn" @click="editTask(task)">
            <span class="icon">✏️</span>
          </button>
          <button class="action-btn delete-btn" @click="deleteTask(task.id)">
            <span class="icon">🗑️</span>
          </button>
        </div>
      </div>
    </div>
    
    <div v-if="tasks.length === 0" class="no-tasks">
      <p>暂无任务</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TaskList',
  props: {
    tasks: {
      type: Array,
      required: true
    }
  },
  methods: {
    toggleTaskStatus(task) {
      this.$emit('toggle-status', task);
    },
    editTask(task) {
      this.$emit('edit-task', task);
    },
    deleteTask(taskId) {
      this.$emit('delete-task', taskId);
    },
    getStatusText(status) {
      const statusMap = {
        'todo': '未开始',
        'in-progress': '进行中',
        'done': '已完成',
        'not_started': '未开始',
        'in_progress': '进行中'
      };
      return statusMap[status] || status;
    },
    formatDate(dateString) {
      if (!dateString) return '无截止日期';
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('zh-CN', options);
    }
  }
}
</script>

<style scoped>
.task-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 0; /* 允许flex项目收缩到内容以下 */
}

.task-item {
  background: var(--card-bg);
  border-radius: 24px;
  border: 1px solid rgba(113, 89, 193, 0.4);
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.task-item::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 24px;
  padding: 1px;
  background: var(--highlight-gradient);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, 
                linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.task-info {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.task-checkbox {
  margin-top: 4px;
}

.task-checkbox input[type="checkbox"] {
  display: none;
}

.task-checkbox label {
  display: block;
  width: 24px;
  height: 24px;
  border: 2px solid #7e57c2;
  border-radius: 6px;
  position: relative;
  cursor: pointer;
  background: rgba(49, 43, 70, 0.6);
}

.task-checkbox input[type="checkbox"]:checked + label {
  background: #7e57c2;
  border-color: #7e57c2;
}

.task-checkbox input[type="checkbox"]:checked + label::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 14px;
}

.task-details {
  flex: 1;
}

.task-title-container {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.task-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #f3f4f6;
  margin: 0;
  flex: 1;
}

.task-status {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.task-status.todo,
.task-status.not_started {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.task-status.in-progress,
.task-status.in_progress {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.task-status.done {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.task-title.completed {
  text-decoration: line-through;
  color: #9ca3af;
}

.task-description {
  color: #d1d5db;
  margin: 0 0 12px 0;
  line-height: 1.5;
}

.task-meta {
  display: flex;
  gap: 16px;
  align-items: center;
}

.task-priority {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.task-priority.low {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.task-priority.medium {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.task-priority.high {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.task-due {
  color: #9ca3af;
  font-size: 0.875rem;
}

.task-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  color: #f3f4f6;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.edit-btn:hover {
  background: rgba(59, 130, 246, 0.2);
}

.delete-btn:hover {
  background: rgba(239, 68, 68, 0.2);
}

.no-tasks {
  text-align: center;
  padding: 40px 20px;
  color: #9ca3af;
}
</style>