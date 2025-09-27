# WeiWan 任务管理系统

基于 FastAPI + SQLite + Vue3 + TailwindCSS 的现代化任务管理首页应用。

## 项目特性

- 🎯 **任务层级管理**：支持多级任务分解，父子任务关联
- 📊 **可视化进度**：实时进度图表和完成度统计
- 📅 **日历视图**：任务时间线展示
- 🚨 **紧急任务提醒**：智能任务优先级管理
- 🎨 **现代化UI**：基于TailwindCSS的响应式设计
- 🔄 **实时数据**：前后端分离架构，数据实时同步

## 项目架构

### 后端 (FastAPI + SQLite)
```
backend/
├── main.py                 # FastAPI应用入口，路由注册和CORS配置
├── database.py             # 数据库连接配置，SQLAlchemy引擎和会话管理
├── models.py               # 数据模型定义，Task实体和TaskStatus枚举
├── data/                   # 数据存储目录
│   ├── database.db         # SQLite数据库文件
│   └── greetings.json      # 欢迎语数据文件
└── welcomePage/            # 业务逻辑模块
    ├── __init__.py         # 模块初始化
    ├── greeting.py         # 欢迎语API路由
    ├── progress.py         # 进度统计API路由
    ├── tasks.py            # 任务管理API路由
    └── my_calendar.py      # 日历数据API路由
```

### 前端 (Vue3 + TailwindCSS)
```
frontend/
├── index.html              # HTML入口文件
├── package.json            # 项目依赖配置
├── vite.config.js          # Vite构建配置，包含API代理设置
├── tailwind.config.js      # TailwindCSS配置
├── src/
│   ├── main.js             # Vue应用入口
│   ├── App.vue             # 根组件，包含导航栏和布局
│   ├── index.css           # 全局样式文件
│   ├── api/
│   │   └── welcomePage.js  # API接口封装，axios配置
│   ├── views/
│   │   └── HomePage.vue    # 首页视图，四象限布局
│   └── components/         # 可复用组件
│       ├── MotivationCard.vue    # 激励卡片组件
│       ├── ProgressChart.vue     # 进度图表组件
│       ├── UrgentTasks.vue       # 紧急任务列表组件
│       └── CalendarView.vue      # 日历视图组件
└── weiwan.html             # 备用HTML文件
```

### 工具脚本
```
scripts/
└── init_db.py              # 数据库初始化脚本，创建表结构和示例数据
```

## 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

## 快速开始

### 1. 克隆项目
```bash
git clone <repository-url>
cd WeiWan
```

### 2. 后端配置

#### 创建虚拟环境
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

#### 安装依赖
```bash
pip install -r requirements.txt
```

#### 初始化数据库
```bash
# 创建数据库表结构和示例数据
python scripts/init_db.py
```

#### 启动后端服务
```bash
uvicorn backend.main:app --reload --port 8000
```

后端服务将在 `http://localhost:8000` 启动

### 3. 前端配置

#### 安装依赖
```bash
cd frontend
npm install
```

#### 启动开发服务器
```bash
npm run dev
```

前端服务将在 `http://localhost:3000` 启动

### 4. 访问应用
打开浏览器访问 `http://localhost:3000` 即可使用应用

## API 接口文档

### 欢迎语接口
- `GET /greeting` - 获取随机欢迎语
  - 返回：`{"greeting": "来自鼠鼠的问候：xxx"}`

### 进度统计接口
- `GET /progress` - 获取任务状态分布统计
  - 返回：按层级分组的任务状态统计
- `GET /completion` - 获取今日任务完成度
  - 返回：`{"today": 完成度百分比}`

### 任务管理接口
- `GET /tasks/urgent?limit=10` - 获取紧急任务列表
  - 参数：`limit` - 返回任务数量限制
  - 返回：紧急任务数组

### 日历接口
- `GET /calendar` - 获取本月任务日历数据
  - 返回：按日期分组的任务数据

### 健康检查
- `GET /health` - 服务健康状态检查
  - 返回：`{"status": "ok"}`

## 配置说明

### 后端配置
- 数据库文件位置：`backend/data/database.db`
- 欢迎语数据文件：`backend/data/greetings.json`
- 默认端口：8000

### 前端配置
- 开发服务器端口：3000
- API代理配置：`frontend/vite.config.js`
- 后端API地址：`http://localhost:8000`

## 开发说明

### 数据库结构
- **Task表**：存储任务信息
  - `id`: 主键
  - `title`: 任务标题
  - `description`: 任务描述
  - `deadline`: 截止日期
  - `status`: 任务状态（NOT_STARTED/IN_PROGRESS/DONE）
  - `progress_percent`: 完成进度百分比
  - `level`: 任务层级（1-3级）
  - `parent_id`: 父任务ID（支持任务分解）
  - `created_at/updated_at`: 创建/更新时间

### 前端组件说明
- **MotivationCard**: 显示欢迎语和今日完成度
- **ProgressChart**: ECharts饼图展示任务状态分布
- **UrgentTasks**: 紧急任务列表，支持状态筛选
- **CalendarView**: 日历视图，显示任务时间线

### 技术栈
- **后端**: FastAPI + SQLAlchemy + SQLite
- **前端**: Vue3 + Vite + TailwindCSS + ECharts
- **状态管理**: Vue3 Composition API
- **HTTP客户端**: Axios

## 故障排除

### 常见问题

1. **后端启动失败**
   ```bash
   # 检查Python版本
   python --version
   
   # 重新安装依赖
   pip install -r requirements.txt --force-reinstall
   ```

2. **前端无法连接后端**
   - 确认后端服务在8000端口运行
   - 检查`frontend/vite.config.js`中的代理配置
   - 确认防火墙设置

3. **数据库初始化失败**
   ```bash
   # 删除现有数据库重新初始化
   rm backend/data/database.db
   python scripts/init_db.py
   ```

4. **前端依赖安装失败**
   ```bash
   # 清除缓存重新安装
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

### 开发模式
- 后端支持热重载：`uvicorn backend.main:app --reload`
- 前端支持热重载：`npm run dev`
- API文档：访问 `http://localhost:8000/docs`

## 打包为 EXE（方向）

后端可使用 PyInstaller 将服务端封装为可执行程序，前端可打包为静态资源，由桌面壳（如 Electron/Tauri）或本地 WebView 加载。由于本项目定位为演示首页，未内置完整打包脚本。

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情


