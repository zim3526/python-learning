# 演示：相对路径是相对于"你站在哪个目录"，不是"脚本在哪个目录"
# 这个脚本在 day05 里，但它写的文件会落在"当前工作目录"

import os

print("=" * 55)
print("这个脚本自己在哪里：")
print(f"  os.getcwd()  当前工作目录 = {os.getcwd()}")
print(f"  __file__     脚本文件路径 = {__file__}")
print("=" * 55)

with open("demo_output.txt", "w", encoding="utf-8") as f:
    f.write("这个文件会被创建在：当前工作目录\n")

print()
print("文件已写入 demo_output.txt")
print(f"它实际落在：{os.path.abspath('demo_output.txt')}")
