import re

from ltp import StnSplit

'''
处理冒号的并列关系
该代码可以将类似于：
“
第二条【目的】  网络信息管理员的目的：
（一）对网络设备定期检查，确保其正常运行；
（二）融合网络改进和扩展项目，以满足业务的不断增长的需求。”
这种句子，即符合以冒号作为一句话的最后一个字符，并且下面有中文括号的编号，如“（一），（二）”等的段落，变为：
“
第二条【目的】
网络信息管理员的目的是对网络设备定期检查，确保其正常运行；
网络信息管理员的目的是融合网络改进和扩展项目，以满足业务的不断增长的需求。
”
这种并列关系的句子供ltp代码识别
'''


def readTxt(filePath):
    # 打开文件
    with open(filePath, 'r') as file:
        # 读取文件内容
        content = file.read()
        # 将空格和换行删除
        cleaned_content = content.replace(" ", "").replace("\n", "")
        # 打印文件内容
        return cleaned_content


def writeTxt(filePath, res):
    with open(filePath, 'w') as file:
        file.write(res)

def extract_content(sentence):
    # 获取目标内容 即】...：的内容
    #print(sentence)
    p = re.compile(r'[】](.*?)[：]', re.S)
    matches = re.findall(p, sentence)
    return matches[0] + '是' if len(matches) > 0 else None


def replace_numbered_markers(text, replacement):
    # 使用正则表达式进行替换
    # 将：（[一]）替换为是
    pattern = r'：.*（[一]）'
    replacement_text = "是"
    text = re.sub(pattern, replacement_text, text)
    # 将：（[二三四五六七八九十]）替换为xxxx是
    pattern = re.compile(r'（[二三四五六七八九十]+）')

    return re.sub(pattern, replacement, text) if replacement is not None else text


def updateTxt(filePath, ):
    content = readTxt(filePath)
    lastIndex = 0
    sents = StnSplit().split(content)
    res = ""
    colonE = ':'
    colonC = '：'
    for sent in sents:
        if colonC in sent:
            sentsBeforeColon = ''.join(sents[lastIndex:sents.index(sent)])
            print(sentsBeforeColon)
            lastIndex = sents.index(sent)
            replacement = extract_content(sentsBeforeColon)
            res += replace_numbered_markers(sentsBeforeColon, replacement)
    sentsBeforeColon = ''.join(sents[lastIndex:])
    replacement = extract_content(sentsBeforeColon)
    res += replace_numbered_markers(sentsBeforeColon, replacement)
    print(res)
    writeTxt(filePath,res)



if __name__ == '__main__':
    filePath = "冒号测试.txt"

    updateTxt(filePath)

    # 使用正则表达式提取目标内容