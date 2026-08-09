import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AmazonScraper:

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

        for page in range(1, self.pages):
            url = f"https://www.amazon.in/s?k={self.keyword}&page={page}"
            try:
                self.driver.get(url)
            except Exception as e:
                print(f"Failed to load page: {e}")
                self.driver.quit()
                return []

            try:
                time.sleep(3)
                WebDriverWait(self.driver, 100).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         "//div[@data-component-type='s-search-result']")))
                print(f"Page {page} loaded successfully.")
            except Exception as e:
                print(f"Error loading page {page}: {e}")
                continue

            containers = self.driver.find_elements(
                By.XPATH, "//div[@data-component-type='s-search-result']")

            for idx, item in enumerate(containers):
                try:
                    try:
                        title_elem = item.find_element(By.XPATH, ".//h2/span")
                    except:
                        try:
                            title_elem = item.find_element(
                                By.XPATH,
                                './/span[@class="a-size-medium a-color-base a-text-normal"]'
                            )
                        except:
                            title = None
                            pass

                    title = title_elem.text.strip()

                    try:
                        price_whole = item.find_element(
                            By.XPATH,
                            ".//span[@class='a-price-whole']").text.replace(
                                ',', '')
                        price = float(f"{price_whole}")
                    except:
                        price = None

                    try:
                        # Locate the 'review-block' div
                        review_block = item.find_element(
                            By.XPATH, ".//div[@data-cy='reviews-block']")

                        # Extract product rating from within review-block
                        rating_element = review_block.find_element(
                            By.XPATH,
                            ".//*[@data-cy='reviews-ratings-slot']//span[contains(@class, 'a-icon-alt')]"
                        )
                        rating_text = self.driver.execute_script(
                            "return arguments[0].textContent;", rating_element)
                        rating = float(rating_text.split()[0])
                    except:
                        rating = None

                    try:
                        # Extract number of reviews from within review-block
                        review_elem = review_block.find_element(
                            By.XPATH,
                            ".//a[contains(@class, 's-underline-text')]")
                        reviews = review_elem.text.replace(
                            ',', '') if review_elem else None
                    except:
                        reviews = None

                    # print(f"Rating: {rating}, Reviews: {reviews}")

                    try:
                        seller_elem = item.find_element(
                            By.XPATH, ".//div[contains(text(),'Sold by')]")
                        seller = seller_elem.text.replace("Sold by ",
                                                          "").strip()
                    except:
                        seller = "Amazon or Unknown Seller"

                    if title or price or rating or reviews:
                        products.append({
                            'title': title,
                            'price': price,
                            'rating': rating,
                            'reviews': reviews,
                            'seller': seller
                        })
                    print("DATA", title, price, reviews, rating)

                except Exception as e:
                    print(f"Error scraping item {idx + 1}: {e}")
                    continue

        self.driver.quit()
        print(f"Scraped {len(products)} products")
        return products
