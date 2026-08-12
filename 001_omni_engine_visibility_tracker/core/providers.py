"""Provider query engines – live API + demo fallback."""
import asyncio
import os

_MOCK = {
    "Gemini": """\
According to research at Stanford AI Lab, generative engine visibility \
is reshaping search attribution.
Source: https://stanford.edu/research/geo-2024
Author: Dr. Sarah Chen

The McKinsey Digital Report "AI Attribution 2024" highlights key shifts:
- 73% of B2B buyers trust AI-cited sources over traditional search.
Source: https://mckinsey.com/insights/ai-attribution-2024

MIT Technology Review adds context: "Semantic Search & LLM Sourcing"
Source: https://technologyreview.com/2024/llm-sourcing
Author: James Rodriguez

Additional references:
Source: https://openai.com/research/gpt-visibility
Source: https://deepmind.google/research/semantic-index""",

    "Perplexity": """\
**Sources retrieved for your query:**

1. Harvard Business Review – "GEO Visibility Guide 2025"
   URL: https://hbr.org/2025/geo-visibility
   Author: Amanda Foster

2. Search Engine Journal – Real-time GEO rankings
   URL: https://searchenginejournal.com/geo-rankings-2025

3. Moz Research by Pete Meyers: LLM citation analysis
   URL: https://moz.com/research/llm-citation-patterns

4. Ahrefs Data Study on AI citations
   URL: https://ahrefs.com/blog/ai-citations-2025

5. Semrush GEO Industry Report
   URL: https://semrush.com/blog/geo-study-2025""",

    "SearchGPT": """\
I searched the web for your query. Here are the most relevant results:

From Wikipedia: https://en.wikipedia.org/wiki/Generative_engine_optimization
First introduced by Prof. Michael Zhang, Columbia University.

Forbes Technology Council – "Understanding GEO Visibility"
Author: Sarah Johnson
URL: https://forbes.com/technology/geo-visibility-2025

Academic paper – "Semantic Attribution in LLM Systems"
URL: https://arxiv.org/abs/2025.geo-attribution
Authors: Chen, Liu, Wang et al.

Industry research: https://gartner.com/research/ai-search-2025
Analyst report: https://forrester.com/report/ai-attribution-2025""",
}


class ProviderEngine:
    def __init__(self, api_keys: dict, log_fn=None):
        self.keys = api_keys
        self.log  = log_fn or (lambda msg: None)

    async def query(self, provider: str, query: str) -> dict:
        method = {
            "gemini":     self._gemini,
            "perplexity": self._perplexity,
            "searchgpt":  self._searchgpt,
        }.get(provider)
        if method is None:
            return {"text": "", "status": "error"}
        return await method(query)

    async def _gemini(self, query: str) -> dict:
        key = self.keys.get("gemini", "")
        if not key:
            return {"text": _MOCK["Gemini"], "status": "demo"}
        try:
            import google.generativeai as genai
            genai.configure(api_key=key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            resp = await asyncio.to_thread(
                model.generate_content,
                f"Answer with cited URLs for: {query}"
            )
            return {"text": resp.text, "status": "live"}
        except Exception as e:
            self.log(f"[Gemini] {e}")
            return {"text": _MOCK["Gemini"], "status": "demo"}

    async def _perplexity(self, query: str) -> dict:
        key = self.keys.get("perplexity", "")
        if not key:
            return {"text": _MOCK["Perplexity"], "status": "demo"}
        try:
            import openai
            client = openai.AsyncOpenAI(api_key=key, base_url="https://api.perplexity.ai")
            resp = await client.chat.completions.create(
                model="llama-3.1-sonar-large-128k-online",
                messages=[{"role": "user", "content": query}],
            )
            return {"text": resp.choices[0].message.content, "status": "live"}
        except Exception as e:
            self.log(f"[Perplexity] {e}")
            return {"text": _MOCK["Perplexity"], "status": "demo"}

    async def _searchgpt(self, query: str) -> dict:
        key = self.keys.get("openai", "")
        if not key:
            return {"text": _MOCK["SearchGPT"], "status": "demo"}
        try:
            import openai
            client = openai.AsyncOpenAI(api_key=key)
            resp = await client.chat.completions.create(
                model="gpt-4o-search-preview",
                messages=[{"role": "user", "content": query}],
            )
            return {"text": resp.choices[0].message.content, "status": "live"}
        except Exception as e:
            self.log(f"[SearchGPT] {e}")
            return {"text": _MOCK["SearchGPT"], "status": "demo"}
