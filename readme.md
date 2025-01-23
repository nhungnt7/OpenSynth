# Efficient and High-Quality Domain-Specific Synthetic Data Generation Pipeline

Your efficient and high-quality domain-specific synthetic data generation pipeline! This tool allows you to generate diverse questions, long-form responses, and high-quality synthetic data for your specific domain.

## Features:
- **Generate diverse and high-quality domain-specific questions and responses.**
- **Customizable pipeline to fit specific requirements for synthetic data generation.**

## Requirements

- Python 3.10
- OpenAI API Key (or OpenAISource with serving library support, e.g. vllm, sglang....)

## Installation and Setup

1. **Set up environment variables**:
   - Create a `.env` file in the root directory of the project and add your OpenAI API Key as follows:
     ```bash
     OPENAI_API_KEY="your-openai-api-key"
     ```
   - If you're using OpenAISource, refer to [VLLM Documentation](https://docs.vllm.ai/) to set up OpenAI serving. Modify `src/openai_calling/call_openai.py` according to your configuration.

2. **Install dependencies**:
   - Run the following command to install the required dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Configure the pipeline**:
   - Edit the settings in `config.yml` according to your needs. The configuration file provides options to customize the pipeline's behavior.

    #### Data Settings
   - `chunks`: Path to the folder containing data chunks. The data should be in the format: `{"id": id, "text": text}`.
     - Example: `"data/chunks"`
   - `instructions`: Path to the folder storing the temporary instruction data.
     - Example: `"data/instructions"`
   - `responses`: Path to the folder containing the temporary response data that corresponds to the instructions.
     - Example: `"data/responses"`
   - `sft_data`: Path to the folder where the final synthetic data will be saved.
     - Example: `"data/sft_data"`

   #### Domain and Language
   - `domain`: Define the domain of your data. This can be any domain (e.g., economic, healthcare, technology).
     - Example: `"economic"`
   - `output_language`: The language for the generated synthetic data. For example, Vietnamese or English.
     - Example: `"Vietnamese"`
   - `instruction_requirements`: Additional specifications for the content of instructions. Leave empty for default settings.
   - `response_requirements`: Additional specifications for the content of responses. Leave empty for default settings.

   #### Question and Chunk Settings
   - `number_questions_per_openai_call`: Defines the number of questions to generate per OpenAI API call for each question type.
     - Example: `1`
   - `number_questions_per_chunk`: Defines how many questions will be generated for each chunk of data. The total number of questions/chunks would be less than or equal to `number_questions_per_openai_call * number_questions_per_chunk`. A small number of questions per chunk (less than 10) is recommended for more variety in tasks.
     - Example: `2`

   ### Filter Settings
   These settings allow you to apply thresholds for filtering instructions and responses based on specific criteria.

    - `instruction_length`: Threshold for the minimum number of characters in an instruction.
        - Example: `10`

   - `instruction_quality`: Quality level of the instruction, with values:
     - `'very poor': 0`
     - `'poor': 1`
     - `'average': 2`
     - `'good': 3`
     - `'excellent': 4`
     - **Recommended**: `3` (Good).
   - `instruction_difficulty`: Difficulty level of the instruction, with values:
     - `'very easy': 0`
     - `'easy': 1`
     - `'moderate': 2`
     - `'difficult': 3`
     - `'very difficult': 4`
     - **Recommended**: `2` (Moderate).
   - `response_length`: Minimum number of characters required for a valid response.
     - Example: `10`
   - `response_length_over_document`: Threshold ratio of output length to the document length.
     - Example: `0`
   - `response_quality`: Quality level of the response, with values:
     - `'very poor': 0`
     - `'poor': 1`
     - `'average': 2`
     - `'good': 3`
     - `'excellent': 4`
     - **Recommended**: `3` (Good).

   - `filter_instructions_first`: Determines if instructions should be filtered before generating the responses.
     - Example: `True`

   ### Model and Batch Settings
   - `llm`: Specifies the model name to use for data generation. You can use a variant of GPT models, such as `gpt-4o-mini` or `gpt-4o`.
     - Example: `"gpt-4o-mini"`
   - `batch_size`: Defines the number of samples that will be synthesized at the same time during each batch.
     - Example: `5`

   By modifying these settings in the `config.yml` file, you can tailor the data generation pipeline to your specific domain and requirements.
4. **Run the pipeline**:
   - Execute the pipeline with the following command:
     ```bash
     python openai-magie-pipeline.py
     ```

5. **Override default configuration for experiments**:
   - If you'd like to run multiple experiments with a custom configuration, pass a different config file via the `--override_default_config` flag:
     ```bash
     python openai-magie-pipeline.py --override_default_config <path_to_your_custom_config.yml>
     ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

If you find this tool useful, don't forget to give me 1 star 🌟.
