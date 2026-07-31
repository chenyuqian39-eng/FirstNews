import json
import logging
from typing import Any

import redis.asyncio as redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

logger = logging.getLogger(__name__)

# 创建redis的链接对象
redis_client = redis.Redis(
    host=REDIS_HOST, #redis服务器的主机地址
    port=REDIS_PORT,#redis端口号
    db=REDIS_DB, #redis数据库编号
    decode_responses=True #是否将字节数据解码为字符串（方便查看和操作）
)


#二次封装 设置 和 读取（两个方法 存之前数据是不一样的 字符串和列表或字典-序列化）缓存。 “[{}]”
#读取： String
async def get_cache(key: str):
    #return await redis_client.get(key)
    try:
        return await redis_client.get(key) #success
    except Exception as e: #fail
        logger.exception("Failed to get Redis cache key=%s: %s", key, e)
        return None

#读取：列表或字典
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        logger.exception("Failed to get Redis JSON cache key=%s: %s", key, e)
        return None
# Redis中室JSON字符串：'["Sydney", "Canberra"]'转换成python字典/列表-{"name": "Zoe", "age": 22}


#设置缓存 setex(key,expire,value)
        # 3600s = 1h
async def set_cache(key: str, value: Any,expire: int = 3600 ):
    try:
        #value判断类型, value是dict或者list
        if isinstance(value, (dict, list)):
            #转字符串再存
            value = json.dumps(value, ensure_ascii=False)#中文正常保存
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        logger.exception("Failed to set Redis cache key=%s: %s", key, e)
        return False
