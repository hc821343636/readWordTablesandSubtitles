import re

import pandas as pd
from docx import Document
from py2neo import Graph, Node, Relationship

class readWord:
    def __init__(self, word_path):
        self.titleDict = {
            '1级': 'Heading 1',
            '2级': 'Heading 2',
            '3级': 'Heading 3',
            '4级': 'Heading 4',
            '5级': 'Heading 5',
            '6级': 'Heading 6',
            '7级': 'Heading 7',
            '8级': 'Heading 8',
            '9级': 'Heading 9',
            '10级': 'Heading 10',
        }
        self.doc = Document(word_path)
        self.all_tables = self.read_all_tables_to_dataframe()
        '''for table in self.all_tables:
            print(table)'''
        # print(len(self.all_tables))
        self.tablesindex = 0
        self.visit = [False] * len(self.doc.paragraphs)

    def read_all_tables_to_dataframe(self):
        # 初始化一个空列表来存储所有表格的DataFrame
        all_tables = []

        # 遍历文档中的所有表格
        for table in self.doc.tables:
            # 将表格转换为DataFrame
            table_df = self.table_to_dataframe(table)
            all_tables.append(table_df)

        return all_tables

    def table_to_dataframe(self, table):
        # 初始化列名为空列表
        columns = []

        # 初始化一个空列表用于存储行数据
        rows_data = []

        # 遍历表格中的行
        for i, row in enumerate(table.rows):
            # 如果是第一行，将其作为列名
            if i == 0:
                columns = [cell.text.strip() for cell in row.cells]
            else:
                # 否则，将行数据添加到列表
                row_data = [cell.text.strip() for cell in row.cells]
                rows_data.append(row_data)

        # 一次性创建DataFrame
        return pd.DataFrame(rows_data, columns=columns)

    def read_first_level_titles(self):
        # 初始化标题列表
        first_level_titles = []
        first_level_titles_index = []

        for i in range(len(self.doc.paragraphs)):
            #print(self.doc.paragraphs[i].style.name)
            #print('$' * 100)
            curParagraph = self.doc.paragraphs[i]
            if curParagraph.style.name.startswith('Heading 1') or curParagraph.style.name == '1级':
                # 获取一级标题文本
                #print("get one title")
                title_text = self.extract_content_inside_brackets(curParagraph.text) or curParagraph.text
                first_level_titles.append(title_text)
                first_level_titles_index.append(i)

        return first_level_titles, first_level_titles_index

    def read_titles(self):
        all_titles_dict = {}
        first_level_titles, first_level_titles_index = self.read_first_level_titles()
        #print(first_level_titles)
        for first_title, i in zip(first_level_titles, first_level_titles_index):
            all_titles_dict[first_title] = self.read_all_titles(current_level=1, start=i)
        return all_titles_dict

    def read_all_titles(self, current_level, start, fillTable=False):
        current_dict = {}
        for i in range(start + 1, len(self.doc.paragraphs)):
            curParagraph = self.doc.paragraphs[i]  # 当前段落
            style_name = curParagraph.style.name  # 当前段落格式
            if style_name in self.titleDict.keys():
                style_name = self.titleDict[style_name]
            # print(style_name)
            # 如果需要进行填表，且当前表没有被填过，或者当前段落不是标题（标题 x或者 x级）
            if self.visit[i] or not style_name.startswith('Heading'):
                # 跳过非标题段落
                continue
            # print(style_name.split())
            level = int(style_name.split()[-1])

            if level > current_level:
                self.visit[i] = True
                title_text = self.extract_content_inside_brackets(curParagraph.text) or curParagraph.text
                current_dict[title_text] = self.read_all_titles(level, i)
            elif level == current_level:
                break
        if fillTable and len(current_dict) == 0:
            current_dict = self.all_tables[self.tablesindex]
            self.tablesindex += 1
        return current_dict

    def extract_content_inside_brackets(self, sentence):
        """
        提取中文方括号内的内容

        Parameters:
        sentence (str): 包含方括号的句子

        Returns:
        str: 方括号内的内容，如果找不到则返回 None
        """
        p = re.compile(r'[\[({【](.*?)[\])}】]', re.S)
        matches = re.findall(p, sentence)
        return matches[0] if len(matches) > 0 else None

    def format_data(self, data, indent=4):
        result = ""
        for key, value in data.items():
            result += " " * indent + f"{key}:\n"
            if isinstance(value, dict):
                result += self.format_data(value, indent + 4)
            else:
                result += " " * (indent + 4) + str(value) + "\n"
        return result

    def create_tree(self,graph, data, parent=None):
        for key, value in data.items():
            node = Node("Chapter", name=key)
            graph.create(node)
            if parent is not None:
                relationship = Relationship(parent, "HAS_CHILD", node)
                graph.create(relationship)
            if isinstance(value, dict):
                self.create_tree(graph, value, node)
    def load2neo4j(self,data,uri="bolt://localhost:7687",user="neo4j",password="12345678"):
        graph = Graph(uri, auth=(user, password))
        graph.delete_all()
        paper = {}
        paper['全文'] = data
        self.create_tree(graph=graph,data=paper)



if __name__ == "__main__":
    # 生成样本文档
    word_path = "格式模板样例-tl（公开）.docx"
    # create_sample_document(word_path)

    rd = readWord(word_path)
    res = rd.read_titles()
    print(rd.format_data(data=res))

    # 打印一级标题列表
