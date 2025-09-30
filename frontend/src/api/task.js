import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// 获取任务列表（扁平结构）
export const getTasks = async (params = {}) => {
  const response = await axios.get(`${API_BASE_URL}/tasks/`, { params });
  return response.data;
};

// 获取任务列表（层级结构）
export const getHierarchicalTasks = async () => {
  const response = await axios.get(`${API_BASE_URL}/tasks/hierarchical`);
  return response.data;
};

// 获取单个任务
export const getTask = async (taskId) => {
  const response = await axios.get(`${API_BASE_URL}/tasks/${taskId}`);
  return response.data;
};

// 创建新任务
export const createTask = async (taskData) => {
  const response = await axios.post(`${API_BASE_URL}/tasks/`, null, {
    params: taskData
  });
  return response.data;
};

// 更新任务
export const updateTask = async (taskId, taskData) => {
  const response = await axios.put(`${API_BASE_URL}/tasks/${taskId}`, null, {
    params: taskData
  });
  return response.data;
};

// 删除任务
export const deleteTask = async (taskId) => {
  const response = await axios.delete(`${API_BASE_URL}/tasks/${taskId}`);
  return response.data;
};

// 更新任务状态
export const updateTaskStatus = async (taskId, status) => {
  const response = await axios.patch(`${API_BASE_URL}/tasks/${taskId}/status`, null, {
    params: { status }
  });
  return response.data;
};

// 更新任务状态及其所有后代
export const updateTaskStatusWithDescendants = async (taskId, status) => {
  const response = await axios.patch(`${API_BASE_URL}/tasks/${taskId}/status-with-descendants`, null, {
    params: { status }
  });
  return response.data;
};

// 拆解任务
export const breakdownTask = async (taskId, prompt) => {
  const response = await axios.post(`${API_BASE_URL}/tasks/${taskId}/breakdown`, null, {
    params: { prompt }
  });
  return response.data;
};

// 确认拆解的子任务
export const confirmBreakdownTasks = async (taskId, subtasks) => {
  const response = await axios.post(`${API_BASE_URL}/tasks/${taskId}/breakdown/confirm`, subtasks);
  return response.data;
};