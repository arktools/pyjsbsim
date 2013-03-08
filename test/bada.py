import devpath
import unittest
import os
import time
import numpy as np
import pickle

from pyjsbsim import FGFDMExec
from pyjsbsim.bada import BadaData

class TestBADA(unittest.TestCase):
    
    def setup(self):
        pass

    def test_f16(self):
        
        class FDMF16(FGFDMExec):

            def __init__(self):
                self.find_root_dir()
                self.load_model("f16")

            def setup_bada_trim(self, mode):
                self.set_property_value("ic/vc-kts", 600)
                self.set_property_value("ic/lat-gc-deg", 0.0)
                self.set_property_value("ic/lon-gc-deg", 0.0)
                self.set_property_value("ic/lat-gc-deg", 47.0)
                self.set_property_value("ic/lon-gc-deg", 122.0)
                self.set_property_value("ic/phi-deg", 0.0)
                self.set_property_value("ic/theta-deg", 0.0)
                self.set_property_value("ic/psi-deg", 0.0)
                if mode == "low":
                    for i_tank in range(3):
                        self.set_property_value("propulsion/tank[{}]/contents-lbs".format(i_tank), 1)
                elif mode == "nom":
                    for i_tank in range(3):
                        self.set_property_value("propulsion/tank[{}]/contents-lbs".format(i_tank), 5000)
                elif mode == "high":
                    for i_tank in range(3):
                        self.set_property_value("propulsion/tank[{}]/contents-lbs".format(i_tank), 10000)
                else:
                    raise IOError("unknown mode")
                for item in ["ic/h-agl-ft","ic/vc-kts","ic/vt-kts"]:
                    print "{}\t: {}".format(item,self.get_property_value(item))

        file_name = "save.bada_data_f16-" + time.strftime("%m_%d_%y__%H_%M")
        bada_data = BadaData.from_fdm(
            fdm=FDMF16(),
            flight_levels = np.array([0, 5]),
            file_name=file_name,
            verbose=False)
        bada_data_loaded = pickle.load(open(file_name,"rb"))

        print bada_data_loaded

if __name__ == '__main__':
    unittest.main()
