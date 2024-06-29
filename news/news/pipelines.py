# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class NewsPipeline:
    def process_item(self, item, spider):
        #TODO 存入数据库
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
        return item
