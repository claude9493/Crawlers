import scrapy, string, re

class AppleDailySpider(scrapy.Spider):
    name = "appledaily"
    # allowed_domains = ["https://hk.appledaily.com", "https://s.nextmedia.com"]
    start_urls = ["https://hk.appledaily.com/hit"]

    def parse(self, response):
        hits = response.xpath("//div[contains(@class, 'item')]/div[contains(@class, 'text')]/a/@href").extract()
        for url in hits:
            self.logger.info('Find: %s', url)
            yield scrapy.Request(url, callback=self.parse_news)
    
    def parse_news(self, response):
        title = response.xpath("/html/head/title/text()").extract_first()
        self.logger.info('Parsing: %s\n Title: %s'%(response.url, title))
        content = response.xpath("//div[contains(@class, 'ArticleContent_Inner')]/p/text()").extract() 
        with open('news.txt', 'a', encoding='utf-8') as f:
            f.write("\n".join([title.strip(), '\n'.join([c.strip() for c in content]), '\n']))
