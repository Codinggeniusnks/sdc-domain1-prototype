import json

transcript_path = r"C:\Users\LENOVO\.gemini\antigravity\brain\7a36d160-d644-4de2-97b3-0ba64a8bc91c\.system_generated\logs\transcript_full.jsonl"
output_path = r"C:\Users\LENOVO\.gemini\antigravity\scratch\sdc-domain1-prototype\artifacts\user_prompt_12b.txt"

with open(transcript_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

user_inputs = []
for line in lines:
    try:
        data = json.loads(line)
        if data.get("type") == "USER_INPUT":
            user_inputs.append(data.get("content", ""))
    except Exception as e:
        pass

if user_inputs:
    last_prompt = user_inputs[-1]
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(last_prompt)
    print(f"Extracted last prompt: {len(last_prompt)} chars.")
else:
    print("No USER_INPUT found.")
