import json
import os
import sqlite3


def build_table(pinyin_word_database_path, word_word_database_path):
    """
    Build pinyin-word table and word-word table using database from database_path.
        pinyin-word table: pinyin -> [[word, probability]] with count over a threshold.
        word-word table: str(word1-word2) -> probability with count over a threshold.

    Args:
        pinyin_word_database_path: Path to pinyin-word sqlite database file.
        word_word_database_path: Path to word-word sqlite database file.

    Returns:
        pinyin-word table: A dict, key->pinyin, value->[[word, probability]].
        word-word table: A dict, key->str(word1-word2), value->probability
    """
    pinyin_word_table = dict()
    pinyin_word_count = 0
    try:
        connection = sqlite3.connect(pinyin_word_database_path)
        cursor = connection.cursor()
        cursor.execute("""
            select pinyin, word, count
            from PinyinWord
            """)
        while True:
            # Data flow from database to table
            data_list = cursor.fetchmany()
            if not data_list:
                break
            for (pinyin, word, count) in data_list:
                pinyin_word_count += count
                # Add threshold to avoid wrongly cut words and reduce number of words
                if count > 10:
                    if pinyin in pinyin_word_table:
                        pinyin_word_table[pinyin].append([word, count])
                    else:
                        pinyin_word_table[pinyin] = [[word, count], ]
        # Change count to probability
        for pinyin, word_list in pinyin_word_table.items():
            word_list = [(word, count / pinyin_word_count)
                         for word, count in word_list]
            pinyin_word_table[pinyin] = word_list
    finally:
        cursor.close()
        connection.close()

    word_word_table = dict()
    word_word_count = 0
    try:
        connection = sqlite3.connect(word_word_database_path)
        cursor = connection.cursor()
        cursor.execute("""
            select word1, word2, count
            from PinyinPinyinWordWord
            """)
        while True:
            data_list = cursor.fetchmany()
            if not data_list:
                break
            for (word1, word2, count) in data_list:
                word_word_count += count
                # Add threshold to avoid wrongly cut words and reduce number of words
                if count > 1:
                    word_pair = '-'.join((word1, word2))
                    if word_pair in word_word_table:
                        # 同词不同音，忽略
                        word_word_table[word_pair] += count
                    else:
                        word_word_table[word_pair] = count
        # Change count to probability
        for word_word, count in word_word_table.items():
            word_word_table[word_word] = count / word_word_count
    finally:
        cursor.close()
        connection.close()

    return pinyin_word_table, word_word_table


def check_table(pinyin_word_table):
    """
    Check pinyin_word_table to be properly set.

    Args:
        pinyin_word_table: A dict, key->pinyin, value->[(word, count)].
    """
    # Make sure all the possible pinyin of a single Chinese character
    # is in pinyin_word_table.
    pinyin_character_table = {'cui': '崔', 'jiu': '就', 'dun': '吨', 'gui': '贵', 'nian': '年', 'que': '却', 'yue': '月', 'nuo': '诺', 'guai': '拐', 'kui': '亏', 'zen': '怎', 'lue': '略', 'suo': '所', 'ben': '本', 'bin': '斌', 'teng': '疼', 'ming': '名', 'nie': '捏', 'nv': '女', 'cuo': '错', 'wa': '挖', 'duan': '段', 'mo': '末', 'chao': '超', 'pao': '跑', 'qiao': '桥', 'bie': '别', 'xue': '学', 'bo': '波', 'ba': '把', 'gang': '刚', 'fou': '否', 'pa': '怕', 'ka': '卡', 'lu': '路', 'du': '度', 'song': '送', 'lun': '轮', 'shen': '深', 'sa': '撒', 'mang': '忙', 'gai': '该', 'xia': '下', 'shan': '山', 'geng': '更', 'ding': '定', 'heng': '横', 'kun': '崑', 'jia': '家', 'wen': '问', 'ou': '欧', 'jiao': '较', 'mu': '亩', 'zhu': '住', 'gu': '古', 'ei': '诶', 'la': '拉', 'lang': '琅', 'gan': '干', 'sen': '森', 'you': '有', 'su': '苏', 'diu': '丢', 'neng': '能', 'lei': '类', 'can': '餐', 'ti': '提', 'fei': '非', 'zhuai': '拽', 'ken': '啃', 'duo': '多', 'cuan': '窜', 'liao': '聊', 'ting': '听', 'xian': '县', 'chi': '吃', 'dui': '对', 'tuan': '团', 'nai': '奶', 'luan': '乱', 'dei': '得', 'ang': '昂', 'chan': '产', 'deng': '等', 'jun': '均', 'yong': '用', 'xi': '系', 'hong': '红', 'zhi': '至', 'ma': '吗', 'lo': '咯', 'jue': '绝', 'pian': '骗', 'dou': '都', 'ci': '次', 'pou': '抔', 'qie': '且', 'ge': '个', 'zhen': '镇', 'cang': '藏', 'liang': '两', 'qing': '请', 'ze': '则', 'zhai': '寨', 'he': '和', 'sha': '啥', 'bai': '白', 'hei': '黑', 'shu': '属', 'te': '特', 'ye': '也', 'lan': '蓝', 'da': '大', 'chuang': '创', 'tiao': '条', 'cun': '村', 'fu': '副', 'qu': '去', 'dan': '但', 'fo': '佛', 'guang': '光', 'nan': '难', 'kai': '开', 'wai': '外', 'kan': '看', 'nu': '怒', 'sui': '岁', 'miao': '秒', 'lai': '来', 'zhang': '张', 'me': '么', 'ban': '办', 'zu': '组', 'long': '龙', 'ji': '及', 'pu': '铺', 'feng': '风', 'shuai': '衰', 'po': '破', 'dang': '党', 'zheng': '正', 'hu': '户', 'ru': '如', 'qian': '前', 'kuang': '矿', 'nen': '嫩', 'shua': '刷', 'meng': '梦', 'zeng': '增', 'yao': '要', 'ya': '牙', 'zhuan': '转', 'dong': '东', 'ruo': '若', 'men': '们', 'quan': '全', 'man': '满', 'nuan': '暖', 'ai': '爱', 'pi': '批', 'shuang': '双', 'gua': '挂', 'mai': '买', 'dao': '到', 'gei': '给', 'huai': '坏', 'kou': '口', 'huo': '或', 'she': '摄', 'chun': '纯', 'miu': '谬', 'tuo': '拖', 'jie': '届', 'chui': '吹', 'guan': '馆', 'kong': '控', 'shui': '水', 'dai': '带', 'sai': '赛', 'hua': '化', 'rao': '绕', 'chuan': '穿', 'cai': '才', 'lv': '率', 'piao': '票', 'bing': '并', 'niang': '娘', 'jin': '近', 'weng': '翁', 'zui': '最', 'beng': '泵', 'xing': '性', 'ku': '哭', 'sou': '艘', 'zhan': '站', 'jing': '经', 'qiang': '强', 'ren': '人', 'che': '车', 'peng': '彭', 'wo': '我', 'biao': '表',
                              'nin': '您', 'han': '含', 'shao': '少', 'li': '里', 'pang': '旁', 'lou': '楼', 'shun': '顺', 'jian': '件', 'gun': '丨', 'ning': '宁', 'yang': '杨', 'zou': '走', 'hao': '好', 'chai': '拆', 'zai': '在', 'chen': '陈', 'zhei': '这', 'wang': '网', 'cha': '茶', 'yi': '以', 'tai': '太', 'zha': '扎', 'zhuang': '撞', 'gou': '狗', 'cheng': '称', 'guo': '过', 'niu': '牛', 'shei': '谁', 'chuo': '戳', 'di': '第', 'shuan': '拴', 'zuo': '做', 'le': '了', 'fan': '反', 'xiong': '熊', 'pai': '拍', 'a': '啊', 'qiong': '穷', 'diao': '掉', 'zhe': '这', 'chou': '抽', 'cen': '涔', 'tun': '屯', 'se': '色', 'en': '恩', 'tou': '头', 'zhua': '抓', 'sao': '扫', 'ying': '应', 'huang': '黄', 'chuai': '踹', 'qun': '群', 'yun': '云', 'rong': '蓉', 'ce': '侧', 're': '热', 'pei': '陪', 'nou': '耨', 'wu': '无', 'juan': '卷', 'yo': '哟', 'zi': '自', 'gao': '高', 'yan': '严', 'nong': '弄', 'mei': '没', 'ao': '奥', 'hen': '很', 'ri': '日', 'mie': '灭', 'ga': '伽', 'zei': '贼', 'de': '的', 'si': '四', 'zong': '总', 'bi': '比', 'niao': '鸟', 'ruan': '软', 'ju': '据', 'cong': '从', 'zhong': '中', 'zhao': '找', 'kuan': '款', 'mao': '猫', 'na': '那', 'dia': '嗲', 'san': '三', 'zao': '早', 'er': '而', 'rui': '睿', 'tong': '同', 'zun': '尊', 'kuai': '快', 'chang': '场', 'fen': '分', 'ping': '坪', 'cou': '凑', 'ta': '他', 'hai': '还', 'bian': '便', 'hou': '后', 'qia': '掐', 'hun': '混', 'die': '跌', 'gen': '跟', 'sheng': '省', 'zuan': '钻', 'dian': '点', 'yu': '与', 'bang': '帮', 'shi': '是', 'tang': '躺', 'ha': '哈', 'rang': '让', 'nei': '内', 'chu': '出', 'kua': '跨', 'pen': '喷', 'pie': '撇', 'wei': '为', 'shang': '上', 'tan': '谈', 'ke': '可', 'pin': '拼', 'nang': '囊', 'zhou': '周', 'ne': '呢', 'zhuo': '桌', 'hang': '杭', 'qi': '其', 'sang': '桑', 'reng': '仍', 'shou': '受', 'tu': '图', 'keng': '坑', 'suan': '算', 'jiong': '囧', 'nue': '虐', 'run': '润', 'jiang': '将', 'cu': '促', 'zang': '脏', 'ling': '另', 'kuo': '扩', 'liu': '刘', 'hui': '会', 'bao': '报', 'xun': '讯', 'kao': '靠', 'chong': '冲', 'min': '民', 'ceng': '曾', 'mian': '面', 'zan': '赞', 'seng': '僧', 'ca': '擦', 'sun': '孙', 'huan': '换', 'wan': '万', 'zhui': '追', 'xiang': '向', 'lia': '俩', 'tian': '天', 'o': '哦', 'shuo': '说', 'ni': '你', 'fa': '法', 'tui': '推', 'zhun': '准', 'qiu': '球', 'qin': '亲', 'yuan': '原', 'an': '按', 'yin': '因', 'xin': '新', 'mou': '某', 'xie': '写', 'tao': '套', 'fang': '房', 'tie': '贴', 'lian': '连', 'ran': '然', 'xiu': '秀', 'lin': '林', 'nao': '闹', 'xiao': '小', 'luo': '罗', 'mi': '米', 'rou': '肉', 'cao': '曹', 'shai': '晒', 'kang': '抗', 'xuan': '选', 'bei': '被', 'leng': '冷', 'lie': '列', 'lao': '老', 'xu': '需', 'gong': '共', 'pan': '潘', 'tei': '忒', 'e': '俄', 'bu': '不', 'za': '砸'}
    for key, value in pinyin_character_table.items():
        if not key in pinyin_word_table:
            pinyin_word_table[key] = [[value, 1], ]
            print("Miss: " + key + " Set to: " + value)


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
Build and save pinyin-word table.
"""
if __name__ == "__main__":
    pinyin_word_database_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, "data", "pinyin_word.db")
    pinyin_word_table_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, "data", "word2_pinyin_word_table.json")
    pinyin_pinyin_word_word_database_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, "data", "pinyin_pinyin_word_word.db")
    word_word_table_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, "data", "word2_word_word_table.json")
    pinyin_word_table, word_word_table = build_table(
        pinyin_word_database_path, pinyin_pinyin_word_word_database_path)
    check_table(pinyin_word_table)
    save_table(pinyin_word_table, pinyin_word_table_path)
    save_table(word_word_table, word_word_table_path)
