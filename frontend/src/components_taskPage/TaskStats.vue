<template>
  <div class="stats-container">
    <div class="stat-card">
      <div class="stat-value">{{ todoTasksCount }}</div>
      <div class="stat-label">未开始</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{{ inProgressTasksCount }}</div>
      <div class="stat-label">进行中</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{{ completedTasksCount }}</div>
      <div class="stat-label">已完成</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{{ totalTasksCount }}</div>
      <div class="stat-label">总计</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TaskStats',
  props: {
    tasks: {
      type: Array,
      required: true
    }
  },
  computed: {
    todoTasksCount() {
      return this.tasks.filter(task => task.status === 'todo').length;
    },
    inProgressTasksCount() {
      return this.tasks.filter(task => task.status === 'in-progress').length;
    },
    completedTasksCount() {
      return this.tasks.filter(task => task.status === 'done').length;
    },
    totalTasksCount() {
      return this.tasks.length;
    }
  }
}
</script>

<style scoped>
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: var(--card-bg);
  border-radius: 24px;
  border: 1px solid rgba(113, 89, 193, 0.4);
  padding: 24px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.stat-card::after {
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

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #e38eff;
  margin-bottom: 4px;
}

.stat-label {
  color: #9ca3af;
  font-size: 0.875rem;
}
</style>