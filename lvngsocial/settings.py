
BOT_NAME = 'livingsocial'

SPIDER_MODULES = ['lvngsocial.spiders']

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': '-',
    'password': '-',
    'database': 'scrape'
}

ITEM_PIPELINES = {
	'lvngsocial.pipelines.LvngSocialPipeline': 300,
}

# LOG_STDOUT = True
# LOG_FILE = 'scrapy_output.txt'

ITEM_PIPELINES = {'lvngsocial.pipelines.LvngSocialPipeline': 300 }