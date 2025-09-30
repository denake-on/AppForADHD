<template>
  <div class="hierarchical-task-list">
    <div 
      v-for="task in rootTasks" 
      :key="task.id" 
      class="task-group"
    >
      <!-- 将整个任务组包装在一个父容器中，以包含父任务和所有子任务 -->
      <div class="task-container">
        <!-- 父任务（level 1） -->
        <div class="parent-task task-item card">
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
                <!-- 展开/收起图标按钮 -->
                <button 
                  v-if="task.children && task.children.length > 0" 
                  class="expand-collapse-btn" 
                  @click="toggleChildrenVisibility(task)"
                  :title="isTaskExpanded(task.id) ? '收起子任务' : '展开子任务'"
                >
                  <span class="icon">{{ isTaskExpanded(task.id) ? '▼' : '▶' }}</span>
                </button>
                <h3 :class="['task-title', { completed: task.status === 'done' }]">
                  {{ task.title }}
                </h3>
                <!-- 只为level 1的任务显示状态 -->
                <span v-if="task.level === 1" class="task-status" :class="task.status">
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
        </div>
        
        <!-- 子任务（level 2及以上） - 只使用递归组件来显示所有子任务层级 -->
        <div v-if="task.children && task.children.length > 0 && isTaskExpanded(task.id)" class="subtasks-container">
          <!-- 递归处理所有层级的子任务 -->
          <HierarchicalSubtasks 
            :tasks="task.children"
            :depth="2"
            @toggle-status="toggleTaskStatus"
            @edit-task="editTask"
            @delete-task="deleteTask"
            @show-add-options="showAddTaskOptions"
            @task-added="onTaskAdded"
          />
        </div>
      </div>
    </div>
    
    <div v-if="rootTasks.length === 0" class="no-tasks">
      <p>暂无任务</p>
    </div>
    
    <!-- 添加任务选项弹窗 -->
    <div v-if="showAddOptions" class="add-task-options-overlay" @click="showAddOptions = false">
      <div class="add-task-options" @click.stop>
        <h4>选择添加类型</h4>
        <div class="option-buttons">
          <button class="option-btn" @click="addTask('child')">
            添加子任务
          </button>
          <button class="option-btn" @click="addTask('sibling')">
            添加同级任务
          </button>
        </div>
      </div>
    </div>
    
    <!-- 添加任务模态框 -->
    <div v-if="showAddTaskModal" class="add-task-modal-overlay" @click="cancelAddTask">
      <div class="add-task-modal" @click.stop>
        <div class="modal-header">
          <h3>添加新任务</h3>
          <button class="close-btn" @click="cancelAddTask">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="task-title">任务名称 *</label>
            <input 
              id="task-title" 
              type="text" 
              v-model="newTaskTitle" 
              placeholder="输入任务名称"
              required
            />
          </div>
          <div class="form-group">
            <label for="task-description">描述</label>
            <textarea 
              id="task-description" 
              v-model="newTaskDescription" 
              placeholder="输入任务描述"
            ></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="task-priority">优先级</label>
              <select id="task-priority" v-model="newTaskPriority">
                <option value="low">低优先级</option>
                <option value="medium">中优先级</option>
                <option value="high">高优先级</option>
              </select>
            </div>
            <div class="form-group">
              <label for="task-due-date">截止日期</label>
              <input 
                id="task-due-date" 
                type="date" 
                v-model="newTaskDueDate"
              />
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="cancelAddTask">取消</button>
          <button class="btn-primary" @click="confirmAddTask" :disabled="!newTaskTitle">添加</button>
        </div>
      </div>
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
import HierarchicalSubtasks from '@/components_taskPage/HierarchicalSubtasks.vue';
import ToastNotification from '@/components/ToastNotification.vue';

export default {
  name: 'HierarchicalTaskList',
  components: {
    HierarchicalSubtasks,
    ToastNotification
  },
  props: {
    tasks: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      expandedTasks: {}, // 存储展开/收起状态，key为task id，value为布尔值
      showAddOptions: false, // 是否显示添加任务选项
      addTaskTarget: null, // 添加任务的目标任务
      addTaskType: null, // 添加任务类型：'sibling' 或 'child'
      newTaskTitle: '', // 新任务标题
      newTaskDescription: '', // 新任务描述
      newTaskPriority: 'medium', // 新任务优先级
      newTaskDueDate: '', // 新任务截止日期
      showAddTaskModal: false, // 是否显示添加任务模态框
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
  computed: {
    rootTasks() {
      // 只显示level 1的父任务，子任务已经在内部展示
      return this.tasks.filter(task => task.level === 1 || task.parent_id === null || task.parent_id === undefined);
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
        
        // 不管任务层级如何，都使用普通更新API，后端会自动处理父任务状态
        const response = await import('@/api/task').then(api => 
          api.updateTaskStatus(task.id, backendStatus)
        );
        
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
    // 递归标记所有子任务为完成
    markAllChildrenAsDone(parentTask) {
      if (parentTask.children && parentTask.children.length > 0) {
        parentTask.children.forEach(child => {
          // 更新子任务状态为完成
          child.status = 'done';
          
          // 如果子任务还有子任务，递归处理
          this.markAllChildrenAsDone(child);
        });
      }
    },
    
    // 递归标记所有子任务为未完成
    markAllChildrenAsNotDone(parentTask) {
      if (parentTask.children && parentTask.children.length > 0) {
        parentTask.children.forEach(child => {
          // 更新子任务状态为未完成
          child.status = 'todo';
          
          // 如果子任务还有子任务，递归处理
          this.markAllChildrenAsNotDone(child);
        });
      }
    },
    // 切换子任务的可见性
    toggleChildrenVisibility(task) {
      // 在Vue 3中，直接赋值即可触发响应式更新
      this.expandedTasks[task.id] = !this.isTaskExpanded(task.id);
    },
    // 检查任务是否已展开
    isTaskExpanded(taskId) {
      // 如果任务ID在expandedTasks中存在，则返回其状态；否则默认为展开(true)
      if (this.expandedTasks[taskId] !== undefined) {
        return this.expandedTasks[taskId];
      } else {
        // 默认展开状态，但需要在expandedTasks中记录，以便后续切换
        this.expandedTasks[taskId] = true;
        return true;
      }
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
    formatDate(dateString) {
      if (!dateString) return '无截止日期';
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('zh-CN', options);
    },
    getNestedSubtasks(tasks) {
      // 获取所有非直接子任务（level > 2）
      const nestedSubtasks = [];
      
      const findNested = (taskList) => {
        for (const task of taskList) {
          if (task.children && task.children.length > 0) {
            nestedSubtasks.push(...task.children);
            findNested(task.children);
          }
        }
      };
      
      findNested(tasks);
      return nestedSubtasks;
    },
    
    showAddTaskOptions(task) {
      this.addTaskTarget = task;
      this.showAddOptions = true;
    },
    
    async addTask(type) {
      this.addTaskType = type;
      this.showAddOptions = false;
      this.showAddTaskModal = true;
    },
    
    async confirmAddTask() {
      try {
        // 构建新任务的数据
        let parent_id = null;
        let level = 1;
        
        if (this.addTaskType === 'child') {
          // 添加子任务
          parent_id = this.addTaskTarget.id;
          level = this.addTaskTarget.level + 1;
        } else if (this.addTaskType === 'sibling') {
          // 添加同级任务
          parent_id = this.addTaskTarget.parent_id;
          level = this.addTaskTarget.level;
        }
        
        // 调用后端API创建新任务
        const { createTask } = await import('@/api/task');
        const newTaskData = {
          title: this.newTaskTitle,
          description: this.newTaskDescription || null,
          priority: this.mapPriorityForBackend(this.newTaskPriority),
          deadline: this.newTaskDueDate || null,
          parent_id: parent_id,
          level: level
        };
        
        const response = await createTask(newTaskData);
        
        // 通知父组件刷新任务列表
        this.$emit('task-added');
        
        // 重置表单
        this.resetAddTaskForm();
        
        // 关闭模态框
        this.showAddTaskModal = false;
        
      } catch (error) {
        console.error('添加任务失败:', error);
        alert('添加任务失败，请稍后重试');
      }
    },
    
    resetAddTaskForm() {
      this.newTaskTitle = '';
      this.newTaskDescription = '';
      this.newTaskPriority = 'medium';
      this.newTaskDueDate = '';
      this.addTaskTarget = null;
      this.addTaskType = null;
    },
    
    cancelAddTask() {
      this.showAddTaskModal = false;
      this.resetAddTaskForm();
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
.hierarchical-task-list {
  display: grid;
  grid-template-columns: 1fr; /* 默认为单列 */
  gap: 16px;
}

/* 在较大屏幕上显示为两列 */
@media (min-width: 1024px) {
  .hierarchical-task-list {
    grid-template-columns: repeat(2, 1fr);
  }
}

.task-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.parent-task {
  background: var(--card-bg);
  border-radius: 24px;
  border: 1px solid rgba(113, 89, 193, 0.6); /* 使用更明显的边框来区分父任务 */
  padding: 20px;
  position: relative;
  overflow: visible; /* 改为visible以确保子任务不会被隐藏 */
  min-height: auto;
}

.parent-task::after {
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

.task-container {
  position: relative;
  display: flex;
  flex-direction: column;
  min-height: auto;
}

.subtasks-container {
  margin-top: 12px;
  margin-left: 20px; /* 为子任务提供缩进 */
  padding-left: 16px; /* 添加左边框效果 */
  position: relative;
  border-left: 1px solid rgba(126, 87, 194, 0.3); /* 添加左边框以视觉上包含子任务 */
}

.subtask-item {
  background: rgba(49, 43, 70, 0.6); /* 更暗的背景色区分子任务 */
  border-radius: 18px;
  border: 1px solid rgba(113, 89, 193, 0.3);
  padding: 16px;
  position: relative;
  overflow: hidden;
  margin-bottom: 8px;
}

.subtask-item::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 18px;
  padding: 1px;
  background: linear-gradient(135deg, rgba(126, 87, 194, 0.3), rgba(167, 139, 250, 0.1));
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
  font-size: 1rem; /* 减小字体大小 */
  font-weight: 600;
  color: #f3f4f6;
  margin: 0;
  flex: 1;
}

.subtask-indent {
  color: #7e57c2;
  font-weight: bold;
  margin-right: 4px;
}

.task-title.completed {
  text-decoration: line-through;
  color: #9ca3af;
}

.expand-collapse-btn {
  background: transparent;
  border: none;
  color: #a78bfa;
  cursor: pointer;
  font-size: 0.8rem;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  flex-shrink: 0; /* 防止按钮被压缩 */
}

.expand-collapse-btn:hover {
  background: rgba(167, 139, 250, 0.2);
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

.add-btn {
  background: rgba(167, 139, 250, 0.2);
  border: none;
  color: #a78bfa;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 12px;
  transition: background 0.2s;
}

.add-btn:hover {
  background: rgba(167, 139, 250, 0.3);
}

.ai-breakdown-btn {
  background: rgba(34, 197, 94, 0.2);
  border: none;
  color: #22c55e;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 12px;
  transition: background 0.2s;
}

.ai-breakdown-btn:hover {
  background: rgba(34, 197, 94, 0.3);
}

.add-task-options-overlay {
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

.add-task-options {
  background: #374151;
  border-radius: 12px;
  padding: 20px;
  min-width: 200px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.add-task-options h4 {
  margin: 0 0 15px 0;
  color: #f3f4f6;
  font-size: 1rem;
  text-align: center;
}

.option-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-btn {
  padding: 10px 15px;
  border: 1px solid #4b5563;
  border-radius: 8px;
  background: #4b5563;
  color: #f3f4f6;
  cursor: pointer;
  transition: background 0.2s;
}

.option-btn:hover {
  background: #6b7280;
}

.add-task-modal-overlay {
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

.add-task-modal {
  background: #374151;
  border-radius: 16px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #4b5563;
}

.modal-header h3 {
  margin: 0;
  color: #f3f4f6;
  font-size: 1.2rem;
}

.close-btn {
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 1.5rem;
  cursor: pointer;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #f3f4f6;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  color: #d1d5db;
  font-weight: 500;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #4b5563;
  background: #1f2937;
  color: #f3f4f6;
  font-size: 1rem;
}

.form-group textarea {
  min-height: 80px;
  resize: vertical;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 20px;
  border-top: 1px solid #4b5563;
}

.btn-primary {
  padding: 10px 20px;
  background: #7e57c2;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.btn-primary:hover:not(:disabled) {
  background: #6d4c9a;
}

.btn-primary:disabled {
  background: #6b7280;
  cursor: not-allowed;
}

.btn-secondary {
  padding: 10px 20px;
  background: #4b5563;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.btn-secondary:hover {
  background: #6b7280;
}

.add-btn {
  background: rgba(167, 139, 250, 0.2) !important; /* 紫色系添加按钮 */
}

.add-btn:hover {
  background: rgba(167, 139, 250, 0.3) !important;
}

/* 添加任务选项弹窗样式 */
.add-task-options-overlay {
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

.add-task-options {
  background: #374151;
  border-radius: 12px;
  padding: 20px;
  min-width: 200px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.add-task-options h4 {
  margin: 0 0 15px 0;
  color: #f3f4f6;
  text-align: center;
}

.option-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-btn {
  padding: 10px 15px;
  border: 1px solid #4b5563;
  border-radius: 8px;
  background: #4b5563;
  color: #f3f4f6;
  cursor: pointer;
  transition: background 0.2s;
}

.option-btn:hover {
  background: #6b7280;
}

/* 添加任务模态框样式 */
.add-task-modal-overlay {
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

.add-task-modal {
  background: #374151;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 20px 10px;
  border-bottom: 1px solid #4b5563;
}

.modal-header h3 {
  margin: 0;
  color: #f3f4f6;
  font-size: 1.25rem;
}

.close-btn {
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #f3f4f6;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #d1d5db;
  font-weight: 500;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #4b5563;
  background: #1f2937;
  color: #f3f4f6;
  box-sizing: border-box;
}

.form-group textarea {
  min-height: 80px;
  resize: vertical;
}

.form-row {
  display: flex;
  gap: 15px;
}

.form-row .form-group {
  flex: 1;
}

.modal-footer {
  padding: 15px 20px 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  border-top: 1px solid #4b5563;
}

.btn-primary {
  padding: 10px 20px;
  background: var(--highlight-gradient);
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.btn-primary:disabled {
  background: #6b7280;
  cursor: not-allowed;
}

.btn-primary:hover:not(:disabled) {
  opacity: 0.9;
}

.btn-secondary {
  padding: 10px 20px;
  background: transparent;
  border: 1px solid #6b7280;
  border-radius: 8px;
  color: #d1d5db;
  font-weight: 600;
  cursor: pointer;
}

.btn-secondary:hover {
  background: #4b5563;
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