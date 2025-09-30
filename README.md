# WeiWan 任务管理系统

基于 FastAPI + SQLite + Vue3 + TailwindCSS。

## 核心功能

- 任务管理：创建、编辑、删除和追踪任务
- **AI任务拆解**：利用AI将复杂任务智能拆解为多个可执行的子任务
- 层级任务管理：支持多层级子任务结构
- 进度统计：任务完成度可视化展示
- 日历视图：任务时间线管理
- 激励系统：每日随机欢迎语和完成度激励

## 项目架构

### 后端 (FastAPI + SQLite)
```
backend/
├── main.py                 # FastAPI应用入口，路由注册和CORS配置
├── database.py             # 数据库连接配置，SQLAlchemy引擎和会话管理
├── models.py               # 数据模型定义，Task实体和TaskStatus枚举
├── run_app.py              # 应用启动脚本 (EXE打包入口)
├── data/                   # 数据存储目录
│   ├── database.db         # SQLite数据库文件
│   └── greetings.json      # 欢迎语数据文件
├── task/                   # 任务管理模块
│   ├── __init__.py         # 模块初始化
│   ├── BreakDownTask.py    # AI任务拆解服务 (使用OpenRouter API)
│   ├── crud.py             # 任务操作CRUD方法
│   └── routes.py           # 任务相关API路由 (包括AI拆解和层级结构)
├── welcomePage/            # 欢迎页业务逻辑模块
│   ├── __init__.py         # 模块初始化
│   ├── greeting.py         # 欢迎语API路由
│   ├── progress.py         # 进度统计API路由
│   ├── tasks.py            # 任务管理API路由
│   └── my_calendar.py      # 日历数据API路由
└── __pycache__/            # Python缓存文件目录
```

### 前端 (Vue3 + TailwindCSS)
```
frontend/
├── index.html              # HTML入口文件
├── package.json            # 项目依赖配置
├── vite.config.js          # Vite构建配置，包含API代理设置
├── tailwind.config.js      # TailwindCSS配置
├── WeiWan.html             # 原型图HTML文件
├── dist/                   # 构建后的静态文件目录
├── public/                 # 静态资源目录
├── src/                    # 源代码目录
│   ├── main.js             # Vue应用入口
│   ├── App.vue             # 根组件，包含导航栏和布局
│   ├── index.css           # 全局样式文件
│   ├── api/                # API接口封装目录
│   │   └── welcomePage.js  # API接口封装，axios配置
│   ├── components/         # 通用可复用组件目录
│   │   ├── MotivationCard.vue    # 激励卡片组件
│   │   ├── ProgressChart.vue     # 进度图表组件
│   │   ├── UrgentTasks.vue       # 紧急任务列表组件
│   │   └── CalendarView.vue      # 日历视图组件
│   ├── components_taskPage/        # 任务页面专用组件目录
│   │   ├── DeleteConfirmModal.vue    # 删除确认模态框组件
│   │   ├── DualTaskList.vue          # 双列任务列表组件 (AI拆解预览)
│   │   ├── HierarchicalSubtasks.vue  # 层级子任务组件
│   │   ├── HierarchicalTaskList.vue  # 层级任务列表组件
│   │   ├── TaskFilters.vue           # 任务过滤组件
│   │   ├── TaskList.vue              # 基础任务列表组件
│   │   ├── TaskModal.vue             # 任务编辑模态框组件
│   │   └── TaskStats.vue             # 任务统计组件
│   └── views/              # 页面视图目录
│       └── HomePage.vue    # 首页视图，四象限布局
├── node_modules/           # Node.js依赖包目录
└── package-lock.json       # 依赖锁定文件
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
- API密钥 (用于AI任务拆解功能，支持OpenRouter API)

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
# 如需使用AI任务拆解功能，可能需要安装额外依赖
pip install requests
```

#### 初始化数据库
```bash
# 创建数据库表结构和示例数据
python scripts/init_db.py
```

#### 配置AI任务拆解 (可选)
如需使用AI任务拆解功能，需设置API密钥：
```bash
# 在项目根目录创建 .env 文件
echo OPENROUTER_API_KEY="your-api-key-here" > .env
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

### 5. AI任务拆解功能使用
1. 在任务页面创建一个复杂任务
2. 点击任务旁的"AI拆解"按钮
3. 输入对AI的拆解要求 (如"将此任务拆解为3-5个具体步骤")
4. AI将生成子任务建议，确认后自动创建到任务列表中

## API 接口文档

### 欢迎语接口
- `GET /greeting` - 获取随机欢迎语
  - 返回：`{"greeting": "来自/*6的问候：xxx"}`

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

### 任务层级管理接口
- `GET /api/tasks/` - 获取任务列表
  - 参数：`skip`, `limit`, `status`, `priority`, `search`
  - 返回：任务数组
- `GET /api/tasks/hierarchical` - 获取层级结构任务列表
  - 参数：`status`, `priority`, `search`
  - 返回：包含父子关系的层级任务结构
- `GET /api/tasks/{task_id}` - 获取单个任务详情
- `POST /api/tasks/` - 创建新任务
  - 参数：`title`, `description`, `deadline`, `priority`, `parent_id`, `level`
- `PUT /api/tasks/{task_id}` - 更新任务
- `DELETE /api/tasks/{task_id}` - 删除任务
- `PATCH /api/tasks/{task_id}/status` - 更新任务状态
- `PATCH /api/tasks/{task_id}/status-with-descendants` - 更新任务及其所有后代状态

### AI任务拆解接口
- `POST /api/tasks/{task_id}/breakdown` - AI拆解任务
  - 参数：`task_id`, `prompt` (拆解要求描述)
  - 返回：AI生成的子任务建议数组
- `POST /api/tasks/{task_id}/breakdown/confirm` - 确认并保存AI拆解的子任务
  - 参数：`task_id`, `subtasks` (子任务数组)
  - 返回：确认创建的子任务信息

### 健康检查
- `GET /health` - 服务健康状态检查
  - 返回：`{"status": "ok"}`

## 配置说明

### 后端配置
- 数据库文件位置：`backend/data/database.db`
- 欢迎语数据文件：`backend/data/greetings.json`
- AI任务拆解API密钥：通过环境变量 `OPENROUTER_API_KEY` 配置
- AI模型：使用 `deepseek/deepseek-r1-0528` 模型 (可在 `backend/task/BreakDownTask.py` 中修改)
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

### AI任务拆解功能
- **AI服务**: 通过OpenRouter API调用DeepSeek R1模型
- **拆解逻辑**: 基于任务标题、描述、截止日期和优先级进行智能拆解
- **输出格式**: JSON格式的子任务数组，包含标题、描述、截止日期和优先级
- **API密钥**: 通过环境变量 `OPENROUTER_API_KEY` 配置
- **请求超时**: 30秒

### 前端组件说明
- **MotivationCard**: 显示欢迎语和今日完成度
- **ProgressChart**: ECharts饼图展示任务状态分布
- **UrgentTasks**: 紧急任务列表，支持状态筛选
- **CalendarView**: 日历视图，显示任务时间线
- **HierarchicalTaskList**: 层级任务列表组件，支持多级任务展示
- **HierarchicalSubtasks**: 子任务展示组件，支持展开/折叠
- **DualTaskList**: 双列任务列表，用于AI拆解预览
- **TaskModal**: 任务编辑模态框，支持任务创建和编辑
- **TaskFilters**: 任务过滤组件，支持按状态、优先级筛选
- **DeleteConfirmModal**: 删除确认模态框

### 后端模块说明
- **task.crud**: 任务CRUD操作和层级关系处理
- **task.routes**: 任务相关API路由，包括AI拆解接口
- **task.BreakDownTask**: AI任务拆解核心服务
- **welcomePage**: 欢迎页相关API（问候语、统计等）

### 技术栈
- **后端**: FastAPI + SQLAlchemy + SQLite + Requests (AI API)
- **前端**: Vue3 + Vite + TailwindCSS + ECharts + Axios
- **状态管理**: Vue3 Composition API
- **AI服务**: OpenRouter API + DeepSeek R1模型

## AI任务拆解功能详解

AI任务拆解是WeiWan应用的核心创新功能，它能够将复杂任务自动拆解为可执行的子任务。该功能的工作流程如下：

1. **任务分析**: AI分析任务标题、描述、截止日期和优先级
2. **智能拆解**: 利用大语言模型将任务拆解为具体的、可执行的子任务
3. **时间规划**: 为每个子任务设置合理的截止日期
4. **优先级分配**: 根据子任务的重要性和紧急性设置优先级
5. **结果呈现**: 在前端以双列列表形式展示原任务和AI生成的子任务
6. **一键确认**: 用户可选择确认并创建AI生成的子任务到数据库

该功能特别适合处理复杂项目，帮助用户将宏观目标转化为具体行动步骤。

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

5. **AI任务拆解功能失败**
   - 确认已设置正确的 `OPENROUTER_API_KEY` 环境变量
   - 检查网络连接是否正常
   - 确认API密钥有足够的调用额度
   - 查看后端日志中的详细错误信息

6. **层级任务显示异常**
   - 确认任务的parent_id和level字段正确设置
   - 检查数据库中父子关系是否正确建立

### 开发模式
- 后端支持热重载：`uvicorn backend.main:app --reload`
- 前端支持热重载：`npm run dev`
- API文档：访问 `http://localhost:8000/docs`

## 打包为 EXE（方向）

后端可使用 PyInstaller 将服务端封装为可执行程序，前端可打包为静态资源，由桌面壳（如 Electron/Tauri）或本地 WebView 加载。由于本项目定位为演示首页，未内置完整打包脚本。

如需打包包含AI功能的EXE：
1. 在打包前确认 `OPENROUTER_API_KEY` 已正确配置
2. 将API密钥信息安全地集成到打包配置中
3. 在 `run_app.py` 中包含AI功能相关的依赖导入
4. 确保打包后的EXE能够正确调用OpenRouter API

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情


