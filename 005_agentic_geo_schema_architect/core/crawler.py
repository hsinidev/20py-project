import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin

class AdvancedCrawler:
    def crawl(self, url):
        try:
            res = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # 1. Existing JSON-LD
            existing = []
            for s in soup.find_all('script', type='application/ld+json'):
                try: existing.append(json.loads(s.string))
                except: pass
            
            # 2. Meta Data
            meta = {}
            for m in soup.find_all('meta'):
                p = m.get('property') or m.get('name')
                if p and m.get('content'): meta[p] = m.get('content')
            
            # 3. Breadcrumbs
            breadcrumbs = []
            # Common breadcrumb selectors
            bc_tags = soup.find_all(['nav', 'div', 'ul'], class_=re.compile(r'breadcrumb|path', re.I))
            for tag in bc_tags:
                for a in tag.find_all('a'):
                    breadcrumbs.append({"name": a.get_text(strip=True), "item": urljoin(url, a.get('href', ''))})
            
            # 4. Ratings & Game Info
            rating_val = soup.find(text=re.compile(r'Rating|Score', re.I))
            rating_count = soup.find(text=re.compile(r'votes|reviews', re.I))
            
            # 5. Image Detection
            primary_image = meta.get('og:image') or meta.get('twitter:image')
            if not primary_image:
                img = soup.find('img', src=re.compile(r'cover|thumb|featured', re.I))
                if img: primary_image = urljoin(url, img.get('src'))

            return {
                "url": url,
                "title": soup.title.string if soup.title else "",
                "description": meta.get('description') or meta.get('og:description', ""),
                "existing": existing,
                "meta": meta,
                "breadcrumbs": breadcrumbs,
                "primary_image": primary_image,
                "text_sample": soup.get_text()[:3000]
            }
        except Exception as e:
            return {"error": str(e)}
