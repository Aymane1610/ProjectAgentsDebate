import os
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMProvider:
    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
        
        if self.openai_key:
            self.openai_client = OpenAI(api_key=self.openai_key)

    def is_available(self) -> bool:
        return bool(self.gemini_key or self.openai_key)

    def generate(self, prompt: str, system_instruction: str = "", provider: str = "gemini") -> str:
        if provider == "gemini" and self.gemini_key:
            try:
                full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt
                response = self.gemini_model.generate_content(full_prompt)
                return response.text
            except Exception as e:
                print(f"Gemini error: {e}")
                if self.openai_key:
                    return self.generate(prompt, system_instruction, provider="openai")
                return f"Local RAG Fallback: {prompt[:100]}..."
        
        elif provider == "openai" and self.openai_key:
            try:
                messages = []
                if system_instruction:
                    messages.append({"role": "system", "content": system_instruction})
                messages.append({"role": "user", "content": prompt})
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"OpenAI error: {e}")
                return f"Local RAG Fallback: {prompt[:100]}..."
        
        return "LOCAL_MODE_ACTIVE"

# Singleton instance
llm_provider = LLMProvider()
