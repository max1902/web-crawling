#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import scrapy
from pwdhounds.items import PwdhoundsItem

BASE_URL = 'http://www.powderhounds.com'
MAIN_PATH = './/ul[@class="rmRootGroup rmHorizontal"]/li'
SND_PATH = './/ul[@class="rmVertical rmGroup rmLevel1"]/li'
THRD_PATH = './/ul[@class="rmVertical rmGroup rmLevel2"]/li'
FTH_PATH = './/ul[@class="rmVertical rmGroup rmLevel3"]/li'

reload(sys)
sys.setdefaultencoding('utf-8')


class PwdSpider(scrapy.Spider):
    name = 'powder_hounds'

    allowed_domains = ['powderhounds.com']
    start_urls = ['http://www.powderhounds.com/']

    def parse(self, response):
        departments = response.xpath(MAIN_PATH)

        for i, cat in enumerate(departments):
            name, url = self._make_name_url(cat)
            n_item = self._make_category(name=name, url=url, index=i)
            yield n_item
            
            second_lvl = cat.xpath(SND_PATH)
            if second_lvl:
                for _ in self.parse_sec_lvl(second_lvl, n_item):
                    yield _

    def parse_sec_lvl(self, second_lvl, _item):
        for i, s_l in enumerate(second_lvl):
            name2, url2 = self._make_name_url(s_l)
            cat_id = '{}_{}'.format(_item['id'], name2)
            n_item = self._make_category(name=name2, url=url2, index=i,
                                         parent_id=_item['id'], category_id=cat_id)
            yield n_item
            third_lvl = s_l.xpath(THRD_PATH)
            if third_lvl:
                for _ in self.parse_thrd_lvl(third_lvl, n_item):
                    yield _

    def parse_thrd_lvl(self, third_lvl, _item):
        for i, ss_l in enumerate(third_lvl):
            name3, url3 = self._make_name_url(ss_l)
            cat_id = '{}_{}'.format(_item['id'], name3)
            n_item = self._make_category(name=name3, url=url3, index=i,
                                         parent_id=_item['id'], category_id=cat_id)
            yield n_item
            fth_lvl = ss_l.xpath(FTH_PATH)
            if fth_lvl:
                for _ in self.parse_fth_lvl(fth_lvl, n_item):
                    yield _

    def parse_fth_lvl(self, fth_lvl, _item):
        for i, sss_l in enumerate(fth_lvl):
            name4, url4 = self._make_name_url(sss_l)
            cat_id = '{}_{}'.format(_item['id'], name4)
            n_item = self._make_category(name=name4, url=url4, index=i,
                                        parent_id=_item['id'], category_id=cat_id)
            yield n_item

    def _make_name_url(self, raw_tag):
        name = raw_tag.xpath('.//a/span/text()').extract_first().strip()
        url = raw_tag.xpath('.//a/@href').extract_first()
        if 'www.powderhounds.com' not in url:
                url = BASE_URL + url
        return name, url

    def _make_category(self, name, url, index, parent_id=None, category_id=None):
        c = PwdhoundsItem()
        c['name'] = name
        c['link'] = url
        c['index'] = index
        c['id'] = self._make_category_id(name, category_id, parent_id)
        c['parent_id'] = self._make_id(parent_id) if parent_id else parent_id

        return c

    @classmethod
    def _make_id(cls, text):
        for symbol in [' ', '&', '\'', u'’']:
            text = text.replace(symbol, '')
        return text

    @classmethod
    def _make_category_id(cls, name, category_id, parent_id):
        """ Genarate categoty id """
        if category_id:  # was made in crawler/by hand
            _id = category_id
        else:
            _id = u'{}_{}'.format(parent_id, name) if parent_id else name

        return cls._make_id(_id)
