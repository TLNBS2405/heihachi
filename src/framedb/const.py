import enum
from typing import Dict, List

NUM_CHARACTERS = 33


class CharacterName(enum.Enum):
    ALISA = "alisa"
    ASUKA = "asuka"
    AZUCENA = "azucena"
    BRYAN = "bryan"
    CLAUDIO = "claudio"
    DEVIL_JIN = "devil_jin"
    DRAGUNOV = "dragunov"
    FENG = "feng"
    HWOARANG = "hwoarang"
    JACK_8 = "jack-8"
    JIN = "jin"
    JUN = "jun"
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
    EDDY = "eddy"

    def pretty(self) -> str:
        return self.value.replace("_", " ").title()

    def url_encode(self) -> str:
        return self.pretty().replace(" ", " ")


CHARACTER_ALIAS: Dict[CharacterName, List[str]] = {
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
    CharacterName.JUN: [],
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
    CharacterName.EDDY: ["ed"],
}


class MoveType(enum.Enum):
    RA = "Rage Art"
    T = "Tornado"
    HOMING = "Homing"
    PC = "Power Crush"
    TH = "Throw"
    HE = "Heat Engager"
    HS = "Heat Smash"


MOVE_TYPE_ALIAS: Dict[MoveType, List[str]] = {
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

SORT_ORDER: Dict[MoveType, int] = {
    MoveType.RA: 0,
    MoveType.HE: 1,
    MoveType.HS: 2,
    MoveType.T: 3,
    MoveType.HOMING: 4,
    MoveType.PC: 5,
    MoveType.TH: 6,
}

REPLACE: Dict[str, str] = {
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

EMOJI_LIST: List[str] = [
    "1\ufe0f\u20e3",
    "2\ufe0f\u20e3",
    "3\ufe0f\u20e3",
    "4\ufe0f\u20e3",
    "5\ufe0f\u20e3",
]
