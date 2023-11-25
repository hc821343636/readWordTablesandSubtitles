from docx import Document


def read_first_level_titles(doc):
    # 初始化标题列表
    first_level_titles = []
    first_level_titles_index = []

    for i in range(len(doc.paragraphs)):
        if doc.paragraphs[i].style.name.startswith('Heading 1'):
            # 获取一级标题文本
            title_text = doc.paragraphs[i].text
            first_level_titles.append(title_text)
            first_level_titles_index.append(i)

    return first_level_titles, first_level_titles_index


def read_titles(doc):
    all_titles_dict = {}
    _, first_level_titles_index = read_first_level_titles(doc)
    for i in first_level_titles_index:
        all_titles_dict.update(read_all_titles(doc, start=i))
    return all_titles_dict


def read_all_titles(doc=None, current_level=1, start=0, current_dict=None):
    if current_dict is None:
        current_dict = {}

    for i in range(start, len(doc.paragraphs)):
        style_name = doc.paragraphs[i].style.name
        if not style_name.startswith('Heading'):
            # 跳过非标题段落
            continue
        # print(style_name.split())
        level = int(style_name.split()[-1])

        if level == current_level:
            title_text = doc.paragraphs[i].text
            current_dict[title_text] = {}
        elif level == current_level + 1:
            current_dict[title_text] = read_all_titles(doc, level, i, current_dict[title_text])
        else:
            break

    return current_dict


if __name__ == "__main__":
    # 生成样本文档
    word_path = "sampleTitleDocument.docx"
    # create_sample_document(word_path)

    doc = Document(word_path)
    print(read_titles(doc))

    # 打印一级标题列表
