<template>
  <div class="home-grid">
    <!-- 左上角：欢迎卡片 -->
    <div class="quadrant quadrant-1">
      <MotivationCard :greeting="greeting" :today-completion="todayCompletion" />
    </div>
    
    <!-- 右上角：进度饼图 -->
    <div class="quadrant quadrant-2">
      <ProgressChart :progress-data="progressData" />
    </div>
    
    <!-- 左下角：紧急任务列表 -->
    <div class="quadrant quadrant-3">
      <UrgentTasks :urgent-tasks="urgentTasks" />
    </div>
    
    <!-- 右下角：日历 -->
    <div class="quadrant quadrant-4">
      <CalendarView :calendar-data="calendarData" />
    </div>
  </div>
</template>

<script>
import MotivationCard from '@/components/MotivationCard.vue'
import ProgressChart from '@/components/ProgressChart.vue'
import UrgentTasks from '@/components/UrgentTasks.vue'
import CalendarView from '@/components/CalendarView.vue'
import { getGreeting, getProgress, getUrgentTasks, getCalendar } from '@/api/welcomePage'

export default {
  name: 'HomePage',
  components: {
    MotivationCard,
    ProgressChart,
    UrgentTasks,
    CalendarView
  },
  data() {
    return {
      greeting: '加载中...',
      todayCompletion: 0,
      progressData: {
        level_1: { NOT_STARTED: 0, IN_PROGRESS: 0, DONE: 0 },
        level_2: { NOT_STARTED: 0, IN_PROGRESS: 0, DONE: 0 },
        level_3: { NOT_STARTED: 0, IN_PROGRESS: 0, DONE: 0 }
      },
      urgentTasks: [],
      calendarData: {}
    }
  },
  async mounted() {
    await this.fetchData()
  },
  methods: {
    async fetchData() {
      try {
        // 获取欢迎语
        const greetingResponse = await getGreeting()
        this.greeting = greetingResponse.greeting
        
        // 获取进度数据（包括今日完成度）
        const progressResponse = await getProgress()
        this.progressData = progressResponse
        if (progressResponse.today !== -1) {
          this.todayCompletion = progressResponse.today
        } else {
          this.todayCompletion = 0
        }
        
        // 获取紧急任务
        const tasksResponse = await getUrgentTasks()
        this.urgentTasks = tasksResponse
        
        // 获取日历数据
        const calendarResponse = await getCalendar()
        this.calendarData = calendarResponse
      } catch (error) {
        console.error('获取首页数据失败:', error)
        // 设置默认值
        this.greeting = '获取问候语失败'
        this.todayCompletion = 0
        this.urgentTasks = []
        this.calendarData = {}
      }
    }
  }
}
</script>

<style scoped>
.home-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;  /* 将容器分为两列 */
  grid-template-rows: 1fr 1fr;     /* 将容器分为两行 */
  gap: 24px;
  height: calc(100vh - 56px);      /* 减去顶部和底部的边距 */
}

.quadrant {
  min-height: 300px;  /* 设置最小高度 */
  display: flex;
  flex-direction: column;
  height: 100%;       /* 确保充满分配的空间 */
}

.quadrant-1 {
  grid-column: 1;   /* 第一列 */
  grid-row: 1;      /* 第一行 */
}

.quadrant-2 {
  grid-column: 2;   /* 第二列 */
  grid-row: 1;      /* 第一行 */
}

.quadrant-3 {
  grid-column: 1;   /* 第一列 */
  grid-row: 2;      /* 第二行 */
}

.quadrant-4 {
  grid-column: 2;   /* 第二列 */
  grid-row: 2;      /* 第二行 */
}

/* 确保卡片组件填充整个象限 */
.quadrant > div {
  height: 100%;
  min-height: 0;  /* 允许flex子项收缩 */
  display: flex;
  flex-direction: column;
}

/* 为日历组件设置最大高度，防止溢出 */
.quadrant-4 .calendar-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.quadrant-4 .calendar-grid {
  flex: 1;
  min-height: 0; /* 允许内容收缩 */
  overflow-y: auto;
}

/* 小屏幕适配 */
@media (max-width: 768px) {
  .home-grid {
    gap: 16px;
    height: calc(100vh - 48px);
  }
  
  .quadrant {
    min-height: 250px;
  }
}

@media (max-width: 480px) {
  .home-grid {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto auto;
    gap: 12px;
  }
  
  .quadrant-1, .quadrant-2, .quadrant-3, .quadrant-4 {
    grid-column: 1;
  }
  
  .quadrant-1 { grid-row: 1; }
  .quadrant-2 { grid-row: 2; }
  .quadrant-3 { grid-row: 3; }
  .quadrant-4 { grid-row: 4; }
}
</style>