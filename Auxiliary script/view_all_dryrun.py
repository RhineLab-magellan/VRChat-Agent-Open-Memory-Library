import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/CherryStudio/Agent/UdonSharpAgent/memory/_curator_tools/a19-2_refine_dryrun.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
n = 0
for d in data:
    if d['grade'] == 'B':
        print(d['file'], d['type'])
        print('  reason:', d['reason'])
        print('  proposed:', d['proposed'])
        print()
        n += 1
print(f'--- Total B: {sum(1 for d in data if d["grade"] == "B")} ---')
