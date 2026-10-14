scores = [85, 92, 78, 90, 66, 100, 45]
def calc_total(scores):
    return sum(scores)

def calc_average(scores):
    return sum(scores) / len(scores)

def count_pass(scores):
    num = 0
    for i in scores:
        if i >= 60:
            num += 1
    return num

print(f"总分：{calc_total(scores)}")
print(f"平均分：{calc_average(scores):.2f}")
print(f"及格人数：{count_pass(scores)}")
