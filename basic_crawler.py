import time
from all_types import CrawlMode
from browser_wrapper import Browser
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
import multiprocessing.pool
from tqdm import tqdm


class Crawler:
    base_url = 'https://www.google.com/search'

    results = {'url': [], }
    MAX_PROCESSES = 6
    MAX_BROWSERS = 3
    AVAILABLE = set()

    def __init__(self, query: str, num_results: int):
        self.query = query
        self.num_results = num_results
        self.browsers = {}
        self.mode: CrawlMode = CrawlMode.SPACE_SAVER

        self.init_browsers()

    def init_browsers(self):

        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-crash-reporter")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-in-process-stack-traces")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--output=/dev/null")

        for id in range(self.MAX_BROWSERS):
            browser = webdriver.Chrome(chrome_options=chrome_options)
            self.browsers[id] = Browser(id=id, driver=browser)
            self.AVAILABLE.add(id)

    def get_browser(self):

        while True:
            if len(self.AVAILABLE) == 0:
                time.sleep(1)
            else:
                browser_number = self.AVAILABLE.pop()
                browser = self.browsers[browser_number]
                return browser

    def make_available(self, id):

        self.AVAILABLE.add(id)

    def crawler(self, query: str, handler: callable):

        browser = self.get_browser()

        browser.driver.get(search_query)

        time.sleep(5)

        links = browser.driver.find_elements(By.TAG_NAME, value='a')

        self.make_available(browser.id)

    def google_search_crawler(self, start):

        search_query = f'{self.base_url}?query={self.query}&start={start}'

        browser = self.get_browser()

        browser.driver.get(search_query)

        time.sleep(5)

        links = browser.driver.find_elements(By.TAG_NAME, value='a')

        self.make_available(browser.id)

        for link in links:
            href = link.get_attribute('href')
            if href and 'youtube.com' in href:
                self.results['url'].append(href)
        if len(self.results['url']) >= self.num_results:
            self.exit_crawling()

    def exit_crawling(self):
        if self.channels_unlocked:
            return
        else:
            self.google_search_crawler()

    def run(self):

        print(f"Fetching {self.num_results} results for {self.query}")

        print(f"AVAILABLE BROWSERS: {self.AVAILABLE}")

        start = time.time()

        with multiprocessing.pool.ThreadPool(processes=self.MAX_PROCESSES) as pool:
            for _ in tqdm(pool.imap_unordered(self.google_search_crawler, range(0, self.num_results, 10)), total=self.num_results // 10, desc=f"Links: {len(self.results['url'])}"):
                pass

        print(f"Time taken: {time.time() - start:.2f} seconds")

        return self.results


num_results = 10000
search_query = 'site:youtube.com openinapp.co'

if __name__ == '__main__':

    crawler = Crawler(search_query, num_results)
    channel_links = crawler.run()

    print(f"Total links {len(channel_links)}")
