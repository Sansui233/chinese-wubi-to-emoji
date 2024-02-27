import argparse
import json
import os
import re

from codec.wubi86 import wubi86
from codec.wubi98 import wubi98

d_dict = "dict"
f_emoji = "emoji.txt"
f_emoji_wubi86 = "emoji_wubi86.txt"
f_emoji_wubi98 = "emoji_wubi98.txt"


def emojijson2txt():
    """
    清理源 json 数据。源 json 数据有点脏。
    1. 单个 emoji 的编码有重复。
    2. 编码中如果有空格，而有输入法是以空格分词的，去掉
    3. 编码中有非中文，有不少小众编码是定长的，且无中英混输规则，去掉
    4. 排除汉字描述过长的 emoji，因为没有人会打，还有的是格式错误
    5. 联想范围控制：对于重码率过高的词，只显示前 2 个 emoji，防止 emoji 刷屏
    """
    print("\n[Info] 清理 json 数据……")
    if not os.path.exists(d_dict):
        os.mkdir(d_dict)

    with open("emoji.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        freq_record: dict[str, int] = {}
        result: list[list[str]] = []

        with open(
            os.path.join(d_dict, f_emoji), "w", newline="", encoding="utf-8"
        ) as emoji_txt:
            print("[Info] 共 {} 个 emoji".format(len(data["content"])))

            for item in data["content"]:
                d = []  # 对于单个 emoji 的编码重复记录

                for alias in item["alias"]:
                    word = alias.strip()

                    # 验证 word 长度和编码是否有空格
                    if word == "" or len(word) > 8:
                        continue
                    parts = word.split(" ")
                    if len(parts) > 0:
                        word = "".join(parts)

                    # 验证是否有非中文字符
                    pattern = re.compile(r"[^\u4e00-\u9fa5]")
                    if bool(pattern.search(word)):
                        continue

                    if word not in d:
                        d.append(word)
                        if word in freq_record:
                            freq_record[word] += 1
                        else:
                            freq_record[word] = 1
                        result.append([word, item["emoji"]])

            # 写入数据
            count: dict[str, int] = {}  # 限制高频词写入条数
            for [word, emoji] in result:
                if freq_record[word] > 8:
                    if word not in count:
                        emoji_txt.write(word + "\t" + emoji + "\n")
                        count[word] = 1
                        print("[Info] {}: {} 频率偏高".format(word, freq_record[word]))
                    elif count[word] < 2:
                        emoji_txt.write(word + "\t" + emoji + "\n")
                        count[word] += 1
                    else:
                        pass
                else:
                    emoji_txt.write(word + "\t" + emoji + "\n")


def convert(codec_engine, output_path: str):
    count = 0
    with open(output_path, "w", newline="", encoding="utf-8") as output:
        with open(os.path.join(d_dict, f_emoji), "r", encoding="utf-8") as emoji_txt:
            try:
                for line in emoji_txt.readlines():
                    # 忽略空行
                    if line.strip() == "":
                        continue

                    [word, emoji] = line.strip().split("\t")
                    codecs: list[str] = codec_engine.lookup(word)

                    # 写入编码到 wubi98 的文件，同一个汉字词只写最短的码
                    if len(codecs) > 0:
                        output.write(codecs[0] + "\t" + emoji + "\n")
                        count += 1
            except Exception as e:
                print("\n\n\n[Error] 处理出错:", e)

    print("[Info] 共 {} 条 emoji".format(count))


def wubi86_function():
    print("\n[Info] 输出 emoji_wubi98 版...")
    wubi = wubi86()
    output_path = os.path.join(d_dict, f_emoji_wubi86)
    convert(wubi, output_path)


def wubi98_function():
    print("\n[Info] 输出 emoji_wubi98 版...")
    wubi = wubi98()
    output_path = os.path.join(d_dict, f_emoji_wubi98)
    convert(wubi, output_path)


def main():
    emojijson2txt()

    parser = argparse.ArgumentParser(description="Process some parameters.")
    parser.add_argument("--code", choices=["wubi86", "wubi98"], help="选择五笔版本")
    args = parser.parse_args()

    if args.code == "wubi86":
        wubi86_function()
    elif args.code == "wubi98":
        wubi98_function()
    else:
        print("Invalid code specified. Please use 'wubi86' or 'wubi98'.")


if __name__ == "__main__":
    main()
