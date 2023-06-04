import json
import signal
import time
from all_types import CrawlMode

from database import DatabaseManager
from browser_manager import BrowserManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import multiprocessing.pool
from tqdm import tqdm
import bs4


class Crawler:
    google_search_url = 'https://www.google.com/search'

    results = {'youtube_urls': [], 'urls': [], 'channel_urls': []}

    def __init__(self, query: str, num_results: int, max_processes=5, mode: CrawlMode = CrawlMode.DRIVER_DIRECT):

        self.query = query
        self.num_results = num_results
        self.max_processes = max_processes
        self.mode = mode
        self.google_search_completed = False

        self.download_tracker = {}
        self.browsers = {}
        self.last_download_id = -1
        self.channels_unlocked = False
        self.browser_manager = BrowserManager(browsers=1)
        self.database = DatabaseManager()

    def get_download_id(self):
        self.last_download_id += 1
        return self.last_download_id

    def download_page(self, driver: webdriver.Chrome):

        content = driver.page_source

        self.download_tracker[driver.current_url] = self.get_download_id()

        with open(f'page{self.download_tracker[driver.current_url]}.txt', 'w') as f:
            f.write(content)

    def crawler(self, query: str, handler: callable):

        browser = self.browser_manager.get_browser()

        browser.driver.get(query)

        time.sleep(10)

        if self.mode == CrawlMode.DOWNLOAD_HTML:
            content = self.download_page(browser.driver)
            self.browser_manager.make_available(browser.id)
            handler(content=content)
        else:
            handler(driver=browser.driver)

        self.browser_manager.make_available(browser.id)
        return browser.driver.current_url

    def google_search_crawler(self,  args: tuple[str, int]):
        if args is not None:
            query, start = args
            search_query = f'{query}&start={start}'

        return self.crawler(search_query, self.parse_google_search)

    def parse_google_search(self, driver: webdriver.Chrome = None, content: str = None):
        if driver is not None:

            links = driver.find_elements(By.TAG_NAME, value='a')
            one_found = False
            for link in links:
                href = link.get_attribute('href')
                self.results['urls'].append(href)
                # self.database.insert_url(href)
                if href and 'youtube.com' in href:
                    one_found = True
                    self.results['youtube_urls'].append(href)
                    # self.database.insert_url(href)
                    if (href.startswith('https://youtube.com/c') or href.startswith('https://youtube.com/@')):
                        self.results['channel_urls'].append(href)
                        # self.database.insert_channel(href)
            if not one_found:
                self.exit_crawling()
            if len(self.results['urls']) >= self.num_results:
                self.exit_crawling()

                return
        elif content is None:
            parser = bs4.BeautifulSoup(content, 'html.parser')
            # TODO: parse content

    def youtube_channel_crawler(self, query: str):

        self.crawler(query, self.parse_youtube_channel)

        if len(self.results['channel_urls']) >= self.num_results:
            self.exit_crawling()

    def parse_youtube_channel(self, driver: webdriver.Chrome = None, content: str = None):
        if driver is not None:
            links = driver.find_elements(By.TAG_NAME, value='a')
            for link in links:
                href = link.get_attribute('href')

                if href and (href.startswith('https://youtube.com/c') or href.startswith('https://youtube.com/@')):
                    self.results['channel_urls'].append(href)
                    # self.database.insert_channel(href)
        if content is not None:
            parser = bs4.BeautifulSoup(content, 'html.parser')
            # TODO: parse content

    def exit_crawling(self):
        if self.channels_unlocked:
            exit(0)
        else:
            self.channels_unlocked = True
            for url in tqdm(self.results['urls']):
                self.youtube_channel_crawler(url)
            self.exit_crawling()

    def save_results(self):
        self.database.insert_urls(self.results['urls'])
        self.database.insert_channels(self.results['channel_urls'])

        with open('results.json', 'w') as f:
            json.dump(self.results, f)

    def handler(signum, frame):

        print('Signal handler called with signal', signum)

        exit(0)

    def first_crawl_operate(self, driver: webdriver.Chrome = None, content: str = None):
        input("Waiting for captcha to be solved. Press enter to continue: ")

    def first_crawl(self):
        self.query = self.crawler(
            query=f'{self.google_search_url}?q={self.query}&start=280', handler=self.first_crawl_operate)

    def run(self):
        signal.signal(signal.SIGINT, self.handler)

        print(f"Fetching {self.num_results} results for {self.query}")

        self.first_crawl()
        start = time.time()

        if self.max_processes == 1:
            for i in (pbar := tqdm(range(0, self.num_results, 10), desc=f"Links: {len(self.results['urls'])}")):
                self.google_search_crawler((self.query, i))
                pbar.set_description(f"Links: {len(self.results['urls'])}")
                if self.channels_unlocked:
                    break
        else:
            with multiprocessing.pool.ThreadPool(processes=self.max_processes) as pool:
                for _ in (pbar := tqdm(pool.imap_unordered(self.google_search_crawler, [(self.query, i)for i in range(0, self.num_results, 10)]), total=self.num_results // 10, desc=f"Links: {len(self.results['urls'])}")):
                    pbar.set_description(f"Links: {len(self.results['urls'])}")

        print(f"Time taken: {time.time() - start:.2f} seconds")

        return self.results


num_results = 10000
search_query = 'site:youtube.com openinapp.co'

if __name__ == '__main__':
    import os

    os.system('cls' if os.name == 'nt' else 'clear')
    crawler = Crawler(search_query, num_results,
                      max_processes=1, mode=CrawlMode.DRIVER_DIRECT)
    channel_links = crawler.run()

    print(f"Total links {len(channel_links)}")
