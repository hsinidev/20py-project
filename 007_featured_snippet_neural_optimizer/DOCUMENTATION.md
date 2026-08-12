# DOCUMENTATION: Featured-Snippet Neural Optimizer

![Screenshot](asset/1.PNG)

Version: 1.0.0
Author: HSINI MOHAMED

## 1. Overview
The Featured-Snippet Neural Optimizer is a desktop application designed to restructure content for maximum visibility in AI search engine snippets (Gemini, Perplexity, GPT). It focuses on "Atomic Paragraph Deconstruction" to align content with preferred answer structures.

## 2. Technical Stack
- **GUI**: WxPython (Phoenix) with "Agency-Modern" theme.
- **NLP**: TextStat, NLTK (with regex-based offline fallbacks).
- **Export**: Semantic HTML5 Boilerplate.

## 3. Core Logic
1. **Atomic Deconstruction**: Sentences are broken down and re-evaluated for clarity and factual density.
2. **Preference Mapping**: 
   - **Gemini Mode**: Prioritizes step-by-step, structured lists.
   - **Perplexity Mode**: Prioritizes concise, fact-dense statements.
3. **GEO Confidence Score**: A composite metric (0-100) based on readability, entity density, and fact-count.

## 4. Key Metrics
- **Readability**: Calculated using Flesch-Kincaid Grade Level.
- **Entity Density**: Ratio of recognized entities to total word count.
- **Fact-Count**: Heuristic detection of specific factual claims.

## 5. Metadata
- **Project ID**: 7
- **Developer**: HSINI MOHAMED
