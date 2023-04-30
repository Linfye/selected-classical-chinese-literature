import json
import hashlib

# 读取现存诗歌，将每首诗哈希值保存在一个列表里
def ReadExistJson():
    hash_list = []
    with open("./shi.json", "r", encoding="utf-8") as shi:
        exist_shi = json.load(shi)
    for i in exist_shi:
        hash_list.append(i["hash"])
    return hash_list

# 请求输入
def ReadInput(hash_list):
    print("请输入诗名（无书名号）（无请输入无题）：")
    title = input()
    print("请输入作者（无请输入无名氏）：")
    author = input()
    print("选择操作：\n1.逐句输入\n2.一次性输入")
    choice = input()
    paragaph = None
    paragaphs = []
    if choice == "1":
        print("请逐句输入（不加标点）（一个逗号算一句）（end结束）诗句:")
        while paragaph != "end":
            paragaph = input()
            paragaphs.append(paragaph)
        paragaphs.pop()
    elif choice == "2":
        print("请一次性输入诗句，空格分隔")
        paragaphs = input().split(" ")

    shi_hash = hashlib.md5("{}{}{}{}".format(title, author, paragaphs[0], paragaphs[1]).encode(encoding='utf-8')).hexdigest()
    f_paragraphs = []
    if len(paragaphs) % 2 == 0:
        for i in range(0, len(paragaphs), 2):
            f_paragraphs.append("{}，{}。".format(paragaphs[i], paragaphs[i+1]))
    elif len(paragaphs) % 2 == 1:
        paragaphs.append(" ")
        for i in range(0, len(paragaphs), 2):
            f_paragraphs.append("{}，{}。".format(paragaphs[i], paragaphs[i+1]))
        f_paragraphs[-1] = f_paragraphs[-1][0:-3] + "。"
    if shi_hash in hash_list:
        print("重复提交\n")
        return  "0"
    else:
        new_shi = {
            "title": title,
            "author": author,
            "paragraphs": f_paragraphs,
            "hash": shi_hash
        }
        return new_shi

# 保存JSON文件
def SaveJSON(new_shi):
    with open("./shi.json", "r", encoding='utf-8') as shi:
        shi_data = json.load(shi)
    shi_data.append(new_shi)

    with open("./shi.json", "w", encoding="utf-8") as f:
        json.dump(shi_data, f, ensure_ascii=False)
        print("保存成功\n")

while True:
    if __name__ == "__main__":
        hash_list = ReadExistJson()
        new_shi = ReadInput(hash_list=hash_list)
        if new_shi != "0":
            SaveJSON(new_shi=new_shi)