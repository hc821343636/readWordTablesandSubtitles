import re

from py2neo import Graph

# 将字符串类型的'[[探查:5~16GHz,130km],[监控:6~13GHz,130km]]'
# 转换为dict形式的{'探查': ['5~16GHz,130km'], '监控': ['6~13GHz,130km']}

# 去除最外层的方括号
graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"), name='mac0110')


def parse_to_dict(data_str):
    # 去除最外层的方括号
    data_str = data_str.strip("[]")

    # 分割字符串获取各个项
    items = re.split(r'\],\s*\[', data_str)

    # 解析每一项并存入字典
    result = {}
    for item in items:
        key, value = item.split(':')
        # 分割值部分并去除多余的空格
        values = [v.strip() for v in value.split(',')]
        result[key] = values

    return result


def quarry(query="MATCH (n) RETURN n"):
    records = graph.run(query)
    nodes_dict = {}
    # 遍历查询结果
    for record in records:
        # 获取节点
        node = record['n']
        # 提取节点的name属性作为字典的键
        node_name = node['name']
        # 如果name已存在于字典中，可以选择跳过或更新
        node_class = list(node.labels)[0] if node.labels else None
        # 提取其他属性并存入字典
        node_attributes = dict(node)
        for key, value in node_attributes.items():
            if value[0] == '[' and value[-1] == ']':
                node_attributes[key] = parse_to_dict(value)
        nodes_dict[node_name] = {
            'class': node_class,  # 使用转换后的标签
            **node_attributes  # 添加其他属性
        }
        # 打印结果
    ''' 
   for key, value in nodes_dict.items():
        print(f'键: {key}, 值: {value}')
    '''

    return nodes_dict


# 将[数字]～[数字][单位] 这种格式的数据提取出来 如5~16GHz  提取为 （5,16,GHz）
def extract_data(s):
    # 首先尝试匹配 [数字]~[数字][单位] 格式
    pattern_range = r'(\d+)~(\d+)(\D+)'
    match = re.match(pattern_range, s)
    if match:
        return match.groups()

    # 如果第一种格式不匹配，尝试匹配 [数字][单位] 格式
    pattern_single = r'(\d+)(\D+)'
    match = re.match(pattern_single, s)
    if match:
        return (0,) + match.groups()

    # 如果都不匹配，返回 None
    return None


#    将句子特征内容提取
def extract_variables(sentence):
    pattern = r'距(.+)位置发现一目标，频率范围为(.+)，我方确定其采用xx外设，(.+)可否对其进行(.+)\?'
    match = re.match(pattern, sentence)
    if match:
        return match.groups()
    else:
        return None


def doMyJob(sentence: str):
    res = extract_variables(sentence=sentence)
    if res is None:
        print("查询语句错误")
        return
    else:
        distance, frequency, group_name, method = res
        # print(distance, frequency, group_name, method)
        frequency_low, frequency_high, unit = extract_data(frequency)
        _, distance, _ = extract_data(distance)
        ans1 = quarryWeapon(group_name, method, frequency_high, frequency_low, distance)
        if ans1 is not None:
            for ans1_item in ans1:
                query = f"MATCH (m:`工具`{{name:'{ans1_item}'}}) --(n:`编制类型`) return n"
                res = quarry(query)
                for key, value in res.items():
                    print(f"能！使用{ans1_item},编制类型为{key}")
        else:
            choose2 = False
            # MATCH(n:`组别`) -[r]->(m:`组别`{name:'2组'}) RETURN n,TYPE(r) AS relationship_type
            query = f"MATCH(n:`组别`) -[r:`编制支援`]->(m:`组别`{{name:'{group_name}'}}) RETURN n"
            res = quarryGroupAndRelationship(query)
            print('$' * 100)
            print(res)
            if res is None:
                print("啥也干不成！")
            else:
                for group_name, _ in res.items():
                    ans2 = quarryWeapon(group_name, method, frequency_high, frequency_low, distance)  # 获得武器
                    if ans2 is not None:  # 可以支援：当前组别下存在武器可以攻击敌方
                        choose2 = True
                        for ans2_item in ans2:
                            query = f"MATCH (k:`组别`{{name:'{group_name}'}})--> (n:`编制类型`)-->(m:`工具`{{name:'{ans2_item}'}}) return n"
                            # 查询与当前武器存在相邻的关系的编制
                            res = quarry(query)
                            for key, value in res.items():
                                print(f"请求获取{group_name}下使用{ans2_item},编制类型为{key}")
            if choose2 is False:
                print("啥也干不成！")


def quarryGroupAndRelationship(query: str):
    records = graph.run(query)
    nodes_dict = {}

    for record in records:
        # 获取节点
        node = record['n']
        node_name = node['name']
        # print(node)
        node_class = list(node.labels)[0] if node.labels else None
        # 提取其他属性并存入字典
        node_attributes = dict(node)
        for key, value in node_attributes.items():
            if value[0] == '[' and value[-1] == ']':
                node_attributes[key] = parse_to_dict(value)
        nodes_dict[node_name] = {
            'class': node_class,  # 使用转换后的标签
            **node_attributes  # 添加其他属性
        }
    print(nodes_dict)
    return nodes_dict


def quarryWeapon(group_name: str, method: str, frequency_high: str, frequency_low: str, distance: str):
    ans = []
    query = f"match (m:`组别`{{name:'{group_name}'}}) --(n:`工具`)return n"
    nodes_dict = quarry(query)
    print('%' * 100)
    for key, value in nodes_dict.items():
        print(key, value)
        value_ability = value['能力']
        choose = True
        if method in value_ability.keys():  # 如果该武器有我需要的能力[探查/监控/阻碍] value={'阻碍': ['5~19GHz', '100km']}
            capacity = value_ability[method]  # capacity=['5~19GHz', '100km']
            for capacity_item in capacity:
                low, high, unit = extract_data(capacity_item)
                if unit == 'GHz' and int(low) <= int(frequency_low) and int(high) >= int(
                        frequency_high) or unit == 'km' and int(high) >= int(distance):
                    if unit == 'GHz':
                        print(
                            f"The {group_name}'s frequency band between {low}GHz and {high}GHz can {method} enemy's which frequency band between {frequency_low}GHz and {frequency_high}GHz")
                    else:
                        print(
                            f"The {group_name} is equipped with a range of {high}km o meet the enemy's range of {distance}km")
                else:
                    choose = False
            if choose is True:
                ans.append(key)
    return ans if len(ans) > 0 else None


if __name__ == '__main__':
    res = quarry()
    for key, value in res.items():
        print(key, value)
    # 示例字符串

    # 示例句子
    sentence = "距190km位置发现一目标，频率范围为6~16Ghz，我方确定其采用xx外设，2组可否对其进行探查?"

    # 提取变量
    doMyJob(sentence=sentence)
