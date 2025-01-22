import os
import argparse
import asyncio
from tqdm import tqdm 

async def main():
    total_files = get_relative_jsonl_paths(settings.CONF['data']['chunks'])
    for file in tqdm(total_files, desc="Processing files", unit="file"):
        print(f"Processing {file}")
        await synthesize_instruction(file)
        await synthesize_response(file)
        filter_responses(file)        

if __name__ == "__main__":
    # load hyper-params
    parser = argparse.ArgumentParser(description="Synthesize SFT Data")
    parser.add_argument(
        "--override_default_config",
        type=str,
        help="Path to the folder containing the configuration that overrides the default for each experiment name.",
        default=None,
    )
    args = parser.parse_args()

    from configs.config import set_config
    set_config(args)

    from configs.config import settings
    for key, value in vars(args).items():
        settings.CONF[key] = value

    from dotenv import load_dotenv
    load_dotenv(override=True)
    
    from src.instruction_generation.synthesize_instructions import synthesize_instruction
    from src.response_generation.synthesize_responses import synthesize_response
    from src.filters.filter import filter_responses
    from src.utils.load_data import get_relative_jsonl_paths

    asyncio.run(main())