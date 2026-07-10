import json

with open('/Users/mdtariqueahamad/.gemini/antigravity-ide/brain/f7f56000-a164-4456-b4a1-7b34e46225a2/.system_generated/logs/transcript_full.jsonl', 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get('type') == 'PLANNER_RESPONSE':
                for tool in data.get('tool_calls', []):
                    if tool['name'] == 'write_to_file' and tool['args'].get('TargetFile', '').endswith('ui/index.html'):
                        code = tool['args']['CodeContent']
                        with open('/Users/mdtariqueahamad/Project/Password Manager/ui/index.html', 'w') as out:
                            out.write(code)
                        print("Recovered original ui/index.html")
                        exit(0)
        except Exception as e:
            pass

print("Not found")
