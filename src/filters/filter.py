import json
import os

# the following two rows Only use for testing
# from configs.config import set_config
# set_config()
from configs.config import settings

def filter_instruction(instruction, params=settings.CONF['filters']):
    instruction_quality = {'very poor': 0, 'poor': 1, 'average': 2, 'good': 3, 'excellent': 4}
    instruction_difficulty = {'very easy': 0, 'easy': 1, 'moderate': 2, 'difficult': 3, 'very difficult': 4}

    include = True
    for key, condition in params.items():
        if key == 'instruction_quality':
            if instruction_quality[instruction['instruction_quality']] < condition:
                include = False
                break
        elif key == 'instruction_difficulty':
            if instruction_difficulty[instruction['instruction_difficulty']] < condition:
                include = False
                break
        elif key == 'instruction_length':
            if instruction['instruction_length'] < condition:
                include = False
                break
        else:
            continue

    return include

def filter_responses(file_name, params=settings.CONF['filters']):

    """
    Filters entries in a JSONL file based on specified parameters.

    Args:
        filename (str): name of the JSONL file.
        params (dict): A dictionary of filtering parameters. Keys correspond to JSON fields, 
                       and values are either lists (for categorical fields) or tuples (for numeric ranges).
                       Example:
                       {
                           'instruction_quality': very poor/poor/average/good/excellent,
                           'instruction_difficulty': very easy/easy/moderate/difficult/very difficult,
                           'response_quality': very poor/poor/average/good/excellent,
                           'response_length_over_document': 0.15
                       }

    Returns:
        list: A list of filtered entries (dictionaries).
    """

    filtered_data = []
    instruction_quality = {'very poor': 0, 'poor': 1, 'average': 2, 'good': 3, 'excellent': 4}
    instruction_difficulty = {'very easy': 0, 'easy': 1, 'moderate': 2, 'difficult': 3, 'very difficult': 4}
    response_quality = {'very poor': 0, 'poor': 1, 'average': 2, 'good': 3, 'excellent': 4}

    responses_file = os.path.join(settings.CONF['data']['responses'], file_name)
    if not os.path.exists(responses_file):
        raise FileNotFoundError(f"File {responses_file} not found. No instructions met the filter criterias. Recommendation: Please consider lowering the filter thresholds or adjusting your prompt to better match the data. OR SET filter_instructions_first = FALSE in your config file  to continue")
    
    # Open and read the JSONL file
    with open(responses_file, 'r', encoding='utf-8') as file:
        for line in file:
            entry = json.loads(line.strip())

            # Check each parameter
            include = True
            for key, condition in params.items():
                if key == 'instruction_quality':
                    if instruction_quality[entry[key]] < condition:
                        include = False
                        break
                elif key == 'instruction_difficulty':
                    if instruction_difficulty[entry[key]] < condition:
                        include = False
                        break
                elif key == 'response_quality':
                    if response_quality[entry[key]] < condition:
                        include = False
                        break
                else:
                    if entry[key] < condition:
                        include = False
                        break

            if include:
                filtered_data.append(entry)
    # save to sft_data 
    sft_file = os.path.join(settings.CONF['data']['sft_data'], file_name)
    directory = os.path.dirname(sft_file)
    if not os.path.exists(directory):
        os.makedirs(directory)
            

    for filtered_sample in filtered_data:
        with open(sft_file, mode='a', encoding='utf-8') as file:
            json.dump(filtered_sample, file, ensure_ascii=False)
            file.write('\n') 

    return f"Processing Done. Please check your synthetic data in {sft_file}"
