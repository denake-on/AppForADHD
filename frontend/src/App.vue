<template>
  <div class="dashboard-container">
    <!-- 左侧导航栏 -->
    <nav class="nav-bar">
      <div class="nav-icons">
        <div 
          class="nav-icon" 
          :class="{ active: currentPage === 'home' }"
          @click="changePage('home')"
        >
          <span class="icon">🏠</span>
        </div>
        <div 
          class="nav-icon" 
          :class="{ active: currentPage === 'task' }"
          @click="changePage('task')"
        >
          <span class="icon">📋</span>
        </div>
      </div>
    </nav>

    <!-- 右侧主内容区 -->
    <main class="main-content">
      <HomePage v-if="currentPage === 'home'" />
      <TaskPage v-if="currentPage === 'task'" />
    </main>
  </div>
</template>

<script>
import HomePage from './views/HomePage.vue'
import TaskPage from './views/TaskPage.vue'

export default {
  name: 'App',
  components: {
    HomePage,
    TaskPage
  },
  data() {
    return {
      currentPage: 'home'
    }
  },
  methods: {
    changePage(page) {
      this.currentPage = page;
    }
  }
}
</script>

<style>
:root {
  --bg-gradient: linear-gradient(140deg, #2A233B 0%, #1C1B2E 100%);
  --card-bg: rgba(49, 43, 70, 0.6);
  --highlight-gradient: linear-gradient(90deg, #E38EFF 0%, #7E57C2 100%);
}

.dashboard-container {
  width: 100%;
  height: 100vh;
  display: flex;
  position: relative;
  z-index: 1;
}

/* 导航栏样式 */
.nav-bar {
  width: 72px;
  height: 100vh;
  background: var(--bg-gradient);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
  position: fixed;
  border-right: 1px solid rgba(113, 100, 152, 0.3);
  z-index: 10;
}

.nav-icons {
  display: flex;
  flex-direction: column;
  gap: 32px;
  flex: 1;
}

.nav-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.nav-icon.active {
  background: rgba(127, 87, 194, 0.2);
  box-shadow: 0 0 0 2px transparent;
  position: relative;
}

.nav-icon.active::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 14px;
  padding: 2px;
  background: var(--highlight-gradient);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, 
                linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
}

.main-content {
  margin-left: 72px;
  flex: 1;
  padding: 28px;
  overflow-y: auto;
  scrollbar-width: none;
}

.main-content::-webkit-scrollbar {
  display: none;
}

/* 通用卡片样式 */
.card {
  background: var(--card-bg);
  border-radius: 24px;
  border: 1px solid rgba(113, 89, 193, 0.4);
  position: relative;
  overflow: hidden;
  margin-bottom: 24px;
}

.card::after {
  content: "";
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

.card-header {
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.p-6 {
  padding: 24px;
}

.mb-6 {
  margin-bottom: 24px;
}

.mb-3 {
  margin-bottom: 12px;
}

.py-3 {
  padding: 12px 0;
}

.border-b {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.border-gray-700 {
  border-color: rgba(77, 74, 99, 1);
}

.text-2xl {
  font-size: 1.5rem;
  line-height: 2rem;
}

.text-xl {
  font-size: 1.25rem;
  line-height: 1.75rem;
}

.text-lg {
  font-size: 1.125rem;
  line-height: 1.75rem;
}

.font-bold {
  font-weight: 700;
}

.font-medium {
  font-weight: 500;
}

.text-center {
  text-align: center;
}

.text-gray-400 {
  color: #9CA3AF;
}

.text-purple-400 {
  color: #C4B5FD;
}

.w-full {
  width: 100%;
}

.h-3 {
  height: 0.75rem;
}

.rounded-full {
  border-radius: 9999px;
}

.bg-gray-700 {
  background-color: #374151;
}

.bg-gradient-to-r {
  background-image: linear-gradient(to right, var(--tw-gradient-stops));
}

.from-purple-500 {
  --tw-gradient-from: #a78bfa;
  --tw-gradient-to: rgba(167, 139, 250, 0);
  --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to);
}

.to-indigo-600 {
  --tw-gradient-to: #4f46e5;
}

.flex {
  display: flex;
}

.flex-col {
  flex-direction: column;
}

.items-center {
  align-items: center;
}

.justify-center {
  justify-content: center;
}

.justify-between {
  justify-content: space-between;
}

.w-3 {
  width: 0.75rem;
}

.h-3 {
  height: 0.75rem;
}

.rounded {
  border-radius: 0.25rem;
}

.btn-primary {
  background: var(--highlight-gradient);
  border: none;
  padding: 12px 24px;
  border-radius: 16px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  font-size: 1rem;
}

.mt-8 {
  margin-top: 2rem;
}

.mb-10 {
  margin-bottom: 2.5rem;
}

.mb-2 {
  margin-bottom: 0.5rem;
}

.mb-4 {
  margin-bottom: 1rem;
}

.mr-2 {
  margin-right: 0.5rem;
}

.ml-auto {
  margin-left: auto;
}

.text-sm {
  font-size: 0.875rem;
  line-height: 1.25rem;
}

.py-2 {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

.py-4 {
  padding-top: 1rem;
  padding-bottom: 1rem;
}
</style>