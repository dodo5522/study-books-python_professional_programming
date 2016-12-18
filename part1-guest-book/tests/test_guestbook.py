#!/usr/bin/env python
# -*- coding:utf-8 -*-

#   Copyright 2016 Takashi Ando - http://blog.rinka-blossom.com/
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
import shelve
import unittest
from datetime import datetime
from guestbook import DatabaseManager

try:
    from unittest.mock import MagicMock, patch
except:
    from mock import MagicMock, patch


class TestGreetingBackend(unittest.TestCase):
    TEST_DATA_FILE = "test.bin"

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_data(self):
        if os.path.isfile(self.TEST_DATA_FILE):
            os.remove(self.TEST_DATA_FILE)

        dbm = DatabaseManager(self.TEST_DATA_FILE)
        dbm.add_data("Takashi Ando", "hogehoge", datetime(1970, 1, 1))

        with shelve.open(self.TEST_DATA_FILE) as f:
            greeting_list = f[dbm.data_key_]
            self.assertEqual(len(greeting_list), 1)
            self.assertEqual(greeting_list[0]["name"], "Takashi Ando")
            self.assertEqual(greeting_list[0]["comment"], "hogehoge")

        dbm.add_data("Erika Ando", "fugafuga", datetime(1970, 1, 2))

        with shelve.open(self.TEST_DATA_FILE) as f:
            greeting_list = f[dbm.data_key_]
            self.assertEqual(len(greeting_list), 2)
            self.assertEqual(greeting_list[0]["name"], "Erika Ando")
            self.assertEqual(greeting_list[0]["comment"], "fugafuga")
            self.assertEqual(greeting_list[1]["name"], "Takashi Ando")
            self.assertEqual(greeting_list[1]["comment"], "hogehoge")

    def test_load_data(self):
        pass


if __name__ == "__main__":
    unittest.main()
