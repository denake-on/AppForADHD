<template>
  <div class="card calendar-card">
    <div class="card-header">
      <h2 class="text-xl font-bold">{{ currentMonthYear }}</h2>
    </div>
    <div class="month-header">
      <button class="nav-button" @click="prevMonth" title="上个月">
        ◀
      </button>
      <span class="month-year-display">
        {{ currentMonthYear }}
        <span v-if="loading" class="loading-indicator">⏳</span>
      </span>
      <button class="nav-button" @click="nextMonth" title="下个月">
        ▶
      </button>
    </div>
    <div class="calendar-grid">
      <div class="calendar-day text-gray-500">一</div>
      <div class="calendar-day text-gray-500">二</div>
      <div class="calendar-day text-gray-500">三</div>
      <div class="calendar-day text-gray-500">四</div>
      <div class="calendar-day text-gray-500">五</div>
      <div class="calendar-day text-gray-500">六</div>
      <div class="calendar-day text-gray-500">日</div>
      
      <!-- 空白格子用于填充月份开始前的日期 -->
      <div 
        v-for="i in firstDayOfMonth" 
        :key="'empty-' + i" 
        class="calendar-day"
      ></div>
      
      <!-- 日期格子 -->
      <div 
        v-for="day in daysInMonth" 
        :key="day"
        :data-day="day"
        class="calendar-day relative"
        :class="{
          'today': isToday(day),
          'has-task': hasTasksOnDate(day),
          'selected': isSelectedDate(day)
        }"
        @click="selectDate(day)"
        @mouseenter="showTooltip(day)"
        @mouseleave="hideTooltip"
      >
        <div class="date-number">{{ day }}</div>
        <!-- 显示当天任务数的小圆点 -->
        <div v-if="hasTasksOnDate(day)" class="task-indicator-dot"></div>
        
        <!-- 鼠标悬停提示框 -->
        <div 
          v-if="hoveredDate === day && getTasksForDate(day).length > 0"
          class="tooltip"
        >
          <div class="tooltip-header">{{ formatDateForDisplay(day) }}</div>
          <div class="tooltip-content">
            <div v-for="task in getTasksForDate(day)" :key="task.id" class="tooltip-task">
              <span 
                class="tooltip-status-dot"
                :class="{
                  'status-not-started': task.status === 'NOT_STARTED',
                  'status-in-progress': task.status === 'IN_PROGRESS',
                  'status-done': task.status === 'DONE'
                }"
              ></span>
              <span class="tooltip-task-title">{{ task.title }}</span>
            </div>
          </div>
        </div>
        
        <!-- 显示选中日期的弹出框 -->
        <div 
          v-if="isSelectedDate(day) && selectedDateTasks.length > 0"
          class="selected-popup"
        >
          <div class="popup-header">{{ formatDateForDisplay(day) }}</div>
          <div class="popup-content">
            <div v-for="task in selectedDateTasks" :key="task.id" class="popup-task">
              <span 
                class="popup-status-dot"
                :class="{
                  'status-not-started': task.status === 'NOT_STARTED',
                  'status-in-progress': task.status === 'IN_PROGRESS',
                  'status-done': task.status === 'DONE'
                }"
              ></span>
              <span class="popup-task-title">{{ task.title }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getCalendarByMonth } from '@/api/welcomePage'

export default {
  name: 'CalendarView',
  props: {
    calendarData: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      currentDate: new Date(),
      selectedDate: null,
      selectedDateTasks: [],
      hoveredDate: null,
      currentMonthData: {}, // 当前月份的数据
      loading: false
    }
  },
  computed: {
    currentMonthYear() {
      return `${this.currentDate.getFullYear()}年${this.currentDate.getMonth() + 1}月`
    },
    daysInMonth() {
      return new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 0).getDate()
    },
    firstDayOfMonth() {
      // 获取月份第一天是星期几 (0=周日, 1=周一, ..., 6=周六)
      // 转换为 0=周一, 1=周二, ..., 6=周日 (符合中国习惯)
      const firstDay = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth(), 1).getDay()
      return firstDay === 0 ? 6 : firstDay - 1
    },
    dateRangeText() {
      // 显示当前周的范围，这里简化处理，显示当前月份
      return `${this.currentDate.getMonth() + 1}月`
    }
  },
  async mounted() {
    // 初始化时使用传入的数据
    this.currentMonthData = this.calendarData
    // 如果传入的数据为空，则获取当前月份的数据
    if (Object.keys(this.calendarData).length === 0) {
      await this.fetchCurrentMonthData()
    }
  },
  watch: {
    // 监听传入的calendarData变化
    calendarData: {
      handler(newData) {
        if (Object.keys(newData).length > 0) {
          this.currentMonthData = newData
        }
      },
      immediate: true
    }
  },
  methods: {
    isToday(day) {
      const today = new Date()
      return (
        this.currentDate.getMonth() === today.getMonth() &&
        this.currentDate.getFullYear() === today.getFullYear() &&
        day === today.getDate()
      )
    },
    isSelectedDate(day) {
      return this.selectedDate && 
             this.currentDate.getMonth() === new Date(this.selectedDate).getMonth() &&
             this.currentDate.getFullYear() === new Date(this.selectedDate).getFullYear() &&
             day === new Date(this.selectedDate).getDate()
    },
    hasTasksOnDate(day) {
      // 检查指定日期是否有任务
      const dateStr = `${this.currentDate.getFullYear()}-${String(this.currentDate.getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
      return this.currentMonthData[dateStr] && this.currentMonthData[dateStr].length > 0
    },
    selectDate(day) {
      // 选中特定日期，显示该日期的任务详情
      const dateStr = `${this.currentDate.getFullYear()}-${String(this.currentDate.getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
      
      if (this.selectedDate === dateStr) {
        // 如果再次点击已选中的日期，则取消选择
        this.selectedDate = null
        this.selectedDateTasks = []
      } else {
        this.selectedDate = dateStr
        this.selectedDateTasks = this.currentMonthData[dateStr] || []
        
        // 计算弹出框位置
        this.$nextTick(() => {
          this.positionPopup(day)
        })
      }
    },
    formatDateForDisplay(day) {
      return `${this.currentDate.getFullYear()}年${this.currentDate.getMonth() + 1}月${day}日`
    },
    async prevMonth() {
      const newDate = new Date(this.currentDate)
      newDate.setMonth(newDate.getMonth() - 1)
      this.currentDate = newDate
      // 切换月份时清除选中的日期
      this.selectedDate = null
      this.selectedDateTasks = []
      this.hoveredDate = null
      // 获取新月份的数据
      await this.fetchCurrentMonthData()
    },
    async nextMonth() {
      const newDate = new Date(this.currentDate)
      newDate.setMonth(newDate.getMonth() + 1)
      this.currentDate = newDate
      // 切换月份时清除选中的日期
      this.selectedDate = null
      this.selectedDateTasks = []
      this.hoveredDate = null
      // 获取新月份的数据
      await this.fetchCurrentMonthData()
    },
    showTooltip(day) {
      if (this.hasTasksOnDate(day)) {
        this.hoveredDate = day
      }
    },
    hideTooltip() {
      this.hoveredDate = null
    },
    getTasksForDate(day) {
      const dateStr = `${this.currentDate.getFullYear()}-${String(this.currentDate.getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
      return this.currentMonthData[dateStr] || []
    },
    async fetchCurrentMonthData() {
      try {
        this.loading = true
        const year = this.currentDate.getFullYear()
        const month = this.currentDate.getMonth() + 1
        const response = await getCalendarByMonth(year, month)
        this.currentMonthData = response
      } catch (error) {
        console.error('获取月份数据失败:', error)
        this.currentMonthData = {}
      } finally {
        this.loading = false
      }
    },
    positionPopup(day) {
      // 定位弹出框到合适的位置
      this.$nextTick(() => {
        const popup = this.$el.querySelector('.selected-popup')
        if (popup) {
          const dayElement = this.$el.querySelector(`[data-day="${day}"]`)
          if (dayElement) {
            const rect = dayElement.getBoundingClientRect()
            const popupRect = popup.getBoundingClientRect()
            
            // 计算最佳位置 - 让弹出框从当前日期格子的下方显示
            let top = rect.bottom + 8
            let left = rect.left + (rect.width / 2) - (popupRect.width / 2)
            
            // 确保弹出框不超出视窗右边界
            if (left + popupRect.width > window.innerWidth - 16) {
              left = window.innerWidth - popupRect.width - 16
            }
            // 确保弹出框不超出视窗左边界
            if (left < 16) {
              left = 16
            }
            
            // 如果下方空间不够，显示在上方
            if (top + popupRect.height > window.innerHeight - 16) {
              top = rect.top - popupRect.height - 8
            }
            
            popup.style.top = `${top}px`
            popup.style.left = `${left}px`
            popup.style.position = 'fixed'
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.calendar-card {
  background: rgba(49, 43, 70, 0.6);
  border-radius: 24px;
  border: 1px solid rgba(113, 89, 193, 0.4);
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.calendar-card::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 24px;
  padding: 1px;
  background: linear-gradient(90deg, #E38EFF 0%, #7E57C2 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, 
                linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.card-header {
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 1;
}

.month-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  position: relative;
  z-index: 1;
}

.nav-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #EAE9F1;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 16px;
  font-weight: bold;
}

.nav-button:hover {
  background: rgba(227, 142, 255, 0.2);
  border-color: rgba(227, 142, 255, 0.4);
  transform: scale(1.05);
}

.nav-button:active {
  transform: scale(0.95);
}

.month-year-display {
  font-size: 16px;
  font-weight: 600;
  color: #EAE9F1;
  display: flex;
  align-items: center;
  gap: 8px;
}

.loading-indicator {
  font-size: 14px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
  padding: 0 16px 20px;
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  position: relative;
  z-index: 1;
  min-height: 0;
}

/* 滚动条样式 */
.calendar-grid::-webkit-scrollbar {
  width: 4px;
}

.calendar-grid::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

.calendar-grid::-webkit-scrollbar-thumb {
  background: rgba(227, 142, 255, 0.6);
  border-radius: 2px;
}

.calendar-grid::-webkit-scrollbar-thumb:hover {
  background: rgba(227, 142, 255, 0.8);
}

.calendar-day {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-weight: 500;
  font-size: 12px;
  position: relative;
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 4px;
  min-height: 32px;
  height: 36px;
  color: #EAE9F1;
  isolation: isolate; /* 创建新的层叠上下文 */
  aspect-ratio: 1;
  box-sizing: border-box;
}

/* 小屏幕适配 */
@media (max-width: 768px) {
  .calendar-day {
    min-height: 28px;
    height: 32px;
    font-size: 11px;
    padding: 2px;
  }
  
  .calendar-grid {
    gap: 1px;
    padding: 0 8px 16px;
  }
  
  .month-header {
    padding: 12px 16px;
  }
  
  .card-header {
    padding: 16px 20px;
  }
}

.calendar-day:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: scale(1.05);
}

.calendar-day.today {
  background: rgba(227, 142, 255, 0.2);
  border: 1px solid rgba(227, 142, 255, 0.4);
  color: #E38EFF;
  font-weight: 600;
}

.calendar-day.has-task .date-number {
  position: relative;
}

.task-indicator-dot {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 4px;
  height: 4px;
  background: #E38EFF;
  border-radius: 50%;
  box-shadow: 0 0 4px rgba(227, 142, 255, 0.6);
}

.date-number {
  position: relative;
  z-index: 1;
}

/* 工具提示样式 */
.tooltip {
  position: fixed;
  bottom: auto;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(42, 35, 59, 0.95);
  border: 1px solid rgba(227, 142, 255, 0.4);
  border-radius: 12px;
  padding: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  z-index: 99999;
  min-width: 200px;
  max-width: 250px;
  margin-bottom: 8px;
}

.tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 6px solid transparent;
  border-top-color: rgba(227, 142, 255, 0.4);
}

.tooltip-header {
  font-size: 12px;
  font-weight: 600;
  color: #E38EFF;
  margin-bottom: 8px;
  text-align: center;
}

.tooltip-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.tooltip-task {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
}

.tooltip-status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.tooltip-task-title {
  color: #EAE9F1;
  line-height: 1.3;
  word-break: break-word;
}

/* 选中日期弹出框样式 */
.selected-popup {
  position: fixed;
  background: rgba(42, 35, 59, 0.95);
  border: 1px solid rgba(227, 142, 255, 0.4);
  border-radius: 12px;
  padding: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  z-index: 99999;
  min-width: 200px;
  max-width: 250px;
}

.popup-header {
  font-size: 12px;
  font-weight: 600;
  color: #E38EFF;
  margin-bottom: 8px;
  text-align: center;
}

.popup-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.popup-task {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
}

.popup-status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.popup-task-title {
  color: #EAE9F1;
  line-height: 1.3;
  word-break: break-word;
}

/* 状态点颜色 */
.status-not-started {
  background-color: #9CA3AF;
}

.status-in-progress {
  background-color: #3B82F6;
}

.status-done {
  background-color: #10B981;
}
</style>