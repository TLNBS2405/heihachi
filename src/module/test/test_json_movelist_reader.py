import unittest
from src.module import json_movelist_reader

class MyTestCase(unittest.TestCase):

    def test_get_movelist_from(self):

        result = json_movelist_reader.get_movelist_from_json("azucena")
        self.assertEqual(result[0]["id"],"Azucena-1")

        result = json_movelist_reader.get_movelist_from_json("azu")
        self.assertEqual(result[0]["id"],"Azucena-1")

