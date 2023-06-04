## Code Documentation: Crawler

The provided code defines a class called `Crawler` that implements a web crawler functionality for fetching search results from Google and extracting YouTube channel links. 

### Import Statements:
The code imports the following modules and classes:
- `json`
- `signal`
- `time`
- `CrawlMode` enum from `all_types` module
- `DatabaseManager` class from `database` module
- `BrowserManager` class from `browser_manager` module
- `webdriver` from `selenium` module
- `By` class from `selenium.webdriver.common.by` module
- `multiprocessing.pool`
- `tqdm` module

### Class Definition:
The `Crawler` class is defined with the following attributes and methods:

#### Attributes:
- `google_search_url`: A string representing the URL for Google search.
- `results`: A dictionary that stores the fetched results including YouTube URLs, general URLs, and channel URLs.
- `query`: A string representing the search query.
- `num_results`: An integer indicating the desired number of search results.
- `max_processes`: An optional integer specifying the maximum number of processes to use.
- `mode`: An optional `CrawlMode` enum specifying the crawl mode.
- `google_search_completed`: A boolean indicating whether the Google search is completed.
- `download_tracker`: A dictionary that tracks the downloaded pages.
- `browsers`: A dictionary of available browser instances.
- `last_download_id`: An integer representing the ID of the last downloaded page.
- `channels_unlocked`: A boolean indicating whether the channels are unlocked.
- `browser_manager`: An instance of the `BrowserManager` class.
- `database`: An instance of the `DatabaseManager` class.

#### Methods:
- `__init__(self, query: str, num_results: int, max_processes=5, mode: CrawlMode = CrawlMode.DRIVER_DIRECT)`: The constructor method that initializes the `Crawler` instance with the provided parameters.
- `get_download_id(self)`: Returns the next download ID.
- `download_page(self, driver: webdriver.Chrome)`: Downloads the page source of the current driver and writes it to a file.
- `crawler(self, query: str, handler: callable)`: Performs the crawling operation based on the specified query and handler function.
- `google_search_crawler(self, args: tuple[str, int])`: Crawls the Google search results for the given query and start position.
- `parse_google_search(self, driver: webdriver.Chrome = None, content: str = None)`: Parses the Google search results page to extract URLs and update the results dictionary.
- `youtube_channel_crawler(self, query: str)`: Crawls the YouTube channel page for the given query.
- `parse_youtube_channel(self, driver: webdriver.Chrome = None, content: str = None)`: Parses the YouTube channel page to extract channel URLs and update the results dictionary.
- `exit_crawling(self)`: Exits the crawling process either by unlocking the channels or recursively crawling the YouTube channel pages.
- `save_results(self)`: Saves the results to the database and a JSON file.
- `handler(signum, frame)`: Signal handler function used to handle the interruption signal.
- `first_crawl_operate(self, driver: webdriver.Chrome = None, content: str = None)`: Waits for the user to solve the captcha by pressing Enter.
- `first_crawl(self)`: Performs the first crawl operation by initiating the Google search and waiting for the user to solve the captcha.
- `run(self)`: Runs the crawler by initiating the crawling process, either sequentially or using multiple processes.

### Main Code Execution:


The main code block includes a `num_results` variable indicating the desired number of search results and a `search_query` variable representing the search query.

The code creates an instance of the `Crawler` class with the specified parameters and calls the `run()` method on the `crawler` instance to initiate the crawling process.

Finally, the total number of channel links found is printed.

This code essentially provides a web crawling functionality for fetching search results from Google and extracting YouTube channel links based on a given search query and the desired number of results.
