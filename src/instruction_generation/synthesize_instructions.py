import asyncio
import os
import json
from tqdm import tqdm

from src.openai_calling.call_openai import OpenAIGenerator
from src.filters.metrics import FilteringMetrics
from src.utils.load_data import load_jsonl, get_random_tasks
from src.utils.utils import remove_number_from_start
from src.prompts.instructions import INSTRUCTION_GENERATION, INSTRUCTION_TYPE, REQUIREMENTS
# The following two rows Only use for testing
# from configs.config import set_config
# set_config()
from configs.config import settings

async def process_chunk(id, content, openai_client, instructions_file, filtering_metrics, number_questions_per_chunk=settings.CONF['number_questions_per_chunk']):

    try:
        instructions = []
        existing_instruction_types = []
        for _ in range(number_questions_per_chunk):

            # Get a random instruction type
            while True:
                instruction_type = get_random_tasks(instruction_type=INSTRUCTION_TYPE)
                if instruction_type not in existing_instruction_types or len(existing_instruction_types) >= len(INSTRUCTION_TYPE.split('\n'))/2:
                    existing_instruction_types.append(instruction_type)
                    break

            messages = [
                {
                    "role": "user",
                    "content": INSTRUCTION_GENERATION.format(
                        instruction_requirements=settings.CONF['instruction_requirements'],
                        response_requirements=settings.CONF['response_requirements'],
                        domain=settings.CONF['domain'],
                        number_questions_per_openai_call=settings.CONF['number_questions_per_openai_call'],
                        content=content,
                        instruction_type=instruction_type,
                        requirements=REQUIREMENTS,
                        output_language=settings.CONF['output_language']
                    )
                }
            ]
            sample = openai_client.call_openai(messages)

            if sample.strip() != "":
                for line in sample.split('\n'):
                    line = line.strip()
                    if line != "" and line not in instructions:
                        instructions.append((remove_number_from_start(line), instruction_type))

        # Save the instructions to the file
        directory = os.path.dirname(instructions_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        for instruction in instructions:
            filters_threshold = await filtering_metrics.get_instruction_quality_and_difficulty(instruction[0])
            with open(instructions_file, mode='a', encoding='utf-8') as file:
                json.dump({
                    'id': id,
                    'document': content,
                    'instruction': instruction[0],
                    'instruction_type': instruction[1],
                    'instruction_length': filtering_metrics.get_input_length(instruction[0]),
                    'instruction_quality': filters_threshold[0],
                    'instruction_difficulty': filters_threshold[1]
                }, file, ensure_ascii=False)
                file.write('\n')  

    except Exception as e:
        print(f"Error: {e}")
        raise e

async def synthesize_instruction(file_name, batch_size=settings.CONF['batch_size']):

    openai_client = OpenAIGenerator(settings.CONF['llm'])
    filtering_metrics = FilteringMetrics()
    instructions_file = os.path.join(settings.CONF['data']['instrutions'], file_name)
    chunks_file = os.path.join(settings.CONF['data']['chunks'], file_name)
    
    processed_chunks = set()
    if os.path.exists(instructions_file):
        with open(instructions_file, mode='r', encoding='utf-8') as file:
            for line in file:
                entry = json.loads(line)
                processed_chunks.add(entry['id'])

    data = load_jsonl(chunks_file)
    tasks = []
    for line in data:
        if line['id'] not in processed_chunks:
            tasks.append(process_chunk(line['id'],line['text'], openai_client, instructions_file, filtering_metrics))

    for i in tqdm(range(0, len(tasks), batch_size), desc="Synthesizing instructions"):
        batch_tasks = tasks[i:i+batch_size]
        await asyncio.gather(*batch_tasks)

    print(f"Instructions have been saved to {instructions_file}")

if __name__ == "__main__":
    # asyncio.run(synthesize_sft(batch_size=5))
    from dotenv import load_dotenv
    load_dotenv(override=True)
    asyncio.run(synthesize_instruction(file_name='tmp/pretraining.jsonl'))