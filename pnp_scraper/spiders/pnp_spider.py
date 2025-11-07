import scrapy
from pnp_scraper.items import PnpScraperItem
import re


class PnpSpider(scrapy.Spider):
    name = "pnp"
    allowed_domains = ["pnp.co.za"]
    start_urls = ["https://www.pnp.co.za/"]
    
    custom_settings = {
        'FEEDS': {
            'products.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True,
            },
        },
    }

    def parse(self, response):
        """
        Parse the main page and follow product links.
        This is a template method that should be customized based on the actual
        PnP website structure.
        """
        # Extract product links from the page
        # Note: These selectors need to be adjusted based on actual website structure
        product_links = response.css('a.product-link::attr(href)').getall()
        
        for link in product_links:
            yield response.follow(link, callback=self.parse_product)
        
        # Handle pagination
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_product(self, response):
        """
        Parse individual product pages and extract product information.
        """
        try:
            item = PnpScraperItem()
            
            # Extract product name
            # Adjust selectors based on actual website structure
            name = response.css('h1.product-name::text').get()
            if not name:
                name = response.css('h1::text').get()
            
            # Extract price
            price = response.css('span.product-price::text').get()
            if not price:
                price = response.css('.price::text').get()
            
            # Extract image URL
            image_url = response.css('img.product-image::attr(src)').get()
            if not image_url:
                image_url = response.css('img::attr(src)').get()
            
            # Clean and assign values
            if name:
                item['name'] = name.strip()
            
            if price:
                item['price'] = self.clean_price(price)
            
            if image_url:
                # Handle relative URLs
                item['image_url'] = response.urljoin(image_url)
            
            # Only yield if we have at least a name
            if item.get('name'):
                yield item
            else:
                self.logger.warning(f"No product name found on {response.url}")
                
        except Exception as e:
            self.logger.error(f"Error parsing product at {response.url}: {str(e)}")
    
    def clean_price(self, price_text):
        """
        Clean price text to extract numeric value.
        Handles various price formats like "R 123.45", "R123,45", etc.
        """
        if not price_text:
            return None
        
        # Remove currency symbols, whitespace, and commas
        price_clean = re.sub(r'[R\s,]', '', price_text.strip())
        
        # Handle decimal separators
        price_clean = price_clean.replace(',', '.')
        
        try:
            return price_clean
        except ValueError:
            self.logger.warning(f"Could not clean price: {price_text}")
            return None
