from collections import defaultdict
from typing import List, Dict, Set, Tuple

def getwords(splitedWords: list[str], singleDep: dict):

    headList = singleDep['head']
    labelList = singleDep['label']
    splitedWords.insert(0, 'head')
    headList.insert(0, 'head')
    labelList.insert(0, 'head')
    if 'IOB' in labelList or 'DBL' in labelList:
        for i in range(1, len(splitedWords)):
            print(f'{splitedWords[i]}->{labelList[i]}->{splitedWords[headList[i]]}')
        return True
    return False

def find_element_positions(lst: List[str]) -> Dict[str, List[int]]:
    """
    获取列表中每个元素出现的位置下标的字典。

    Parameters:
        lst (List[str]): 输入的字符串列表。

    Returns:
        Dict[str, List[int]]: 字典，其中 key 为元素，value 为该元素在原始列表中出现的下标列表。
    """
    element_positions = defaultdict(list)

    for i, element in enumerate(lst):
        element_positions[element].append(i)

    return dict(element_positions)


def get_head_tuples(
        label: List[str],
        target_element: str,
        head: List[int]
) -> List[Tuple[int, int]]:
    """
    获取目标元素在 label 中的所有下标和对应的 head 值的 tuple 列表。

    Parameters:
        label (List[str]): 标签列表。
        target_element (str): 目标元素。
        head (List[int]): head 列表。

    Returns:
        List[Tuple[int, int]]: 包含每对 'target_element' 下标和对应的 'head' 值的 tuple 的列表。
    """
    result_tuples = []

    # 获取目标元素在label中的所有下标
    element_positions = find_element_positions(label)

    # 获取目标元素的下标列表
    target_positions = element_positions.get(target_element, [])

    # 创建tuple并添加到结果列表中
    for pos in target_positions:
        if 0 <= pos < len(head):
            result_tuples.append((pos, head[pos]-1))

    return result_tuples


def get_head_tuples_for_all_targets(
        label: List[str],
        targets: Set[str],
        head: List[int]
) -> Dict[str, List[Tuple[int, int]]]:
    """
    获取所有目标元素对应的 head 值的 tuple 列表的字典。

    Parameters:
        label (List[str]): 标签列表。
        targets (Set[str]): 所有可能的目标元素集合。
        head (List[int]): head 列表。

    Returns:
        Dict[str, List[Tuple[int, int]]]: 字典，其中每个键对应一个在 'label' 中出现的元素，
            对应的值是该元素在 'label' 中的下标和对应的 'head' 值的 tuple 列表。
    """
    result_dict = {}

    # 获取每个目标元素在label中的所有下标和对应的head值的tuple列表
    for target_element in targets:
        element_positions = find_element_positions(label)
        target_positions = element_positions.get(target_element, [])

        tuples_list = [(pos, head[pos]) for pos in target_positions if 0 <= pos < len(head)]
        result_dict[target_element] = tuples_list

    return result_dict
def process_semantic_roles(semantic_roles):
    """
    处理语义角色分析结果，提取三元组信息。

    Parameters:
        semantic_roles (list): 语义角色分析结果列表，每个元素为一个字典，包含 'predicate' 和 'arguments'。

    Returns:
        list: 三元组列表，每个元素为一个 tuple，包含 (subject, predicate, object)。
    """

    triples = []

    # 处理每个语义角色分析结果
    for i in range(len(semantic_roles) - 1):
        current_role = semantic_roles[i]
        next_role = semantic_roles[i + 1]
        current_dict={}
       # print('$'*200)
        #print(current_role['arguments'])
        #
        for current_item in current_role['arguments']:
            current_dict[current_item[0]]=current_item[1]
        next_dict = {}
        for next_item in next_role['arguments']:
            next_dict[next_item[0]]=next_item[1]
        # 提取当前和下一个 A0
        current_a0 = current_dict['A0']if 'A0' in current_dict.keys() else None
        if current_a0 is None:
            continue
        next_a0 =  next_dict['A0'] if 'A0' in next_dict.keys() else None
        if next_a0 is None:
            next_a0= next_dict['A1' ]if 'A1' in next_dict.keys() else None
        if next_a0 is None:
            next_a0 = next_dict['A2']if 'A2' in next_dict.keys() else None

        # 如果当前和下一个 A0 都存在，则添加三元组
        if current_a0 and next_a0:
            triples.append((f"{current_a0}", current_role['predicate'], f"{next_a0}"))

        ''' elif not next_a0 and current_a0:
            # 如果下一个没有 A0，但下一个有 arguments，则使用 arguments[0][1] 作为下一个的 A0
            next_a0 = next_role['arguments'][0][1]
            triples.append((f"{current_a0}", current_role['predicate'], f"{next_a0}"))'''

    return triples

# 示例数据
'''my_dict: Dict[str, List] = {'head': [5, 3, 1, 5, 0, 5, 5, 9, 7],
                            'label': ['SBV', 'LAD', 'COO', 'ADV', 'HED', 'RAD', 'VOB', 'LAD', 'COO']}
all_targets: Set[str] = set(my_dict['label'])  # 使用集合去除重复的元素

# 获取所有目标元素对应的head值的tuple列表的字典
result_dict: Dict[str, List[Tuple[int, int]]] = get_head_tuples_for_all_targets(
    my_dict['label'], all_targets, my_dict['head']
)

# 输出结果
print(result_dict)
'''