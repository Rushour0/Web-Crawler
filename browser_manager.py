
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
import time


class Browser:
    def __init__(self, id, driver):
        self.id = id
        self.driver: webdriver.Chrome = driver
        self.is_busy = False


class BrowserManager:
    def __init__(self, browsers: int = 5):
        self.max_browsers = 10
        self.browser_no = browsers
        self.AVAILABLE = set()
        self.browsers = {}
        self.init_browsers()

    def make_available(self, id):
        self.AVAILABLE.add(id)

    def init_browsers(self):

        chrome_options = ChromeOptions()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-crash-reporter")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-in-process-stack-traces")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--output=/dev/null")

        for id in range(self.browser_no):
            browser = webdriver.Chrome(chrome_options=chrome_options)
            self.browsers[id] = Browser(id=id, driver=browser)
            self.AVAILABLE.add(id)

    def get_browser(self) -> Browser:

        while True:
            time.sleep(1)
            if len(self.AVAILABLE) != 0:
            
                browser_number = self.AVAILABLE.pop()
                browser = self.browsers[browser_number]
                return browser
