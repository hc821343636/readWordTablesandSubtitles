import csv

from ltp import LTP, StnSplit
from tqdm import tqdm

import getDepinfo

from typing import List, Tuple
from py2neo import Graph, Node, Relationship


# 分词 cws
# 词性标注 pos
# 命名实体识别ner
# 语义角色标注srl
# 依存句法分析 dep
# 语义依存分析(树) sdp
# 语义依存分析(图) sdpg

class AtoA:



    def __init__(self,ltp:LTP):
        self.COOnumber = 0
        self.ltp = ltp

    def srl_AtoA(self, sent):
        # 直接从句子提取消除并列关系的三元组
        result = self.ltp.pipeline(sent, tasks=["cws", "srl"])
        # print(result.srl)
        result = result.srl
        triples = []

        for frame in result:
            predicate = frame['predicate']
            a0, a1, cflag0, cflag1 = None, None, -1, -1
            for arg in frame['arguments']:
                if arg[0] == 'A0':
                    cflag0, a0 = self.getARG(arg[1], triples)
                elif arg[0] == 'A1':
                    cflag1, a1 = self.getARG(arg[1], triples)
            if a0 is not None and a1 is not None:
                triples.append((a0, predicate, a1, '_' if cflag0 == -1 else cflag0, '_' if cflag1 == -1 else cflag1))
        # print('###'*100)
        # print(triples)
        return triples

    def getTripleWithoutCoordination(self, tripleList: list[tuple[str, str, str]]):
        triples = []
        # 从已经提取好的三元组中消除并列关系并返回triple的list
        for tripleItem in tripleList:
            cflag0, a0 = self.getARG(tripleItem[0], triples)
            cflag1, a1 = self.getARG(tripleItem[2], triples)
            if a0 is not None and a1 is not None:
                triples.append(
                    (a0, tripleItem[1], a1, '_' if cflag0 == -1 else cflag0, '_' if cflag1 == -1 else cflag1))
        return triples

    def getARG(self, a: str, triples: list):
        conjunction, COOans = self.dosomething(s=a)
        if COOans is not None and conjunction is not None:
            unique_list = [(COOans_item[i], '_', conjunction, '_', self.COOnumber) for COOans_item in COOans for i in
                           range(2)]
            unique_list = self.remove_duplicates(unique_list)
            triples.extend(unique_list)
            self.COOnumber += 1
            return self.COOnumber - 1, conjunction
        return -1, a

    def dosomething(self, s: str):
        """
        将当前元组中并列关系的两两实体返回，并列连词返回
        Parameters:
            s: 为一个实体，A0或者A1

        Returns:
            conjunction: 并列连词，没有返回None
            COOans : 有并列的实体，没有返回None
        """
        # print(f's is {s}')
        result_s = self.ltp.pipeline(s, tasks=["cws", 'dep'])
        coo = getDepinfo.get_head_tuples(result_s.dep['label'], 'COO', result_s.dep['head'])
        lad = getDepinfo.get_head_tuples(result_s.dep['label'], 'LAD', result_s.dep['head'])
        """print("5" * 100)
        print(result_s.dep)
        print(result_s.cws)
        print(coo)
        print("5" * 100)"""
        if not coo:
            return None, None
        COOans = []
        # print(lad,"213"*100)
        conjunction = None if len(lad) == 0 else result_s.cws[lad[0][0]]
        for coo_item in coo:
            # print(result_s.cws[coo_item[0]], "  ", result_s.cws[coo_item[1]])
            COOans.append((result_s.cws[coo_item[0]], result_s.cws[coo_item[1]]))

        # print(result_s.cws[lad[0][0]], "右", result_s.cws[lad[0][1]])
        # print("5" * 100)
        return conjunction, COOans

    def remove_duplicates(self, original_list: List[Tuple]) -> List[Tuple]:
        """
        从元组列表中移除重复的元素。

        Parameters:
            original_list (List[Tuple[str, str, str]]): 原始的元组列表。

        Returns:
            List[Tuple[str, str, str]]: 移除重复元素后的元组列表。
        """
        # 转换为字符串形式的元组列表，并使用集合去重
        unique_set = set(str(item) for item in original_list)
        # print(unique_set)
        # 转回元组形式
        unique_list = [eval(item) for item in unique_set]

        return unique_list

    def sents2csv(self, csv_file_path: str, sents: List[str]):
        '''
        将进行了语义实体识别的句子得到的三元组写入csv
        Parameters:
            csv_file_path: csv地址
            sents: 句子们，即一篇txt中经过分句以后的内容

        Returns:
            None
        '''
        # csv_file_path = 'output.csv'

        # 打开CSV文件，如果文件不存在会被创建，如果已存在会被覆盖

        # 将tuple数据写入CSV文件

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            for sent in tqdm(sents, position=0):
                result = self.srl_AtoA(sent)
                # 创建CSV写入器
                csv_writer.writerows(result)

    def triple2csv(self, csv_file_path: str, tripleList: list):
        '''

        :param csv_file_path:
        :param tripleList:
        :return:None
        '''
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            for triple in tqdm(tripleList, position=0):
                #print(triple)
                csv_writer.writerow(triple)

    def getTxt(self, txt_file_path: str):
        '''
        获得txt文本
        Args:
            txt_file_path:

        Returns:

        '''
        # txt_file_path = '第一章.txt'

        # 打开文本文件
        with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
            # 读取文件内容
            file_content = txt_file.read()
            return file_content

    def assign_numbers(self, input_file, output_file, current_number):
        '''

        Args:
            input_file:
            output_file:
            current_number: 当前并列连词编号

        Returns:

        '''
        objects = {}  # 用于存储实物及其编号的字典
        current_number  # 当前编号553

        with open(input_file, 'r', newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='',
                                                                                 encoding='utf-8') as outfile:
            reader = csv.reader(infile)
            #print(reader)
            writer = csv.writer(outfile)

            for row in tqdm(reader, position=0):
                # 获取实物名称

                # 检查行的长度，如果不足5个字段则跳过
                if len(row) < 5:
                    continue
                # print(row)
                # 获取实物名称
                object1, relation, object2, number1, number2 = row[:5]

                # 处理第一列实物
                if object1 not in objects:
                    if number1 == '_':
                        objects[object1] = current_number
                        current_number += 1
                    else:
                        objects[object1] = number1

                # 处理第二列实物
                if object2 not in objects:
                    if number2 == '_':
                        objects[object2] = current_number
                        current_number += 1
                    else:
                        objects[object2] = number2

                # 更新行中的编号
                row[3] = objects[object1] if number1 == '_' else number1
                row[4] = objects[object2] if number2 == '_' else number2

                # 写入到输出文件
                writer.writerow(row)

    # 调用函数，传递输入和输出文件名
    def create_graph_from_csv(self, csv_file: str, uri: str, username: str, password: str, name: str,
                              deleteAll: bool = True):
        '''

        :param csv_file:  需要导入的csv
        :param uri: 图数据库地址
        :param username: 用户名
        :param password: 密码
        :param name: 数据库名称
        :param deleteAll: 是否在导入以前清除所有点 默认为True
        :return:
        '''
        graph = Graph(uri, auth=(username, password), name=name)
        if deleteAll:
            graph.delete_all()  # 清除neo4j中原有的结点等所有信息
        created_nodes = {}

        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            # 跳过表头
            next(csv_reader, None)

            for row in tqdm(csv_reader, position=0):
                sender_name, action_name, receiver_name, sender_number, receiver_number = row[:5]

                # 检查节点是否已存在，如果不存在则创建
                if action_name == '_':
                    nodetype = 'Conjunction'
                else:
                    nodetype = 'Person'
                sender_node = created_nodes.get(sender_number, Node('Person', name=sender_name, number=sender_number))
                receiver_node = created_nodes.get(receiver_number,
                                                  Node(nodetype, name=receiver_name, number=receiver_number))

                # 将节点添加到已创建的节点字典
                created_nodes[sender_number] = sender_node
                created_nodes[receiver_number] = receiver_node

                # 创建关系
                action_relationship = Relationship(sender_node, action_name, receiver_node)

                # 将节点和关系添加到图数据库
                graph.create(sender_node | receiver_node | action_relationship)


if __name__ == '__main__':
    ltp = LTP("base2")
    "change"
    """result = ltp.pipeline(["小王和小明合伙杀死了小张和小白"], tasks=["cws", "srl", 'ner', 'dep', 'pos'])
    print(result.srl)
    print(result.cws)
    print(result.pos)
    print(result.ner)
    print(result.dep)"""
    atoa = AtoA()
    txt_file_path = '../data/第一、二章'
    txt = atoa.getTxt(txt_file_path=txt_file_path + '.txt')
    sents = StnSplit().split(txt)
    # atoa.getCsv(csv_file_path=f'{txt_file_path}hchchchch.csv', sents=sents)
    # atoa.assign_numbers(f'{txt_file_path}hchchchch.csv', 'output_file.csv')

    for sent in sents:
        # print(sent)
        result = ltp.pipeline(sent, tasks=["cws", "srl", 'ner', 'dep', 'pos'])
        # print(f'语义角色分析:{result.srl}')
        res = getDepinfo.getwords(result.cws, result.dep)

        print(sent)
        result = ltp.pipeline(sent, tasks=["cws", "srl", 'ner', 'dep', 'pos'])
        print(f'语义角色分析:{result.srl}')
        # triples=atoa.srl_AtoA(sent)
