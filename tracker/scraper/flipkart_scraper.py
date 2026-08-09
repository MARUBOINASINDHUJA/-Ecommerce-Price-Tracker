import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# NOT WORKING
class FlipkartScraper:

    def __init__(self, keyword, pages):
        self.keyword = keyword
        self.pages = pages
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("start-maximized")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        self.driver = webdriver.Chrome(options=options)

    def scrape(self):
        products = []

        for page in range(1,
                          self.pages):  # You can scrape more pages if needed
            url = f"https://www.flipkart.com/search?q={self.keyword}&page={page}"
            self.driver.get(url)

            try:
                # Wait for the page to load and the product containers to appear
                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[contains(@class, '_1AtVbE')]")))

                # Wait for other visible elements to ensure the page is rendered
                WebDriverWait(self.driver, 60).until(
                    EC.visibility_of_all_elements_located(
                        (By.XPATH, "//div[contains(@class, '_1AtVbE')]")))

                print(f"Page {page} loaded successfully.")
            except Exception as e:
                print(f"Error loading page {page}: {e}")
                continue

            containers = self.driver.find_elements(
                By.XPATH, "//div[contains(@class, '_1AtVbE')]")

            for idx, item in enumerate(containers):
                try:
                    # Extract title
                    try:
                        title = item.find_element(By.CLASS_NAME,
                                                  '_4rR01T').text.strip()
                    except Exception:
                        title = None

                    # Extract price
                    try:
                        price = item.find_element(By.CLASS_NAME,
                                                  '_30jeq3').text.replace(
                                                      '₹',
                                                      '').replace(',', '')
                        price = float(price)
                    except Exception:
                        price = None

                    # Extract rating
                    try:
                        rating = item.find_element(By.CLASS_NAME,
                                                   '_3LWZlK').text.strip()
                        rating = float(rating)
                    except Exception:
                        rating = None

                    # Extract number of reviews (optional)
                    try:
                        reviews_elem = item.find_elements(
                            By.CLASS_NAME, '_2_R_DZ')
                        if reviews_elem:
                            text = reviews_elem[0].text
                            import re
                            match = re.search(r'(\d+(?:,\d+)*)\s+Reviews',
                                              text)
                            reviews = int(match.group(1).replace(
                                ',', '')) if match else None
                        else:
                            reviews = None
                    except Exception:
                        reviews = None

                    # Extract seller name (if available)
                    try:
                        seller_elem = item.find_element(
                            By.CLASS_NAME, '_2X5GzR')
                        seller = seller_elem.text.strip()
                    except Exception:
                        seller = "Flipkart or Unknown Seller"

                    # Store the data
                    if title or price or rating or reviews:
                        products.append({
                            'title': title,
                            'price': price,
                            'rating': rating,
                            'reviews': reviews,
                            'seller': seller
                        })
                    print("DATA", title, price, rating, reviews, seller)

                except Exception as e:
                    print(f"Error scraping item {idx + 1}: {e}")
                    continue

        self.driver.quit()
        print(f"Scraped {len(products)} products")
        return products
