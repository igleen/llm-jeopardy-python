# llm-jeopardy-python

This is a jeopardy benchmark for LLM using api

Dataset and orginal benchmark by aigoopy
https://github.com/aigoopy/llm-jeopardy

## Usage
1. register at together.ai (its free)
2. get your api key https://api.together.xyz/settings/api-keys
3. set global variable TOGETHER_API_KEY
 - using default linux shell:`export TOGETHER_API_KEY=your_key`
 - using fish shell: `set -Ux TOGETHER_API_KEY your_key`

4. edit main.py:

model_name = "mistralai/Mistral-7B-Instruct-v0.2"

5. `python3 main.py`
