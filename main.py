import os, time
import sqlite3
import requests
import json

# select API and model 
#provider = "https://openrouter.ai/api/v1/chat/completions"
#api_key = os.environ.get('OPENROUTER_API_KEY')
#model_name = "meta-llama/llama-3-8b-instruct"

provider = "https://api.together.xyz/v1/chat/completions"
api_key = os.environ.get('TOGETHER_API_KEY')
model_name = "meta-llama/Llama-3-8b-chat-hf"

# Read the Jeopardy database
conn = sqlite3.connect("dbljeopardy.sqlite")
cursor = conn.cursor()
cursor.execute("""
    SELECT prompt.query, prompt.answer
    FROM prompt
    WHERE NOT EXISTS (
        SELECT 1
        FROM model_prompt
        WHERE model_prompt.prompt_id = prompt.prompt_id
        AND model_prompt.model_id = (SELECT model_id FROM model WHERE name = ?)
    )
""", (model_name,))
prompts = cursor.fetchall()
conn.close()

# main loop
correct_count = 0
headers = {"Authorization": f"Bearer {api_key}"}
for i, (query, answer) in enumerate(prompts):
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": query}],
#        "temperature": 0.3, 
#        "max_tokens": 100,
    }
    response = requests.post(provider, json=payload, headers=headers)
    resp = json.loads(response.text)
    while 'error' in resp:
        print(resp)
        time.sleep(1)
        resp = json.loads(requests.post(provider, json=payload, headers=headers).text)

    correct_answers = answer.split(";")
    if not 'choices' in resp: 
        print(i, False, correct_answers, "")
        continue
    model_answer = resp['choices'][0]['message']['content'].strip()
    is_correct = any(ca.lower() in model_answer.lower() for ca in correct_answers)

    if is_correct: correct_count += 1
#    if correct_count > 2: break # debug

    # V comment for quiet mode V
    print(i, is_correct, correct_answers, model_answer)

score = (correct_count / len(prompts)) * 100

print('\n---\n')

print(model_name)
print(correct_count, 'T')
print(len(prompts)-correct_count, 'F')
print(score, '%')
