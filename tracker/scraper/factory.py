from .amazon_scraper import AmazonScraper
from .flipkart_scraper import FlipkartScraper


class ScraperFactory:

    @staticmethod
    def get_scraper(site, keyword, pages):
        if site == 'amazon':
            return AmazonScraper(keyword, pages)
        elif site == 'flipkart':
            return FlipkartScraper(keyword, pages)
        else:
            raise ValueError("Unsupported site")
