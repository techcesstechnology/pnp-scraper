# PnP Scraper

A Scrapy-based web scraper for extracting product information from the Pick n Pay (PnP) website.

## Features

- Extract product names, prices, and image URLs
- Automatic price cleaning and formatting
- Rate limiting to respect server resources (2-second delay between requests)
- HTTP caching to avoid redundant requests
- Robots.txt compliance
- Pagination handling
- Error handling and logging

## Project Structure

```
pnp-scraper/
├── scrapy.cfg              # Scrapy project configuration
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore patterns
└── pnp_scraper/           # Main package directory
    ├── __init__.py
    ├── items.py           # Data models for scraped items
    ├── pipelines.py       # Data processing pipelines
    ├── settings.py        # Scrapy settings
    └── spiders/           # Spider implementations
        ├── __init__.py
        └── pnp_spider.py  # Main PnP spider
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/techcesstechnology/pnp-scraper.git
cd pnp-scraper
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the spider to scrape product information:

```bash
scrapy crawl pnp
```

### Save Results to JSON

```bash
scrapy crawl pnp -o products.json
```

### Save Results to CSV

```bash
scrapy crawl pnp -o products.csv
```

### Adjust Settings

You can override settings from the command line:

```bash
# Increase download delay to 5 seconds
scrapy crawl pnp -s DOWNLOAD_DELAY=5

# Disable cache
scrapy crawl pnp -s HTTPCACHE_ENABLED=False
```

## Configuration

### Key Settings (in `pnp_scraper/settings.py`)

- **USER_AGENT**: Identifies the scraper to the website
- **ROBOTSTXT_OBEY**: Set to `True` to respect robots.txt rules
- **DOWNLOAD_DELAY**: 2 seconds between requests (rate limiting)
- **HTTPCACHE_ENABLED**: HTTP caching enabled to avoid redundant requests
- **ITEM_PIPELINES**: Price cleaning pipeline enabled

### Customizing the Spider

The spider in `pnp_scraper/spiders/pnp_spider.py` contains CSS selectors that need to be adjusted based on the actual PnP website structure. Key methods to customize:

- `parse()`: Main page parsing and link extraction
- `parse_product()`: Product detail page parsing

The price cleaning logic is handled by the pipeline in `pnp_scraper/pipelines.py`.

## Data Model

Each scraped product contains:

- **name** (string): Product name
- **price** (float): Product price (cleaned and converted to float)
- **image_url** (string): Full URL to product image

## Development

### Running in Debug Mode

```bash
scrapy crawl pnp -L DEBUG
```

### Checking Spider List

```bash
scrapy list
```

### Testing Selectors in Scrapy Shell

```bash
scrapy shell "https://www.pnp.co.za/"
```

## Best Practices

1. **Respect Rate Limits**: The default 2-second delay helps avoid overloading the server
2. **Check robots.txt**: Always ensure `ROBOTSTXT_OBEY = True` in settings
3. **Use Caching**: HTTP cache is enabled to speed up development and testing
4. **Handle Errors**: The spider includes basic error handling and logging
5. **Monitor Logs**: Check logs for warnings and errors during scraping

## Troubleshooting

### Spider Not Found

Make sure you're in the project root directory (where `scrapy.cfg` is located).

### Import Errors

Verify all dependencies are installed:
```bash
pip install -r requirements.txt
```

### No Data Scraped

The CSS selectors in `pnp_spider.py` may need adjustment. Use Scrapy shell to test:
```bash
scrapy shell "https://www.pnp.co.za/p/your-product-url"
response.css('h1::text').get()  # Test selectors
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for educational purposes. Please respect the website's terms of service and robots.txt when scraping.

## Disclaimer

This scraper is provided as-is for educational purposes. Users are responsible for ensuring their use complies with the target website's terms of service and applicable laws.