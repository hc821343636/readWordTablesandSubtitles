import pandas as pd
from py2neo import Graph, Relationship, Node


def read_excel_file(file_path: str) -> pd.ExcelFile:
    """读取Excel文件并返回一个ExcelFile对象。"""
    return pd.ExcelFile(file_path)


def import_entities(graph: Graph, entity_file: str) -> None:
    """导入实体到Neo4j数据库。"""
    xls = read_excel_file(entity_file)
    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)
        for _, row in df.iterrows():
            properties = dict(row)
            name = properties.pop('名称')
            node = Node(sheet_name, name=name, **properties)
            graph.create(node)


def import_relationships(graph: Graph, relationship_file: str) -> None:
    """导入关系到Neo4j数据库。"""
    xls = read_excel_file(relationship_file)
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(relationship_file, sheet_name=sheet_name)
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
    entity_file = './data/实体表删除第一sheet1.xlsx'
    relationship_file = './data/关系表删除第一sheet1.xlsx'
    import_entities(graph, entity_file)
    import_relationships(graph, relationship_file)
