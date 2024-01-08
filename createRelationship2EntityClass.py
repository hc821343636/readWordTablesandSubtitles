import pandas as pd
from py2neo import Graph, Relationship, Node

# 连接到 Neo4j 数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"),name="relationship-entityclass")
graph.delete_all()
# 读取 Excel 文件
excel_file = './data/关系表sheet1.xlsx'  # 替换为您的 Excel 文件路径
df = pd.read_excel(excel_file)

# 遍历 DataFrame 并创建图结构
for index, row in df.iterrows():
    # 创建节点
    node1 = Node("Entity", name=row['头'])
    node2 = Node("Entity", name=row['尾'])

    # 添加节点到图中（如果它们还不存在）
    graph.merge(node1, "Entity", "name")
    graph.merge(node2, "Entity", "name")
    relation_properties = dict(row[3:])

    # 创建关系
    relationship = Relationship(node1, row['关系名'], node2,**relation_properties)
    # 添加关系到图中
    graph.merge(relationship)