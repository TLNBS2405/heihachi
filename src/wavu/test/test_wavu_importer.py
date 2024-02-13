import unittest
import json
import os
from src.wavu import wavu_importer

dir_path = os.path.dirname(os.path.realpath(__file__))


class MyTestCase(unittest.TestCase):
    def test_character_importer(self):
        azu_json = dir_path + "/azu.json"
        with open(azu_json) as azu:
            azu_meta = json.load(azu)
            azucena = wavu_importer.import_character(azu_meta)
            self.assertEqual(azucena.name, "Azucena")
