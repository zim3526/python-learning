"""
主程序：只负责菜单和用户交互。
"""
from storage import load_scores, save_scores
from logic import calc_stats, find_by_name
from ai import generate_all_comments


def get_number(prompt, low, high):
    """通用输入校验。"""
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
        for name, score in scores.items():
            print(f"{name}：{score}分")
    else:
        print("暂无数据")


def show_stats(scores):
    """显示统计结果。"""
    stats = calc_stats(scores)
    if stats is None:
        print("暂无数据")
        return
    print(f"总人数：{stats['count']}")
    print(f"总分：{stats['total']}")
    print(f"平均分：{stats['average']:.2f}")
    print(f"最高分：{stats['highest']}")
    print(f"最低分：{stats['lowest']}")
    print(f"及格人数：{stats['pass_count']}")


def query_score(scores):
    """查询某个学生的成绩。"""
    query_name = input("姓名：")
    score = find_by_name(scores, query_name)
    if score is None:
        print("查无此人")
    else:
        print(f"分数为：{score}")


def delete_score(scores):
    del_name = input("姓名：")
    if del_name in scores:
        scores.pop(del_name)
        print("已删除")
    else:
        print("查无此人")


def show_ai_comments(scores):
    if not scores:
        print("暂无数据")
        return

    print(f"\n开始为 {len(scores)} 位学生生成评语，请稍候...\n")

    results = generate_all_comments(scores)

    if not results:
        print("生成失败，请检查网络或者API配置")
        return

    for name, info in results.items():
        print(f"\n===== {name} =====")
        if not info:
            print("(生成失败)")
            continue
        print(f"  等级：{info['等级']}")
        print(f"  评语：{info['评语']}")
        print(f"  建议：{info['建议']}")
def main():
    scores = load_scores()          # ← 用默认路径（storage 模块自己算好的）

    while True:
        print("===== 学生成绩管理系统 =====")
        print("1. 录入成绩")
        print("2. 查看全部成绩")
        print("3. 统计分析")
        print("4. 查询学生")
        print("5. 删除学生")
        print("6. AI 生成评语")
        print("7. 退出")
        print("==========================")

        choice = input("请选择（1-7）：")
        if choice == "1":
            input_score(scores)
            save_scores(scores)      # ← 也用默认路径
        elif choice == "2":
            show_all(scores)
        elif choice == "3":
            show_stats(scores)
        elif choice == "4":
            query_score(scores)
        elif choice == "5":
            delete_score(scores)
            save_scores(scores)
        elif choice == "6":
            show_ai_comments(scores)
        elif choice == "7":
            print("再见！")
            break
        else:
            print("无效选择，请重新输入")


if __name__ == "__main__":
    main()