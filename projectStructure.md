mcp-system/
├── client/                         # 🧑‍💻 用户调用入口（CLI/Web UI）
│   ├── cli.py                      # 命令行控制器
│   └── streamlit_app.py           # Streamlit 前端控制台（可选）
│
├── server/                         # 🌐 MCP Server（调度中心/接口服务）
│   ├── routes/                    # FastAPI 路由定义
│   ├── services/                  # 将请求映射到 Agent + tools 调用
│   └── main.py                    # 主服务入口（uvicorn 启动）
│
├── agent/                          # 🧠 MCP Agent 本体（Model + Context + Protocol）
│   ├── model/                     # 模型相关（Planner、LLM接口等）
│   │   └── planner.py
│   ├── context/                   # 记忆系统（如 chroma、历史状态）
│   │   ├── memory.py
│   │   └── retriever.py
│   ├── protocol/                  # 工具层：可执行动作（Tool）
│   │   ├── local/                # 本地工具（自己实现的）
│   │   │   ├── search.py
│   │   │   ├── generator.py
│   │   │   └── poster.py
│   │   ├── remote/               # 外部 MCP Server 提供的工具调用封装
│   │   │   ├── ask_llm_server.py
│   │   │   └── invoke_toolhub.py
│   │   └── interaction.py       # 与人交互类通用动作
│   ├── registry.py               # Tool schema 注册、调用分发
│   └── agent_loop.py            # Agent 主循环（Model 决策 - 调 Tool - 更新）
│
├── configs/                       # ⚙️ 配置文件（Persona、行为规则、API Key）
│   ├── persona_profiles/
│   └── global_config.yaml
│
├── scripts/                       # 🛠️ 脚本运行入口（调试、测试、单次任务）
│   ├── run_agent_once.py
│   └── test_tools.py
│
├── data/                          # 🗃️ 本地存储层（缓存、嵌入、日志等）
│   ├── chroma/
│   ├── logs/
│   └── cache/
│
├── frontend/                      # 🖼️ 如需使用独立前端框架（如 Next.js）
│   └── (预留)
│
├── tests/                         # ✅ 测试
│   └── test_memory.py
│
├── requirements.txt / pyproject.toml
├── .env.example
└── README.md


🧠 项目定位

构建一个具有人设、学习能力、自我成长动机和社交互动能力的内容创作型 AI Agent，它能从现实世界中获取信息 → 内化知识 → 创作内容 → 推广自己 → 不断优化风格与策略，成为“网络领域专家”。

🛡️ 核心模块总览图（系统视角）

╔══════════════════════════════╗
║        🎯 Agent Controller        ║ ←— 控制流程、调度行为、目标推进
╚══════════════════════════════╝
           ▲              ▲              ▲
           │              │              │
 ┌──────────────┐ ┌────────────────┐ ┌─────────────────┐
 │  🔍 信息获取系统  │ │ 🧠 语义知识库       │ │ 🗣️ 交互与社交行为控制 │
 └──────────────┘ └────────────────┘ └─────────────────┘
        ▲                         ▲                         ▲
        │                         │                         │
 [Search APIs]          [Chroma Embedding]         [Twitter / Notion]
 [RSS / Feeds]         [Topic Memory JSON]       [互动 & 发布模块]
 [Trending Sources]     [RAG Query System]        [互动行为策略逻辑]

🧬 Agent 生命周期（行为流程）

每次运行 agent，会经历以下几个逻辑阶段：

目标与任务检查

当前的目标是什么？（如：涨粉1000、发20篇评论、写5个系列）

我还差什么？最近互动数据怎样？

信息感知（信息摄取）

主动搜索（搜索引擎 API）

被动吸收（RSS Feed）

热点检测（Twitter trending / pytrends）

评论监听（针对自己的账号或领域人物）

内容判断与主题生成

使用 LLM 判断哪些主题值得写

对比已有历史内容，避免重复

给出内容规划（写短评 or 系列 or 长文）

知识回忆（Memory 调用）

调用语义记忆库（Chroma）

拿出“我过去写过这些话题”做写作参考

内容生成（Content Creation）

写短评、推文、长文（调用 GPT-4 + persona prompt）

加 tag、设计发文节奏

自动格式化/归档

发布 & 推广

发推、转推、加评论（tweepy）

写 Notion 页面（notion-sdk）

主动点赞别人内容或互动

内容表现评估

拉推文数据（点赞数、转发数）

聚合评论内容（分类 + 热度 +争议度）

根据表现调整未来风格或主题偏好（兴趣漂移）

日志记录与成长追踪

写入日志/数据库（行为记录）

更新目标进度（比如“互动数+1”，“风格B写了3次，表现好”）

生成自我反馈（像“我这周学到了什么”）

🌎 各模块作用说明

模块

作用

技术核心

🎯 Agent Controller

调度每个阶段，保持目标驱动

agent_runner.py + YAML 配置

🔍 信息获取系统

获取外部世界内容，激发写作

RSS、Search API、Trending API

🧠 知识库 / 长期记忆

保存语义化记忆，支持对比、查找、自我一致性

Chroma, embedding, topic归档

✍️ 内容生成器

写出有风格的原创推文、评论、长文

GPT-4 + persona prompt

📣 行动系统（发推、互动）

在社交平台中活动、影响读者

tweepy、notion-sdk-py

📊 表现分析系统

判断写得好不好，是否有效果

拉取互动数据 + GPT摘要评论趋势

🧭 兴趣演化/目标系统

随着经验，调整行为风格/偏好/行动策略

Topic scorer + 行为优化规则

📍 项目分阶段推进建议

阶段

目标

重点模块

Phase 1

建立 Agent 写作 & 发布闭环

信息抓取 → 写作 → 发推 → 归档

Phase 2

加入知识库 + 自我记忆回调

Chroma + query → 改进内容风格

Phase 3

加入热点探测与互动机制

Twitter trending → 自我推广

Phase 4

自主成长与兴趣策略调整

Agent 自我评分 + 策略规划器上线

✅ 当前项目状态（Recap）

✅ 已确认模块选型：模型、嵌入存储、调度、内容生成、社交接口

✅ 已明确整体 Agent 目标：内容创作 + 自我推广 + 自我优化

🔧 正在细化的部分：信息摄取模块设计、兴趣演化机制、行为评分系统

📌 准备进入下一步：确定第一个 Agent 身份 + 选择信息来源 + 跑通第一轮内容生产链

