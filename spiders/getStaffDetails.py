# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class GetstaffdetailsSpider(CrawlSpider):
    name = 'getStaffDetails'
    allowed_domains = ['pdn.ac.lk/academics/teaching_staff_az.php']
    start_urls = ['http://www.pdn.ac.lk/academics/teaching_staff_az.php/']
    rules = [Rule(LinkExtractor(allow='pdn.ac.lk/'),
                  callback='parse_filter_book', follow=True)]

    def parse(self, response):
        staffDetails = response.xpath('//table//tr')
        #profieInfo = response.xpath('//td/a[@href]')

        for staff in staffDetails[1556:]:
            name = staff.xpath('td[1]/a[@href]//text()').extract_first()
            department = staff.xpath('td[2]//text()').extract_first()
            faculty = staff.xpath('td[3]//text()').extract_first()
            profile = staff.xpath('td/a/@href').extract_first()

            yield {'Name': name, 'Department': department, 'Faculty': faculty, 'Profile_Link': profile}

        pages = response.xpath('//div[@class="dataTables_paginate paging_simple_numbers//a"]')
        for page in pages:
            yield Request(url=response.urljoin(page), callback=self.parse)