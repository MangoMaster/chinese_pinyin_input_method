# 拼音输入法

## 作者

魏家栋，计72班，学号2017011445

## 运行环境

Python3

## 使用方法

通过bin文件夹下的脚本运行：
```sh
cd ./bin
chmod +x ./pinyin.sh
./pinyin.sh input.txt output.txt
```
或者通过Python源文件运行：
```sh
cd ./src/word2
python3 ./pinyin.py input.txt output.txt
```
支持命令行形式提供输入文件名和输出文件名并运行程序，如上面的命令那样。也支持交互模式运行程序，如直接运行`pinyin.sh`或者`python3 pinyin.py`。

## 目录层次

- bin文件夹：运行程序的脚本。
- doc文件夹：程序[文档](./doc/report.md)。
- data文件夹：输入的拼音文件、输出的转换汉字文件、程序运行时需要读入的“词库”文件等。
- src文件夹：拼音输入法程序的源代码，内含char2（字的二元模型）、word1（词的一元模型）、word2（词的二元模型）三个子文件夹，分别实现相应模型。
- test文件夹：测试程序的拼音-汉字转换正确率、制作拼音-汉字测试集等源代码。
