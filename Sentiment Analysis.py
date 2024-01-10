from py2neo import Graph

# 连接到Neo4j数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"),name='mac0110')

# 编写Cypher查询，以获取关系名称
# 假设我们想要获取所有的关系名称
query = "MATCH ()-[r]->() RETURN TYPE(r) AS relationship_type"

# 执行查询
relationships = graph.run(query)

# 输出每个关系的类型
for relationship in relationships:
    print(relationship['relationship_type'])