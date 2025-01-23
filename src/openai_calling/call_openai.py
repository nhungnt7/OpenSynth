import json
import os

from openai import OpenAI
from datetime import datetime
class OpenAIGenerator():
    
    def __init__(self, model = "gpt-4o-mini") -> None:
        """
         Initialize OpenAI.
        """
        self.client = OpenAI()
        self.model = model

    def call_openai(self, messages, **kwargs):
        res = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            temperature=0.4,
            stream=False,
            **kwargs
        )
        
        if res.choices:
            answer = res.choices[0].message.content
            usage = {
                "completion_tokens": res.usage.completion_tokens,
                "prompt_tokens": res.usage.prompt_tokens,
                "total_tokens": res.usage.total_tokens,
            }

            log_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "completion_tokens": usage["completion_tokens"],
                "prompt_tokens": usage["prompt_tokens"]
            }
            # Check if the 'logs' directory exists, if not, create it
            if not os.path.exists("logs"):
                os.makedirs("logs")

            with open("logs/openai_usages.jsonl", 'a') as f:
                json.dump(log_entry, f)
                f.write("\n")
            
            return answer
