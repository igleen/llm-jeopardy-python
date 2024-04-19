# llm-jeopardy-python

This is a jeopardy benchmark for LLM using api

Dataset and original benchmark by aigoopy
https://github.com/aigoopy/llm-jeopardy

## Usage
1. register at together.ai / openrouter.ai
2. get your api key https://api.together.xyz/settings/api-keys | https://openrouter.ai/keys
3. set global variable in your terminal
 - using default linux shell:`export TOGETHER_API_KEY=your_key`
 - or using fish shell: `set -Ux OPENROUTER_API_KEY your_key`

4. edit main.py:

model_name = "mistralai/Mistral-7B-Instruct-v0.2"

5. `python3 main.py`
