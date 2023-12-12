import unittest
from src.module import json_movelist_reader

class MyTestCase(unittest.TestCase):

    def test_get_movelist_from_json(self):

        result = json_movelist_reader.get_movelist_from_json("azucena")
        self.assertEqual(result[0]["id"],"Azucena-1")


    def test_get_move(self):

        azu_move_list = json_movelist_reader.get_movelist_from_json("azucena")
        move = json_movelist_reader.get_move("d/f+1",azu_move_list)

        self.assertEqual(move["id"],"Azucena-df+1")
        move = json_movelist_reader.get_move("df141",azu_move_list)
        self.assertEqual(move["id"],"Azucena-df+1,4,1")
        move = json_movelist_reader.get_move("fc df3",azu_move_list)
        self.assertEqual(move["id"],"Azucena-FC.df+3")

        move = json_movelist_reader.get_move("ff3+4",azu_move_list)
        self.assertEqual(move["id"],"Azucena-f,F+3+4")

        move = json_movelist_reader.get_move("LIB 2",azu_move_list)
        self.assertEqual(move["id"],"Azucena-LIB.2")
        move = json_movelist_reader.get_move("LIB.2",azu_move_list)
        self.assertEqual(move["id"],"Azucena-LIB.2")

        move = json_movelist_reader.get_move("wr3",azu_move_list)
        self.assertEqual(move["id"],"Azucena-f,f,F+3")

        move = json_movelist_reader.get_move("f214",azu_move_list)
        self.assertEqual(move["id"],"Azucena-f+2,1,4")

        move = json_movelist_reader.get_move("rage d/f+1+2",azu_move_list)
        self.assertEqual(move["id"],"Azucena-R.df+1+2")

        move = json_movelist_reader.get_move("R.d/f+1+2",azu_move_list)
        self.assertEqual(move["id"],"Azucena-R.df+1+2")

        move = json_movelist_reader.get_move("H.LIB.2,F",azu_move_list)
        self.assertEqual(move["id"],"Azucena-H.LIB.2,F")
        move = json_movelist_reader.get_move("Heat LIB.2,F",azu_move_list)
        self.assertEqual(move["id"],"Azucena-H.LIB.2,F")

        move = json_movelist_reader.get_move("Heat lib2f",azu_move_list)
        self.assertEqual(move["id"],"Azucena-H.LIB.2,F")

        move = json_movelist_reader.get_move("ws41",azu_move_list)
        self.assertEqual(move["id"],"Azucena-ws4,1")