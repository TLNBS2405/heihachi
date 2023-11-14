from typing import List, Type

from mediawiki import MediaWiki
from bs4 import BeautifulSoup
import requests, re

from src.character import Move, Character
from src.resources import const

wavuwiki = MediaWiki(url=const.WAVU_API_URL)
session = requests.Session()

def get_character_html_movelist(character_name: str) -> List[Move]:
    params = {
        "action": "parse",
        "page": character_name + "_movelist",
        "format": "json"
    }

    response = session.get(const.WAVU_API_URL, params=params)
    html_output= response.json()["parse"]["text"]["*"]

    soup = BeautifulSoup(html_output, 'html.parser')
    divs = soup.find_all("div",{"id": re.compile(r'^' + character_name +'.*$')})

    move_list = []
    for div in divs:
        move = convert_html_move(str(div))
        move_list.append(move)
    return move_list

def convert_html_move(div: str) -> Move:
    soup = BeautifulSoup(div,'html.parser')

    id = soup.find("div", {"class": "movedata hover-bg-grey-03"})['id']
    name =  soup.find("div", {"class": "movedata-name"}).get_text()
    input = soup.find("span", {"class": "movedata-inputLead"}).get_text() + soup.find("span", {"class": "movedata-input"}).get_text()
    target = soup.find("span", {"class": "movedata-target"}).get_text()
    damage = soup.find("span", {"class": "movedata-damage"}).get_text()

    on_block = soup.find("div", {"class": "movedata-block"}).get_text()
    on_hit = soup.find("div", {"class": "movedata-hit"}).get_text()
    on_ch = soup.find("div", {"class": "movedata-ch"}).get_text()
    startup = soup.find("div", {"class": "movedata-startup"}).get_text()
    recovery = soup.find("div", {"class": "movedata-recv"}).get_text()

    notes = soup.find("div", {"class": "movedata-notes"}).get_text()

    move = Move(id,name,input,target,damage,on_block,on_hit,on_ch,startup,recovery,notes,"")
    return move

