# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter

class CardsPipeline:
    """크롤링 작업 후 Json파일로 저장"""

    def open_spider(self, spider):
        """크롤링 시작 작업"""
        self.file = open('items.jsonl', 'w')

    def close_spider(self, spider):
        """크롤링 후 작업"""
        self.file.close()

    def process_item(self, item, spider):
        """크롤링 한 item을 저장"""
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item