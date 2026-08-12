import asyncio
import aiohttp
import json
import logging

class OSINTScanner:
    """
    High-concurrency OSINT scanner for social media platforms.
    Replicates Sherlock-style logic using asynchronous networking.
    """
    def __init__(self, semaphore_limit=50):
        self.semaphore = asyncio.Semaphore(semaphore_limit)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Simplified site list for initial implementation - can be expanded to 400+
        self.platforms = {
            "GitHub": "https://github.com/{}",
            "Twitter": "https://twitter.com/{}",
            "Instagram": "https://www.instagram.com/{}/",
            "Reddit": "https://www.reddit.com/user/{}",
            "Pinterest": "https://www.pinterest.com/{}/",
            "Tumblr": "https://{}.tumblr.com",
            "YouTube": "https://www.youtube.com/@{}",
            "TikTok": "https://www.tiktok.com/@{}",
            "Medium": "https://medium.com/@{}",
            "Spotify": "https://open.spotify.com/user/{}",
            "Telegram": "https://t.me/{}",
            "Steam": "https://steamcommunity.com/id/{}",
            "Flickr": "https://www.flickr.com/people/{}",
            "Disqus": "https://disqus.com/by/{}",
            "Dribbble": "https://dribbble.com/{}",
            "Behance": "https://www.behance.net/{}",
            "Codepen": "https://codepen.io/{}",
            "GitLab": "https://gitlab.com/{}",
            "SlideShare": "https://www.slideshare.net/{}",
            "About.me": "https://about.me/{}",
            "Archive.org": "https://archive.org/details/@{}",
            "Badoo": "https://badoo.com/en/{}",
            "Bandcamp": "https://bandcamp.com/{}",
            "Bitbucket": "https://bitbucket.org/{}/",
            "Canva": "https://www.canva.com/{}",
            "CashApp": "https://cash.app/${}",
            "DailyMotion": "https://www.dailymotion.com/{}",
            "DeviantArt": "https://www.deviantart.com/{}",
            "Etsy": "https://www.etsy.com/people/{}",
            "Facebook": "https://www.facebook.com/{}",
            "Giphy": "https://giphy.com/{}",
            "Imgur": "https://imgur.com/user/{}",
            "Keybase": "https://keybase.io/{}",
            "Kick": "https://kick.com/{}",
            "Last.fm": "https://www.last.fm/user/{}",
            "Letterboxd": "https://letterboxd.com/{}",
            "Mastodon": "https://mastodon.social/@{}",
            "Mixcloud": "https://www.mixcloud.com/{}",
            "OkCupid": "https://www.okcupid.com/profile/{}",
            "Patreon": "https://www.patreon.com/{}",
            "ProductHunt": "https://www.producthunt.com/@{}",
            "Quora": "https://www.quora.com/profile/{}",
            "Roblox": "https://www.roblox.com/user.aspx?username={}",
            "SoundCloud": "https://soundcloud.com/{}",
            "Substack": "https://{}.substack.com",
            "Twitch": "https://www.twitch.com/{}",
            "Vimeo": "https://vimeo.com/{}",
            "Wattpad": "https://www.wattpad.com/user/{}",
            "WordPress": "https://{}.wordpress.com",
            "Xbox": "https://www.xboxgamertag.com/search/{}"
        }

    async def scan_platform(self, session, platform_name, url_template, username, callback=None):
        url = url_template.format(username)
        async with self.semaphore:
            try:
                async with session.get(url, headers=self.headers, timeout=10, allow_redirects=True) as response:
                    # Sherlock logic: 200 usually means found, though some sites need string matching
                    # For this implementation, we focus on status codes and basic exclusion
                    if response.status == 200:
                        content = await response.text()
                        # Basic exclusion for common "not found" pages that return 200
                        if any(term in content.lower() for term in ["not found", "404", "doesn't exist", "page not found"]):
                            return None
                        
                        result = {
                            "platform": platform_name,
                            "url": url,
                            "status": response.status
                        }
                        if callback:
                            callback(result)
                        return result
            except Exception as e:
                logging.debug(f"Error scanning {platform_name}: {e}")
            return None

    async def run_scan(self, username, callback=None):
        # Create a connector with increased header limits and disabled SSL verification
        # to prevent "Header value too long" and "SSL Certificate Verify Failed" errors on Windows
        connector = aiohttp.TCPConnector(ssl=False, force_close=True)
        async with aiohttp.ClientSession(
            connector=connector, 
            headers=self.headers,
            max_field_size=16384, # Increase limit for large headers
            max_line_size=16384
        ) as session:
            tasks = [
                self.scan_platform(session, name, template, username, callback)
                for name, template in self.platforms.items()
            ]
            results = await asyncio.gather(*tasks)
            return [r for r in results if r is not None]

if __name__ == "__main__":
    # Test runner
    async def test():
        scanner = OSINTScanner()
        print(f"Scanning for 'jack'...")
        results = await scanner.run_scan("jack")
        for res in results:
            print(f"[+] Found: {res['platform']} - {res['url']}")
    
    asyncio.run(test())
