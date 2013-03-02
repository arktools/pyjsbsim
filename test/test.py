import unittest

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def test_FGFDMExec(self):
        from pyjsbsim.jsbsim import FGFDMExec
        a = FGFDMExec()
        print a
        del a

if __name__ == '__main__':
    unittest.main()
