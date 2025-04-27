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
