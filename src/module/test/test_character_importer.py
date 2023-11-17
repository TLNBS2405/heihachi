import unittest, json
from src.module import character_importer


class MyTestCase(unittest.TestCase):

    def test_character_importer(self):
        with open("azu.json") as azu:
            azu_meta = json.load(azu)
            azucena = character_importer.import_character(azu_meta)
            self.assertEqual(azucena.name, "Azucena")
