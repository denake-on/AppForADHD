<template>
  <div class="task-page">
    <div class="page-header">
      <h1 class="page-title">任务管理</h1>
      <div class="header-actions">
        <button class="btn-primary" @click="openCreateTaskModal">
          <span class="icon">+</span>
          新建任务
        </button>
      </div>
    </div>

    <!-- 任务筛选和搜索区域 -->
    <TaskFilters 
      :initial-search-query="searchQuery"
      :initial-status-filter="statusFilter"
      :initial-priority-filter="priorityFilter"
      @filter-change="onFilterChange"
    />

    <!-- 任务统计卡片 -->
    <TaskStats :tasks="tasks" />

    <!-- 任务列表 -->
    <div class="tasks-container">
      <div class="task-list-header">
        <h2>任务列表</h2>
      </div>
      
      <TabbedTaskList 
        :tasks="filteredTasks"
        @toggle-status="toggleTaskStatus"
        @edit-task="editTask"
        @delete-task="deleteTask"
        @task-added="loadTasks"
      />
    </div>

    <!-- 创建/编辑任务模态框 -->
    <TaskModal 
      :show-modal="showTaskModal"
      :task="editingTask"
      @close="closeTaskModal"
      @save="saveTask"
    />
  </div>
</template>

<script>
import { getTasks, createTask, updateTask, deleteTask, updateTaskStatus, getHierarchicalTasks } from '@/api/task';
import TaskList from '@/components_taskPage/TaskList.vue';
import TabbedTaskList from '@/components_taskPage/DualTaskList.vue';
import TaskFilters from '@/components_taskPage/TaskFilters.vue';
import TaskStats from '@/components_taskPage/TaskStats.vue';
import TaskModal from '@/components_taskPage/TaskModal.vue';

export default {
  name: 'TaskPage',
  components: {
    TaskList,
    TabbedTaskList,
    TaskFilters,
    TaskStats,
    TaskModal
  },
  data() {
    return {
      tasks: [],
      hierarchicalTasks: [],
      filteredTasks: [],
      searchQuery: '',
      statusFilter: '',
      priorityFilter: '',
      showTaskModal: false,
      editingTask: null
    }
  },
  computed: {
    todoTasks() {
      return this.tasks.filter(task => task.status === 'not_started');
    },
    inProgressTasks() {
      return this.tasks.filter(task => task.status === 'in_progress');
    },
    completedTasks() {
      return this.tasks.filter(task => task.status === 'done');
    },
    totalTasks() {
      return this.tasks.length;
    }
  },
  mounted() {
    this.loadTasks();
  },
  methods: {
    async loadTasks() {
      try {
        // 从后端API获取层级结构的任务列表
        const response = await getHierarchicalTasks();
        // 将后端返回的优先级和状态值映射到前端使用的值
        this.tasks = this.flattenTasks(response);
        this.filteredTasks = [...this.tasks];
      } catch (error) {
        console.error('获取任务列表失败:', error);
        // 如果API调用失败，显示错误提示
        alert('获取任务列表失败，请稍后重试');
      }
    },
    
    // 将层级结构的任务转换为扁平结构，便于过滤和显示
    flattenTasks(hierarchicalTasks) {
      const flatTasks = [];
      
      const flatten = (tasks) => {
        for (const task of tasks) {
          // 映射当前任务
          const mappedTask = {
            ...task,
            status: this.mapStatusForFrontend(task.status),
            priority: this.mapPriorityForFrontend(task.priority),
            dueDate: task.dueDate
          };
          flatTasks.push(mappedTask);
          
          // 递归处理子任务
          if (task.children && task.children.length > 0) {
            flatten(task.children);
          }
        }
      };
      
      flatten(hierarchicalTasks);
      return flatTasks;
    },
    onFilterChange(filters) {
      this.searchQuery = filters.searchQuery;
      this.statusFilter = filters.statusFilter;
      this.priorityFilter = filters.priorityFilter;
      
      let result = this.tasks;
      
      // 根据搜索关键词过滤
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(task => 
          task.title.toLowerCase().includes(query) || 
          (task.description && task.description.toLowerCase().includes(query))
        );
      }
      
      // 根据状态过滤
      if (this.statusFilter) {
        result = result.filter(task => this.mapStatusForBackend(task.status) === this.statusFilter);
      }
      
      // 根据优先级过滤
      if (this.priorityFilter) {
        result = result.filter(task => this.mapPriorityForBackend(task.priority) === this.priorityFilter);
      }
      
      this.filteredTasks = result;
    },
    openCreateTaskModal() {
      this.editingTask = null;
      this.showTaskModal = true;
    },
    closeTaskModal() {
      this.showTaskModal = false;
    },
    editTask(task) {
      this.editingTask = { ...task };
      this.showTaskModal = true;
    },
    async saveTask(formData) {
      try {
        if (this.editingTask) {
          // 更新现有任务
          const response = await updateTask(this.editingTask.id, {
            title: formData.title,
            description: formData.description,
            priority: this.mapPriorityForBackend(formData.priority),
            deadline: formData.dueDate
          });
          
          // 更新本地任务列表
          const index = this.tasks.findIndex(task => task.id === this.editingTask.id);
          if (index !== -1) {
            this.tasks[index] = {
              ...this.tasks[index],
              title: response.title,
              description: response.description,
              priority: this.mapPriorityForFrontend(response.priority),
              dueDate: response.dueDate
            };
          }
        } else {
          // 创建新任务
          const response = await createTask({
            title: formData.title,
            description: formData.description,
            priority: this.mapPriorityForBackend(formData.priority),
            deadline: formData.dueDate
          });
          
          // 添加到本地任务列表
          this.tasks.push({
            ...response,
            status: this.mapStatusForFrontend(response.status),
            priority: this.mapPriorityForFrontend(response.priority),
            dueDate: response.dueDate
          });
        }
        
        this.closeTaskModal();
        // 重新应用过滤
        this.onFilterChange({
          searchQuery: this.searchQuery,
          statusFilter: this.statusFilter,
          priorityFilter: this.priorityFilter
        });
      } catch (error) {
        console.error('保存任务失败:', error);
        alert('保存任务失败，请稍后重试');
      }
    },
    async toggleTaskStatus(task) {
      try {
        // 确定下一个状态
        let nextStatus;
        if (task.status === 'done') {
          nextStatus = 'todo';
        } else {
          nextStatus = 'done'; // 简化逻辑 - 点击未完成的任务变为完成，完成的任务变为未完成
        }
        
        // 调用后端API更新状态
        const backendStatus = this.mapStatusForBackend(nextStatus);
        
        // 检查任务层级，如果是level 1的任务，使用后代更新API
        let response;
        if (task.level === 1) {
          const { updateTaskStatusWithDescendants } = await import('@/api/task');
          response = await updateTaskStatusWithDescendants(task.id, backendStatus);
        } else {
          response = await updateTaskStatus(task.id, backendStatus);
        }
        
        // 由于后端可能更新了多个任务的状态，重新加载整个任务列表以确保数据一致性
        await this.loadTasks();
        
      } catch (error) {
        console.error('更新任务状态失败:', error);
        alert('更新任务状态失败，请稍后重试');
      }
    },
    async deleteTask(taskId) {
      if (confirm('确定要删除这个任务吗？')) {
        try {
          await deleteTask(taskId);
          // 从本地任务列表中删除
          this.tasks = this.tasks.filter(task => task.id !== taskId);
          // 重新应用过滤
          this.onFilterChange({
            searchQuery: this.searchQuery,
            statusFilter: this.statusFilter,
            priorityFilter: this.priorityFilter
          });
        } catch (error) {
          console.error('删除任务失败:', error);
          alert('删除任务失败，请稍后重试');
        }
      }
    },
    
    // 递归更新所有后代任务的状态
    updateAllDescendantsStatus(parentId, newStatus) {
      // 找到所有子任务并更新它们的状态
      for (let i = 0; i < this.tasks.length; i++) {
        if (this.tasks[i].parent_id === parentId) {
          this.tasks[i].status = newStatus;
          // 递归更新这个子任务的子任务
          this.updateAllDescendantsStatus(this.tasks[i].id, newStatus);
        }
      }
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
    },
    
    
  }
}
</script>

<style scoped>
.task-page {
  padding: 24px;
  min-height: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 1.75rem;
  font-weight: bold;
  color: #f3f4f6;
}

.header-actions .btn-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: var(--highlight-gradient);
  border: none;
  border-radius: 16px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  font-size: 1rem;
}

.tasks-container .task-list-header {
  margin-bottom: 16px;
}

.tasks-container .task-list-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #f3f4f6;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .filters-container {
    flex-direction: column;
  }
}
</style>