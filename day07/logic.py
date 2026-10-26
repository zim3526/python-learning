def is_pass(score):
    """判断是否及格（>= 60）。"""
    return score >= 60


def calc_stats(scores):

    if not scores:
        return None
    
    data = list(scores.values())
    pass_count = sum(1 for s in data if is_pass(s))

    return {"count":len(scores), 
            "total":sum(data),
            "average":sum(data)/len(scores),
            "highest":max(data),
            "lowest":min(data), 
            "pass_count":pass_count}


def find_by_name(scores, name):
    """查找某个学生的成绩。找到返回分数，找不到返回 None。"""
    # 提示：用 scores.get(name) 或 in 判断
    return scores.get(name)