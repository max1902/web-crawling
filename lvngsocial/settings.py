
BOT_NAME = 'livingsocial'

SPIDER_MODULES = ['scr_app.spiders']

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': '------',
    'password': '------',
    'database': 'scrape'
}

ITEM_PIPELINES = {
	'scr_app.pipelines.LvngSocialPipeline': 300,
}