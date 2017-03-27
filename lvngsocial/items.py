
from scrapy.item import Item, Field


class LivingSocial(Item):
	"""Define fields which we want to scrape
	   in order to create CSV file with from our database
	   ust use \copy (Select * From foo) To '/tmp/test.csv' With CSV
	"""
	title = Field()
	link = Field()
	location = Field()
	original_price = Field()
	price = Field()
	end_date = Field()
