import os
import openai
import google.generativeai as genai
import ollama
import asyncio
import time
import subprocess
import re

class PersonaEngine:
    def __init__(self):
        self.openai_key = None
        self.gemini_key = None

    def list_local_models(self):
        """Fetch models installed in local Ollama using subprocess (CMD)."""
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, shell=True, timeout=5)
            if result.returncode != 0:
                models_info = ollama.list()
                return [m['name'] for m in models_info['models']]
            
            lines = result.stdout.strip().split('\n')
            if len(lines) <= 1: return ["llama3"]
            
            models = []
            for line in lines[1:]:
                parts = re.split(r'\s+', line)
                if parts:
                    models.append(parts[0])
            return models
        except Exception as e:
            return ["llama3", "mistral", "phi3"]

    async def get_ollama_response(self, persona, prompt, model_name="llama3"):
        """Fetch response from local Ollama instance with extended timeout."""
        try:
            start = time.time()
            def sync_call():
                # Setting keep_alive to -1 to keep model in memory once loaded
                return ollama.chat(
                    model=model_name, 
                    messages=[
                        {'role': 'system', 'content': f"You are a {persona}. Be brief."},
                        {'role': 'user', 'content': prompt},
                    ],
                    options={'num_predict': 500} # Limit length for speed
                )
            
            # Extended timeout to 180 seconds for slow HDDs/GPUs
            response = await asyncio.wait_for(asyncio.to_thread(sync_call), timeout=180)
            return {
                "text": response['message']['content'],
                "latency": time.time() - start,
                "source": f"Ollama ({model_name})"
            }
        except asyncio.TimeoutError:
            return {"text": "Ollama Timeout: The local model is taking too long to load or generate. Try restarting Ollama or using a smaller model.", "latency": 0, "source": "Ollama"}
        except Exception as e:
            if "not found" in str(e).lower():
                return {"text": f"Ollama Error: Model '{model_name}' not found. Please run 'ollama pull {model_name}' in CMD.", "latency": 0, "source": "Ollama"}
            return {"text": f"Ollama Error: {str(e)}", "latency": 0, "source": "Ollama (Local)"}

    async def get_cloud_response(self, persona, prompt, provider="openai", api_key=None, model="gpt-4o"):
        """Fetch response from OpenAI or Gemini Cloud with timeout."""
        if not api_key:
            return {"text": f"{provider.upper()} API Key Missing.", "latency": 0, "source": f"{provider.upper()} (Cloud)"}
            
        try:
            start = time.time()
            if provider == "openai":
                def sync_openai():
                    client = openai.OpenAI(api_key=api_key)
                    return client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": f"You are a {persona}."},
                            {"role": "user", "content": prompt}
                        ],
                        timeout=20
                    )
                response = await asyncio.wait_for(asyncio.to_thread(sync_openai), timeout=25)
                text = response.choices[0].message.content
            else: # Gemini
                def sync_gemini():
                    genai.configure(api_key=api_key)
                    # Explicit model mapping for Gemini to avoid 404s
                    m_map = {
                        "gemini-1.5-pro": "gemini-1.5-pro",
                        "gemini-1.5-flash": "gemini-1.5-flash",
                        "gemini-pro": "gemini-pro"
                    }
                    m_name = m_map.get(model, "gemini-1.5-flash")
                    gemini_model = genai.GenerativeModel(m_name)
                    return gemini_model.generate_content(f"You are a {persona}. Answer this: {prompt}")
                
                response = await asyncio.wait_for(asyncio.to_thread(sync_gemini), timeout=25)
                text = response.text

            return {
                "text": text,
                "latency": time.time() - start,
                "source": f"{provider.upper()} (Cloud)"
            }
        except asyncio.TimeoutError:
            return {"text": f"{provider.upper()} Timeout: Cloud API took too long.", "latency": 0, "source": provider.upper()}
        except Exception as e:
            return {"text": f"Cloud Error ({provider}): {str(e)}", "latency": 0, "source": f"{provider.upper()} (Cloud)"}
