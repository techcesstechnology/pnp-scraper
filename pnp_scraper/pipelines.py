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
            # Remove currency symbol 'R' and whitespace from the beginning
            # Extract numeric value from strings like "R 123.45" or "R 123,45"
            price_clean = re.sub(r'^\s*R\s*', '', price).strip()
            # Remove any remaining spaces (e.g., thousand separators like "1 234.56")
            price_clean = price_clean.replace(' ', '')
            # Replace comma with dot for decimal separator (handles European format)
            price_clean = price_clean.replace(',', '.')
            try:
                adapter['price'] = float(price_clean)
            except ValueError:
                spider.logger.warning(f"Could not convert price to float: {price}")
                adapter['price'] = None
        
        return item
