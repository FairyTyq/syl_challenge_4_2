# -*- coding: utf-8 -*-
import scrapy
from sylgithub.items import SylgithubItem

class GitspiderSpider(scrapy.Spider):
    name = 'gitspider'
    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return(url_tmpl.format(i) for i in range(1,5))
    
    def parse(self, response):
        for info in response.css('div#user-repositories-list li'):
            item = SylgithubItem()
                
            item['name'] = info.xpath('.//a[contains(@itemprop,"name codeRepository")]/text()').re_first('([\w-]+)')
            item['update_time'] = info.css('relative-time::attr(datetime)').extract_first()
            #构造仓库详情页面的链接，用urljoin 方法就将爬取到的相对链接构造成全链接
            repository_url = response.urljoin(info.xpath('.//a[contains(@itemprop,"name codeRepository")]/@href').extract_first())
            # 构造到课程详情页的请求，指定回调函数
            request = scrapy.Request(repository_url,callback=self.parse_left)
            # 将未完成的item通过meta传入parse_left
            request.meta['item'] = item
            yield request
            
            
    def parse_left(self,response):
        #获取未完成的item
        item = response.meta['item']
        #解析commit，branches，releases
        item['commits'] = response.xpath('//ul[contains(@class,"numbers-summary")]/li[contains(@class,"commits")]/a/span/text()').extract_first()

        item['branches'] = response.xpath('//ul[contains(@class,"numbers-summary")]/li[2]/a/span/text()').extract_first()

        item['releases'] = response.xpath('//ul[contains(@class,"numbers-summary")]/li[3]/a/span/text()').extract_first()
        # item构造完成，生成
        yield item
