scores = {"张三": 80, "李四": 90, "王五": 70, "赵六": 60}                  # ① 数据存在循环外面，不会被重置

while True:                    # ② 无限循环（靠 break 退出）
    print("===== 学生成绩管理系统 =====")
    print("1. 录入成绩")
    print("2. 查看全部成绩")
    print("3. 统计分析")
    print("4. 查询学生")
    print("5. 退出")
    print("==========================")

    choice = input("请选择（1-5）：")

    if choice == "1":
        name = input("请输入姓名：")   
        while True:
            try:
                score = int(input("请输入分数："))
                if 0 <= score <= 100:
                    break
                else:
                    print("分数必须在0到100之间")
            except ValueError:
                print("请重新输入分数")
        scores[name] = score
        
    elif choice == "2":
        if len(scores) == 0:
            print("暂无数据")
        else:
            for n,s in scores.items():
                print(f"{n}：{s}分")
        
    elif choice == "3":
        if len(scores) == 0:
            print("暂无数据")
        else:
            num = 0
            alist = []
            for b in scores.values():
                alist.append(b)
                if b >= 60:
                    num += 1
            print(f"总人数：{len(scores)}")
            print(f"总分：{sum(alist)}")
            print(f"平均分：{sum(alist)/num:.2f}")
            print(f"最高分：{max(alist)}")
            print(f"最低分：{min(alist)}")
            print(f"及格人数：{num}")
        
    elif choice == "4":
        query_name = input("请输入姓名：")
        if query_name in scores:
            print(f"分数为{scores[query_name]}")
        else:
            print("查无此人")
        
    elif choice == "5":
        print("再见！")
        break                  # ③ 跳出循环，程序结束
    else:
        print("无效选择，请重新输入")
