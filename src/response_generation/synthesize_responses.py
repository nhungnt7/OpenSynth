import asyncio
import os
import json
from tqdm import tqdm

from src.openai_calling.call_openai import OpenAIGenerator
from src.filters.metrics import FilteringMetrics
from src.utils.load_data import load_jsonl, get_random_tasks
from src.filters.filter import filter_instruction
from src.utils.utils import remove_number_from_start
from src.prompts.responses import RESPONSES_GENERATION, REQUIREMENTS
from configs.config import settings

async def process_chunk(
    id, instruction, instruction_type, document, openai_client, filtering_metrics, metadata
):
    try:
        messages = [
            {
                "role": "user",
                "content": RESPONSES_GENERATION.format(
                    instruction_requirements=settings.CONF['instruction_requirements'],
                    instruction_type=instruction_type,
                    response_requirements=settings.CONF['response_requirements'],
                    domain=settings.CONF['domain'],
                    document=document,
                    instruction=instruction,
                    requirements=REQUIREMENTS,
                    output_language=settings.CONF['output_language']
                )
            }
        ]
        response = openai_client.call_openai(messages)

        if response.strip():
            filters_threshold = await filtering_metrics.get_response_quality(
                instruction, response, document
            )
            return {
                'id': id,
                'document': document,
                'instruction': instruction,
                'instruction_type': instruction_type,
                'instruction_length': metadata['instruction_length'],
                'instruction_quality': metadata['instruction_quality'],
                'instruction_difficulty': metadata['instruction_difficulty'],
                'response_length': filtering_metrics.get_ouput_length(response),
                'response_quality': filters_threshold,
                'response_length_over_document': filtering_metrics.get_ouput_length_ratio(response, document),
                'response': response
            }
    except Exception as e:
        print(f"Error processing chunk {id}: {e}")
        return None

async def synthesize_response(file_name, batch_size=settings.CONF['batch_size']):
    openai_client = OpenAIGenerator(settings.CONF['llm'])
    filtering_metrics = FilteringMetrics()
    instructions_file = os.path.join(settings.CONF['data']['instrutions'], file_name)
    responses_file = os.path.join(settings.CONF['data']['responses'], file_name)

    # Track processed chunks
    processed_chunks = set()
    if os.path.exists(responses_file):
        with open(responses_file, mode='r', encoding='utf-8') as file:
            processed_chunks.update(json.loads(line)['id'] for line in file)

    # Load and filter data
    data = load_jsonl(instructions_file)
    tasks = [
        process_chunk(
            line['id'], line['instruction'], line['instruction_type'], line['document'],
            openai_client, filtering_metrics, metadata=line
        )
        for line in data if line['id'] not in processed_chunks and filter_instruction(line)
    ]

    # Process tasks in batches
    results = []
    for i in tqdm(range(0, len(tasks), batch_size), desc="Synthesizing responses"):
        batch_tasks = tasks[i:i+batch_size]
        batch_results = await asyncio.gather(*batch_tasks)
        results.extend(filter(None, batch_results))  # Filter out any None results

    # Batch write results to the file
    os.makedirs(os.path.dirname(responses_file), exist_ok=True)
    with open(responses_file, mode='a', encoding='utf-8') as file:
        for result in results:
            json.dump(result, file, ensure_ascii=False)
            file.write('\n')

    print(f"Responses have been saved to {responses_file}")
