import unittest
from src.wavu import wavu_reader

class MyTestCase(unittest.TestCase):

    def test_get_character_movelist(self):
        character_movelist = wavu_reader.get_character_movelist("Azucena")
        self.assertEqual(character_movelist[0].input,"1")


    def test_get_move(self):
        character_movelist = wavu_reader.get_character_movelist("Azucena")
        move = wavu_reader.get_move("Azucena-df+1,4",character_movelist)
        self.assertEqual(move.id,"Azucena-df+1,4")

    def test_complete_parent_input(self):
        character_movelist = wavu_reader.get_character_movelist("Azucena")
        move = wavu_reader.get_move("Azucena-df+1,4,1",character_movelist)
        move2 = wavu_reader.get_move("Azucena-f+4,4~3",character_movelist)
        move3 = wavu_reader.get_move("Azucena-LIB.1,2",character_movelist)
        move4 = wavu_reader.get_move("Azucena-b+4,3,4,3",character_movelist)
        move5 = wavu_reader.get_move("Azucena-df+1,4,1~2",character_movelist)
        move6 = wavu_reader.get_move("Azucena-ws4,1,3",character_movelist)
        self.assertEqual(move.input,"df+1,4,1")
        self.assertEqual(move2.input,"f+4,4~3")
        self.assertEqual(move3.damage,"14,20")
        self.assertEqual(move4.damage,"10,10,16,23")
        self.assertEqual(move5.input,"df+1,4,1~2")
        self.assertEqual(move6.on_ch,"+27a")

        character_movelist = wavu_reader.get_character_movelist("Bryan")
        move7 = wavu_reader.get_move("Bryan-4,3,f+4",character_movelist)
        self.assertEqual(move7.on_ch,"+31a (+21)")

