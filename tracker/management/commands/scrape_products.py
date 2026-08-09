from django.core.management.base import BaseCommand
from tracker.scraper.factory import ScraperFactory
from tracker.models import Product, PriceHistory


class Command(BaseCommand):
    help = 'Scrape product data from a given site'

    def add_arguments(self, parser):
        parser.add_argument('--site', type=str, required=True)
        parser.add_argument('--keyword', type=str, required=True)
        parser.add_argument('--pages', type=int, required=True)

    def handle(self, *args, **options):
        scraper = ScraperFactory.get_scraper(options['site'],
                                             options['keyword'],
                                             options['pages'])
        print(
            f"Running scraper for {options['site']} with keyword '{options['keyword']}'"
        )

        data = scraper.scrape()
        for item in data:
            try:
                try:
                    product = Product.objects.get(title=item['title'])

                    if product.price != item['price']:

                        # Update product price
                        product.price = item['price']
                        product.rating = item.get('rating')
                        product.reviews = item.get('reviews')
                        product.seller = item.get('seller')
                        product.source = options['site']
                        product.save()

                        # Save price history
                        PriceHistory.objects.create(product=product,
                                                    price=item['price'])

                except Product.DoesNotExist:
                    # Create new product if it doesn't exist
                    product = Product.objects.create(
                        title=item['title'],
                        price=item['price'],
                        rating=item.get('rating'),
                        reviews=item.get('reviews'),
                        seller=item.get('seller'),
                        source=options['site'],
                    )
                    print(f"New product added: {product.title}")

                    # Save initial price history
                    PriceHistory.objects.create(product=product,
                                                price=item['price'])
            except Exception as e:
                print(
                    f"Error ocuur while saving the record entry for {item['title']}"
                )
