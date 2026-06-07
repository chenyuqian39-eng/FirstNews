# FirstNews

## Project Structure
FirstNews_backend/                         
├── crud/                              # db 增删改查
│   ├── favorite.py                 
│   ├── history.py                  
│   ├── news.py                     
│   └── users.py                    
│
├── models/                            # 数据模型定义
│   ├── favorite.py                 
│   ├── history.py                   
│   ├── news.py                      
│   └── users.py                     
│
├── routers/                        # API路由层 （按模块划分）
│   ├── favorite.py                  
│   ├── history.py                   
│   ├── news.py                     
│   └── users.py                    
│
├── schemas/                         # 数据验证模型（Pydantic模型）
│   ├── favorite.py                
│   ├── history.py                   
│   ├── news.py                     
│   └── users.py                   
│
├── utils/                             # 工具函数目录Utility functions
│
├── config/                             # 配置相关
│   ├── db_conf.py                    # 数据库配置文件
│   ├── cache_conf.py                 # Redis缓存配置Redis cache configuration
│ 
├── main.py                           # Application entry point
└── test_main.http                    # HTTP接口测试文件