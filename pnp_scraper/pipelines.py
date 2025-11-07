# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class PnpScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Clean and process the price field
        if adapter.get('price'):
            price = adapter['price']
            # Remove currency symbols, commas, and whitespace
            # Extract numeric value from strings like "R 123.45" or "R123,45"
            price_clean = re.sub(r'[R\s,]', '', price)
            # Replace comma with dot for decimal point if needed
            price_clean = price_clean.replace(',', '.')
            try:
                adapter['price'] = float(price_clean)
            except ValueError:
                spider.logger.warning(f"Could not convert price to float: {price}")
                adapter['price'] = None
        
        return item
