import unittest
import xconfig


def create_definition():
    d = xconfig.Definition()
    d.append(xconfig.Entry('RootEntry1', default=True))
    return d


class IniTest(unittest.TestCase):
    def test_load(self):
        definition = create_definition()
        self.assertIsNotNone(definition)

if __name__ == '__main__':
    unittest.main()
