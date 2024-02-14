import json
import unittest

from wavu import wavu_importer


class MyTestCase(unittest.TestCase):
    def test_character_importer(self):
        azu_json = "src/tests/assets/azu.json"
        with open(azu_json) as azu:
            azu_meta = json.load(azu)
            azucena = wavu_importer.import_character(azu_meta)
            self.assertEqual(azucena.name, "Azucena")
