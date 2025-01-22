RESPONSES_GENERATION = """
You are an AI assistant designed to provide helpful, step-by-step guidance for the task of document understanding.
You are provided with a document in the field of {domain}. Your task is to generate the answer to the given question based on the provided document.

# The document is about:
{document}
# The question is:
{instruction}

**TYPES OF ANSWER:** The answer should be of the following type:
{instruction_type}

**REQUIREMENTS:** The answer should adhere to the following requirements:
{requirements} {response_requirements}
Output language: {output_language}
Your response:
"""

REQUIREMENTS = """
  -name: "Accurate and Complete Answer"
    description: "The answer should directly respond to the question and provide all necessary information based on the context. The answer have to based on the provided text. No external information is allowed."
  - name: "Clear and Understandable Language"
    description: "Both the question and answer should use clear, simple language to ensure they are easy to understand."
  - name: "Logical Consistency"
    description: "The answer should logically follow the question and maintain coherence, avoiding contradictions."
  - name: "Information Verification"
    description: "The information in the answer must be accurate and backed by the provided text, avoiding any false or speculative content."
  - name: "No Omission of Key Details"
    description: "Ensure that the answer includes all relevant details from the text that are necessary to clarify the question."
  - name: "**Clear Context**"
    description: "Ensure that the question provides a clear context without any reference to external information. PLEASE DO NOT INCLUDE ANY REFERENCES TO THE PROVIDED TEXT."
  - name: "Formatting"
    description: "The answer must be long and reasoning steps by steps. If the length of answer is sort, the quality of the answer would be low."
"""