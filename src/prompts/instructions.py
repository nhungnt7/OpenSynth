INSTRUCTION_GENERATION = """
You are an AI assistant designed to provide helpful, step-by-step guidance for the task of document understanding.
You are provided with a text in the field of {domain}. Your task is to generate {number_questions_per_openai_call} questions to capture the key content of the provided text.

# The text content:
{content}

# The questions must meet the following requirements:
**TYPES OF QUESTIONS:** The questions should be of the following type:
{instruction_type}

**REQUIREMENTS:** The questions should adhere to the following requirements:
{requirements} {instruction_requirements}

Output language: {output_language}
Your synthetic instructions:
"""

INSTRUCTION_TYPE = """
  - name: "Information seeking"
    description: "Users ask for specific information or facts about various topics."
  - name: "Reasoning"
    description: "Queries require logical thinking, problem−solving, or processing of complex ideas. Response need to Offer a step-by-step explanation of the reasoning process, providing intermediate steps and conclusions."
  - name: "Planning"
    description: "Users need assistance in creating plans or strategies for activities and projects. Response provide a structured, step-by-step plan, highlighting key objectives, actions, and deadlines if relevant."
  - name: "Editing"
    description: "Involves editing, rephrasing, proofreading, or other tasks related to the composition of general written content. Response Suggest revisions, offering explanations for changes made, focusing on clarity, grammar, and style improvements."
  - name: "Coding & Debugging"
    description: "Users seek help with writing, reviewing, or fixing code in programming. Response Provide clear and well-commented code solutions, or step-by-step debugging guidance, explaining each modification."
  - name: "Math"
    description: "Queries related to mathematical concepts, problems, and calculations. Response Show a step-by-step solution, explaining each part of the calculation or mathematical concept clearly."
  - name: "Role playing"
    description: "Users engage in scenarios requiring ChatGPT to adopt a character or persona. Repsonse Engage fully in character, explaining actions, motivations, and decisions in context."
  - name: "Data analysis"
    description: "Requests involve interpreting data, statistics, or performing analytical tasks. Offer a detailed, step-by-step analysis, explaining the methodology, results, and conclusions drawn from the data."
  - name: "Creative writing"
    description: "Users seek assistance with crafting stories, poems, or other creative texts. Response Provide creative suggestions, plot ideas, or sample text, with explanations for stylistic choices."
  - name: "Advice seeking"
    description: "Users ask for recommendations or guidance on various personal or professional issues. Response Offer thoughtful, well-explained advice, considering the user's context and providing practical suggestions."
  - name: "Brainstorming"
    description: "Involves generating ideas, creative thinking, or exploring possibilities. Response Generate a variety of ideas or solutions, clearly explaining the thought process behind each one."
"""

REQUIREMENTS = """
  - name: "Specific and Detailed Question"
    description: "The question should be clear, specific, and unambiguous to avoid confusion."
  - name: "Clear and Understandable Language"
    description: "The question should use clear, simple language to ensure they are easy to understand."
  - name: "Logical Consistency"
    description: "The question should be logically framed and coherent, without contradictions."
  - name: "No Omission of Key Details"
    description: "Ensure that the answer includes all relevant details from the text that are necessary to clarify the question."
  - name: "Avoid Time Ambiguity"
    description: "Ensure that the question does not contain any ambiguity regarding time (past, present, or future)."
  - name: "**Clear Context**"
    description: "Ensure that the question provides a clear context without any reference to external information. PLEASE DO NOT INCLUDE ANY REFERENCES TO THE PROVIDED TEXT."
  - name: "Formatting"
    description: "Please output only the questions, with each question on a new line."
"""