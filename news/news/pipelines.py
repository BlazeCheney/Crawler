# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from db.sqlserver.database_helper import add_news_to_db


class NewsPipeline:
    def process_item(self, item, spider):

        print('===========爬取结果=============' * 5)
        print(f'爬虫: {spider.name}')

        print(f"标题: {item['Title']}")
        print(f"摘要: {item['Summary']}")
        print(f"链接: {item['Url']}")
        print(f"日期: {item['Date']}")
        print(f"内容: {item['Content']}")
        print(f"分类: {item['Category']}")
        print(f"来源: {item['Source']}")
        print(f"作者: {item['Author']}")
        print(f"标签: {item['Tags']}")

        print('===========爬取结束=============' * 5)
        try:
            add_news_to_db(item)
        except ValueError as e:
            raise DropItem(str(e))
        return item
