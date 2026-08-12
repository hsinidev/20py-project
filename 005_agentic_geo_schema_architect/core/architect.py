import google.generativeai as genai
import os
import json

class SchemaArchitect:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')

    def generate_json_ld(self, url: str, crawl_data: dict):
        if not self.model:
            return self._industrial_heuristic(url, crawl_data)

        prompt = f"""
        Act as a World-Class Schema Architect. 
        Analyze this page: {url}
        Title: {crawl_data.get('title')}
        Desc: {crawl_data.get('description')}
        Image: {crawl_data.get('primary_image')}
        Breadcrumbs: {json.dumps(crawl_data.get('breadcrumbs'))}
        
        Task: Generate a MASSIVE, 100% Comprehensive JSON-LD @graph.
        MUST include:
        1. ItemPage (The container)
        2. BreadcrumbList (All steps from the page)
        3. VideoGame / WebApplication (with gamePlatform, operatingSystem, genre, author, aggregateRating, offers)
        4. WebSite (with search potentialAction)
        5. Organization (Full corporate identity with ContactPoint, PostalAddress, founder, and sameAs links)
        
        Requirement: Matches the complexity of crazygames.com/schema.
        Output: ONLY valid JSON.
        """
        
        try:
            response = self.model.generate_content(prompt)
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except:
            return self._industrial_heuristic(url, crawl_data)

    def _industrial_heuristic(self, url, crawl_data):
        title = crawl_data.get('title', "Product")
        image = crawl_data.get('primary_image', f"{url}/logo.png")
        desc = crawl_data.get('description', f"Professional service for {title}")
        domain = "/".join(url.split("/")[:3])
        
        # Build Complex Graph
        graph = [
            {
                "@type": "ItemPage",
                "@id": f"{url}#ItemPage",
                "url": url,
                "name": title,
                "description": desc,
                "breadcrumb": {"@id": f"{url}#breadcrumb"},
                "mainEntity": {"@id": f"{url}#primary"}
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{url}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": i+1, "name": b['name'], "item": b['item']}
                    for i, b in enumerate(crawl_data.get('breadcrumbs', []))
                ] if crawl_data.get('breadcrumbs') else [{"@type": "ListItem", "position": 1, "name": "Home", "item": domain}]
            },
            {
                "@type": ["VideoGame", "WebApplication"],
                "@id": f"{url}#primary",
                "name": title,
                "url": url,
                "description": desc,
                "image": image,
                "applicationCategory": "GameApplication",
                "operatingSystem": "Windows, MacOS, Linux, Android, iOS",
                "gamePlatform": ["https://schema.org/DesktopWebPlatform", "https://schema.org/MobileWebPlatform"],
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": "8.9",
                    "bestRating": "10",
                    "ratingCount": "12500"
                },
                "offers": {
                    "@type": "Offer",
                    "price": "0",
                    "priceCurrency": "USD",
                    "availability": "http://schema.org/InStock"
                }
            },
            {
                "@type": "WebSite",
                "@id": f"{domain}/#website",
                "url": domain,
                "name": domain.split("//")[1],
                "publisher": {"@id": f"{domain}/#organization"}
            },
            {
                "@type": "Organization",
                "@id": f"{domain}/#organization",
                "name": domain.split("//")[1].capitalize(),
                "url": domain,
                "logo": image,
                "contactPoint": {
                    "@type": "ContactPoint",
                    "contactType": "customer support",
                    "email": f"support@{domain.split('//')[1]}"
                }
            }
        ]

        return {"@context": "https://schema.org", "@graph": graph}
