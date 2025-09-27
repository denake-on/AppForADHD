// src/api/welcomePage.js
import axios from 'axios'

// 创建axios实例
const apiClient = axios.create({
  baseURL: '/api', // 通过vite代理转发到后端
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  config => {
    // 在发送请求之前做些什么
    return config
  },
  error => {
    // 对请求错误做些什么
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  response => {
    // 对响应数据做点什么
    return response.data
  },
  error => {
    // 对响应错误做点什么
    console.error('API请求错误:', error)
    return Promise.reject(error)
  }
)

// 获取欢迎语
export const getGreeting = () => {
  return apiClient.get('/greeting')  // 实际后端路由是 /greeting
}

// 获取进度数据
export const getProgressSummary = () => {
  return apiClient.get('/progress')  // 实际后端路由是 /progress
}

// 获取今日完成度
export const getTodayCompletion = () => {
  return apiClient.get('/completion')  // 实际后端路由是 /completion
}

// 获取紧急任务列表
export const getUrgentTasks = (limit = 10) => {
  return apiClient.get(`/tasks/urgent?limit=${limit}`)  // 实际后端路由是 /tasks/urgent
}

// 获取日历数据
export const getCalendar = () => {
  return apiClient.get('/calendar')  // 实际后端路由是 /calendar
}

// 将进度和完成度合并为一个函数（因为它们可能都需要）
export const getProgress = async () => {
  try {
    const [progressSummary, todayCompletion] = await Promise.all([
      getProgressSummary(),
      getTodayCompletion()
    ]);
    
    return {
      ...progressSummary,
      today: todayCompletion.today
    };
  } catch (error) {
    console.error('获取进度数据失败:', error);
    throw error;
  }
};

export default apiClient