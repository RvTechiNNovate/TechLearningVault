project_root/
│
├── main.py            # Entry point, contains FastAPI app initialization
│
├── api/
│   ├── __init__.py   # Initialize api package
│   ├── dependencies.py # Contains dependency definitions (e.g., OAuth2PasswordBearer)
│   ├── models.py      # Pydantic models (e.g., Token, User)
│   ├── routers/
│   │   ├── __init__.py   # Initialize routers package
│   │   ├── auth.py        # Authentication related endpoints (/token)
│   │   └── chat.py        # Chat related endpoints (/chat)
│   └── services/
│       ├── __init__.py        # Initialize services package
│       ├── auth_service.py    # Authentication service
│       └── ai_service.py      # AI service (OpenAI integration)
│
├── config/
│   ├── __init__.py        # Initialize config package
│   ├── settings.py        # Configuration settings (e.g., SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES)
│   └── logging_config.py  # Logging configuration
│
├── database/
│   ├── __init__.py        # Initialize database package
│   ├── database.py        # Database connection setup
│   └── alembic/
│       ├── __init__.py    # Initialize alembic package
│       ├── alembic.ini    # Alembic configuration
│       └── versions/      # Alembic migration versions
│
├── redis_client.py        # Redis client setup (new file)
├── cache_decorator.py     # Cache decorator for endpoints (new file)
│
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci-cd.yml      # CI/CD configuration
│
└── locales/
    ├── en.json
    └── fr.json
