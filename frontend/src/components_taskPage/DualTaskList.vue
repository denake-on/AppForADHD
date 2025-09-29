<template>
  <div class="tabbed-task-list">
    <!-- 任务分类选项卡 -->
    <div class="tabs">
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'pending' }"
        @click="setActiveTab('pending')"
      >
        未完成任务
        <span class="task-count">({{ pendingTasks.length }})</span>
      </button>
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'history' }"
        @click="setActiveTab('history')"
      >
        历史任务
        <span class="task-count">({{ historyTasks.length }})</span>
      </button>
    </div>

    <!-- 任务列表 -->
    <div class="task-list-container">
      <HierarchicalTaskList 
        v-if="activeTab === 'pending'"
        :tasks="pendingTasks"
        @toggle-status="toggleTaskStatus"
        @edit-task="editTask"
        @delete-task="deleteTask"
        @task-added="onTaskAdded"
      />
      <HierarchicalTaskList 
        v-if="activeTab === 'history'"
        :tasks="historyTasks"
        @toggle-status="toggleTaskStatus"
        @edit-task="editTask"
        @delete-task="deleteTask"
        @task-added="onTaskAdded"
      />
    </div>
  </div>
</template>

<script>
import HierarchicalTaskList from '@/components_taskPage/HierarchicalTaskList.vue';
import HierarchicalSubtasks from '@/components_taskPage/HierarchicalSubtasks.vue';

export default {
  name: 'TabbedTaskList',
  components: {
    HierarchicalTaskList,
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
      activeTab: 'pending' // 默认显示未完成任务
    }
  },
  computed: {
    pendingTasks() {
      return this.filterHierarchicalTasks(task => {
        // 检查是否属于已完成的组（即其level 1根任务是否已完成）
        const isInCompletedGroup = this.isTaskInCompletedGroup(task);
        // 未完成的任务包括：不属于已完成组的任务，以及未过期的任务
        const isOverdue = this.isTaskOverdue(task);
        return !isInCompletedGroup && !isOverdue;
      });
    },
    historyTasks() {
      return this.filterHierarchicalTasks(task => {
        // 历史任务包括：属于已完成组的任务和已过期的任务
        const isInCompletedGroup = this.isTaskInCompletedGroup(task);
        const isOverdue = this.isTaskOverdue(task);
        return isInCompletedGroup || isOverdue;
      });
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
    setActiveTab(tab) {
      this.activeTab = tab;
    },
    isTaskOverdue(task) {
      if (!task.dueDate) return false; // 没有截止日期的任务不算过期
      
      // 将日期字符串转换为Date对象进行比较
      let dueDate;
      if (typeof task.dueDate === 'string') {
        dueDate = new Date(task.dueDate);
      } else if (task.dueDate instanceof Date) {
        dueDate = task.dueDate;
      } else {
        return false; // 如果日期格式不正确，不视为过期
      }
      
      const now = new Date();
      // 只有当截止日期早于当前日期且任务未完成时才视为过期
      return dueDate < now && task.status !== 'done';
    },
    // 从扁平结构重构层级结构
    groupTasksByHierarchy(tasks) {
      const rootTasks = [];
      const taskMap = {};
      
      // 创建任务映射
      tasks.forEach(task => {
        taskMap[task.id] = { ...task };
        taskMap[task.id].children = [];
      });
      
      // 构建层级关系
      tasks.forEach(task => {
        if (task.parent_id) {
          const parent = taskMap[task.parent_id];
          if (parent) {
            parent.children.push(taskMap[task.id]);
          }
        } else {
          rootTasks.push(taskMap[task.id]);
        }
      });
      
      // 按层级和创建时间排序
      const sortTasks = (taskList) => {
        taskList.sort((a, b) => {
          // 首先按层级排序，然后按创建时间排序
          if (a.level !== b.level) {
            return a.level - b.level;
          }
          // 如果创建时间存在，按创建时间排序
          if (a.createdAt && b.createdAt) {
            return new Date(a.createdAt) - new Date(b.createdAt);
          }
          return 0;
        });
        
        taskList.forEach(task => {
          if (task.children && task.children.length > 0) {
            sortTasks(task.children);
          }
        });
      };
      
      sortTasks(rootTasks);
      
      return rootTasks;
    },
    
    // 过滤层级任务
    filterHierarchicalTasks(filterFn) {
      // 对层级数据进行递归过滤
      const filterRecursively = (tasks) => {
        const result = [];
        for (const task of tasks) {
          // 递归处理子任务
          const filteredChildren = task.children ? filterRecursively(task.children) : [];
          
          // 检查当前任务是否符合过滤条件
          const currentTaskMatches = filterFn(task);
          
          if (currentTaskMatches || filteredChildren.length > 0) {
            // 如果当前任务符合条件，或者子任务中有符合条件的
            const taskCopy = { ...task };
            if (filteredChildren.length > 0) {
              taskCopy.children = filteredChildren;
            }
            result.push(taskCopy);
          }
        }
        return result;
      };
      
      // 执行过滤
      return filterRecursively(this.tasks);
    },
    
    // 检查任务是否属于已完成的组（即其level 1根任务是否已完成）
    isTaskInCompletedGroup(task) {
      // 递归查找根任务
      let currentTask = task;
      while (currentTask.parent_id) {
        // 在任务列表中查找父任务
        const parentTask = this.tasks.find(t => t.id === currentTask.parent_id);
        if (!parentTask) {
          break; // 没有找到父任务，跳出循环
        }
        currentTask = parentTask;
        
        // 如果当前任务是level 1任务，则停止查找
        if (currentTask.level === 1) {
          break;
        }
      }
      
      // 返回根任务（或level 1父任务）是否完成
      return currentTask.status === 'done';
    },
    
    onTaskAdded() {
      // 将事件冒泡到父组件
      this.$emit('task-added');
    }
  }
}
</script>

<style scoped>
.tabbed-task-list {
  width: 100%;
}

.tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.tab-btn {
  padding: 12px 24px;
  border: none;
  background: transparent;
  color: #9ca3af;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab-btn:hover {
  color: #f3f4f6;
  background: rgba(113, 89, 193, 0.1);
}

.tab-btn.active {
  color: #c084fc;
  border-bottom: 2px solid #c084fc;
  background: rgba(113, 89, 193, 0.15);
}

.task-count {
  font-size: 0.875rem;
  color: #9ca3af;
}

.tab-btn.active .task-count {
  color: #c084fc;
}

.task-list-container {
  min-height: 100px; /* 确保容器有最小高度 */
}
</style>