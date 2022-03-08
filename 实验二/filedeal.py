import os
import re
import sys

info = []
# filename = "./yq_in.txt"
filename = sys.argv[1]
f = open(filename, 'r')
line = f.readline()
while line:
    province = line[0:3]
    # 使用正则表达式取出一行里面的以制表符/空格/回车开头和结尾的中文字符（即城市名）
    matchObj1 = re.search(r'(?<=\s)[\u4e00-\u9fa5]*(?=\s)', line)
    # 取出一行里面的数字，即人数
    matchObj2 = re.search(r'\d+\.?\d*', line, re.U)
    city = matchObj1.group(0)
    num = matchObj2.group(0)
    # 构建一个字典列表来存储这些信息
    info.append({"province": province, "city": city, "num": num})
    line = f.readline()
f.close()

# path = './yq_out_03.txt'

# 给输出文件命名
path = filename.replace("in", "out")
# 如果有同名文件就删除
if os.path.exists(path):
    os.remove(path)

isOneLine = True
tmp = ""
# 逐行写入文件，借助tmp变量来实现一个省份下面跟着市这种结构
for i in info:
    f = open(path, 'a')
    if tmp != i['province']:
        if isOneLine:
            f.write(str(i['province']) + ':' + '\n')
            isOneLine = False
        else:
            f.write('\n' + str(i['province']) + ':' + '\n')
        tmp = i['province']
    f.write(str(i['city']) + '\t' + str(i['num']) + '\n')
    f.close()


