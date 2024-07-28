from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os

driver = webdriver.Chrome()
url = 'https://www.goodreads.com/genres/most_read/non-fiction/'
driver.get(url)

time.sleep(5)


books = []


bookElements = WebDriverWait(driver, 10).until(
    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.bookImage'))
)
# ele = bookElements[:6]
for index, element in enumerate(bookElements[:48]):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(1)
    action = ActionChains(driver)
    

    action.move_to_element(element).perform()
    time.sleep(1)

    title_elements = driver.find_elements(By.CSS_SELECTOR, 'a.readable.bookTitle')
    titles = [title_element.text.strip() for title_element in title_elements if title_element.text.strip()]

    # Extract author names
    author_elements = driver.find_elements(By.CSS_SELECTOR, '.authorName')
    authors = [author_element.text.strip() for author_element in author_elements if author_element.text.strip()]

    more_buttons = driver.find_elements(By.CSS_SELECTOR, 'div.addBookTipDescription a')
    if more_buttons:
        try:
            more_button = more_buttons[index]
            if more_button:
                driver.execute_script("arguments[0].click();", more_button)
                time.sleep(1)
                long_description_elements = driver.find_elements(By.CSS_SELECTOR, 'div.addBookTipDescription span[id^=freeText]:not([id*="Container"])')
            else:
                long_description_elements = driver.find_elements(By.CSS_SELECTOR, 'div.addBookTipDescription span[id^=freeTextContainer]')
        except Exception as e:
            print(f"{index + 1}: {e}")
    
    long_description_elements = driver.find_elements(By.CSS_SELECTOR, 'div.addBookTipDescription span[id^=freeText]:not([id*="Container"])')
    long_descriptions = [description.text.strip() for description in long_description_elements if description.text.strip()]


    for title, author, description in zip(titles, authors, long_descriptions):
        print(f"Book {index + 1}: {title} by {author}")
        print(f"Description: {description}")
        print("---")
        books.append({'title': title, 'author': author, 'decription':description})

    if index < len(bookElements[:48]) - 1:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(1)

df = pd.DataFrame(books)
print(df.head())

if os.path.exists('books.csv'):
    df.to_csv('books.csv', mode='a', header=False, index=False)
else:
    df.to_csv('books.csv', index=False)
df.to_csv('books_fiction.csv', index=False)

driver.quit()

