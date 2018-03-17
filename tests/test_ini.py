import unittest
import xconfig


class IniTest(unittest.TestCase):
    def setUp(self):
        d = xconfig.Definition()
        d.append(xconfig.Option('Root_Option1', xconfig.Boolean, default=True))
        d.append(xconfig.Option('Root_Username', xconfig.String, required=True, hidden=True))
        self.definition = d

    def test_load(self):
        assert(self.definition.load("test.ini", file_type=xconfig.FileType.INI, monitor_file=False))


if __name__ == '__main__':
    unittest.main()
