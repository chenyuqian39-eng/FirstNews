from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud import news
#创建api router实例
#prefix 路由前缀（API接口规范文档）
#tags分组 标签
router = APIRouter(prefix="/api/news", tags=["news"])

#接口实现流程
#1模块化路由-API接口规范文档
#2.定义模型类 -数据库设计文档
#3. 在crud文件夹里面创建文件 封装操作数据库的方法
#4.在路由处理函数里面调用crud封装好的方法，响应结果

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession =Depends(get_db)):
    #先获取数据库里面分类数据 -先定义模型类 - 封装查询数据的方法
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "msg": "success",
        "data": categories
    }

@router.get("/list")
async def get_news_list(
        category_id: int = Query(...,alias="categoryId"),
        page: int = 1,
        page_size: int = Query(10, alias="pageSize"),
        db: AsyncSession = Depends(get_db)
):
    #思路： 处理分页规则-> 查询新闻列表crud-> 计算总量crud ->计算是否还有更多
    offset = (page -1)  * page_size
    news_list = await news.get_news_list(db, category_id, offset, page_size)
    return{
        "code": 200,
        "msg": "success",
        "data":{
            "list": news_list,
            "total": "total",
            "hasMore": "hasMore",

        }
    }

@router.get("/detail")
async def get_news_detail(news_id:int = Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    #获取新闻详情+浏览量+1+相关新闻
    news_detail = await news.get_news_detail(db,news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="news not found")
    await news.increase_news_count(db, news_detail.id)
    return{
        "code": 200,
        "message": "success",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": []
        }

    }
