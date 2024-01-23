import scrapy
from spider24.items import MovieItem
from scrapy.http import HtmlResponse
from scrapy import Request

class DoubanSpider(scrapy.Spider):
    name = "game"
    allowed_domains = ["4399.com"]
    start_urls = ["https://www.4399.com/flash/"]

    def parse(self, response: HtmlResponse, **kwargs):

        sel = scrapy.Selector(response)
        list_items = response.xpath("//ul[@class='n-game cf']/li")

        for list_item in list_items:
            detail_url = response.urljoin(list_item.xpath('./a/@href').extract_first())
            movie_item = MovieItem()
            movie_item['title'] = list_item.xpath('./a/b/text()').extract_first()

            movie_item['category'] = list_item.xpath('./em/a/text()').extract_first()
            movie_item['date'] = list_item.xpath('./em/text()').extract_first()
            #yield movie_item
            yield Request(url=detail_url, callback=self.parse_detail, cb_kwargs={'item': movie_item})


        hrefs_list = sel.css('div.pag > a::attr(href)')
        for href in hrefs_list:
            url = response.urljoin(href.extract())
            yield Request(url=url)


    def parse_detail(self, response, **kwargs):
        movie_item = kwargs['item']
        sel = scrapy.Selector(response)
        temp = sel.css('div[id="introduce"] font::text').extract_first()
        if temp is not None:
            movie_item['intro'] = temp.strip()
        else:
            movie_item['intro'] = '暂无'
        yield movie_item
