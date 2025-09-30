# WeiWan 任务管理系统

基于 FastAPI + SQLite + Vue3 + TailwindCSS 的现代化任务管理应用，支持层级任务分解、智能日历视图和美观的UI界面。


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
├── welcomePage/            # 欢迎页业务逻辑模块
│   ├── __init__.py         # 模块初始化
│   ├── greeting.py         # 欢迎语API路由
│   ├── progress.py         # 进度统计API路由
│   ├── tasks.py            # 任务管理API路由
│   └── my_calendar.py      # 日历数据API路由
└── task/                   # 任务管理核心模块
    ├── __init__.py         # 模块初始化
    ├── routes.py           # 任务CRUD API路由
    ├── crud.py             # 数据库操作层
    └── BreakDownTask.py    # AI任务分解服务
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
│   │   ├── welcomePage.js  # 欢迎页API接口封装
│   │   └── task.js         # 任务管理API接口封装
│   ├── views/
│   │   ├── HomePage.vue    # 首页视图，四象限布局
│   │   └── TaskPage.vue    # 任务管理页面
│   ├── components/         # 欢迎页组件
│   │   ├── MotivationCard.vue    # 激励卡片组件（支持随机图片和换行文本）
│   │   ├── ProgressChart.vue     # 进度图表组件
│   │   ├── UrgentTasks.vue       # 紧急任务列表组件
│   │   └── CalendarView.vue      # 日历视图组件（支持任务弹出框）
│   └── components_taskPage/ # 任务页组件
│       ├── TaskList.vue          # 任务列表组件
│       ├── TaskModal.vue         # 任务编辑弹窗
│       ├── HierarchicalTaskList.vue # 层级任务列表
│       ├── TaskFilters.vue       # 任务筛选组件
│       ├── TaskStats.vue         # 任务统计组件
│       └── DeleteConfirmModal.vue # 删除确认弹窗
└── weiwan.html             # 原型图HTML文件（backup为备份）
```

### 工具脚本
```
scripts/
└── init_db.py              # 数据库初始化脚本，创建表结构和示例数据

### 打包文件
├── packaged_main.py        # 打包专用主程序
├── build.spec             # PyInstaller配置文件
├── build.bat              # Windows打包脚本
└── requirements.txt       # Python依赖列表
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

## 主要功能

### 🏠 欢迎页功能
- **随机问候语**：支持换行显示的个性化问候语
- **随机图片**：4张可爱的鼠鼠图片随机显示
- **进度统计**：ECharts饼图展示任务完成情况
- **紧急任务**：显示即将到期的任务列表
- **智能日历**：点击日期查看任务详情，支持弹出框显示

### 📋 任务管理功能
- **层级任务**：支持1-3级任务分解
- **任务CRUD**：创建、编辑、删除、状态更新
- **智能筛选**：按状态、优先级、关键词筛选
- **AI分解**：使用OpenRouter API智能分解复杂任务
- **批量操作**：支持批量状态更新和删除

#### AI任务分解使用方法

配置好OpenRouter API Key后，可以使用AI智能分解功能：

1. **创建主任务**：先创建一个需要分解的复杂任务
2. **点击分解按钮**：在任务列表中找到对应任务，点击"AI分解"按钮
3. **输入分解要求**：在弹窗中描述如何分解任务（如：分解为3-5个子任务）
4. **查看AI建议**：系统会调用AI生成子任务建议，包含标题、描述、截止日期和优先级
5. **确认保存**：检查AI生成的子任务，确认后保存到系统中

### 🎨 UI/UX特性
- **响应式设计**：适配桌面端和移动端
- **毛玻璃效果**：现代化的半透明背景
- **渐变边框**：美观的紫色渐变边框
- **动画效果**：平滑的过渡和悬停效果
- **深色主题**：护眼的深色配色方案

## API 接口文档

### 欢迎页接口
- `GET /api/greeting` - 获取随机欢迎语
  - 返回：`{"greeting": "问候语文本（支持\\n换行）"}`
- `GET /api/progress` - 获取任务状态分布统计
  - 返回：按层级分组的任务状态统计
- `GET /api/completion` - 获取今日任务完成度
  - 返回：`{"today": 完成度百分比}`
- `GET /api/tasks/urgent?limit=10` - 获取紧急任务列表
  - 参数：`limit` - 返回任务数量限制
  - 返回：紧急任务数组
- `GET /api/calendar?year=2025&month=1` - 获取指定月份任务日历数据
  - 参数：`year` - 年份，`month` - 月份
  - 返回：按日期分组的任务数据

### 任务管理接口
- `GET /api/tasks/` - 获取任务列表（支持分页、筛选、搜索）
- `GET /api/tasks/hierarchical` - 获取层级结构任务列表
- `GET /api/tasks/{id}` - 获取单个任务详情
- `POST /api/tasks/` - 创建新任务
- `PUT /api/tasks/{id}` - 更新任务信息
- `DELETE /api/tasks/{id}` - 删除任务
- `PATCH /api/tasks/{id}/status` - 更新任务状态
- `POST /api/tasks/{id}/breakdown` - AI分解任务
- `POST /api/tasks/{id}/breakdown/confirm` - 确认并保存分解的子任务

### 健康检查
- `GET /api/health` - 服务健康状态检查
  - 返回：`{"status": "ok", "message": "WeiWan API is running"}`

## 配置说明

### OpenRouter API Key 申请教程

WeiWan 使用 OpenRouter API 来提供 AI 任务分解功能。要使用此功能，需要申请 OpenRouter API Key：

#### 1. 注册 OpenRouter 账号

1. 访问 [OpenRouter 官网](https://openrouter.ai/)
2. 点击右上角 "Sign Up" 注册账号
3. 可以使用 GitHub、Google 账号快速注册

#### 2. 获取 API Key

1. 登录后点击右上角用户头像，选择 "API Keys"
2. 点击 "Create Key" 创建新的 API 密钥
3. 输入密钥名称（如：WeiWan-TaskBreakdown）
4. 复制生成的 API Key
5. ⚠️ **重要**：请立即保存此密钥，页面刷新后将无法再次查看

#### 3. 配置环境变量

在项目根目录创建 `.env` 文件：

```bash
# 项目根目录下创建 .env 文件
OPENROUTER_API_KEY=你的实际密钥
```

### 后端配置

- 数据库文件位置：`backend/data/database.db`
- 欢迎语数据文件：`backend/data/greetings.json`
- 默认端口：8000
- OpenRouter API Key：通过环境变量 `OPENROUTER_API_KEY` 配置

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

## 打包为 EXE

### 快速打包
```bash
# Windows用户直接运行
build.bat

# 或手动执行
cd frontend && npm run build && cd ..
pyinstaller --clean --noconfirm build.spec
```

### 打包说明
- **前端构建**：自动构建Vue前端为静态文件
- **依赖安装**：自动安装Python依赖和PyInstaller
- **一键打包**：生成完整的可执行程序
- **自动启动**：打包完成后自动打开浏览器

### 打包结果
- 可执行文件：`dist/WeiWan/WeiWan.exe`
- 包含前端静态文件和后端服务
- 自动初始化数据库和示例数据
- 支持单机运行，无需额外配置

### 技术实现
- 使用PyInstaller将Python后端打包为exe
- 前端静态文件嵌入到exe中
- 自动处理路径和依赖问题
- 支持跨平台打包（Windows/Linux/macOS）

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情


