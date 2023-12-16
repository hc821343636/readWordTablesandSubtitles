import pandas as pd

def process_excel_file(file_path: str) -> dict:
    """
    处理 Excel 文件，创建嵌套字典结构。

    参数:
    file_path (str): Excel 文件的路径。

    返回:
    dict: 以行动为键，每个键下有多个要素，每个要素下有关键词列表的字典。
    """
    # 加载 Excel 文件
    df = pd.read_excel(file_path)

    # 初始化一个空字典来存储数据
    actions_dict = {}

    # 追踪当前行动的名称，用于处理合并单元格
    current_action = None

    # 遍历 DataFrame 的列
    for col in df.columns:
        if 'Unnamed' not in col:
            current_action = col
            actions_dict[current_action] = {}

        # 提取当前行动的要素和关键词
        element = df.iloc[0][col]
        if pd.notna(element):  # 检查要素名称是否非空
            keywords = df[col].dropna().tolist()[1:]  # 排除第一行（表头）
            actions_dict[current_action][element] = keywords

    return actions_dict

def main():
    """
    主函数，用于展示 process_excel_file 函数的用法。
    """
    file_path = 'data/行动要素关键词.xlsx'  # Excel 文件路径
    action_data = process_excel_file(file_path)
    print(action_data)

# 调用主函数
if __name__ == '__main__':

    main()
