import scrapy
from news.items import NewsItem
import json


class SohuSpider(scrapy.Spider):
    name = "sohu"

    # allowed_domains = ["sohu.com"]
    # start_urls = ["https://sohu.com"]

    def start_requests(self):
        url = 'https://odin.sohu.com/odin/api/blockdata'
        headers = {'Content-Type': 'application/json'}
        body = {
            "pvId": "1719636978544_oBLsZgd",
            "pageId": "1719636979164_24051019295_wAK",
            "mainContent": {
                "productType": "13",
                "productId": "7313",
                "secureScore": "50",
                "categoryId": "18",
                "adTags": "20000131",
                "authorId": 121135924
            },
            "resourceList": [
                {
                    "tplCompKey": "TPLFeed_2_0_pc_1643130452918",
                    "isServerRender": True,
                    "isSingleAd": False,
                    "content": {
                        "spm": "smpc.channel_159.block3_218_AB1PKt_1_fd",
                        "productType": "13",
                        "productId": "7313",
                        "page": 1,
                        "size": 20,
                        "pro": "0,1",
                        "innerTag": "channel",
                        "feedType": "XTOPIC_SYNTHETICAL",
                        "view": "multiFeedMode",
                        "requestId": "1719636978984Eg2aaz6_7313"
                    },
                    "adInfo": {
                        "posCode": ""
                    },
                    "context": {}
                }
            ]
        }
        yield scrapy.Request(url, method='POST', headers=headers, body=json.dumps(body),
                             callback=self.parse_article_list)

    def parse_article_list(self, response):
        res = response.json()
        data = res.get('data')
        compent = data.get('TPLFeed_2_0_pc_1643130452918')
        article_list = compent.get("list")
        for article in article_list:
            url = article.get("url")
            title = article.get("title")
            summary = article.get("brief")
            author = article.get("extraInfoList")[0]['text']
            date = article.get("extraInfoList")[1]['text']
            category = compent.get("meta").get("displayTitle")

            icon = article.get("icon")
            if "video" in icon:
                continue

            if "http" not in url:
                url = f'https://www.sohu.com{url}&spm=smpc.channel_159.block3_218_AB1PKt_1_fd.1.1719636978984Eg2aaz6_7313'

            item = NewsItem()
            item['Title'] = title
            item['Summary'] = summary
            item['Url'] = url
            item['Date'] = date
            item['Author'] = author
            item['Source'] = '搜狐汽车'
            item['Category'] = category
            item['Tags'] = '自媒体'
            yield scrapy.Request(url, callback=self.parse_article, meta={'item': item})

    def parse_article(self, response):
        item = response.meta['item']

        content_node = response.xpath('//article')
        content = content_node.xpath('.//p/text()').getall()

        content = ''.join(content) if content else ''
        item['Content'] = content.replace('\n', '').replace('\t', '').replace('\r', '')

        date = response.xpath('//span[@class="time"]/text()').get()
        if date:
            item['Date'] = date.replace('\n', '').replace('\t', '').replace('\r', '').strip()
        yield item
