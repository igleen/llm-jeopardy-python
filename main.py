import os
import sqlite3
from together import Together

# Initialize Together client
client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))
model_name = "mistralai/Mistral-7B-Instruct-v0.2"

# Connect to the Jeopardy database
conn = sqlite3.connect("dbljeopardy.sqlite")
cursor = conn.cursor()

# Fetch unprocessed prompts for the model
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

correct_count = 0
total_count = len(prompts)

for i, (query, answer) in enumerate(prompts):
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": query}]
    )

    model_answer = response.choices[0].message.content.strip()
    correct_answers = answer.split(";")
    is_correct = any(
        ca.lower() in model_answer.lower() for ca in correct_answers
    )
    if is_correct: correct_count += 1

#    if correct_count > 2: break # debug

    # V comment for quiet mode V
    print(i, is_correct, correct_answers, model_answer)

score = (correct_count / total_count) * 100

print('\n---\n')

print(model_name)
print(correct_count, 'T')
print(total_count-correct_count, 'F')
print(score, '%')
