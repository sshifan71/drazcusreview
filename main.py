from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup ChromeDriver
service = webdriver.FirefoxOptions()  # Replace with your ChromeDriver path
driver = webdriver.Firefox(options=service)

# Open Daraz and search for polarized glasses
driver.get("https://www.daraz.com.bd")
search_box = driver.find_element(By.NAME, "q")  # Update the search box selector if needed
search_box.send_keys("polarized glasses")
search_box.send_keys(Keys.RETURN)

# Wait for the page to load
time.sleep(8)
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.Bm3ON:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)"))
)
# Collect product links (first 10)
product_links = []
products = driver.find_elements(By.CSS_SELECTOR, "div.Bm3ON:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)")[:10]
for product in products:
    product_links.append(product.get_attribute("href"))
print(product_links)
# Scrape reviews from each product
all_reviews = {}
for i, link in enumerate(product_links, start=1):
    driver.get(link)
    time.sleep(3)  # Wait for the page to load
    
    reviews = []
    while True:  # Loop through review pages
        review_elements = driver.find_elements(By.CSS_SELECTOR, "div.rating-review__content")
        for review in review_elements:
            reviews.append(review.text.strip())

        # Check for "Next" button
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "button.next-btn")
            next_button.click()
            time.sleep(3)  # Wait for the next page to load
        except:
            break  # No more pages
    
    all_reviews[link] = reviews
    print(f"Scraped reviews for product {i}")

# Close the driver
driver.quit()

# Output scraped reviews
for product, reviews in all_reviews.items():
    print(f"\nProduct: {product}")
    for review in reviews:
        print(f" - {review}")
