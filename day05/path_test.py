from pathlib import Path
import os

print(__file__) # 当前运行文件的地址
print(Path(__file__).parent) # 当前运行文件的上一节地址
print(os.getcwd()) # 当前所在地址

BASE_DIR = Path(__file__).parent
TEST_DIR = BASE_DIR / "test_data.txt"

with open(TEST_DIR, "w", encoding= "utf-8") as t:
    t.write("文本文档一份\n")


print(TEST_DIR) # 当前文件所在的绝对地址
