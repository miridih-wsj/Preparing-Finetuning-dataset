import csv
import json

input_csv = 'human-labelled-data-25.csv'
output_jsonl = 'dataset.jsonl'

with open(input_csv, newline='', encoding='utf-8') as csvfile, open(output_jsonl, 'w', encoding='utf-8') as jsonlfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # The columns are: system, user (input), assistant (output)
        system = row.get('system', '').strip()
        user = row.get('user (input)', '').strip()
        assistant = row.get('assistant (output)', '').strip()
        if not (system and user and assistant):
            continue  # skip incomplete rows
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant}
        ]
        jsonlfile.write(json.dumps({"messages": messages}, ensure_ascii=False) + '\n')
