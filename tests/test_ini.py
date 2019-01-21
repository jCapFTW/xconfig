from unittest import TestCase
from .utils import setup_temp
from xconfig.sources import INI


class IniTest(TestCase):
    def setUp(self):
        setup_temp()
        self.blob = {'BoolTest': {'v1': 'True', 'v 2': 'true', 'v3': 'False', 'v4': 'FALSE'},
                     'TextTest': {'v1': 'This is text', 'v2': 'This is more\ntext'},
                     'IntTest': {'v1': '32243756', 'v2': '\n-347'},
                     'FloatTest': {'v1': '3465.325', 'v2': '-0.2003'}}

    def test_ini_load(self):
        ini = INI("tests/resources/test_in.ini")
        self.assertEqual(ini.read(), self.blob)

    def test_ini_save(self):
        ini_out = INI("temp/test_out.ini")
        ini_in = INI("temp/test_out.ini")
        ini_out.write(self.blob)
        self.assertEqual(ini_in.read(), self.blob)
