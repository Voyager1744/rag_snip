import yaml
from cli import ask

with open("eval/questions.yaml") as f:
    questions = yaml.safe_load(f)

for item in questions:
    print("="*80)
    print("Q:", item["q"])
    ans = ask(item["q"])
    print("A:", ans)
