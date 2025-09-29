<template>
  <div v-if="tasks.length > 0" class="nested-subtasks">
    <div 
      v-for="task in tasks" 
      :key="task.id"
      class="nested-task-item task-item card"
      :style="{ marginLeft: depth * 20 + 'px' }"
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
              <span class="subtask-indent">{{ getIndentSymbol(depth) }}</span> {{ task.title }}
            </h3>
            <span class="task-status" :class="task.status">
              {{ getStatusText(task.status) }}
            </span>
          </div>
          <p class="task-description">{{ task.description }}</p>
          
          <div class="task-meta">
            <span class="task-priority" :class="task.priority">
              {{ getPriorityText(task.priority) }}
            </span>
            <span class="task-due">{{ formatDate(task.dueDate) }}</span>
          </div>
        </div>
        
        <div class="task-actions">
          <!-- 添加子任务或同级任务按钮 -->
          <button 
            v-if="task.level < 4" 
            class="action-btn add-btn" 
            @click="showAddTaskOptions(task)"
            title="添加任务"
          >
            <span class="icon">+</span>
          </button>
          <button class="action-btn edit-btn" @click="editTask(task)">
            <span class="icon">✏️</span>
          </button>
          <button class="action-btn delete-btn" @click="deleteTask(task.id)">
            <span class="icon">🗑️</span>
          </button>
        </div>
      </div>
      
      <!-- 递归处理更深层次的子任务 -->
      <HierarchicalSubtasks 
        v-if="task.children && task.children.length > 0"
        :tasks="task.children || []"
        :depth="depth + 1"
        @toggle-status="toggleTaskStatus"
        @edit-task="editTask"
        @delete-task="deleteTask"
        @show-add-options="showAddTaskOptions"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'HierarchicalSubtasks',
  props: {
    tasks: {
      type: Array,
      required: true
    },
    depth: {
      type: Number,
      default: 1
    }
  },
  methods: {
    async toggleTaskStatus(task) {
      // 确定下一个状态
      let nextStatus;
      if (task.status === 'done') {
        nextStatus = 'todo';
      } else {
        nextStatus = 'done'; // 点击未完成的任务时标记为完成
      }

      try {
        // 调用后端API更新任务状态
        const backendStatus = this.mapStatusForBackend(nextStatus);
        const { updateTaskStatus } = await import('@/api/task');
        const response = await updateTaskStatus(task.id, backendStatus);
        
        // 发射事件让父组件处理状态更新
        this.$emit('toggle-status', task);
      } catch (error) {
        console.error('更新任务状态失败:', error);
        alert('更新任务状态失败，请稍后重试');
      }
    },
    
    editTask(task) {
      this.$emit('edit-task', task);
    },
    
    deleteTask(taskId) {
      this.$emit('delete-task', taskId);
    },
    
    showAddTaskOptions(task) {
      // 通过 emit 将事件传递给父组件处理
      this.$emit('show-add-options', task);
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
    
    getPriorityText(priority) {
      const priorityMap = {
        'low': '低优先级',
        'medium': '中优先级',
        'high': '高优先级'
      };
      return priorityMap[priority] || priority;
    },
    
    getIndentSymbol(depth) {
      // 根据层级深度显示不同的缩进符号
      const symbols = ['↳', '⤷', '↪', '→'];
      return symbols[(depth - 1) % symbols.length] || '→';
    },
    
    formatDate(dateString) {
      if (!dateString) return '无截止日期';
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('zh-CN', options);
    },
    
    // 将前端状态映射到后端状态值
    mapStatusForBackend(frontendStatus) {
      const statusMap = {
        'todo': 'not_started',
        'in-progress': 'in_progress',
        'done': 'done',
        'not_started': 'not_started',
        'in_progress': 'in_progress',
        'completed': 'done'
      };
      return statusMap[frontendStatus] || 'not_started';
    },
    // 将后端状态值映射到前端状态
    mapStatusForFrontend(backendStatus) {
      const statusMap = {
        'not_started': 'todo',
        'in_progress': 'in-progress',
        'done': 'done'
      };
      return statusMap[backendStatus] || 'todo';
    },
    
    // 将前端优先级映射到后端优先级值
    mapPriorityForBackend(frontendPriority) {
      const priorityMap = {
        'low': 'low',
        'medium': 'medium',
        'high': 'high'
      };
      return priorityMap[frontendPriority] || 'medium';
    },
    // 将后端优先级值映射到前端优先级
    mapPriorityForFrontend(backendPriority) {
      const priorityMap = {
        'low': 'low',
        'medium': 'medium',
        'high': 'high'
      };
      return priorityMap[backendPriority] || 'medium';
    }
  }
}
</script>

<style scoped>
.nested-subtasks {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.nested-task-item {
  background: rgba(49, 43, 70, 0.4); /* 随层级加深背景更暗 */
  border-radius: 16px;
  border: 1px solid rgba(113, 89, 193, 0.2);
  padding: 14px;
  position: relative;
  overflow: hidden;
}

.nested-task-item::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 16px;
  padding: 1px;
  background: linear-gradient(135deg, rgba(126, 87, 194, 0.2), rgba(167, 139, 250, 0.05));
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
  font-size: 0.9rem; /* 进一步减小子任务字体大小 */
  font-weight: 500;
  color: #e5e7eb;
  margin: 0;
  flex: 1;
}

.subtask-indent {
  color: #a78bfa;
  font-weight: bold;
  margin-right: 4px;
}

.task-title.completed {
  text-decoration: line-through;
  color: #9ca3af;
}

.task-status {
  padding: 3px 10px;
  border-radius: 18px;
  font-size: 0.7rem;
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

.task-description {
  color: #d1d5db;
  margin: 0 0 10px 0;
  line-height: 1.4;
  font-size: 0.875rem;
}

.task-meta {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.task-priority {
  padding: 3px 10px;
  border-radius: 18px;
  font-size: 0.7rem;
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
  font-size: 0.8rem;
}

.task-actions {
  display: flex;
  gap: 6px;
}

.action-btn {
  width: 32px;
  height: 32px;
  border-radius: 10px;
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

.add-btn:hover {
  background: rgba(167, 139, 250, 0.3);
}

.edit-btn:hover {
  background: rgba(59, 130, 246, 0.2);
}

.delete-btn:hover {
  background: rgba(239, 68, 68, 0.2);
}
</style>