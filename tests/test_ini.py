import unittest
import xconfig


class IniTest(unittest.TestCase):
    def setUp(self):
        self.blob = {'BoolTest': {'v1': 'True', 'v 2': 'true', 'v3': 'False', 'v4': 'FALSE'},
                     'TextTest': {'v1': 'This is text', 'v2': 'This is more\ntext'},
                     'IntTest': {'v1': '32243756', 'v2': '\n-347'},
                     'FloatTest': {'v1': '3465.325', 'v2': '-0.2003'}}

    def test_load(self):
        self.assertEqual(xconfig.INI.read("tests/test_in.ini"), self.blob)

    def test_save(self):
        xconfig.INI.write(self.blob, "text_out.ini" )


if __name__ == '__main__':
    unittest.main()
