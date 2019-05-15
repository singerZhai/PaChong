# -*- coding: utf-8 -*-
import scrapy

from PaChong.items import BossPcItem


class BossPcSpiderSpider(scrapy.Spider):
    name = 'boss_pc_spider'
    allowed_domains = ['www.zhipin.com']
    start_urls = ['https://www.zhipin.com/c101010100/?query=%E7%88%AC%E8%99%AB%E5%B7%A5%E7%A8%8B%E5%B8%88&page=1&ka=page-1']

    def parse(self, response):
        job_list = response.xpath("//div[@class='job-list']//ul//li")
        for i_item in job_list:
            boss_item = BossPcItem()
            boss_item['job_name'] = i_item.xpath(".//div//div//h3//div[@class='job-title']/text()").extract_first()
            boss_item['company_name'] = i_item.xpath(".//div//div//div//h3//a/text()").extract_first()
            boss_item['pay'] = i_item.xpath(".//div//div//h3//a//span[@class='red']/text()").extract_first()
            boss_item['address'] = i_item.xpath(
                ".//div[@class='job-primary']//div[@class='info-primary']//p/text()[1]").extract_first()
            boss_item['person_count'] = i_item.xpath(
                ".//div[@class='job-primary']//div[@class='info-company']//div[@class='company-text']//p/text()[3]").extract_first()
            boss_item['years'] = i_item.xpath(
                ".//div[@class='job-primary']//div[@class='info-primary']//p/text()[2]").extract_first()
            boss_item['study'] = i_item.xpath(
                ".//div[@class='job-primary']//div[@class='info-primary']//p/text()[3]").extract_first()
            yield boss_item

        next_link = response.xpath("//div[@class='job-list']//div[@class='page']//a[@class='next']/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request(
                "https://www.zhipin.com/c101010100/?query=%E7%88%AC%E8%99%AB%E5%B7%A5%E7%A8%8B%E5%B8%88&page=1&ka=page-1" + next_link,
                callback=self.parse)
