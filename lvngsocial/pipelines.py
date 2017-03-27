
from sqlalchemy.orm import sessionmaker
from models import Deals, db_connect, create_deals_table
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter


class LvngSocialPipeline(object):
    """Livingsocial pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.files = {}
        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind=engine)

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s_items.csv' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.fields_to_export = ['title', 'link', 'location', 'original_price', 'price', 'end_date']
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        """Save deals in the database.
        This method is called for every item pipeline component.
        """
        self.exporter.export_item(item)
        session = self.Session()
        deal = Deals(**item)

        try:
            session.add(deal)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item