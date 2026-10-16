# 1. import json
import json
# 2. 创建一个字典（4 个同学的成绩）
scores = {"张三":50, "李四":60, "王五":70, "吴六":80}
# 3. 用 json.dump 存进 scores.json，加上 ensure_ascii=False 和 indent=2
#    然后去 VS Code 里打开 scores.json 看看长什么样
with open("scores.json", "w", encoding="utf-8") as sco:
    json.dump(scores,sco,ensure_ascii=False,indent=2)
# 4. 用 json.load 读回来，打印内容和类型（type 应该是 dict）
with open("scores.json", "r", encoding="utf-8") as res:
    dict_scores = json.load(res)
print(dict_scores)
print(type(dict_scores))
# 5. 加一个新同学，再存一次，再读回来验证
# with open("scores.json", "a", encoding="utf-8") as dic:
#     json.dump({"陈七":90}, dic, ensure_ascii=False)      写错了，小鲸鱼你帮我看看
scores["陈七"] = 90
print(scores)
with open("scores.json", "w", encoding="utf-8") as sco2:
    json.dump(scores,sco2,ensure_ascii=False,indent=2)

with open("scores.json", "r", encoding="utf-8") as res2:
    dict_scores2 = json.load(res2)
print(dict_scores2)
print(type(dict_scores2))