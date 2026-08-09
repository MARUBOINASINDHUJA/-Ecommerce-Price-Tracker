from django.test import TestCase
from unittest.mock import patch

from tracker.scraper.amazon_scraper import AmazonScraper
from tracker.models import Product


class AmazonScraperTest(TestCase):

    @patch("tracker.scraper.amazon_scraper.webdriver.Chrome")
    def test_scrape_returns_products(self, mock_chrome):
        # Mock the Chrome instance and its behavior
        mock_driver = mock_chrome.return_value
        mock_driver.find_elements.return_value = []

        scraper = AmazonScraper(keyword="Phone")
        products = scraper.scrape()

        self.assertIsInstance(products, list)
        mock_driver.quit.assert_called_once()

    @patch("tracker.scraper.amazon_scraper.webdriver.Chrome")
    def test_scrape_timeout_error_handling(self, mock_chrome):
        mock_driver = mock_chrome.return_value

        # Simulate WebDriverWait timeout by raising an exception
        mock_driver.get.side_effect = Exception("Timeout error")

        scraper = AmazonScraper(keyword="Phone")
        products = scraper.scrape()

        self.assertEqual(products, [])
        mock_driver.quit.assert_called_once()


class AmazonScraperAPITestCase(TestCase):

    @patch("tracker.scraper.amazon_scraper.AmazonScraper.scrape")
    def test_amazon_scraper_and_api_integration(self, mock_scrape):
        mock_scrape.return_value = [
            {
                'title': 'Test Amazon Phone',
                'price': 3499.0,
                'rating': 4.3,
                'reviews': 1234,
                'seller': 'Amazon'
            },
            {
                'title': 'Another Phone',
                'price': 1999.0,
                'rating': 3.8,
                'reviews': 456,
                'seller': 'Amazon'
            },
        ]

        scraper = AmazonScraper(keyword="Phone")
        products = scraper.scrape()

        for item in products:
            Product.objects.create(title=item['title'],
                                   price=item['price'],
                                   rating=item['rating'],
                                   reviews=item['reviews'],
                                   seller=item['seller'])

        self.assertEqual(Product.objects.count(), 2)
