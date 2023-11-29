from py2neo import Graph, Node, Relationship

def create_tree(graph, data, parent=None):
    for key, value in data.items():
        node = Node("Chapter", name=key)
        graph.create(node)
        if parent is not None:
            relationship = Relationship(parent, "HAS_CHILD", node)
            graph.create(relationship)
        if isinstance(value, dict):
            create_tree(graph, value, node)

# 在此处替换为你的 Neo4j 数据库连接信息
uri = "bolt://localhost:7687"
user = "neo4j"
password = "12345678"

graph = Graph(uri, auth=(user, password))
graph.delete_all()
# 在此处替换为你的数据
data = {'第一章 总则': {'依据': {}, '目的': {}, '要求': {}}, '第二章 基本工作': {'第一节 设备管理': {'涉及硬件': {}, '流程实施': {}}, '第二节 设备维护': {'涉及硬件': {}, '流程实施': {}}, '第三节 网络流量监控': {'涉及硬件': {}, '流程实施': {}}}, '第五章 网络地址分配任务': {'第一节 目的和要求': {'主要目的': {}, '基本要求': {}}, '第二节 主要步骤与方法': {'核对库存': {}, '实地考察分配': {}, '汇总出入': {}}, '第三节 典型场景网络地址分配任务重点': {'图书馆网络地址分配任务重点': {}, '网吧网络地址分配任务重点': {}}}}
paper={}
paper['全文']=data


# 调用函数创建多叉树
create_tree(graph, paper)