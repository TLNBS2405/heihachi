import unittest, json
from src.wavu import parser

class MyTestCase(unittest.TestCase):

    def test_convert_html_move_to_json(self):

        character_movelist = parser.get_character_html_movelist("Azucena")
        self.assertEqual(character_movelist[0].input,"2+3")



