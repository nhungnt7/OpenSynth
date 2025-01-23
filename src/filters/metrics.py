import asyncio
import re

from src.prompts.filters import instruction_quality, response_quality
from src.openai_calling.call_openai import OpenAIGenerator

class FilteringMetrics():

    def __init__(self):
        self.openai_client = OpenAIGenerator()

    def get_input_length(self, input):
        return len(input)
    
    def get_ouput_length(self, output):
        return len(output)
    
    def get_ouput_length_ratio(self, output, document):
        return len(output) / len(document)
    
    async def get_instruction_quality_and_difficulty(self, input):
        messages = [
            {
                "role": "user",
                "content": instruction_quality.format(question=input)
            }
        ]
        response = self.openai_client.call_openai(messages)
        input_quality = re.search(r'<input_quality>(.*?)</input_quality>', response).group(1)
        if input_quality not in ['very poor', 'poor', 'average', 'good', 'excellent']:
            input_quality = 'average'
        input_difficulty = re.search(r'<input_difficulty>(.*?)</input_difficulty>', response).group(1)
        if input_difficulty not in ['very easy', 'easy', 'moderate', 'difficult', 'very difficult']:
            input_difficulty = 'moderate'
        return input_quality, input_difficulty
    
    async def get_response_quality(self, question, response, knowledge):
        messages = [
            {
                "role": "user",
                "content": response_quality.format(question=question, response=response, knowledge=knowledge)
            }
        ]
        response = self.openai_client.call_openai(messages)
        output_quality = re.search(r'<output_quality>(.*?)</output_quality>', response).group(1)
        if output_quality not in ['very poor', 'poor', 'average', 'good', 'excellent']:
            output_quality = 'average'
        return output_quality
