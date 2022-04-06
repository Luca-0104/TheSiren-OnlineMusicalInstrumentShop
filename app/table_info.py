"""
For inserting the information into the database
Those information should be stored in this file
"""

# users
user_list = [
    ['Customer1@163.com', 'Customer1', '123', 1],
    ['Customer2@163.com', 'Customer2', '123', 1],
    ['Staff1@163.com', 'Staff1', '123', 2],
    ['Staff2@163.com', 'staff2', '123', 2]
]

# products
product_list = [
    # name, serial_number, serial_prefix, serial_rank
    ['Product1', 'A001', 'b1-c1-t1-a1', 1],
    ['Product2', 'A002', 'b1-c1-t1-a1', 2],
    ['Product3', 'A003', 'b1-c1-t1-a1', 3],
    ['Product4', 'A004', 'b1-c1-t1-a1', 4],
    ['Product5', 'A005', 'b1-c1-t1-a1', 5],
    ['Product6', 'A006', 'b1-c1-t1-a1', 6],
    ['Product7', 'A007', 'b1-c1-t1-a1', 7],
    ['Product8', 'A008', 'b1-c1-t1-a1', 8],
    ['Product9', 'A009', 'b1-c1-t1-a1', 9],
    ['Product10', 'A010', 'b1-c1-t1-a1', 10]
]

# brands
brand_list = ['brand1', 'brand2', 'brand3', 'brand4', 'brand5']

'''
Category
* Classification 基本类别
    - Strings 弦乐器
    - Woodwinds 木管乐器
    - Brass 铜管乐器
    - Percussion 打击乐器
    - Keyboard 键盘
    - Accessories 配件
* Type 类型
    - Violin 小提琴
    - Viola 中提琴
    - Cello 大提琴
    - Double Bass 低音提琴
    - Guitar 吉他
    - Bass 贝斯
    - Ukulele 尤克里里
    - Harp 竖琴
    - Erhu 二胡
    - Guzheng 古筝
    - Guqin 古琴
    - Pipa 琵琶
    - Flute 长笛
    - Clarinet 单簧管
    - Oboe 双簧管
    - Piccolo 短笛
    - Saxophone 萨克斯
    - English Horn 英国管
    - Bassoon 巴松
    - Recorder 竖笛
    - Bagpipes 风笛
    - Suona Horn 唢呐
    - Sheng 笙
    - Trumpet 小号
    - Trombone 长号
    - French Horn 圆号
    - Tuba 大号
    - Euphonium 上低音号
    - Harmonica 口琴
    - Timpani 定音鼓
    - Bass Drum 大鼓
    - Snare 小鼓
    - Cajon 箱鼓
    - SoundBox 音箱
    - Tam-tam 锣
    - Tambourine 铃鼓
    - Marimba & Xylophone 马林巴 & 木琴
    - Vibraphone 颤音琴
    - Other Percussion 其它打击乐器
    - Piano 钢琴
    - Accordion 手风琴
    - LaunchPad 打击垫
    - Effects 效果器
    - Synthesizer 合成器
    - Microphone 麦克风
    - Monitor Headphone 监听耳机
* Extra Requirement 其他需求
    - Acoustic Only 仅支持原声
    - Electricity Required 需接电
    - Electricity Support 可接电
    - No Extra Requirement (仅包含乐器配件)
'''

# categories
category_list = [
    'Strings',
    'Woodwinds',
    'Brass',
    'Percussion',
    'Keyboard',
    'Accessories',
    'Violin',
    'Viola',
    'Cello',
    'Double Bass',
    'Guitar',
    'Bass',
    'Ukulele',
    'Harp',
    'Erhu',
    'Guzheng',
    'Guqin',
    'Pipa',
    'Flute',
    'Clarinet',
    'Oboe',
    'Piccolo',
    'Saxophone',
    'English Horn',
    'Bassoon',
    'Recorder',
    'Bagpipes',
    'Suona Horn',
    'Sheng',
    'Trumpet',
    'Trombone',
    'French Horn',
    'Tuba',
    'Euphonium',
    'Harmonica',
    'Timpani',
    'Bass Drum',
    'Snare',
    'Cajon',
    'SoundBox',
    'Tam-tam',
    'Tambourine',
    'Marimba & Xylophone',
    'Vibraphone',
    'Other Percussion',
    'Piano',
    'Accordion',
    'LaunchPad',
    'Effects',
    'Synthesizer',
    'Microphone',
    'Monitor Headphone',
    'Acoustic Only',
    'Electricity Required',
    'Electricity Support',
    'No Extra Requirement'
]
