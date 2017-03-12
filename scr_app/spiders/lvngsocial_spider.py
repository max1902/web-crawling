
from bs4 import BeautifulSoup

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from scr_app.items import LivingSocial


class LvngSocialSpider(BaseSpider):
	"""Spider for www.livingsocial.com"""
	name = "livingsocial"
	allowed_domains = ['livingsocial.com']
	start_urls = ["https://www.livingsocial.com/cities/4-los-angeles"]

	xpath_for_deals = '//li[@dealid]'
	item_fields = {
		'title': './/div[@class="deal-details"]/h2/text()',
		'link': './/a/@href',
		'location': './/a/div[@class="deal-details"]/p[@class="location"]/text()',
		'original_price': './/a/div[@class="deal-prices"]/div[@class="deal-strikethrough-price"]/div[@class="strikethrough-wrapper"]/text()',
		'price': './/a/div[@class="deal-prices"]/div[@class="deal-price"]/text()',
		'end_date': './/a/div[@class="deal-details"]/p[@class="dates"]/text()'
	}

	def parse(self, response):
		"""Get response from start_urls"""
		
		selector = HtmlXPathSelector(response)

		for deal in selector.xpath(self.xpath_for_deals):
			loader = XPathItemLoader(LivingSocial(), selector=deal)

			# define processors
			loader.default_input_processor = MapCompose(unicode.strip)
			loader.default_output_processor = Join()

			# iterate over fields and add xpaths to the loader
			for field, xpath in self.item_fields.iteritems():
				loader.add_xpath(field, xpath.strip())
			yield loader.load_item()

	# def parse(self, response):
	# 	"""Other way to parse deals"""
	# 	item = dict()
	# 	selector = HtmlXPathSelector(response)
		
	# 	for deal in selector.xpath(self.xpath_for_deals):
	# 		item['title'] = deal.xpath('.//h2/text()').extract_first().strip()
	# 		item['link'] = deal.xpath('.//a/@href').extract_first().strip()
	# 		item['location'] = deal.xpath('.//p[@class="location"]/text()').extract_first().strip()
	# 		item['original_price'] = deal.xpath('.//a//div[@class="strikethrough-wrapper"]/text()').extract()[1].strip()
	# 		item['price'] = deal.xpath('.//a/div[@class="deal-prices"]/div[@class="deal-price"]/text()').extract_first().strip()
	# 		item['end_date'] = deal.xpath('.//a/div[@class="deal-details"]/p[@class="dates"]/text()').extract_first().strip()
	# 		yield item


