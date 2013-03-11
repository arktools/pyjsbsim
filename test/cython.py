import devpath
import unittest
import os
from pyjsbsim import FGFDMExec

class TestCython(unittest.TestCase):
    
    def setup(self):
        pass

    def test_construct(self):
        fdm = FGFDMExec()

    def test_accessors(self):
        fdm = FGFDMExec()

        root_dir = "test_root"
        fdm.set_root_dir(root_dir)
        assert (root_dir == fdm.get_root_dir())

        engine_path = "engine"
        fdm.set_engine_path(engine_path)
        assert (root_dir+engine_path == fdm.get_engine_path())

        aircraft_path = "aircraft"
        fdm.set_aircraft_path(aircraft_path)
        assert (root_dir+aircraft_path == fdm.get_aircraft_path())

        systems_path = "systems"
        fdm.set_systems_path(systems_path)
        assert (root_dir+systems_path == fdm.get_systems_path())

    def test_load_model(self):
        fdm = FGFDMExec()
        model = "f16"
        fdm.load_model(model)
        assert (model == fdm.get_model_name())

    def test_simulate(self):
        fdm = FGFDMExec()
        fdm.load_model("f16")
        fdm.simulate(verbose=True,dt=0.1,t_final=1)

if __name__ == '__main__':
    unittest.main()
