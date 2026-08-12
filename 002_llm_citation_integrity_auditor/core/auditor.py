import re
import asyncio
from typing import List
from .models import Claim, Citation, GroundingLevel, AuditResult
from .scraper import AsyncScraper
from .similarity import SimilarityEngine

class CitationAuditor:
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.scraper = AsyncScraper()
        # Mocking LangChain behavior for robustness if key is missing
        # In a real app, this would use ChatOpenAI / Gemini and a specific template

    def parse_citations(self, text: str) -> List[Claim]:
        """Extracts claims and their associated [number] or (url) citations."""
        # Pattern 1: [1], [2]... with a bottom reference list
        # Pattern 2: Inline URLs (https://...)
        
        claims = []
        # Split by sentences or paragraph segments
        segments = re.split(r'(?<=[.!?]) +', text)
        
        # Look for URLs at the bottom
        url_map = {}
        ref_block = re.findall(r'\[(\d+)\][:\s]+(https?://\S+)', text)
        for idx, url in ref_block:
            url_map[idx] = url
            
        for seg in segments:
            found_urls = re.findall(r'https?://[^\s)\]]+', seg)
            found_refs = re.findall(r'\[(\d+)\]', seg)
            
            citations = []
            for url in found_urls:
                citations.append(Citation(url=url, index=0))
            for ref in found_refs:
                if ref in url_map:
                    citations.append(Citation(url=url_map[ref], index=int(ref)))
            
            if citations:
                # Clean segment of citation markers for cleaner similarity analysis
                clean_seg = re.sub(r'\[\d+\]|https?://\S+', '', seg).strip()
                if clean_seg:
                    claims.append(Claim(text=clean_seg, citations=citations))
        
        return claims

    async def audit(self, query: str, response_text: str) -> AuditResult:
        """Full audit loop: Extract -> Fetch -> Verify -> Score."""
        claims = self.parse_citations(response_text)
        
        if not claims:
            return AuditResult(query, response_text, 0.0, [])

        # Unique URLs to fetch
        urls = list(set(c.url for cl in claims for c in cl.citations))
        source_data = await self.scraper.fetch_batch(urls)
        
        total_score = 0.0
        for claim in claims:
            # Aggregate scores if multiple citations exist
            scores = []
            contexts = []
            for citation in claim.citations:
                source_text = source_data.get(citation.url, "")
                score = SimilarityEngine.get_score(claim.text, source_text)
                scores.append(score)
                citation.status = "Verified" if score > 0.7 else "Low Confidence"
                contexts.append(source_text[:500]) # Sample for diff
            
            claim.grounding_score = max(scores) if scores else 0.0
            total_score += claim.grounding_score
            
            if claim.grounding_score > 0.75:
                claim.status = GroundingLevel.VERIFIED
            elif claim.grounding_score > 0.4:
                claim.status = GroundingLevel.PARTIAL
            else:
                claim.status = GroundingLevel.HALLUCINATION
            
            claim.diff_html = SimilarityEngine.generate_diff(claim.text, "\n".join(contexts))

        avg_score = (total_score / len(claims)) * 100 if claims else 0.0
        
        return AuditResult(
            query=query,
            llm_response=response_text,
            overall_score=avg_score,
            claims=claims
        )
