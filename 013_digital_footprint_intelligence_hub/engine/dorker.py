import asyncio
import aiohttp
from bs4 import BeautifulSoup
import urllib.parse
import logging

class GoogleDorker:
    """
    Advanced Google Dorking Service for metadata and sensitive file extraction.
    """
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        self.base_url = "https://www.google.com/search?q="

    def generate_dorks(self, target):
        """Generates a list of dork queries for a target name or domain."""
        return [
            f'site:linkedin.com "{target}"',
            f'site:facebook.com "{target}"',
            f'site:twitter.com "{target}"',
            f'"{target}" filetype:pdf',
            f'"{target}" filetype:doc OR filetype:docx',
            f'"{target}" filetype:xls OR filetype:xlsx',
            f'"{target}" intitle:index.of',
            f'"{target}" inurl:admin',
            f'"{target}" email',
            f'"{target}" password OR secret OR key'
        ]

    async def search(self, query, session):
        """Performs a single search (be careful with rate limits)."""
        url = self.base_url + urllib.parse.quote(query)
        try:
            async with session.get(url, headers=self.headers, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    return self.parse_results(html, query)
                elif response.status == 429:
                    logging.warning("Rate limit hit on Google Dorking.")
                    return []
        except Exception as e:
            logging.error(f"Dorking error for {query}: {e}")
        return []

    def parse_results(self, html, query):
        """Parses Google search results."""
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        # Search for typical result divs in Google (can be brittle)
        for g in soup.find_all('div', class_='tF2Cxc'):
            title_tag = g.find('h3')
            link_tag = g.find('a')
            snippet_tag = g.find('div', class_='VwiC3b')

            if title_tag and link_tag:
                results.append({
                    "query": query,
                    "title": title_tag.get_text(),
                    "url": link_tag['href'],
                    "snippet": snippet_tag.get_text() if snippet_tag else ""
                })
        return results

    async def run_dorking(self, target, callback=None):
        """Runs a full dorking campaign."""
        queries = self.generate_dorks(target)
        async with aiohttp.ClientSession() as session:
            all_results = []
            for query in queries:
                res = await self.search(query, session)
                all_results.extend(res)
                if callback and res:
                    for item in res:
                        callback(item)
                # Small delay to avoid instant block
                await asyncio.sleep(2)
            return all_results

if __name__ == "__main__":
    async def test():
        dorker = GoogleDorker()
        print("Dorking for 'HSINI MOHAMED'...")
        # Note: This might get blocked by Google's bot detection in a CLI environment
        # but the logic is sound for a production-grade tool with proxy rotation.
        results = await dorker.run_dorking("HSINI MOHAMED")
        for r in results:
            print(f"[{r['query']}] {r['title']} - {r['url']}")

    asyncio.run(test())
