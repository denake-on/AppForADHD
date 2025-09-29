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
  </div>
</template>

<script>
import HierarchicalSubtasks from '@/components_taskPage/HierarchicalSubtasks.vue';

export default {
  name: 'HierarchicalTaskList',
  components: {
    HierarchicalSubtasks
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
      showAddTaskModal: false // 是否显示添加任务模态框
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
      } else {
        nextStatus = 'done'; // 点击未完成的任务时标记为完成
      }

      try {
        // 调用后端API更新任务状态
        const backendStatus = this.mapStatusForBackend(nextStatus);
        
        // 如果是层级1的任务，使用后代更新API，否则使用普通更新API
        let response;
        if (task.level === 1) {
          response = await import('@/api/task').then(api => 
            api.updateTaskStatusWithDescendants(task.id, backendStatus)
          );
        } else {
          response = await import('@/api/task').then(api => 
            api.updateTaskStatus(task.id, backendStatus)
          );
        }
        
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
</style>