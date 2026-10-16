# 1. 在当前目录写一个 note.txt，写入三行文字
with open("note.txt","w",encoding="utf-8") as n:
    n.write("第一行\n")
    n.write("第二行\n")
    n.write("第三行\n")
# 2. 用 "a" 模式再追加一行
with open("note.txt","a",encoding="utf-8") as t:
    t.write("第四行\n")
# 3. 用 "r" 模式读出来，完整打印
with open("note.txt","r",encoding="utf-8") as x:
    li = x.read()
    print(li)
# 4. 用 for 循环逐行读，每行前面加序号
#    预期输出：
#    1: 第一行内容
#    2: 第二行内容
#    ...
with open("note.txt","r",encoding="utf-8") as b:
    num = 0
    for z in b:
        num += 1
        print(f"{num}：{z.strip()}")
# 5. 故意用 "r" 模式打开一个不存在的文件，看报什么错
with open("not.txt","r",encoding="utf-8") as m:
    j = m.read()
    print(j)