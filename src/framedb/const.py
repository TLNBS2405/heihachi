import enum
from typing import Callable, Dict, List

NUM_CHARACTERS = 36


class CharacterName(enum.Enum):
    ALISA = "alisa"
    ASUKA = "asuka"
    AZUCENA = "azucena"
    BRYAN = "bryan"
    CLAUDIO = "claudio"
    Clive = "clive"
    DEVIL_JIN = "devil_jin"
    DRAGUNOV = "dragunov"
    EDDY = "eddy"
    FENG = "feng"
    HEIHACHI = "heihachi"
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
    LEROY = "leroy"
    LIDIA = "lidia"
    LILI = "lili"
    NINA = "nina"
    PANDA = "panda"
    PAUL = "paul"
    RAVEN = "raven"
    REINA = "reina"
    SHAHEEN = "shaheen"
    STEVE = "steve"
    VICTOR = "victor"
    YOSHIMITSU = "yoshimitsu"
    XIAOYU = "xiaoyu"
    ZAFINA = "zafina"

    def pretty(self) -> str:
        return self.value.replace("_", " ").title()

    def url_encode(self) -> str:
        return self.pretty().replace(" ", " ")


CHARACTER_ALIAS: Dict[CharacterName, List[str]] = {
    CharacterName.ALISA: ["ali", "als"],
    CharacterName.ASUKA: ["asu", "oscar"],
    CharacterName.AZUCENA: ["azu", "cafe"],
    CharacterName.BRYAN: ["bry", "byron"],
    CharacterName.CLAUDIO: ["cld", "cla", "claud"],
    CharacterName.Clive: ["cli", "clv"],
    CharacterName.DEVIL_JIN: ["dj", "deviljin", "dvj", "djin"],
    CharacterName.DRAGUNOV: ["drag", "sergei", "dragu", "dra"],
    CharacterName.EDDY: ["ed", "capo"],
    CharacterName.FENG: ["fen"],
    CharacterName.HEIHACHI: ["hei", "hachi"],
    CharacterName.HWOARANG: ["hwo"],
    CharacterName.JACK_8: ["j8", "jack8", "jack"],
    CharacterName.JIN: ["jim"],
    CharacterName.JUN: [],
    CharacterName.KAZUYA: ["kaz", "kazze", "masku"],
    CharacterName.KING: ["kin"],
    CharacterName.KUMA: ["karhu", "bear"],
    CharacterName.LARS: ["lar"],
    CharacterName.LAW: ["marshall"],
    CharacterName.LEE: ["violet"],
    CharacterName.LEO: [],
    CharacterName.LEROY: ["ler"],
    CharacterName.LIDIA: ["lid", "pm"],
    CharacterName.LILI: ["lil"],
    CharacterName.NINA: ["nin"],
    CharacterName.PANDA: ["pan"],
    CharacterName.PAUL: [],
    CharacterName.RAVEN: ["masterraven", "mraven", "maven", "mrv", "raven", "rav"],
    CharacterName.REINA: ["rei"],
    CharacterName.SHAHEEN: ["sha"],
    CharacterName.STEVE: ["stv", "ste", "fox"],
    CharacterName.VICTOR: ["vic"],
    CharacterName.YOSHIMITSU: ["yoshi", "manji", "yos"],
    CharacterName.XIAOYU: ["xiao", "ling"],
    CharacterName.ZAFINA: ["zaffy", "zaf"],
}


class MoveType(enum.Enum):
    RA = "Rage Art"
    T = "Tornado"
    HOMING = "Homing"
    PC = "Power Crush"
    TH = "Throw"
    HE = "Heat Engager"
    HS = "Heat Smash"


class FrameSituation(enum.Enum):
    STARTUP = "startup"
    BLOCK = "block"
    HIT = "hit"


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

CONDITION_MAP: Dict[str, Callable[[int, int], bool]] = {
    ">": lambda x, y: x > y,
    ">=": lambda x, y: x >= y,
    "<": lambda x, y: x < y,
    "<=": lambda x, y: x <= y,
    "==": lambda x, y: x == y,
}
