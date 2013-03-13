import devpath
from pyjsbsim import FGFDMExec
import time
import numpy as np
import pickle
import os
from pyjsbsim.bada import BadaData

class ScanEagle(FGFDMExec):

    def __init__(self):
        self.find_root_dir([os.environ.get("UASNAS")])
        self.set_debug_level(0)
        self.load_model("scaneagle")
        print self.print_property_catalog()
        # turn on engine
        self.set_property_value("propulsion/starter_cmd", 1)
        self.set_property_value("propulsion/magneto_cmd", 3)
        self.set_property_value("fcs/mixture-cmd-norm", 1)
        self.propulsion_init_running(0)
        
    def setup_bada_trim(self, mode):

        self.set_property_value("fcs/aileron-cmd-norm", 0.0)
        self.set_property_value("fcs/elevator--cmd-norm", 0.0)
        self.set_property_value("fcs/rudder-cmd-norm", 0.0)
        self.set_property_value("fcs/throttle-cmd-norm", 0.5)

        self.set_property_value("ic/vc-kts", 48)
        self.set_property_value("ic/lat-gc-deg", 0.0)
        self.set_property_value("ic/lon-gc-deg", 0.0)
        self.set_property_value("ic/lat-gc-deg", 47.0)
        self.set_property_value("ic/lon-gc-deg", 122.0)
        self.set_property_value("ic/phi-deg", 0.0)
        self.set_property_value("ic/theta-deg", 0.0)
        self.set_property_value("ic/psi-deg", 0.0)
        if mode == "low":
            self.set_property_value("propulsion/tank[0]/contents-lbs", 0.1)
            self.set_property_value("propulsion/tank[1]/contents-lbs", 0.1)
            self.set_property_value("inertia/pointmass-weight-lbs", 0)
        elif mode == "nom":
            self.set_property_value("propulsion/tank[0]/contents-lbs", 0.87)
            self.set_property_value("propulsion/tank[1]/contents-lbs", 0.87)
            self.set_property_value("inertia/pointmass-weight-lbs", 6.26)
        elif mode == "high":
            self.set_property_value("propulsion/tank[0]/contents-lbs", 1.74)
            self.set_property_value("propulsion/tank[1]/contents-lbs", 1.74)
            self.set_property_value("inertia/pointmass-weight-lbs", 12.52)
        else:
            raise IOError("unknown mode")
        for item in ["ic/h-agl-ft","ic/vc-kts","ic/vt-kts"]:
            print "{}\t: {}".format(item, self.get_property_value(item))

file_name = "save.bada_data_scaneagle-" + time.strftime("%m_%d_%y__%H_%M")
bada_data = BadaData.from_fdm(
    fdm=ScanEagle(),
    flight_levels = np.array([
        0, 5, 10, 15, 20, 30, 40, 60, 80, 100,
        120, 140, 160, 180, 200]),
    file_name=file_name,
    verbose=True)
bada_data_loaded = pickle.load(open(file_name,"rb"))

print bada_data_loaded
