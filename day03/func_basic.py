# 1. 定义 greet()，打印"你好，世界"，然后调用两次
def greet():
    print("你好，世界")

greet()
greet()
# 2. 定义 greet_person(name)，打印"你好，{name}"，传入你的名字
def greet_person(name):
    print(f"你好，{name}")

greet_person("梓明")
# 3. 定义 add(a, b)，用 return 返回两数之和，用变量接住结果再打印
def add(a,b):
    return a+b

num = add(3,4)
print(num)
# 4. 定义 is_even(n)，返回 True 或 False（判断是否偶数）
#    提示：return n % 2 == 0
def is_even(n):
    return n % 2 == 0

print(is_even(5))
print(is_even(4))
# 5. 定义 area_of_rect(width, height)，返回矩形面积
def area_of_rect(width,height):
    return width*height

area = area_of_rect(7,8)
print(area)
# 6. ⭐ 故意做这个实验：
#    定义 print_sum(a, b) 里面用 print(a+b)，不写 return
#    定义 return_sum(a, b) 里面用 return a+b
#    分别用变量接住结果并打印，观察区别
#    预期：print_sum 的结果是 None
def print_sum(a,b):
    print(a+b)

def return_sum(a,b):
    return a+b

result = print_sum(3,4)
print(result)
result2 = return_sum(3,4)
print(result2)