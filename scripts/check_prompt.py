import json

transcript_path = r'C:\Users\LENOVO\.gemini\antigravity\brain\7a36d160-d644-4de2-97b3-0ba64a8bc91c\.system_generated\logs\transcript_full.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if data.get('source') == 'USER_EXPLICIT' and 'Act as a Senior ML Dataset Engineer and Reproducibility Auditor' in data.get('content', ''):
            content = data.get('content', '')
            out_path = r'C:\Users\LENOVO\.gemini\antigravity\scratch\sdc-domain1-prototype\artifacts\prompt10.txt'
            with open(out_path, 'w', encoding='utf-8') as out_f:
                out_f.write(content)
            print("Found user prompt in full transcript, length:", len(content))
            break
