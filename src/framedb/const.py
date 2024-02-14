import enum


class CharacterName(enum.Enum):
    ALISA = "alisa"
    ASUKA = "asuka"
    AZUCENA = "azucena"
    BRYAN = "bryan"
    CLAUDIO = "claudio"
    DEVIL_JIN = "devil jin"
    DRAGUNOV = "dragunov"
    FENG = "feng"
    HWOARANG = "hwoarang"
    JACK_8 = "jack-8"
    JIN = "jin"
    KAZUYA = "kazuya"
    KING = "king"
    KUMA = "kuma"
    LARS = "lars"
    LAW = "law"
    LEE = "lee"
    LEO = "leo"
    LILI = "lili"
    RAVEN = "raven"
    REINA = "reina"
    NINA = "nina"
    PANDA = "panda"
    PAUL = "paul"
    SHAHEEN = "shaheen"
    STEVE = "steve"
    YOSHIMITSU = "yoshimitsu"
    XIAOYU = "xiaoyu"
    ZAFINA = "zafina"
    LEROY = "leroy"
    VICTOR = "victor"


CHARACTER_ALIAS = {
    CharacterName.ALISA: ["ali", "als"],
    CharacterName.ASUKA: ["asu", "oscar"],
    CharacterName.AZUCENA: ["azu", "cafe"],
    CharacterName.BRYAN: ["bry", "byron"],
    CharacterName.CLAUDIO: ["cld", "cla"],
    CharacterName.DEVIL_JIN: ["dj", "deviljin", "dvj", "djin"],
    CharacterName.DRAGUNOV: ["drag", "sergei", "dragu"],
    CharacterName.FENG: ["fen"],
    CharacterName.HWOARANG: ["hwo"],
    CharacterName.JACK_8: ["j8", "jack8", "jack"],
    CharacterName.JIN: ["jim"],
    CharacterName.KAZUYA: ["kaz", "kazze", "masku"],
    CharacterName.KING: ["kin"],
    CharacterName.KUMA: ["karhu"],
    CharacterName.LARS: ["lar"],
    CharacterName.LAW: ["marshall"],
    CharacterName.LEE: ["violet"],
    CharacterName.LEO: [],
    CharacterName.LILI: ["lil"],
    CharacterName.RAVEN: ["masterraven", "mraven", "maven", "mrv", "raven", "rav"],
    CharacterName.REINA: ["rei"],
    CharacterName.NINA: ["nin"],
    CharacterName.PANDA: ["pan"],
    CharacterName.PAUL: [],
    CharacterName.SHAHEEN: ["sha"],
    CharacterName.STEVE: ["stv", "ste", "fox"],
    CharacterName.YOSHIMITSU: ["yoshi", "manji", "yos"],
    CharacterName.XIAOYU: ["xiao", "ling"],
    CharacterName.ZAFINA: ["zaffy", "zaf"],
    CharacterName.LEROY: ["ler"],
    CharacterName.VICTOR: ["vic"],
}


class MoveType(enum.Enum):
    RA = "Rage Art"
    T = "Tornado"
    HOMING = "Homing"
    PC = "Power Crush"
    TH = "Throw"
    HE = "Heat Engager"
    HS = "Heat Smash"


MOVE_TYPE_ALIAS = {
    MoveType.RA: ["ra", "rage_art", "rageart", "rage art"],
    MoveType.T: ["screw", "t!", "t", "screws", "tor", "tornado"],
    MoveType.HOMING: ["homing", "homari"],
    MoveType.PC: [
        "armor",
        "armori",
        "pc",
        "power",
        "power_crush",
        "powercrush",
        "power crush",
    ],
    MoveType.TH: ["throw", "grab", "throws", "grabs"],
    MoveType.HE: ["he", "engage", "engager", "heat engager"],
    MoveType.HS: ["hs", "smash", "heat smash"],
}

SORT_ORDER = {
    MoveType.RA: 0,
    MoveType.HE: 1,
    MoveType.HS: 2,
    MoveType.T: 3,
    MoveType.HOMING: 4,
    MoveType.PC: 5,
    MoveType.TH: 6,
}

REPLACE = {
    " ": "",
    ",": "",
    "/": "",
    "d+": "d",
    "f+": "f",
    "u+": "u",
    "b+": "b",
    "n+": "n",
    "ws+": "ws",
    "fc+": "fc",
    "cd+": "cd",
    "wr+": "wr",
    "fff": "wr",
    "ra+": "ra",
    "ss+": "ss",
    "(": "",
    ")": "",
    "*+": "*",
    ".": "",
    "ws.": "ws",
    "fc.": "fc",
}

BLACKLIST = [
    "ImVeryBad#5231",
    "Nape Brasslers#1131",
    "Sleepii#1337",
    "iaa ibb beb ib#0000",
    "ГЕНИЙ#5448",
    "Beeno#6524",
    "Gigass-7#6960",
    "nickname#0000",
    "Sleepii#6666",
    "scrotum buster#6919",
    "Woozle#6308",
    "Iam#1001",
    "ImVeryBad#5231",
]
ID_BLACKLIST = [1006234003893915679, 240521686531702784]

EMOJI_LIST = [
    "1\ufe0f\u20e3",
    "2\ufe0f\u20e3",
    "3\ufe0f\u20e3",
    "4\ufe0f\u20e3",
    "5\ufe0f\u20e3",
]
