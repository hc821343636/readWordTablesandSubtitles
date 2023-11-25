import pandas as pd
from docx import Document


def read_all_tables_to_dataframe(docx_file):
    doc = Document(docx_file)

    # 初始化一个空列表来存储所有表格的DataFrame
    all_tables = []

    # 遍历文档中的所有表格
    for table in doc.tables:
        # 将表格转换为DataFrame
        table_df = table_to_dataframe(table)
        all_tables.append(table_df)

    return all_tables


def table_to_dataframe(table):
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


if __name__ == "__main__":
    # 替换为你生成的Word文档路径

    docx_file = "sample_document.docx"

    # 打印DataFrame
    # print(dataframe_from_word)
    all_tables = read_all_tables_to_dataframe(docx_file)
    for i, table in enumerate(all_tables):
        print(f"Table {i + 1}:\n{table}\n")
