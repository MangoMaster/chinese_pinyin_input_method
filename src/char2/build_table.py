import json
import math
import os
import sqlite3


def build_table(pinyin_char_database_path, pinyin_pinyin_char_char_database_path):
    """
    Build pinyin-char table and char-char table using database from database_path.
        pinyin-char table: pinyin -> [[char, log(probability)]].
        char-char table: str(char1-char2) -> log(probability).

    Args:
        pinyin_char_database_path: Path to pinyin-char sqlite database file.
        pinyin_pinyin_char_char_database_path: Path to pinyin-pinyin-char-char sqlite database file.

    Returns:
        pinyin-char table: A dict, key->pinyin, value->[[char, log(probability)]].
        char-char table: A dict, key->str(char1-char2), value->log(probability).
    """
    # Build pinyin-char table
    pinyin_char_table = dict()
    pinyin_char_count = 0
    try:
        connection = sqlite3.connect(pinyin_char_database_path)
        cursor = connection.cursor()
        cursor.execute("""
            select pinyin, char, count
            from PinyinChar
            """)
        while True:
            # Data flow from database to table
            data_list = cursor.fetchmany()
            if not data_list:
                break
            for (pinyin, char, count) in data_list:
                pinyin_char_count += count
                if pinyin in pinyin_char_table:
                    pinyin_char_table[pinyin].append([char, count])
                else:
                    pinyin_char_table[pinyin] = [[char, count], ]
    finally:
        cursor.close()
        connection.close()
    # Make sure all the possible pinyin of a single Chinese character
    # is in pinyin_char_table.
    pinyin_character_table = {'nu': '努', 'bo': '博', 'kang': '康', 'nian': '年', 'bin': '宾', 'liang': '两', 'ni': '你', 'ka': '卡', 'huang': '黄', 'zen': '怎', 'gou': '构', 'dan': '但', 'shu': '数', 'chuo': '戳', 'sun': '损', 'zhang': '长', 'sa': '萨', 'dang': '当', 'hang': '行', 'fo': '佛', 'hong': '红', 'hei': '黑', 'man': '满', 'ming': '名', 'lu': '路', 'lia': '俩', 'lei': '类', 'ye': '业', 'ling': '领', 'qie': '切', 'suo': '所', 'ha': '哈', 'chou': '筹', 'gang': '港', 'mei': '美', 'jue': '决', 'xi': '系', 'nei': '内', 'guang': '广', 'cai': '才', 'chang': '场', 'qiao': '桥', 'cheng': '成', 'du': '度', 'lian': '联', 'ping': '平', 'gen': '根', 'sheng': '生', 'luan': '乱', 'zhong': '中', 'xiao': '小', 'dao': '到', 'sen': '森', 'zhuan': '专', 'kai': '开', 'tao': '套', 'wa': '挖', 'da': '大', 'bian': '变', 'zhu': '主', 'ri': '日', 'nin': '您', 'ya': '亚', 'rao': '绕', 'kao': '考', 'mi': '米', 'can': '参', 'pu': '普', 'bai': '百', 'shun': '顺', 'shui': '水', 'lo': '咯', 'mu': '目', 'jing': '经', 'e': '额', 'nan': '南', 'mo': '模', 'pa': '怕', 'jiu': '就', 'xue': '学', 'liao': '了', 'lv': '旅', 'nue': '虐', 'zhou': '州', 'zou': '走', 'zhe': '这', 'gei': '给', 'chai': '拆', 'shua': '刷', 'zong': '总', 'nie': '聂', 'cang': '藏', 'beng': '崩', 'ma': '马', 'yan': '研', 'na': '那', 'le': '了', 'pou': '剖', 'min': '民', 'bei': '被', 'chuang': '创', 'sha': '沙', 'cong': '从', 'cen': '岑', 'wu': '务', 'cui': '崔', 'chu': '出', 'wang': '网', 'zhuang': '装', 'peng': '朋', 'nao': '脑', 'qin': '亲', 'pan': '判', 'ci': '次', 'wai': '外', 'se': '色', 'tai': '台', 'neng': '能', 'cou': '凑', 'nv': '女', 'jie': '解', 'dun': '顿', 'gu': '故', 'ning': '宁', 'jian': '建', 'han': '汉', 'en': '恩', 'run': '润', 'mie': '灭', 'zang': '脏', 'shan': '山', 'shuo': '说', 'zi': '自', 'chun': '春', 'shuan': '栓', 'xing': '行', 'zha': '诈', 'gong': '工', 'ji': '机', 'tuan': '团', 'hu': '户', 'fa': '发', 'chuai': '揣', 'bie': '别', 'dian': '点', 'fang': '方', 'cuan': '窜', 'biao': '标', 'zhun': '准', 'san': '三', 'wan': '万', 'ruan': '软', 'zu': '组', 'qia': '恰', 'zao': '造', 'kan': '看', 'cha': '查', 'tou': '投', 'xian': '现', 'qi': '其', 'sang': '桑', 'dia': '嗲', 'rong': '融', 'shang': '上', 'xiu': '修', 'gun': '滚', 'nuan': '暖', 'yi': '一', 'pin': '品', 'cu': '促', 'miao': '苗', 'ku': '库', 'nang': '囊', 'pie': '撇', 'zheng': '政', 'pai': '排', 'keng': '坑', 'bi': '比', 're': '热', 'weng': '翁', 'qiang': '强', 'pi': '批', 'yun': '运', 'men': '们', 'juan': '捐', 'ren': '人', 'dui': '对', 'bu': '不', 'shou': '手', 'tong': '通', 'teng': '腾', 'ga': '尬', 'ba': '把', 'zhuo': '着', 'lai': '来', 'rang': '让', 'suan': '算', 'jiong': '窘', 'jun': '军', 'mai': '买', 'dei': '得', 'shi': '是',
                              'zun': '尊', 'seng': '僧', 'mou': '某', 'bang': '帮', 'rou': '肉', 'ru': '入', 'yo': '哟', 'kou': '口', 'que': '确', 'te': '特', 'cao': '草', 'ta': '他', 'xin': '新', 'hui': '会', 'chen': '陈', 'chuan': '传', 'gan': '干', 'ang': '昂', 'shei': '谁', 'sao': '扫', 'gai': '改', 'nen': '嫩', 'de': '的', 'ken': '肯', 'ai': '爱', 'zuo': '作', 'zhui': '追', 'pen': '喷', 'xiang': '项', 'qing': '情', 'a': '阿', 'yao': '要', 'kui': '馈', 'pang': '旁', 'piao': '票', 'ran': '然', 'xia': '下', 'cun': '村', 'huai': '怀', 'lang': '朗', 'song': '送', 'lin': '林', 'er': '而', 'hua': '化', 'fu': '服', 'shen': '深', 'shuai': '率', 'geng': '更', 'ceng': '层', 'fou': '否', 'ting': '庭', 'feng': '风', 'kuan': '款', 'tui': '推', 'zhao': '照', 'guan': '关', 'jiao': '交', 'xuan': '选', 'o': '哦', 'jiang': '将', 'meng': '盟', 'zai': '在', 'lan': '兰', 'ca': '擦', 'tiao': '条', 'fan': '范', 'you': '有', 'gui': '规', 'hun': '婚', 'diao': '调', 'xie': '些', 'shuang': '双', 'xun': '讯', 'wo': '我', 'po': '破', 'ban': '办', 'zhuai': '拽', 'zei': '贼', 'chong': '重', 'gua': '挂', 'mian': '面', 'luo': '落', 'ne': '呢', 'kuo': '括', 'quan': '全', 'an': '安', 'zhua': '抓', 'hao': '好', 'qiong': '穷', 'dou': '都', 'gao': '高', 'tu': '图', 'fei': '费', 'zhai': '债', 'su': '速', 'si': '司', 'lie': '列', 'zhan': '展', 'zhen': '镇', 'lou': '楼', 'shai': '晒', 'duo': '多', 'fen': '分', 'sou': '搜', 'heng': '衡', 'lun': '论', 'lue': '略', 'dong': '动', 'reng': '仍', 'chi': '持', 'kuang': '况', 'ju': '据', 'jia': '家', 'huo': '活', 'qiu': '求', 'ding': '定', 'pao': '跑', 'miu': '谬', 'kua': '跨', 'guai': '怪', 'ben': '本', 'che': '车', 'jin': '进', 'bing': '并', 'nuo': '诺', 'dai': '代', 'pian': '片', 'kong': '空', 'di': '地', 'zhi': '制', 'niao': '鸟', 'tang': '堂', 'hai': '还', 'nai': '奶', 'hen': '很', 'tuo': '脱', 'yuan': '员', 'tian': '天', 'zeng': '增', 'tie': '铁', 'ruo': '若', 'zui': '最', 'zhei': '这', 'sui': '随', 'tun': '吞', 'kuai': '快', 'lao': '老', 'diu': '丢', 'ze': '责', 'la': '拉', 'leng': '冷', 'wen': '文', 'zuan': '钻', 'nong': '农', 'yue': '月', 'xu': '需', 'niang': '娘', 'ou': '欧', 'ti': '题', 'long': '龙', 'tei': '忒', 'nou': '耨', 'yang': '样', 'za': '杂', 'li': '理', 'guo': '国', 'duan': '段', 'niu': '牛', 'me': '么', 'liu': '流', 'yong': '用', 'yin': '因', 'wei': '为', 'ying': '应', 'she': '设', 'qu': '区', 'sai': '赛', 'chao': '超', 'kun': '困', 'bao': '报', 'shao': '少', 'ce': '策', 'hou': '后', 'pei': '配', 'mao': '贸', 'huan': '环', 'xiong': '雄', 'qun': '群', 'ke': '可', 'rui': '瑞', 'he': '和', 'mang': '忙', 'zan': '赞', 'yu': '于', 'ge': '个', 'cuo': '措', 'deng': '等', 'die': '跌', 'ao': '奥', 'qian': '前', 'chui': '吹', 'ei': '诶', 'tan': '谈', 'chan': '产'}
    for key, value in pinyin_character_table.items():
        if not key in pinyin_char_table:
            # Reduce an order of magnitude -> 0.1
            pinyin_char_table[key] = [[value, 0.1], ]
            print("Miss: " + key + " Set to: " + value)
    # Change count to log(probability)
    for pinyin, char_list in pinyin_char_table.items():
        char_list = [(char, math.log10(count / pinyin_char_count))
                     for char, count in char_list]
        pinyin_char_table[pinyin] = char_list

    # Build char-char table
    char_char_table = dict()
    char_char_count = 0
    try:
        connection = sqlite3.connect(pinyin_pinyin_char_char_database_path)
        cursor = connection.cursor()
        cursor.execute("""
            select char1, char2, count
            from PinyinPinyinCharChar
            """)
        while True:
            data_list = cursor.fetchmany()
            if not data_list:
                break
            for (char1, char2, count) in data_list:
                char_char_count += count
                char_pair = '-'.join((char1, char2))
                if char_pair in char_char_table:
                    # 同词不同音，忽略
                    char_char_table[char_pair] += count
                else:
                    char_char_table[char_pair] = count
    finally:
        cursor.close()
        connection.close()
    # Change count to log(probability)
    for char_char, count in char_char_table.items():
        char_char_table[char_char] = math.log10(count / char_char_count)

    return pinyin_char_table, char_char_table


def save_table(table, table_path):
    """
    Save table to table_path.

    Args:
        table: A table that can be converted to json.
        table_path: Path to the destination table json file.
    """
    with open(table_path, 'w') as f:
        json.dump(table, f)


"""
Build and save pinyin-char table.
"""
if __name__ == "__main__":
    pinyin_char_database_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, "data", "pinyin_char.db")
    pinyin_char_table_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, "data", "pinyin_char_table.json")
    pinyin_pinyin_char_char_database_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, "data", "pinyin_pinyin_char_char.db")
    char_char_table_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, "data", "char_char_table.json")
    pinyin_char_table, char_char_table = build_table(
        pinyin_char_database_path, pinyin_pinyin_char_char_database_path)
    save_table(pinyin_char_table, pinyin_char_table_path)
    save_table(char_char_table, char_char_table_path)
