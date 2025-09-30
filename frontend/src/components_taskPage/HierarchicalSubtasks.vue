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
            <!-- 不显示level > 1任务的状态 -->
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
          <!-- AI拆解按钮 -->
          <button 
            class="action-btn ai-breakdown-btn" 
            @click="showAIBreakdownModal(task)"
            title="AI拆解任务"
          >
            <span class="icon">🔧</span>
          </button>
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
        @task-added="onTaskAdded"
      />
    </div>
    
    <!-- AI拆解模态框 -->
    <div v-if="showAIBreakdownDialog" class="ai-breakdown-modal-overlay" @click="cancelAIBreakdown">
      <div class="ai-breakdown-modal" @click.stop>
        <div class="modal-header">
          <h3>AI拆解任务</h3>
          <button class="close-btn" @click="cancelAIBreakdown">✕</button>
        </div>
        <div class="modal-body">
          <div class="task-info">
            <h4>任务标题：{{ aiBreakdownTask?.title }}</h4>
            <p class="task-description">{{ aiBreakdownTask?.description }}</p>
          </div>
          
          <!-- 拆解提示词输入 -->
          <div v-if="!aiBreakdownResult" class="form-group">
            <label for="ai-breakdown-prompt">拆解提示词 *</label>
            <textarea 
              id="ai-breakdown-prompt" 
              v-model="aiBreakdownPrompt" 
              placeholder="请描述您希望如何拆解这个任务，例如：'将这个任务拆解为3-5个具体的子任务，每个子任务应该是可执行的步骤'"
              rows="4"
              :disabled="isBreakdownLoading"
            ></textarea>
          </div>
          
          <!-- 拆解中状态 -->
          <div v-if="isBreakdownLoading" class="loading-section">
            <div class="loading-spinner"></div>
            <p>AI正在拆解任务中，请稍候...</p>
          </div>
          
          <!-- 拆解结果展示 -->
          <div v-if="aiBreakdownResult && !isBreakdownLoading" class="breakdown-result">
            <div v-if="aiBreakdownResult.success" class="result-success">
              <h4>✅ 拆解成功！</h4>
              <p>AI为您拆解出了 {{ aiBreakdownResult.subtask_count }} 个子任务：</p>
              
              <div class="subtasks-preview">
                <div 
                  v-for="(subtask, index) in aiBreakdownResult.breakdown_tasks" 
                  :key="index"
                  class="subtask-item"
                >
                  <div class="subtask-header">
                    <span class="subtask-number">{{ index + 1 }}</span>
                    <h5 class="subtask-title">{{ subtask.title }}</h5>
                    <span class="subtask-priority" :class="subtask.priority">{{ getPriorityText(subtask.priority) }}</span>
                  </div>
                  <p class="subtask-description">{{ subtask.description }}</p>
                  <div class="subtask-meta">
                    <span class="subtask-deadline">📅 {{ subtask.deadline }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-else class="result-error">
              <h4>❌ 拆解失败</h4>
              <p>{{ aiBreakdownResult.message }}</p>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="btn-secondary" @click="cancelAIBreakdown">取消</button>
          
          <!-- 拆解按钮 -->
          <button 
            v-if="!aiBreakdownResult" 
            class="btn-primary" 
            @click="confirmAIBreakdown" 
            :disabled="!aiBreakdownPrompt.trim() || isBreakdownLoading"
          >
            {{ isBreakdownLoading ? '拆解中...' : '开始拆解' }}
          </button>
          
          <!-- 确认/重新拆解按钮 -->
          <template v-if="aiBreakdownResult && !isBreakdownLoading">
            <button 
              v-if="aiBreakdownResult.success" 
              class="btn-primary" 
              @click="acceptBreakdownResult"
            >
              接受并创建子任务
            </button>
            <button 
              class="btn-secondary" 
              @click="aiBreakdownResult = null"
            >
              重新拆解
            </button>
          </template>
        </div>
      </div>
    </div>
    
    <!-- Toast通知组件 -->
    <ToastNotification
      :show="showToast"
      :type="toastConfig.type"
      :title="toastConfig.title"
      :message="toastConfig.message"
      @close="showToast = false"
    />
  </div>
</template>

<script>
import ToastNotification from '@/components/ToastNotification.vue';

export default {
  name: 'HierarchicalSubtasks',
  components: {
    ToastNotification
  },
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
  data() {
    return {
      showAIBreakdownDialog: false, // 是否显示AI拆解模态框
      aiBreakdownTask: null, // 当前要拆解的任务
      aiBreakdownPrompt: '', // AI拆解的prompt
      aiBreakdownResult: null, // AI拆解结果
      isBreakdownLoading: false, // 是否正在拆解中
      showToast: false, // 是否显示Toast通知
      toastConfig: { // Toast配置
        type: 'success',
        title: '',
        message: ''
      }
    }
  },
  methods: {
    async toggleTaskStatus(task) {
      // 确定下一个状态
      let nextStatus;
      if (task.status === 'done') {
        nextStatus = 'todo';
      } else if (task.status === 'todo' || task.status === 'not_started') {
        nextStatus = 'in-progress';
      } else if (task.status === 'in-progress') {
        nextStatus = 'done';
      }

      try {
        // 调用后端API更新任务状态
        const backendStatus = this.mapStatusForBackend(nextStatus);
        const { updateTaskStatus } = await import('@/api/task');
        const response = await updateTaskStatus(task.id, backendStatus);
        
        // 获取更新后的任务信息并更新本地状态
        task.status = this.mapStatusForFrontend(response.status);
        
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
    
    // AI拆解相关方法
    showAIBreakdownModal(task) {
      this.aiBreakdownTask = task;
      this.aiBreakdownPrompt = '';
      this.aiBreakdownResult = null;
      this.isBreakdownLoading = false;
      this.showAIBreakdownDialog = true;
    },
    
    async confirmAIBreakdown() {
      if (!this.aiBreakdownTask || !this.aiBreakdownPrompt.trim()) {
        alert('请输入拆解提示词');
        return;
      }
      
      this.isBreakdownLoading = true;
      this.aiBreakdownResult = null;
      
      try {
        // 调用拆解API
        const { breakdownTask } = await import('@/api/task');
        const result = await breakdownTask(this.aiBreakdownTask.id, this.aiBreakdownPrompt);
        
        this.aiBreakdownResult = result;
        this.isBreakdownLoading = false;
        
        if (!result.success) {
          this.showToastNotification(
            'error',
            '❌ 拆解失败',
            result.message || 'AI拆解失败，请稍后重试'
          );
        }
      } catch (error) {
        console.error('AI拆解失败:', error);
        this.isBreakdownLoading = false;
        this.aiBreakdownResult = {
          success: false,
          message: 'AI拆解失败，请稍后重试'
        };
        this.showToastNotification(
          'error',
          '❌ 网络错误',
          'AI拆解请求失败，请检查网络连接后重试'
        );
      }
    },
    
    async acceptBreakdownResult() {
      if (!this.aiBreakdownResult || !this.aiBreakdownResult.success) {
        return;
      }
      
      try {
        // 调用确认拆解API
        const { confirmBreakdownTasks } = await import('@/api/task');
        const result = await confirmBreakdownTasks(this.aiBreakdownTask.id, this.aiBreakdownResult.breakdown_tasks);
        
        // 关闭模态框
        this.cancelAIBreakdown();
        
        // 通知父组件刷新任务列表
        this.$emit('task-added');
        
        // 使用API返回的结果或原始结果中的子任务数量
        const subtaskCount = result?.created_tasks?.length || this.aiBreakdownResult?.subtask_count || 0;
        this.showToastNotification(
          'success',
          '🎉 任务拆解成功！',
          `已成功创建 ${subtaskCount} 个子任务，它们已添加到任务列表中`
        );
      } catch (error) {
        console.error('保存子任务失败:', error);
        this.showToastNotification(
          'error',
          '❌ 保存失败',
          '保存子任务时发生错误，请稍后重试'
        );
      }
    },
    
    cancelAIBreakdown() {
      this.showAIBreakdownDialog = false;
      this.aiBreakdownTask = null;
      this.aiBreakdownPrompt = '';
      this.aiBreakdownResult = null;
      this.isBreakdownLoading = false;
    },
    
    getPriorityText(priority) {
      const priorityMap = {
        'high': '高优先级',
        'medium': '中优先级',
        'low': '低优先级'
      };
      return priorityMap[priority] || '中优先级';
    },
    
    showToastNotification(type, title, message) {
      this.toastConfig = { type, title, message };
      this.showToast = true;
    },
    
    onTaskAdded() {
      // 将事件冒泡到父组件
      this.$emit('task-added');
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

.ai-breakdown-btn {
  background: rgba(34, 197, 94, 0.2);
  border: none;
  color: #22c55e;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  transition: background 0.2s;
}

.ai-breakdown-btn:hover {
  background: rgba(34, 197, 94, 0.3);
}

/* AI拆解模态框样式 */
.ai-breakdown-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.ai-breakdown-modal {
  background: var(--card-bg);
  border-radius: 24px;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  border: 1px solid rgba(113, 89, 193, 0.6);
  position: relative;
}

.ai-breakdown-modal::after {
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

.ai-breakdown-modal .modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 16px;
  border-bottom: 1px solid rgba(113, 89, 193, 0.3);
  background: rgba(113, 89, 193, 0.1);
}

.ai-breakdown-modal .modal-header h3 {
  margin: 0;
  color: #c084fc;
  font-size: 1.3rem;
  font-weight: 600;
}

.ai-breakdown-modal .close-btn {
  background: none;
  border: none;
  color: #a78bfa;
  font-size: 1.5rem;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.2s;
}

.ai-breakdown-modal .close-btn:hover {
  color: #f3f4f6;
  background: rgba(167, 139, 250, 0.2);
}

.ai-breakdown-modal .modal-body {
  padding: 24px;
}

.ai-breakdown-modal .task-info {
  background: rgba(49, 43, 70, 0.6);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 24px;
  border: 1px solid rgba(113, 89, 193, 0.3);
  position: relative;
  overflow: hidden;
}

.ai-breakdown-modal .task-info::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 16px;
  padding: 1px;
  background: linear-gradient(135deg, rgba(126, 87, 194, 0.3), rgba(167, 139, 250, 0.1));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, 
                linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.ai-breakdown-modal .task-info h4 {
  margin: 0 0 12px 0;
  color: #c084fc;
  font-size: 1.2rem;
  font-weight: 600;
}

.ai-breakdown-modal .task-info .task-description {
  margin: 0;
  color: #e5e7eb;
  line-height: 1.6;
  font-size: 0.95rem;
}

.ai-breakdown-modal .form-group {
  margin-bottom: 20px;
}

.ai-breakdown-modal .form-group label {
  display: block;
  margin-bottom: 8px;
  color: #d1d5db;
  font-weight: 600;
  font-size: 1rem;
}

.ai-breakdown-modal .form-group textarea {
  width: 100%;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid rgba(113, 89, 193, 0.3);
  background: rgba(49, 43, 70, 0.4);
  color: #f3f4f6;
  font-size: 1rem;
  box-sizing: border-box;
  resize: vertical;
  transition: all 0.2s;
  font-family: inherit;
}

.ai-breakdown-modal .form-group textarea:focus {
  outline: none;
  border-color: #7e57c2;
  background: rgba(49, 43, 70, 0.6);
  box-shadow: 0 0 0 3px rgba(126, 87, 194, 0.1);
}

.ai-breakdown-modal .form-group textarea::placeholder {
  color: #9ca3af;
}

.ai-breakdown-modal .modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px 24px;
  border-top: 1px solid rgba(113, 89, 193, 0.3);
  background: rgba(113, 89, 193, 0.05);
}

.ai-breakdown-modal .btn-primary {
  padding: 12px 24px;
  background: var(--highlight-gradient);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(126, 87, 194, 0.3);
}

.ai-breakdown-modal .btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(126, 87, 194, 0.4);
}

.ai-breakdown-modal .btn-primary:disabled {
  background: #6b7280;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.ai-breakdown-modal .btn-secondary {
  padding: 12px 24px;
  background: transparent;
  color: #d1d5db;
  border: 1px solid rgba(113, 89, 193, 0.3);
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.2s;
}

.ai-breakdown-modal .btn-secondary:hover {
  background: rgba(113, 89, 193, 0.1);
  border-color: rgba(113, 89, 193, 0.5);
  color: #f3f4f6;
}

/* 加载状态样式 */
.loading-section {
  text-align: center;
  padding: 2rem;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #8b5cf6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-section p {
  color: #64748b;
  font-size: 0.9rem;
}

/* 拆解结果样式 */
.breakdown-result {
  margin-top: 1rem;
}

.result-success h4 {
  color: #059669;
  margin-bottom: 0.5rem;
}

.result-error h4 {
  color: #dc2626;
  margin-bottom: 0.5rem;
}

.result-success p,
.result-error p {
  color: #64748b;
  margin-bottom: 1rem;
}

/* 子任务预览样式 */
.subtasks-preview {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
  background-color: #f8fafc;
}

.subtask-item {
  background: white;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 0.75rem;
  border: 1px solid #e2e8f0;
}

.subtask-item:last-child {
  margin-bottom: 0;
}

.subtask-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.subtask-number {
  background: #8b5cf6;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
}

.subtask-title {
  flex: 1;
  margin: 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: #1e293b;
}

.subtask-priority {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.subtask-priority.high {
  background-color: #fef2f2;
  color: #dc2626;
}

.subtask-priority.medium {
  background-color: #fffbeb;
  color: #d97706;
}

.subtask-priority.low {
  background-color: #f0fdf4;
  color: #059669;
}

.subtask-description {
  color: #64748b;
  font-size: 0.85rem;
  line-height: 1.4;
  margin: 0 0 0.5rem 0;
}

.subtask-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.8rem;
  color: #64748b;
}

.subtask-deadline {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
</style>