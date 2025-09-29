<template>
  <div v-if="showModal" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>{{ task ? '编辑任务' : '新建任务' }}</h2>
        <span class="close-btn" @click="closeModal">×</span>
      </div>
      
      <div class="modal-body">
        <div class="form-group">
          <label for="task-title">任务标题</label>
          <input 
            type="text" 
            id="task-title"
            class="form-input" 
            v-model="formData.title"
            placeholder="输入任务标题"
          />
        </div>
        
        <div class="form-group">
          <label for="task-description">任务描述</label>
          <textarea 
            id="task-description"
            class="form-textarea" 
            v-model="formData.description"
            placeholder="输入任务描述"
          ></textarea>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="task-priority">优先级</label>
            <select 
              id="task-priority"
              class="form-select" 
              v-model="formData.priority"
            >
              <option value="low">低优先级</option>
              <option value="medium">中优先级</option>
              <option value="high">高优先级</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="task-due-date">截止日期</label>
            <input 
              type="date" 
              id="task-due-date"
              class="form-input" 
              v-model="formData.dueDate"
            />
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="btn-secondary" @click="closeModal">取消</button>
        <button class="btn-primary" @click="saveTask">{{ task ? '更新' : '创建' }}</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TaskModal',
  props: {
    showModal: {
      type: Boolean,
      required: true
    },
    task: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      formData: {
        title: '',
        description: '',
        priority: 'medium',
        dueDate: ''
      }
    }
  },
  watch: {
    task: {
      immediate: true,
      handler(newTask) {
        if (newTask) {
          this.formData = {
            title: newTask.title || '',
            description: newTask.description || '',
            priority: newTask.priority || 'medium',
            dueDate: newTask.dueDate || ''
          };
        } else {
          this.formData = {
            title: '',
            description: '',
            priority: 'medium',
            dueDate: ''
          };
        }
      }
    }
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
    saveTask() {
      if (!this.formData.title.trim()) {
        alert('请输入任务标题');
        return;
      }
      
      this.$emit('save', { ...this.formData });
    }
  }
}
</script>

<style scoped>
/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: var(--bg-gradient);
  border-radius: 24px;
  width: 90%;
  max-width: 500px; /* 调整为500px以适应输入框 */
  border: 1px solid rgba(113, 89, 193, 0.4);
  position: relative;
  overflow: hidden;
  max-height: 90vh; /* 添加最大高度限制 */
  overflow-y: auto; /* 允许在内容过多时滚动 */
}

.modal-content::after {
  content: '';
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

.modal-header {
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #f3f4f6;
}

.close-btn {
  font-size: 1.5rem;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  color: #f3f4f6;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.modal-body {
  padding: 24px;
  max-height: 60vh; /* 添加最大高度限制 */
  overflow-y: auto; /* 允许滚动 */
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #f3f4f6;
  font-weight: 500;
}

.form-input, .form-textarea, .form-select {
  width: 100%;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid rgba(113, 89, 193, 0.4);
  background: rgba(49, 43, 70, 0.6);
  color: #f3f4f6;
  font-size: 1rem;
  box-sizing: border-box; /* 添加这个属性确保padding不会增加元素的总宽度 */
}

.form-textarea {
  min-height: 100px;
  max-height: 150px; /* 限制文本域的最大高度 */
  resize: vertical;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.modal-footer {
  padding: 16px 24px 24px;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-secondary {
  padding: 12px 24px;
  border-radius: 16px;
  border: 1px solid rgba(113, 89, 193, 0.4);
  background: transparent;
  color: #f3f4f6;
  font-weight: 600;
  cursor: pointer;
}

.btn-primary {
  padding: 12px 24px;
  border-radius: 16px;
  background: var(--highlight-gradient);
  border: none;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    max-width: 95%;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 0;
  }
}
</style>