import pandas as pd
from docx import Document


class readWord:
    def __init__(self, word_path):
        self.doc = Document(word_path)
        self.all_tables = self.read_all_tables_to_dataframe()
        '''for table in self.all_tables:
            print(table)'''
        print(len(self.all_tables))
        self.tablesindex = 0

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
            if self.doc.paragraphs[i].style.name.startswith('Heading 1'):
                # 获取一级标题文本
                title_text = self.doc.paragraphs[i].text
                first_level_titles.append(title_text)
                first_level_titles_index.append(i)

        return first_level_titles, first_level_titles_index

    def read_titles(self):
        all_titles_dict = {}
        first_level_titles, first_level_titles_index = self.read_first_level_titles()
        for first_title, i in zip(first_level_titles, first_level_titles_index):
            all_titles_dict[first_title] = self.read_all_titles(current_level=1, start=i)
        return all_titles_dict

    def read_all_titles(self, current_level, start):

        current_dict = {}

        for i in range(start + 1, len(self.doc.paragraphs)):
            style_name = self.doc.paragraphs[i].style.name
            #print(style_name)
            if not style_name.startswith('Heading'):
                # 跳过非标题段落
                continue
            # print(style_name.split())
            level = int(style_name.split()[-1])

            if level == current_level + 1-1+1:
                title_text = self.doc.paragraphs[i].text
                current_dict[title_text] = self.read_all_titles(level, i)
            elif level == current_level:
                break
        if current_dict=={}:
            current_dict=self.all_tables[self.tablesindex]
            self.tablesindex+=1
        return current_dict


if __name__ == "__main__":
    # 生成样本文档
    word_path = "sampleTitleDocument.docx"
    # create_sample_document(word_path)

    rd = readWord(word_path)
    print(rd.read_titles())

    # 打印一级标题列表
