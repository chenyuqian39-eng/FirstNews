# News cache helpers.
from typing import Dict, Any, Optional, List

from config.cache_conf import get_json_cache, set_cache



CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX ="news_list:"

# Get cached news categories.
async def get_cached_categories():
    return await get_json_cache(CATEGORIES_KEY)


# Store news categories in Redis.
async def set_news_categories(data: list[Dict[str, Any]], expire: int = 7200):
    return await set_cache(CATEGORIES_KEY, data, expire)


#写入缓存-新闻列表 key = news_list:category id:page:pagesize + list data + expiry time
async def set_cache_news_list(category_id:Optional[int], page:int, size:int, news_list: List[Dict[str, Any]], expire: int = 1800):
    #调用前面封装的redis的设置方法，存新闻列表到缓存
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await set_cache(key, news_list, expire)

#读取缓存-新闻列表
async def get_news_list(category_id:Optional[int], page:int, size:int):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await get_json_cache(key)