import os
import re

package_dir = os.path.dirname(__file__)


class wubi98:
    """
    98五笔词典
    """

    def __init__(self):
        """构造反查词典
        self.dict 格式：{汉字, [编码1, 编码2]}
        """
        with open(
            os.path.join(package_dir, "wubi98_danzi.txt"), "r", encoding="utf-16le"
        ) as wubi98codec:
            print("[wubi98.py] 构造词典……")
            self.dict: dict[str, list[str]] = {}
            for line in wubi98codec.readlines():
                parts = line.strip().split(" ")
                for char in parts[1:]:
                    if char not in self.dict:
                        self.dict[char] = [parts[0]]
                    else:
                        self.dict[char].append(parts[0])

            print("[wubi98.py] 词典共计{}个编码条目".format(len(self.dict)))

            # 非中文编码匹配 bool(pattern.search(input_str))
            self.pattern = re.compile(r"[^\u4e00-\u9fa5]")

    def lookup(self, word: str) -> list[str]:
        """
        反查编码，只能查纯中文字符串，英文与中英混合返回空。
        """
        # 非中文处理：返回空
        if bool(self.pattern.search(word)):
            print('[wubi98.py] "{}" 包含非中文字符'.format(word))
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
                raise Exception("[wubi98.py] 查询的汉字长度为0")
