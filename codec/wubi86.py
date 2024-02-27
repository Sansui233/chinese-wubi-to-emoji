import os
import re

package_dir = os.path.dirname(__file__)


class wubi86:
    """
    86五笔词典
    """

    def __init__(self):
        """构造反查词典
        self.dict 格式：{汉字, [编码1, 编码2]}
        """
        with open(
            os.path.join(package_dir, "wubi86_danzi.txt"), "r", encoding="utf-8"
        ) as wubi86codec:
            print("[wubi86.py] 构造词典……")
            self.dict: dict[str, list[str]] = {}
            for line in wubi86codec.readlines():
                if line.strip() == "":
                    continue
                [word, codec] = line.strip().split("\t")
                if word not in self.dict:
                    self.dict[word] = [codec]
                else:
                    self.dict[word].append(codec)

            print("[wubi86.py] 词典共计{}个编码条目".format(len(self.dict)))

            # 非中文编码匹配 bool(pattern.search(input_str))
            self.pattern = re.compile(r"[^\u4e00-\u9fa5]")

    def lookup(self, word: str) -> list[str]:
        """
        反查编码，只能查纯中文字符串，英文与中英混合返回空。
        """
        # 非中文处理：返回空
        if bool(self.pattern.search(word)):
            print('[wubi86.py] "{}" 包含非中文字符'.format(word))
            return []

        # 中文处理
        match len(word):
            case 1:  # 单字则输出所有编码
                return self.dict[word]
            case 2:  # 双字
                return [
                    self.dict[word[0]][-1][:2]
                    + self.dict[word[1]][-1][:2]  # -1 选择全码，并切片
                ]
            case 3:  # 三字
                return [
                    self.dict[word[0]][-1][0]
                    + self.dict[word[1]][-1][0]
                    + self.dict[word[2]][-1][:2]
                ]
            case _ if len(word) >= 4:
                return [
                    self.dict[word[0]][-1][0]
                    + self.dict[word[1]][-1][0]
                    + self.dict[word[2]][-1][0]
                    + self.dict[word[-1]][-1][0]
                ]
            case _:
                raise Exception("[wubi86.py] 查询的汉字长度为0")
