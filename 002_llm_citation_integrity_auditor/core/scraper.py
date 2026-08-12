import asyncio
import httpx
from bs4 import BeautifulSoup
import re

class AsyncScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        }

    async def fetch_text(self, url: str) -> str:
        """Fetches and cleans text content from a URL."""
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=15.0, follow_redirects=True) as client:
                resp = await client.get(url)
                if resp.status_code != 200:
                    return f"Error {resp.status_code}: Unable to fetch source."
                
                soup = BeautifulSoup(resp.text, 'lxml')
                
                # Remove scripts, styles, and junk
                for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                    tag.decompose()
                
                # Get text and clean whitespace
                text = soup.get_text(separator=' ')
                text = re.sub(r'\s+', ' ', text).strip()
                return text[:10000] # Limit to first 10k chars for analysis
        except Exception as e:
            return f"Fetch Failure: {str(e)}"

    async def fetch_batch(self, urls: list[str]) -> dict[str, str]:
        """Fetches multiple URLs concurrently."""
        tasks = [self.fetch_text(url) for url in urls]
        results = await asyncio.gather(*tasks)
        return dict(zip(urls, results))
