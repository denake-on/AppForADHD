<template>
  <div class="card calendar-card">
    <div class="card-header">
      <h2 class="text-xl font-bold">{{ currentMonthYear }}</h2>
    </div>
    <div class="month-header">
      <span class="cursor-pointer" @click="prevMonth" style="font-size: 20px;">◀</span>
      <span class="font-medium">{{ dateRangeText }}</span>
      <span class="cursor-pointer" @click="nextMonth" style="font-size: 20px;">▶</span>
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
        class="calendar-day relative"
        :class="{
          'today': isToday(day),
          'has-task': hasTasksOnDate(day),
          'selected': isSelectedDate(day)
        }"
        @click="selectDate(day)"
      >
        <div class="date-number">{{ day }}</div>
        <!-- 显示当天任务数的小圆点 -->
        <div v-if="hasTasksOnDate(day)" class="task-indicator-dot"></div>
        <!-- 显示选中日期的弹出框 -->
        <div 
          v-if="isSelectedDate(day) && selectedDateTasks.length > 0"
          class="absolute z-10 top-full left-0 w-64 bg-[#2A233B] border border-purple-500 rounded-lg p-3 shadow-lg"
        >
          <div class="font-bold mb-2">{{ formatDateForDisplay(day) }}</div>
          <div v-for="task in selectedDateTasks" :key="task.id" class="text-sm mb-1 truncate">
            <span 
              class="status-dot inline-block w-2 h-2 rounded-full mr-2"
              :class="{
                'bg-gray-500': task.status === 'NOT_STARTED',
                'bg-blue-500': task.status === 'IN_PROGRESS',
                'bg-gradient-to-r from-purple-500 to-indigo-600': task.status === 'DONE'
              }"
            ></span>
            <span>{{ task.title }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
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
      selectedDateTasks: []
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
      return this.calendarData[dateStr] && this.calendarData[dateStr].length > 0
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
        this.selectedDateTasks = this.calendarData[dateStr] || []
      }
    },
    formatDateForDisplay(day) {
      return `${this.currentDate.getFullYear()}年${this.currentDate.getMonth() + 1}月${day}日`
    },
    prevMonth() {
      this.currentDate.setMonth(this.currentDate.getMonth() - 1)
      // 切换月份时清除选中的日期
      this.selectedDate = null
      this.selectedDateTasks = []
    },
    nextMonth() {
      this.currentDate.setMonth(this.currentDate.getMonth() + 1)
      // 切换月份时清除选中的日期
      this.selectedDate = null
      this.selectedDateTasks = []
    }
  }
}
</script>

<style scoped>
.calendar-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.month-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;  /* 减小月份标题区域的内边距 */
  font-size: 0.9rem;  /* 减小字体 */
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;  /* 进一步减小间距 */
  padding: 0 8px 8px;  /* 减小内边距 */
  flex: 1;
  overflow: hidden;
}

.calendar-day {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  font-weight: 500;
  font-size: 0.6rem;  /* 进一步减小字体大小 */
  position: relative;
  cursor: pointer;
  transition: background-color 0.2s;
  padding: 2px;  /* 添加小的内边距 */
}

.calendar-day:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.calendar-day.today {
  background: rgba(227, 142, 255, 0.15);
  box-shadow: 0 0 0 1.5px rgba(227, 142, 255, 0.4);
}

.calendar-day.has-task::after {
  content: '';
  position: absolute;
  bottom: 1px;
  right: 1px;
  width: 3px;
  height: 3px;
  background-color: #E38EFF;
  border-radius: 50%;
}

.task-indicator-dot {
  position: absolute;
  top: 1px;
  right: 1px;
  width: 3px;
  height: 3px;
  background-color: #E38EFF;
  border-radius: 50%;
  z-index: 1;
}

.date-number {
  position: relative;
  z-index: 0;
}
</style>