import asyncio
import os
import json
from tqdm import tqdm
from src.openai_calling.call_openai import OpenAIGenerator
from src.filters.metrics import FilteringMetrics
from src.utils.load_data import load_jsonl, get_random_tasks
from src.utils.utils import remove_number_from_start
from src.prompts.instructions import INSTRUCTION_GENERATION, INSTRUCTION_TYPE, REQUIREMENTS
from configs.config import settings

async def process_chunk(
    id, content, openai_client, filtering_metrics, number_questions_per_chunk, output_language, instruction_requirements, response_requirements, domain, requirements
):
    try:
        instructions = []
        existing_instruction_types = set()
        max_instruction_types = len(INSTRUCTION_TYPE.split('\n')) // 2

        for _ in range(number_questions_per_chunk):
            while True:
                instruction_type = get_random_tasks(instruction_type=INSTRUCTION_TYPE)
                if instruction_type not in existing_instruction_types or len(existing_instruction_types) >= max_instruction_types:
                    existing_instruction_types.add(instruction_type)
                    break

            messages = [
                {
                    "role": "user",
                    "content": INSTRUCTION_GENERATION.format(
                        instruction_requirements=instruction_requirements,
                        response_requirements=response_requirements,
                        domain=domain,
                        number_questions_per_openai_call=settings.CONF['number_questions_per_openai_call'],
                        content=content,
                        instruction_type=instruction_type,
                        requirements=requirements,
                        output_language=output_language
                    )
                }
            ]
            sample = openai_client.call_openai(messages)

            if sample.strip():
                for line in filter(bool, map(str.strip, sample.split('\n'))):
                    instructions.append((remove_number_from_start(line), instruction_type))

        # Batch results for writing
        results = []
        for instruction, instruction_type in instructions:
            filters_threshold = await filtering_metrics.get_instruction_quality_and_difficulty(instruction)
            results.append({
                'id': id,
                'document': content,
                'instruction': instruction,
                'instruction_type': instruction_type,
                'instruction_length': filtering_metrics.get_input_length(instruction),
                'instruction_quality': filters_threshold[0],
                'instruction_difficulty': filters_threshold[1]
            })

        return results

    except Exception as e:
        print(f"Error processing chunk {id}: {e}")
        raise

async def synthesize_instruction(file_name, batch_size=settings.CONF['batch_size']):
    openai_client = OpenAIGenerator(settings.CONF['llm'])
    filtering_metrics = FilteringMetrics()
    instructions_file = os.path.join(settings.CONF['data']['instrutions'], file_name)
    chunks_file = os.path.join(settings.CONF['data']['chunks'], file_name)
    
    # Track processed chunks
    processed_chunks = set()
    if os.path.exists(instructions_file):
        with open(instructions_file, 'r', encoding='utf-8') as file:
            processed_chunks.update(json.loads(line)['id'] for line in file)

    # Load and filter data
    data = load_jsonl(chunks_file)
    tasks = [
        process_chunk(
            line['id'], line['text'], openai_client, filtering_metrics,
            number_questions_per_chunk=settings.CONF['number_questions_per_chunk'],
            output_language=settings.CONF['output_language'],
            instruction_requirements=settings.CONF['instruction_requirements'],
            response_requirements=settings.CONF['response_requirements'],
            domain=settings.CONF['domain'],
            requirements=REQUIREMENTS
        )
        for line in data if line['id'] not in processed_chunks
    ]

    # Process in batches
    results = []
    for i in tqdm(range(0, len(tasks), batch_size), desc="Synthesizing instructions"):
        batch_tasks = tasks[i:i+batch_size]
        batch_results = await asyncio.gather(*batch_tasks)
        for result in batch_results:
            results.extend(result)

    # Write all results to file at once
    os.makedirs(os.path.dirname(instructions_file), exist_ok=True)
    with open(instructions_file, 'a', encoding='utf-8') as file:
        for result in results:
            json.dump(result, file, ensure_ascii=False)
            file.write('\n')

    print(f"Instructions have been saved to {instructions_file}")
