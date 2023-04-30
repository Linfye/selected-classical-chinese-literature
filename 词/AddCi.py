import json
import hashlib

# 读取现存诗歌，将每首诗哈希值保存在一个列表里
def ReadExistJson():
    hash_list = []
    with open("./ci.json", "r", encoding="utf-8") as ci:
        exist_ci = json.load(ci)
    for i in exist_ci:
        hash_list.append(i["hash"])
    return hash_list

# 请求输入
def ReadInput(hash_list):
    print("请输入词名（无书名号）（如果有词牌名，请用·符号隔开词牌名和词名，无空格，词牌名在前）：")
    title = input()
    print("请输入作者：")
    author = input()
    paragaph = None
    paragaphs = []
    para_hashs = []

    print("请按词的第一句（不加标点）（一个逗号算一句）(检查重复)")
    para_hash = input()
    para_hashs.append(para_hash)
    print("请按词的第二句（不加标点）（一个逗号算一句）")
    para_hash = input()
    para_hashs.append(para_hash)
    ci_hash = hashlib.md5("{}{}{}{}".format(title, author, para_hashs[0], para_hashs[1]).encode(encoding='utf-8')).hexdigest()
    if ci_hash in hash_list:
        print("重复提交\n")
        return  "0"

    print("请按约定俗称的分隔输入词句，加上标点，尽量只用逗号和句号，一次输入两句或一句（重新输入）（输入end结束）")
    while paragaph != "end":
        paragaph = input()
        paragaphs.append(paragaph)
    paragaphs.pop()

    new_ci = {
        "title": title,
        "author": author,
        "paragraphs": paragaphs,
        "hash": ci_hash
    }
    return new_ci

# 保存JSON文件
def SaveJSON(new_ci):
    with open("./ci.json", "r", encoding='utf-8') as ci:
        ci_data = json.load(ci)
    ci_data.append(new_ci)

    with open("./ci.json", "w", encoding="utf-8") as f:
        json.dump(ci_data, f, ensure_ascii=False)
        print("保存成功\n")

while True:
    if __name__ == "__main__":
        hash_list = ReadExistJson()
        new_ci = ReadInput(hash_list=hash_list)
        if new_ci != "0":
            SaveJSON(new_ci=new_ci)