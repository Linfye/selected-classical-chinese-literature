import json
import hashlib

class Shi:
    def __init__(self, title, author, paragraphs, theme):
        self.values = [title, author,paragraphs, theme, hashlib.md5("{}{}{}{}".format(title, author, paragraphs[0], paragraphs[1]).encode(encoding='utf-8')).hexdigest()]

class ShiManager:
    def __init__(self, shi_data_ls):
        self.shis = shi_data_ls

    def AddShi(self):
        themes = self.ReadData()[0]
        authors = self.ReadData()[1]
        # print(themes,authors)
        print("\n请输入诗名（无书名号）（若无，请输入无题）：")
        new_title = input()
        print("\n请输入作者（若无，请输入无名氏）：")
        new_author = input()
        if new_author not in authors:
            authors.append(new_author)
            with open("data.txt", "r+", encoding="utf-8") as f:
                first_line = f.readline()
                second_line = f.readline()
                f.seek(0)
                f.write(first_line)
                f.write(' '.join(authors))
        print("\n请一次性输入诗句，空格分隔")
        new_paragraphs = input().split(" ")
        print("\n请选择题材{}(输入new创建新题材)".format(themes))
        new_theme = input()
        if new_theme not in themes and new_theme != "new" :
            print("\n错误")
            return
        elif new_theme == "new":
            print("\n请输入新题材")
            new_theme = input()
            themes.append(new_theme)
            with open("data.txt", "r+", encoding="utf-8") as f:
                first_line = f.readline()
                second_line = f.readline()
                f.seek(0)
                f.write(' '.join(themes))
                f.write("\n")
                f.write(second_line)
        new_shi = Shi(new_title, new_author, new_paragraphs, new_theme)
        if new_shi.values[4] not in [self.shis[i][4] for i in range(len(self.shis))]:
            self.shis.append(new_shi.values)
            print("保存成功")
            return
        else:
            print("\n与现有诗重复")
            return

    def RemoveShi(self):
        print("\n请输入诗名（无书名号）（若无，请输入无题）：")
        the_title = input()
        print("\n请输入作者（若无，请输入无名氏）：")
        the_author = input()
        print("\n请输入诗的前两句，不加标点空格")
        the_paragraphs = input()
        the_shi_hash = hashlib.md5("{}{}{}".format(the_title, the_author, the_paragraphs).encode(encoding='utf-8')).hexdigest()
        for shi in self.shis:
            if shi[4] == the_shi_hash:
                self.shis.remove(shi)
                print("\n已删除")
                return
        print("\n查无此诗")
        return

    def UpdateShi(self):
        print("\n这个功能太麻烦了，我建议你先删除那首诗然后再添加")
    
    def ReadShi(self):
        temp_author = []
        temp_theme = []
        themes = self.ReadData()[0]
        print("\n1.按作者查询\n2.按题材查\n3.输出全部\n")
        read_choice = input()
        if read_choice == "1":
            print("\n请输入作者（若无，请输入无名氏）：")
            author = input()
            for shi in self.shis:
                if shi[1] == author:
                    temp_author.append(shi)
            if len(temp_author) == 0:
                print("无")
                return
            else:
                for i in temp_author:
                    print("-" * 60)
                    for j in range(3):
                        print("\n", i[j])
                    print("-" * 60)
                return
        if read_choice == "2":
            print("\n请输入题材）（{}）：".format(themes))
            theme = input()
            for shi in self.shis:
                if shi[3] == theme:
                    temp_theme.append(shi)
            if len(temp_theme) == 0:
                print("无")
                return
            else:
                for i in temp_theme:
                    print("-" * 60)
                    for j in range(3):
                        print("\n", i[j])
                    print("-" * 60)
                return
        if read_choice == "3":
            for i in self.shis:
                print("-" * 60)
                for j in range(3):
                    print("\n", i[j])
                print("-" * 60)
            return

    def ReadData(self):
        with open('data.txt',"r", encoding="utf-8") as f:
            themes = f.readline().split()
            authors = f.readline().split()
            return [themes, authors]

    
class ShiProcesser:
    def __init__(self):
        pass
    
    def ReadJson(self):
        shi_data_ls = []
        with open("./shi.json", "r", encoding='utf-8') as f:
            shi_data_dic = json.load(f)
            for i in shi_data_dic:
                i = list(i.values())
                shi_data_ls.append(i)
            # print(shi_data_ls[0][0])
        return shi_data_ls
    
    def SaveJson(self, shi_data_ls):
        temp_ls = []
        for i in range(len(shi_data_ls)):
            title = shi_data_ls[i][0]
            author = shi_data_ls[i][1]
            paragraphs = shi_data_ls[i][2]
            theme = shi_data_ls[i][3]
            shi_hash = shi_data_ls[i][4]
            formated_shi = {
                "title": title,
                "author": author,
                "paragraphs": paragraphs,
                "theme": theme,
                "hash": shi_hash
            }
            temp_ls.append(formated_shi)
        with open("./shi.json", "w", encoding="utf-8") as f:
           json.dump(temp_ls, f, ensure_ascii=False)

while True:
    if __name__ == "__main__":
        shi_data_ls = ShiProcesser().ReadJson()
        manager = ShiManager(shi_data_ls=shi_data_ls)
        ta_data = manager.ReadData()
        print("\n目前共收录{}个诗人的{}首诗\n".format(len(ta_data[1]), len(shi_data_ls)))
        print("请选择操作：\n1.阅读诗\n2.添加诗\n3.删除诗\n4.修改诗\n")
        choice = input()
        if choice == "1":
            manager.ReadShi()
        elif choice == "2":
            manager.AddShi()
        elif choice == "3":
            manager.RemoveShi()
        elif choice == "4":
            manager.UpdateShi()
        ShiProcesser().SaveJson(shi_data_ls=shi_data_ls)