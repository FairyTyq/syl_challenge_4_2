# -*- coding: utf-8 -*-
import scrapy


class GitspiderSpider(scrapy.Spider):
    name = 'gitspider'
    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return(url_tmpl.format(i) for i in range(1,5))
    
    def parse(self, response):
        for info in response.css('div#user-repositories-list li'):
            yield ({
                
                'name':info.xpath('.//a[contains(@itemprop,"name codeRepository")]/text()').extract_first(),

                'update_time':info.css('relative-time::attr(datetime)').extract_first()
            })
