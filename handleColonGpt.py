import re

from ltp import StnSplit

'''
处理冒号的并列关系
该代码可以将类似于：
“
网络信息管理员的目的：
（一）对网络设备定期检查，确保其正常运行；
（二）融合网络改进和扩展项目，以满足业务的不断增长的需求。”
这种句子，即符合以冒号作为一句话的最后一个字符，并且下面有中文括号的编号，如“（一），（二）”等的段落，变为：
“
网络信息管理员的目的是对网络设备定期检查，确保其正常运行；
网络信息管理员的目的是融合网络改进和扩展项目，以满足业务的不断增长的需求。
”
这种并列关系的句子供ltp代码识别

有一个潜在的问题是，如果：
第七条 设备维护主要包括：表单建立、指派人员、维修闭环等环节。
（一）表单建立。跟进反馈系统创建故障表单。
（二）指派人员。依照当前人员调度情况指派维修人员前往维护。
（三）维修闭环。业务结束对该次表单进行总结。
那么一个点会被识别为2句话

'''


def read_text(file_path):
    # 读取文本文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def write_text(file_path, content):
    # 写入处理后的文本到新文件
    with open(file_path, 'w', encoding='utf-8') as file:
        if isinstance(content, list):
            for item in content:
                file.write(item)
        else:
            file.write(content)


def process_text_ignore_extra_content(text):
    # 匹配标题
    """   title_match = re.search(r'第.*?】', text)
       if not title_match:
           return "标题格式不符合要求。"
       title = title_match.group(0)"""

    # 提取】和：之间的内容
    content_to_replace_match = re.search(r'^(.*?)：', text)
    if not content_to_replace_match:
        return "冒号之前的内容格式不符合要求。"
    content_to_replace = content_to_replace_match.group(1).strip()

    # 提取：之后的内容，直到遇到第一个编号（一）
    post_colon_content = re.search(r'：(.*?)（', text, re.DOTALL)
    if not post_colon_content:
        return "编号之前的内容格式不符合要求。"
    post_colon_content = post_colon_content.group(1).strip()

    # 替换编号部分
    processed_text = re.sub(r'（.*?）', content_to_replace + '是', text)

    # 移除：之后到第一个编号之间的所有内容
    processed_text = processed_text.replace(post_colon_content, '', 1)

    # 移除标题之前的内容和冒号
    processed_text = processed_text[processed_text.index('：') + 1:]
    print(StnSplit().split(processed_text))
    return StnSplit().split(processed_text)


# 示例用法
if __name__ == '__main__':
    file_path = "冒号测试.txt"  # 替换为实际的文件路径
    text = read_text(file_path)
    processed_text = process_text_ignore_extra_content(text)
    write_text(file_path.replace('.txt', '_processed.txt'), processed_text)
