import os

import pandas as pd
from py2neo import Graph, Relationship, Node


def read_csv_file(file_path: str) -> pd.DataFrame:
    """读取CSV文件并返回一个DataFrame对象。"""
    return pd.read_csv(file_path)


def import_entities(graph: Graph, entity_folder: str) -> None:
    """导入实体到Neo4j数据库。"""
    # 假设entity_folder中包含了多个CSV文件，每个文件对应一个工作表
    for csv_file in os.listdir(entity_folder):
        if csv_file.endswith('.csv'):
            df = read_csv_file(os.path.join(entity_folder, csv_file))
            sheet_name = os.path.splitext(csv_file)[0]
            for _, row in df.iterrows():
                properties = dict(row)
                name = properties.pop('名称')
                node = Node(sheet_name, name=name, **properties)
                graph.create(node)


def import_relationships(graph: Graph, relationship_folder: str) -> None:
    """导入关系到Neo4j数据库。"""
    # 同上，假设relationship_folder中包含了多个CSV文件
    for csv_file in os.listdir(relationship_folder):
        if csv_file.endswith('.csv'):
            df = read_csv_file(os.path.join(relationship_folder, csv_file))
            sheet_name = os.path.splitext(csv_file)[0]
            for _, row in df.iterrows():
                end_node_name = row['头']
                start_node_name = row['尾']
                start_node = graph.nodes.match(name=start_node_name).first()
                end_node = graph.nodes.match(name=end_node_name).first()
                if start_node and end_node:
                    relation_properties = dict(row[3:])
                    relation = Relationship(start_node, sheet_name, end_node, **relation_properties)
                    graph.create(relation)


if __name__ == '__main__':
    graph = Graph("neo4j://localhost:7687", auth=("neo4j", "12345678"))
    graph.delete_all()
    entity_folder = "./data/实体表删除第一sheet1"
    relationship_folder = './data/关系表删除第一sheet1'
    import_entities(graph, entity_folder)
    import_relationships(graph, relationship_folder)
