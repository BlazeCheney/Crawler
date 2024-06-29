# database_helper.py

from sqlalchemy.exc import IntegrityError
from .models import News
from .db_config import SessionLocal

from sqlalchemy.orm.exc import NoResultFound


def add_news_to_db(item):
    """
    将Scrapy Item转换为ORM模型实例并尝试插入数据库。
    如果Url已存在，则根据策略决定跳过或更新记录。
    """
    session = SessionLocal()
    url = item.get('Url')

    try:
        # 检查Url是否已存在
        existing_news = session.query(News).filter_by(url=url).one()

        # 如果Url已存在，根据需求选择操作
        # 示例：直接跳过
        print(f"News with URL '{url}' already exists. Skipping.")
        return

        # 或者，选择更新现有记录（根据需要自定义哪些字段需要更新）
        # 注意：这里仅作为示例，实际更新逻辑需根据需求调整
        # existing_news.title = item.get('Title')
        # existing_news.summary = item.get('Summary')
        # existing_news.date = item.get('Date')
        # existing_news.content = item.get('Content')
        # existing_news.category = item.get('Category')
        # existing_news.source = item.get('Source')
        # existing_news.author = item.get('Author')
        # existing_news.tags = item.get('Tags')

        session.commit()
        print(f"News with URL '{url}' updated.")

    except NoResultFound:
        # 如果Url不存在，则创建新记录
        db_news = News(
            title=item.get('Title'),
            summary=item.get('Summary'),
            url=url,
            date=item.get('Date'),
            content=item.get('Content'),
            category=item.get('Category'),
            source=item.get('Source'),
            author=item.get('Author'),
            tags=item.get('Tags')
        )
        session.add(db_news)
        session.commit()
        print(f"New news with URL '{url}' added.")
    except IntegrityError:
        session.rollback()
        raise ValueError(f"Duplicate item found (based on URL): {item}")
    except Exception as e:
        session.rollback()
        raise ValueError(f"Error occurred while handling DB operation: {e}")
    finally:
        session.close()
