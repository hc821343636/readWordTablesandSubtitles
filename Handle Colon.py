import re

import pandas as pd
from docx import Document
from py2neo import Graph, Node, Relationship
'''
处理冒号的并列关系
'''
def readtxt(filePath):
    # 打开文件
    with open(filePath, 'r') as file:
        # 读取文件内容
        content = file.read()
        # 将空格和换行删除
        cleaned_content = content.replace(" ", "").replace("\n", "")
        # 打印文件内容
        return cleaned_content
def extract_content(sentence):
    # 获取目标内容 即】...：的内容
    print(sentence)
    p = re.compile(r'[】](.*?)[：]', re.S)
    matches = re.findall(p, sentence)
    return matches[0]+'是' if len(matches) > 0 else None
def replace_numbered_markers(text, replacement):
    # 使用正则表达式进行替换
    # 将：（[一]）替换为是
    pattern = r'：（[一]）'
    replacement_text = "是"
    text = re.sub(pattern, replacement_text , text)
    # 将：（[二三四五六七八九十]）替换为xxxx是
    pattern = re.compile(r'（[二三四五六七八九十]+）')
    result = re.sub(pattern, replacement, text)
    return result

if __name__ == '__main__':
    filePath="冒号测试.txt"
    content=readtxt(filePath)
    for i in content:
        print(i)
    replacement=extract_content(content)
    print(replace_numbered_markers(content,replacement))
    print()

    # 使用正则表达式提取目标内容

