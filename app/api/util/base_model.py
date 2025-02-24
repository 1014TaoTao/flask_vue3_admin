from datetime import datetime
from typing import Any, Dict, List, Union
from sqlalchemy import and_, asc, desc, or_
from flask_sqlalchemy.pagination import Pagination
from app.plugin.init_sqlalchemy import db



# 基类模型
class BaseModel(db.Model):
    __abstract__ = True  # 抽象基类
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="主键ID")
    create_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, onupdate=datetime.now, comment='更新时间')
    description = db.Column(db.Text, nullable=False, comment='描述')  # 更改类型为Text，适合长文本
    
    
    @classmethod
    def paginate(cls, page_no: int, page_size: int, filters: Dict[str, Any] = None, order_by: Union[str, List] = None) -> Pagination:
        """
        分页查询封装方法，支持全字段筛选和排序。
        
        :param page_no: 当前页码
        :param page_size: 每页数量
        :param filters: 筛选条件字典，键为模型字段名，值为筛选值
        :param order_by: 排序字段，可以是单个字段名或元组（字段名，排序方式）
        :return: 分页对象
        """
        query = cls.query
        if filters:
            conditions = [getattr(cls, key).ilike(f'%{value}%') for key, value in filters.items() if value]
            query = query.filter(and_(*conditions))
        
        if order_by:
            if isinstance(order_by, str):
                order_by_field = getattr(cls, order_by)
                ordering = asc if order_by_field == order_by else desc
                query = query.order_by(ordering(order_by_field))
            elif isinstance(order_by, tuple):
                field_name, ordering_direction = order_by
                order_by_field = getattr(cls, field_name)
                ordering = asc if ordering_direction.lower() == 'asc' else desc
                query = query.order_by(ordering(order_by_field))
        
        pagination = query.paginate(page=page_no, per_page=page_size, error_out=False)
        
        results = {
            "items": pagination.items,
            "pageInfo": {
                "counts": pagination.total,
                "pages": pagination.pages,
                "page": pagination.page,
                "per_page": pagination.per_page
            }
        }
        
        return results
