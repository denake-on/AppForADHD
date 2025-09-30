<template>
  <div class="card motivation-card">
    <div class="card-header">
      <h2 class="text-xl font-bold">来自鼠鼠的问候</h2>
    </div>
    <div class="p-6 flex items-start justify-center h-3/4 relative pt-0 pb-8">
      <!-- 主要内容区域 -->
      <div class="main-content">
        <!-- 左侧鼠标图片 -->
        <div class="mouse-container">
          <img 
            :src="`/${mainImage}`" 
            :alt="mainImage" 
            class="mouse-image"
          />
        </div>
        
        <!-- 右侧欢迎语文本 -->
        <div class="greeting-container">
          <p class="font-bold text-center custom-medium-text greeting-text" v-html="greeting.replace(/\n/g, '<br>')"></p>
        </div>
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
      rightImage: '',
      mainImage: ''
    }
  },
  mounted() {
    this.selectRandomImages()
  },
  methods: {
    selectRandomImages() {
      const images = ['cool mouse.png', 'cryingandpeggingmouse.png', 'hurry mouse.png', 'lovelovelove.png']
      // 随机选择两张不同的图片
      const shuffled = images.sort(() => 0.5 - Math.random())
      this.leftImage = shuffled[0]
      this.rightImage = shuffled[1]
      
      // 随机选择主图片
      const mainImages = ['cool mouse.png', 'cryingandpeggingmouse.png', 'hurry mouse.png', 'lovelovelove.png']
      this.mainImage = mainImages[Math.floor(Math.random() * mainImages.length)]
    }
  }
}
</script>

<style scoped>
.custom-large-text {
  font-size: 4rem; /* 64px */
}

.custom-medium-text {
  font-size: clamp(1.2rem, 3vw, 2rem); /* 响应式字体大小 */
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .custom-medium-text {
    font-size: clamp(1rem, 3vw, 1.5rem);
  }
}

@media (max-width: 768px) {
  .custom-medium-text {
    font-size: clamp(0.9rem, 2.5vw, 1.2rem);
  }
}

@media (min-width: 1920px) {
  .custom-medium-text {
    font-size: clamp(1.5rem, 3.5vw, 2.5rem);
  }
}

/* 主要内容区域 */
.main-content {
  display: flex;
  align-items: center;
  gap: -30px;
  justify-content: flex-start;
  flex-direction: row;
  flex-wrap: nowrap;
  width: 100%;
  max-width: 600px;
  margin-left: -40px;
  position: relative;
  margin-top: -40px;
}

/* 鼠标图片容器 */
.mouse-container {
  flex-shrink: 0;
  z-index: 2;
  position: relative;
}

.mouse-image {
  width: 240px;
  height: 240px;
  object-fit: cover;
  border-radius: 16px;
  display: block;
  transition: transform 0.3s ease;
}

.mouse-image:hover {
  transform: scale(1.05);
}

/* 欢迎语容器 */
.greeting-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 欢迎语文本样式 */
.greeting-text {
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  min-width: 250px;
  z-index: 3;
  position: relative;
  margin-left: -30px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-content {
    gap: 16px;
    flex-direction: column;
    text-align: center;
    margin-left: 0;
    justify-content: center;
  }
  
  .mouse-image {
    width: 160px;
    height: 160px;
  }
  
  .greeting-text {
    min-width: 200px;
    font-size: clamp(1rem, 3vw, 1.5rem);
  }
}

@media (min-width: 1200px) {
  .main-content {
    gap: 16px;
  }
  
  .mouse-image {
    width: 260px;
    height: 260px;
  }
  
  .greeting-text {
    min-width: 300px;
  }
}

@media (min-width: 1920px) {
  .main-content {
    gap: 20px;
  }
  
  .mouse-image {
    width: 280px;
    height: 280px;
  }
  
  .greeting-text {
    min-width: 350px;
  }
}
</style>