import re

def remove_number_from_start(question):
    # Regular expression to match a number at the beginning followed by a dot and a space
    modified_question = re.sub(r'^\d+\.\s*', '', question)
    return modified_question
