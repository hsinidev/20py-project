import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager

class PerplexityAutomator:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None

    def _setup_driver(self):
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

        stealth(self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

    def scrape_rank(self, keyword: str):
        """Mocks or executes rank scraping from Perplexity.ai"""
        # For the prototype, we return realistic fluctuating data if no driver
        # Real logic would involve navigating to perplexity.ai and parsing the 'Sources' carousel
        
        # Simulated source data
        domains = ["wikipedia.org", "techcrunch.com", "theverge.com", "nytimes.com", 
                   "github.com", "reddit.com", "medium.com", "bloomberg.com"]
        
        results = []
        count = random.randint(3, 6)
        sample = random.sample(domains, count)
        
        for i, dom in enumerate(sample, 1):
            results.append({
                "position": i,
                "domain": dom,
                "volatility": random.uniform(-2.0, 2.0)
            })
        
        # Introduce a delay to simulate real browsing
        time.sleep(random.uniform(0.5, 1.5))
        return results

    def close(self):
        if self.driver:
            self.driver.quit()
