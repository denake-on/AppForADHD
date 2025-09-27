<template>
  <div class="card progress-card">
    <div class="card-header">
      <h2 class="text-xl font-bold">进度概览</h2>
    </div>
    <div class="p-6 flex items-center justify-around">
      <div class="pie-chart">
        <svg viewBox="0 0 100 100" class="pie-svg">
          <!-- 未开始任务扇形 -->
          <circle 
            v-if="totalTasks > 0"
            class="pie-segment" 
            :class="{ 'segment-orange': totalNotStarted > 0 }"
            cx="50" 
            cy="50" 
            r="40"
            :stroke-dasharray="`${notStartedPercentage * circumference / 100} ${(100 - notStartedPercentage) * circumference / 100}`"
            :stroke-dashoffset="`-${(inProgressPercentage + donePercentage) * circumference / 100}`"
            stroke="#F36C5C"
            stroke-width="8"
            fill="none"
            transform="rotate(-90, 50, 50)"
          />
          
          <!-- 进行中任务扇形 -->
          <circle 
            v-if="totalTasks > 0"
            class="pie-segment"
            :class="{ 'segment-blue': totalInProgress > 0 }"
            cx="50" 
            cy="50" 
            r="40"
            :stroke-dasharray="`${inProgressPercentage * circumference / 100} ${(100 - inProgressPercentage) * circumference / 100}`"
            :stroke-dashoffset="`-${donePercentage * circumference / 100}`"
            stroke="#4D7CFF"
            stroke-width="8"
            fill="none"
            transform="rotate(-90, 50, 50)"
          />
          
          <!-- 已完成任务扇形 -->
          <circle 
            v-if="totalTasks > 0"
            class="pie-segment"
            :class="{ 'segment-gradient': totalDone > 0 }"
            cx="50" 
            cy="50" 
            r="40"
            :stroke-dasharray="`${donePercentage * circumference / 100} ${(100 - donePercentage) * circumference / 100}`"
            :stroke-dashoffset="0"
            stroke="url(#gradient)"
            stroke-width="8"
            fill="none"
            transform="rotate(-90, 50, 50)"
          />
          
          <defs>
            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#E38EFF"></stop>
              <stop offset="100%" stop-color="#7E57C2"></stop>
            </linearGradient>
          </defs>
          
          <!-- 显示总完成百分比 -->
          <text x="50" y="50" text-anchor="middle" font-weight="bold" font-size="10" fill="white">{{ totalCompletion }}%</text>
        </svg>
      </div>
      <div class="legend">
        <div class="legend-item mb-3">
          <div class="status-dot status-orange mr-2"></div>
          <span class="text-sm">未开始 {{ totalNotStarted }}</span>
        </div>
        <div class="legend-item mb-3">
          <div class="status-dot status-blue mr-2"></div>
          <span class="text-sm">进行中 {{ totalInProgress }}</span>
        </div>
        <div class="legend-item">
          <div class="status-dot status-gradient mr-2"></div>
          <span class="text-sm">已完成 {{ totalDone }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProgressChart',
  props: {
    progressData: {
      type: Object,
      default: () => ({
        level_1: { NOT_STARTED: 0, IN_PROGRESS: 0, DONE: 0 },
        level_2: { NOT_STARTED: 0, IN_PROGRESS: 0, DONE: 0 },
        level_3: { NOT_STARTED: 0, IN_PROGRESS: 0, DONE: 0 }
      })
    }
  },
  data() {
    return {
      radius: 40,
    }
  },
  computed: {
    circumference() {
      return 2 * Math.PI * this.radius;
    },
    totalNotStarted() {
      return (this.progressData.level_1?.NOT_STARTED || 0) + 
             (this.progressData.level_2?.NOT_STARTED || 0) + 
             (this.progressData.level_3?.NOT_STARTED || 0);
    },
    totalInProgress() {
      return (this.progressData.level_1?.IN_PROGRESS || 0) + 
             (this.progressData.level_2?.IN_PROGRESS || 0) + 
             (this.progressData.level_3?.IN_PROGRESS || 0);
    },
    totalDone() {
      return (this.progressData.level_1?.DONE || 0) + 
             (this.progressData.level_2?.DONE || 0) + 
             (this.progressData.level_3?.DONE || 0);
    },
    totalTasks() {
      return this.totalNotStarted + this.totalInProgress + this.totalDone;
    },
    notStartedPercentage() {
      return this.totalTasks === 0 ? 0 : (this.totalNotStarted / this.totalTasks) * 100;
    },
    inProgressPercentage() {
      return this.totalTasks === 0 ? 0 : (this.totalInProgress / this.totalTasks) * 100;
    },
    donePercentage() {
      return this.totalTasks === 0 ? 0 : (this.totalDone / this.totalTasks) * 100;
    },
    totalCompletion() {
      if (this.totalTasks === 0) return 0;
      return Math.round((this.totalDone / this.totalTasks) * 100);
    }
  }
}
</script>

<style scoped>
.progress-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.p-6 {
  padding: 24px;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.flex {
  display: flex;
}

.items-center {
  align-items: center;
}

.justify-around {
  justify-content: space-around;
}

.pie-chart {
  position: relative;
  width: 200px;
  height: 200px;
}

.pie-svg {
  width: 100%;
  height: 100%;
}

.pie-segment {
  transition: stroke-dasharray 0.3s ease-out, stroke-dashoffset 0.3s ease-out;
}

.legend {
  display: flex;
  flex-direction: column;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}

.legend-item:last-child {
  margin-bottom: 0;
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 0.5rem;
}

.status-orange { background: #F36C5C; }
.status-blue { background: #4D7CFF; }
.status-gradient { 
  background: linear-gradient(90deg, #E38EFF 0%, #7E57C2 100%) !important; 
}

.mb-3 {
  margin-bottom: 0.75rem;
}

.mr-2 {
  margin-right: 0.5rem;
}

.text-sm {
  font-size: 0.875rem;
  line-height: 1.25rem;
  color: white;
}

.segment-orange {
  stroke: #F36C5C;
}

.segment-blue {
  stroke: #4D7CFF;
}

.segment-gradient {
  stroke: url(#gradient);
}
</style>