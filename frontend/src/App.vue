<template>
  <div class="dashboard-container">
    <!-- 左侧导航栏 -->
    <nav class="nav-bar">
      <div class="nav-icons">
        <div class="nav-icon active" data-page="home">
          <span class="icon">🏠</span>
        </div>
        <div class="nav-icon" data-page="task">
          <span class="icon">📋</span>
        </div>
      </div>
      <!-- 简化的用户头像按钮，无图片 -->
      <div class="user-avatar" @click="toggleProfile">
        👤
      </div>
    </nav>

    <!-- 右侧主内容区 -->
    <main class="main-content">
      <HomePage />
    </main>

    <!-- 个人资料页（左侧滑出面板）- 完全隐藏，直到需要显示 -->
    <div v-show="isProfileOpen" class="profile-panel" @click.self="toggleProfile">
      <div class="profile-header">
        <h1 class="text-2xl font-bold">个人资料</h1>
        <span class="close-btn" @click="toggleProfile">×</span>
      </div>
      
      <div class="profile-content">
        <div class="user-info">
          <div class="avatar-placeholder">👤</div>
          <div class="text-center">
            <h2 class="text-xl font-bold">用户</h2>
            <p class="text-gray-400">默认角色</p>
          </div>
        </div>
        
        <div class="card mb-6">
          <div class="p-6">
            <div class="flex justify-between mb-3">
              <span class="font-medium">级别进度</span>
              <span>Lv. 1</span>
            </div>
            <div class="w-full bg-gray-700 rounded-full h-3 mb-2">
              <div class="bg-gradient-to-r from-purple-500 to-indigo-600 h-3 rounded-full" style="width: 20%"></div>
            </div>
            <div class="flex justify-between text-sm text-gray-400">
              <span>100 Exp</span>
              <span>500 Exp</span>
            </div>
          </div>
        </div>
        
        <div class="card">
          <div class="card-header">
            <h3 class="font-bold">本周数据</h3>
          </div>
          <div class="p-6">
            <div class="flex justify-between py-3 border-b border-gray-700">
              <span>任务完成率</span>
              <span class="font-medium text-purple-400">50%</span>
            </div>
            <div class="flex justify-between py-3 border-b border-gray-700">
              <span>专注时间</span>
              <span class="font-medium">10小时</span>
            </div>
            <div class="flex justify-between py-3">
              <span>效率评分</span>
              <span class="font-medium text-purple-400">3.5/5.0</span>
            </div>
          </div>
        </div>
        
        <button class="btn-primary w-full mt-8">更新资料</button>
      </div>
    </div>
  </div>
</template>

<script>
import HomePage from './views/HomePage.vue'

export default {
  name: 'App',
  components: {
    HomePage
  },
  data() {
    return {
      isProfileOpen: false
    }
  },
  methods: {
    toggleProfile() {
      this.isProfileOpen = !this.isProfileOpen;
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

.user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 2px solid rgba(227, 142, 255, 0.4);
  box-shadow: 0 0 12px rgba(227, 142, 255, 0.5);
  background: #3A3450;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin-top: auto;
  font-size: 24px;
}

/* 个人资料面板样式 */
.profile-panel {
  position: fixed;
  top: 0;
  left: 72px; /* 默认在导航栏右侧，但不可见 */
  width: 420px;
  height: 100vh;
  background: linear-gradient(120deg, #2A233B 0%, #202038 100%);
  box-shadow: 16px 0 30px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  padding: 24px;
  border-radius: 0 24px 24px 0;
  display: flex;
  flex-direction: column;
  transform: translateX(-100%); /* 初始位置完全在左侧隐藏 */
  transition: transform 0.3s ease-out;
}

.profile-panel.v-enter-active,
.profile-panel.v-leave-active {
  transition: transform 0.3s ease-out;
}

.profile-panel.v-enter-from,
.profile-panel.v-leave-to {
  transform: translateX(-100%);
}

.profile-panel.active {
  transform: translateX(0);
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}

.close-btn {
  font-size: 24px;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.profile-content {
  flex: 1;
  overflow-y: auto;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 40px;
}

.avatar-placeholder {
  width: 112px;
  height: 112px;
  border-radius: 50%;
  background: linear-gradient(45deg, #E38EFF, #7E57C2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  margin-bottom: 16px;
  padding: 4px;
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