import scrapy
# noinspection PyUnresolvedReferences
from news.items import NewsItem


class AutohomeSpider(scrapy.Spider):
    name = "autohome"

    # allowed_domains = ["autohome.com.cn"]
    # start_urls = ["https://autohome.com.cn"]

    def start_requests(self):
        for i in range(1, 2):
            url = f'https://www.autohome.com.cn/hangye/list/{i}'
            yield scrapy.Request(url, callback=self.parse_article_list)

    def parse_article_list(self, response):
        article_list_node = response.xpath('//div[@id="auto-channel-lazyload-article"]/ul/li')
        for article_node in article_list_node:
            url = article_node.xpath('./a/@href').extract_first()
            title = article_node.xpath('./a/h3/text()').extract_first()
            summary = article_node.xpath('./a/p/text()').extract_first()
            date = article_node.xpath('./a/div[@class="article-bar"]/span[1]/text()').extract_first()
            if "http" not in url:
                url = f'https:{url}'

            item = NewsItem()
            item['Title'] = title
            item['Summary'] = summary
            item['Url'] = url
            item['Date'] = date
            item['Source'] = '汽车之家'
            yield scrapy.Request(url, callback=self.parse_article, meta={'item': item})

    def parse_article(self, response):
        item = response.meta['item']

        category = response.xpath('//div[@class="breadnav fn-left"]/a[2]/text()').extract_first()
        item['Category'] = category.replace('\n', '').replace('\t', '').replace('\r', '') if category else ''

        tag = response.xpath('//div[@class="breadnav fn-left"]/a[3]/text()').extract_first()
        item['Tags'] = tag.replace('\n', '').replace('\t', '').replace('\r', '') if tag else ''

        author = response.xpath('//div[@class="article-info"]/div[@class="name"]/a/text()').extract_first()
        item['Author'] = author.replace('\n', '').replace('\t', '').replace('\r', '') if author else ''

        date = response.xpath('//div[@class="article-info"]/span[@class="time"]/text()').extract_first()
        item['Date'] = date.replace('\n', '').replace('\t', '').replace('\r', '') if date else ''

        content_node = response.xpath('//div[@id="articleContent"]')
        content = content_node.xpath('./p/text()').getall()

        content = ''.join(content) if content else ''
        item['Content'] = content.replace('\n', '').replace('\t', '').replace('\r', '')
        yield item
