<template>
  <div v-if="show" class="modal-overlay" @click.self="cancel">
    <div class="modal-container">
      <div class="modal-header">
        <h3 class="modal-title">确认删除</h3>
        <button class="close-btn" @click="cancel">×</button>
      </div>
      
      <div class="modal-body">
        <div class="warning-icon">⚠️</div>
        <div class="warning-text">
          <p class="primary-text">您确定要删除这个任务吗？</p>
          <p class="secondary-text">此操作无法撤销，任务及其所有子任务都将被永久删除。</p>
        </div>
        
        <div v-if="taskTitle" class="task-preview">
          <span class="label">任务标题：</span>
          <span class="task-title">{{ taskTitle }}</span>
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="btn-cancel" @click="cancel">
          取消
        </button>
        <button class="btn-delete" @click="confirm">
          确认删除
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DeleteConfirmModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    taskTitle: {
      type: String,
      default: ''
    }
  },
  methods: {
    confirm() {
      this.$emit('confirm')
      this.$emit('close')
    },
    cancel() {
      this.$emit('cancel')
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  backdrop-filter: blur(4px);
}

.modal-container {
  background: linear-gradient(135deg, #2A233B 0%, #1C1B2E 100%);
  border-radius: 20px;
  border: 1px solid rgba(227, 142, 255, 0.3);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
  max-width: 480px;
  width: 90%;
  max-height: 90vh;
  overflow: hidden;
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 20px;
}

.modal-title {
  font-size: 20px;
  font-weight: 600;
  color: #EAE9F1;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: #9CA3AF;
  font-size: 24px;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #EAE9F1;
}

.modal-body {
  padding: 0 24px 20px;
  text-align: center;
}

.warning-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.warning-text {
  margin-bottom: 20px;
}

.primary-text {
  font-size: 16px;
  font-weight: 600;
  color: #EAE9F1;
  margin: 0 0 8px 0;
}

.secondary-text {
  font-size: 14px;
  color: #9CA3AF;
  margin: 0;
  line-height: 1.5;
}

.task-preview {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 16px;
  text-align: left;
}

.label {
  font-size: 12px;
  color: #9CA3AF;
  display: block;
  margin-bottom: 4px;
}

.task-title {
  font-size: 14px;
  color: #EAE9F1;
  font-weight: 500;
  word-break: break-word;
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 20px 24px 24px;
  justify-content: flex-end;
}

.btn-cancel {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #EAE9F1;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 80px;
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}

.btn-delete {
  background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: white;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 100px;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.btn-delete:hover {
  background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(239, 68, 68, 0.4);
}

.btn-delete:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
}

/* 响应式设计 */
@media (max-width: 480px) {
  .modal-container {
    width: 95%;
    margin: 0 10px;
  }
  
  .modal-header {
    padding: 20px 20px 0;
  }
  
  .modal-body {
    padding: 0 20px 16px;
  }
  
  .modal-footer {
    padding: 16px 20px 20px;
    flex-direction: column;
  }
  
  .btn-cancel,
  .btn-delete {
    width: 100%;
  }
}
</style>

