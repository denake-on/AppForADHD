<template>
  <div class="card motivation-card">
    <div class="card-header">
      <h2 class="text-xl font-bold">来自鼠鼠的问候</h2>
    </div>
    <div class="p-6 flex items-center justify-center h-3/4 relative">
      <!-- 主要内容区域 -->
      <div class="main-content">
        <!-- 左侧鼠标图片 -->
        <div class="mouse-container">
          <img 
            src="/mouse1.jpg" 
            alt="来自鼠鼠的问候" 
            class="mouse-image"
          />
        </div>
        
        <!-- 欢迎语文本 -->
        <p class="font-bold text-center custom--text greeting-text">{{ greeting }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MotivationCard',
  props: {
    greeting: {
      type: String,
      default: '加载中...'
    },
    todayCompletion: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      leftImage: '',
      rightImage: ''
    }
  },
  mounted() {
    this.selectRandomImages()
  },
  methods: {
    selectRandomImages() {
      const images = ['cry.png', 'love.png', 'portrait.png']
      // 随机选择两张不同的图片
      const shuffled = images.sort(() => 0.5 - Math.random())
      this.leftImage = shuffled[0]
      this.rightImage = shuffled[1]
    }
  }
}
</script>

<style scoped>
.custom-large-text {
  font-size: 4rem; /* 64px */
}

.custom-medium-text {
  font-size: clamp(1.5rem, 4vw, 2.5rem); /* 响应式字体大小 */
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .custom-medium-text {
    font-size: clamp(1.25rem, 3.5vw, 2rem);
  }
}

@media (max-width: 768px) {
  .custom-medium-text {
    font-size: clamp(1rem, 3vw, 1.5rem);
  }
}

@media (min-width: 1920px) {
  .custom-medium-text {
    font-size: clamp(2rem, 4.5vw, 3rem);
  }
}

/* 主要内容区域 */
.main-content {
  display: flex;
  align-items: center;
  gap: 24px;
  justify-content: center;
  flex-direction: row;
  flex-wrap: nowrap;
  width: 100%;
  max-width: 600px;
}

/* 鼠标图片容器 */
.mouse-container {
  flex-shrink: 0;
}

.mouse-image {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 16px;
  display: block;
  transition: transform 0.3s ease;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.mouse-image:hover {
  transform: scale(1.05);
}

/* 欢迎语文本样式 */
.greeting-text {
  flex: 1;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  background: rgba(255, 255, 255, 0.1);
  padding: 12px 20px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  min-width: 250px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-content {
    gap: 16px;
    flex-direction: column;
    text-align: center;
  }
  
  .mouse-image {
    width: 80px;
    height: 80px;
  }
  
  .greeting-text {
    min-width: 200px;
    font-size: clamp(1rem, 3vw, 1.5rem);
  }
}

@media (min-width: 1200px) {
  .main-content {
    gap: 32px;
  }
  
  .mouse-image {
    width: 140px;
    height: 140px;
  }
  
  .greeting-text {
    min-width: 300px;
  }
}

@media (min-width: 1920px) {
  .main-content {
    gap: 40px;
  }
  
  .mouse-image {
    width: 160px;
    height: 160px;
  }
  
  .greeting-text {
    min-width: 350px;
  }
}
</style>