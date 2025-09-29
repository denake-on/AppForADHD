<template>
  <div class="filters-container">
    <div class="search-box-wrapper">
      <div class="search-box">
        <input 
          type="text" 
          class="search-input" 
          placeholder="搜索任务..." 
          v-model="searchQuery"
          @input="onSearchChange"
        />
        <span class="search-icon">🔍</span>
      </div>
    </div>
    
    <div class="filter-options">
      <select class="filter-select" v-model="statusFilter" @change="onFilterChange">
        <option value="">全部状态</option>
        <option value="todo">待办</option>
        <option value="in-progress">进行中</option>
        <option value="done">已完成</option>
      </select>
      
      <select class="filter-select" v-model="priorityFilter" @change="onFilterChange">
        <option value="">全部优先级</option>
        <option value="low">低优先级</option>
        <option value="medium">中优先级</option>
        <option value="high">高优先级</option>
      </select>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TaskFilters',
  props: {
    initialSearchQuery: {
      type: String,
      default: ''
    },
    initialStatusFilter: {
      type: String,
      default: ''
    },
    initialPriorityFilter: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      searchQuery: this.initialSearchQuery,
      statusFilter: this.initialStatusFilter,
      priorityFilter: this.initialPriorityFilter
    }
  },
  methods: {
    onSearchChange() {
      this.$emit('filter-change', {
        searchQuery: this.searchQuery,
        statusFilter: this.statusFilter,
        priorityFilter: this.priorityFilter
      });
    },
    onFilterChange() {
      this.$emit('filter-change', {
        searchQuery: this.searchQuery,
        statusFilter: this.statusFilter,
        priorityFilter: this.priorityFilter
      });
    }
  }
}
</script>

<style scoped>
.filters-container {
  display: grid;
  grid-template-columns: 1fr auto; /* 使用网格布局，搜索框占剩余空间，筛选器自动宽度 */
  gap: 16px;
  margin-bottom: 24px;
  align-items: center; /* 垂直居中对齐 */
  padding: 0 8px; /* 添加一些内边距 */
}

.search-box-wrapper {
  position: relative;
  min-width: 200px;
  max-width: 400px; /* 限制最大宽度 */
}

.search-box {
  position: relative;
}

.search-input {
  width: 100%;
  padding: 12px 16px 12px 40px;
  border-radius: 12px;
  border: 1px solid rgba(113, 89, 193, 0.4);
  background: rgba(49, 43, 70, 0.6);
  color: #f3f4f6;
  font-size: 0.875rem;
  transition: border-color 0.2s; /* 添加过渡效果 */
}

.search-input:focus {
  outline: none;
  border-color: #7e57c2; /* 聚焦时的边框颜色 */
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  pointer-events: none; /* 防止图标影响输入框点击 */
}

.filter-options {
  display: flex;
  gap: 12px;
  align-items: center;
}

.filter-select {
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid rgba(113, 89, 193, 0.4);
  background: rgba(49, 43, 70, 0.6);
  color: #f3f4f6;
  min-width: 130px;
  width: 130px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: border-color 0.2s, background-color 0.2s; /* 添加背景过渡效果 */
  appearance: none; /* 移除默认样式 */
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%239ca3af' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px;
  padding-right: 40px; /* 为下拉箭头留出空间 */
}

/* 悬停效果 */
.filter-select:hover {
  background: rgba(66, 57, 94, 0.8); /* 添加悬停时的背景色，更符合整体色调 */
  border-color: rgba(126, 87, 194, 0.6);
}

/* 焦点效果 */
.filter-select:focus {
  outline: none;
  border-color: #7e57c2; /* 聚焦时的边框颜色 */
  background: rgba(66, 57, 94, 0.9); /* 聚焦时的背景色 */
}

.filter-select:focus {
  outline: none;
  border-color: #7e57c2; /* 聚焦时的边框颜色 */
}

/* 针对小屏幕的响应式调整 */
@media (max-width: 768px) {
  .filters-container {
    grid-template-columns: 1fr; /* 小屏幕上单列布局 */
    grid-template-rows: auto auto;
  }
  
  .search-box-wrapper {
    max-width: 100%; /* 小屏幕上搜索框占满宽度 */
  }
  
  .filter-options {
    width: 100%;
    justify-content: space-between;
  }
  
  .filter-select {
    flex: 1;
    min-width: calc(50% - 6px); 
  }
}
</style>