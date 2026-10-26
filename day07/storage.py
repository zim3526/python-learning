import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
DEFAULT_FILE = BASE_DIR / "scores.json"

def load_scores(filename=DEFAULT_FILE):
    try:
        with open(filename,"r",encoding= "utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

    except json.JSONDecodeError:
        print("数据文件损坏，将从空数据开始")
        return {}


def save_scores(scores,filename=DEFAULT_FILE):
    with open(filename,"w",encoding="utf-8") as fi:
        json.dump(scores, fi, ensure_ascii=False, indent=2)
