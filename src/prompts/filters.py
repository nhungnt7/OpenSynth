instruction_quality = """
You need to rate the quality of the question based on its clarity, specificity, and coherence. Additionally, you need to assess the difficulty level of understanding and interpreting the question based on its complexity, ambiguity, and the effort required to respond effectively.  

### The Rating Scale for question Quality:  
− **very poor**: The question is unclear, vague, or incoherent. It lacks essential information and context.  
− **poor**: The question is somewhat unclear or lacks important details. It requires significant clarification.  
− **average**: The question is moderately clear and specific. It may require some additional information for a complete understanding.  
− **good**: The question is clear, specific, and mostly well-formed. It provides sufficient context for understanding the user’s intent.  
− **excellent**: The question is very clear, specific, and well-articulated. It contains all the necessary information and context for providing a comprehensive response.  

### The Rating Scale for question Difficulty:  
− **very easy**: The question is simple, straightforward, and easy to interpret and respond to.  
− **easy**: The question is relatively simple and requires minimal effort to interpret and respond to.  
− **moderate**: The question has a reasonable level of complexity and requires a moderate effort to understand and respond to.  
− **difficult**: The question is complex or ambiguous and requires significant effort to interpret and respond to effectively.  
− **very difficult**: The question is highly complex or poorly defined, making it very challenging to interpret and respond to effectively.  

## User Question  
{question}

## Output Format  
<input_quality>very poor/poor/average/good/excellent</input_quality>
<input_difficulty>very easy/easy/moderate/difficult/very difficult</input_difficulty>
"""

response_quality = """
You need to assess the quality of a response provided to a given question. You will also be given a passage containing the relevant knowledge required to answer the question. Your evaluation should consider the accuracy, relevance, completeness, and clarity of the response in relation to the question and the knowledge provided.

The Rating Scale for Response Quality:
− very poor: The response is inaccurate, irrelevant, or incoherent. It fails to address the question or uses incorrect information from the provided knowledge.
− poor: The response partially addresses the question but contains inaccuracies, lacks relevance, or fails to use key information from the provided knowledge.
− average: The response is somewhat accurate and relevant but may miss key details or lack clarity. It demonstrates partial use of the provided knowledge.
− good: The response is accurate, relevant, and mostly complete. It uses the provided knowledge effectively and is mostly clear.
− excellent: The response is fully accurate, highly relevant, complete, and clearly articulated. It makes the best use of the provided knowledge to address the question comprehensively.

### Knowledge Passage
{knowledge}

### User Question
{question}

### Response
{response}

## Output Format
<output_quality>very poor/poor/average/good/excellent</output_quality>
"""