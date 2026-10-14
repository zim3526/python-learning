def get_number(prompt, low, high):
    """通用输入校验：反复询问，直到得到范围内的整数。"""
    while True:
        try:
            num = int(input(prompt))
            if low <= num <= high:
                return num
            print(f"请输入{low}到{high}之间的数字")
        except ValueError:
            print("请输入数字")


def input_score(scores):
    """录入一个学生的成绩。"""
    name = input("姓名：")
    score = get_number("请输入数字：", 0, 100)
    scores[name] = score


def show_all(scores):
    """显示所有成绩。"""
    if len(scores) != 0:
        for i,j in scores.items():
            print(f"{i}：{j}分")
    else:
        print("暂无数据")


def calc_stats(scores):
    """计算统计结果，返回一个字典。"""
    data = []
    num = 0
    for s in scores.values():
        data.append(s)
        if s >= 60:
            num += 1

    return {"count":len(scores), "total":sum(data),
             "average":sum(data)/len(scores),
             "highest":max(data), "lowest":min(data), 
             "pass_count":num}


def show_stats(scores):
    """显示统计结果。"""
    if len(scores) == 0:
        print("暂无数据")
    else:
        stats = calc_stats(scores)
        print(f"总人数：{stats['count']}")
        print(f"总分：{stats['total']}")
        print(f"平均分：{stats['average']:.2f}")
        print(f"最高分：{stats['highest']}")
        print(f"最低分：{stats['lowest']}")
        print(f"及格人数：{stats['pass_count']}")


def query_score(scores):
    """查询某个学生的成绩。"""
    query_name = input("姓名：")
    if query_name in scores:
        print(f"分数为：{scores[query_name]}")
    else:
        print("查无此人")


def main():
    """主循环：菜单 + 分发。"""
    scores = {}

    while True:
        print("===== 学生成绩管理系统 =====")
        print("1. 录入成绩")
        print("2. 查看全部成绩")
        print("3. 统计分析")
        print("4. 查询学生")
        print("5. 退出")
        print("==========================")

        choice = input("请选择（1-5）：")

        if choice == "1":
            input_score(scores)
        elif choice == "2":
            show_all(scores)
        elif choice == "3":
            show_stats(scores)
        elif choice == "4":
            query_score(scores)
        elif choice == "5":
            print("再见！")
            break
        else:
            print("无效选择，请重新输入")


if __name__ == "__main__":
    main()