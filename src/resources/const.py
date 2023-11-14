CHARACTER_ALIAS = {
    'Alisa': ['ali', 'als'],
    'Asuka': ['asu'],
    'Bryan': ['bry'],
    'Claudio': ['cld', 'cla'],
    'Devil_jin': ['dj', 'deviljin', 'dvj'],
    'Dragunov': ['drag', 'sergei', 'dragu'],
    'Eliza': ['elz'],
    'Feng': ['fen'],
    'Hwoarang': ['hwo'],
    'Jack8': ['j8', 'jack-8', 'jack'],
    'Jin': ['jim'],
    'Kazuya': ['kaz', 'kazze', 'masku'],
    'King': ['kin'],
    'Kuma': ['panda', 'karhu', 'bear'],
    'Lars': ['lar'],
    'Law': ['marshall'],
    'Lee': ['violet'],
    'Leo': [],
    'Lili': ['lil'],
    'Raven': ['masterraven', 'mraven', 'maven', 'mrv', 'raven', 'mr'],
    'Nina': ['nin'],
    'Paul': [],
    'Shaheen': ['sha'],
    'Steve': ['stv', 'ste', 'fox'],
    'Yoshimitsu': ['yoshi', 'manji', 'yos'],
    'Xiaoyu': ['xiao', 'ling'],
    'Zafina': ['zaffy', 'zaf'],
    "Leroy": ['ler'],
    "Generic": []
}

MOVE_TYPES = {
    "Rage Art": ["ra", "rage_art", "rageart", "rage art"],
    "Tornado": ["screw", "t!", "t", "screws","tor"],
    "Homing": ["homing", "homari"],
    "Power Crush": ["armor", "armori", "pc", "power", "power_crush", "powercrush", "power crush"],
    "Throw": ["throw", "grab", "throws", "grabs"],
    "Heat Engager":["he", "engager"],
    "Heat Smash" : ["hs", "smash"]
}

SORT_ORDER = {"Rage Art": 0, "Heat Engager": 1, "Heat Smash": 2, "Tornado": 3, "Homing": 4, "Power Crush": 5,
              "Throw": 6}

REPLACE = {
    ' ': '',
    ',': '',
    '/': '',
    'd+': 'd',
    'f+': 'f',
    'u+': 'u',
    'b+': 'b',
    'n+': 'n',
    'ws+': 'ws',
    'fc+': 'fc',
    'cd+': 'cd',
    'wr+': 'wr',
    'ra+': 'ra',
    'rd+': 'rd',
    'ss+': 'ss',
    '(': '',
    ')': '',
    '*+': '*'
}

BLACKLIST = ['ImVeryBad#5231', 'Nape Brasslers#1131', 'Sleepii#1337', 'iaa ibb beb ib#0000', 'ГЕНИЙ#5448', 'Beeno#6524',
             'Gigass-7#6960', 'nickname#0000', 'Sleepii#6666', 'scrotum buster#6919', 'Woozle#6308', 'Iam#1001',
             'ImVeryBad#5231']
ID_BLACKLIST = [1006234003893915679,240521686531702784]

EMOJI_LIST = ['1\ufe0f\u20e3', '2\ufe0f\u20e3', '3\ufe0f\u20e3', '4\ufe0f\u20e3', '5\ufe0f\u20e3']
