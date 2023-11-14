from typing import List


class Move:
    def __init__(self, id: str, name: str, input: str, target: str, damage: str, on_block: str, on_hit: str, on_ch: str,
                 startup: str, recovery: str, notes: str, gif: str):
        self.id = id
        self.name = name
        self.input = input
        self.target = target
        self.damage = damage
        self.on_block = on_block
        self.on_hit = on_hit
        self.on_ch = on_ch
        self.startup = startup
        self.recovery = recovery
        self.notes = notes
        self.gif = gif


class Character:
    def __init__(self, name: str, wavu_page: str, portrait: str, move_list: List[Move]):
        self.name = name
        self.wavu_page = wavu_page,
        self.portrait = portrait,
        self.move_list = move_list


