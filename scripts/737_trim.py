import devpath
from pyjsbsim.jsbsim import FGFDMExec
from utils import BinarySolver
import time
import numpy as np

class FDM737(FGFDMExec):

    def __init__(self):
        super(FDM737, self).__init__()

        self.set_root_dir("/usr/local/share/JSBSim/")
        self.set_aircraft_path("aircraft")
        self.set_engine_path("engine")
        self.set_systems_path("systems")
        self.load_model("737")

        #print 'catalog\n', fdm.query_property_catalog("/")

        self.set_property_value("ic/vt-fps", 750.0)
        self.set_property_value("ic/h-agl-ft", 30000.0)
        self.set_property_value("ic/gamma-deg", 0.0)
        self.set_property_value("ic/lat-gc-deg", 47.0)
        self.set_property_value("ic/lon-gc-deg", 122.0)
        self.set_property_value("ic/phi-deg", 0.0)
        self.set_property_value("ic/theta-deg", 0.0)
        self.set_property_value("ic/psi-deg", 0.0)

        self.set_property_value("trim/solver/iterMax", 300)
        self.set_property_value("trim/solver/showConvergence", False)
        self.set_property_value("trim/solver/showSimplex", False)
        self.set_property_value("trim/solver/pause", False)

class MaxFlightPathAngleProblem(object):

    def __init__(self, fdm):
        self.fdm = fdm

    def setup(self, param):
        self.fdm.set_property_value("ic/gamma-deg", -param)
        #print 'gamma: ', self.fdm.get_property_value("ic/gamma-deg")

    def solve(self):
        result = {}
        try:
            self.fdm.do_simplex_trim(0)
            result['status'] = 'optimal'
        except RuntimeError as e:
            result['status'] = 'exception'
        return result

def generate_bada_data(fdm, vels, alts):

    gamma_table = []
    solver = BinarySolver(verbose=False)

    for i_vel in range(len(vels)):
        fdm.set_property_value("ic/vt-fps", vels[i_vel])
        gamma_table.append([])

        for i_alt in range(len(alts)):
            fdm.set_property_value("ic/h-agl-ft", alts[i_alt])

            print "vt-fps: {}\nh-agl-ft: {}\n".format(
                fdm.get_property_value("ic/vt-fps"),
                fdm.get_property_value("ic/h-agl-ft"))

            start = time.time()

            solver.solve(MaxFlightPathAngleProblem(fdm),
                x_guess=0, x_min=-50, x_max=50, tol=0.1, speed=0.5)


            gamma_table[i_vel].append(fdm.get_property_value("ic/gamma-deg"))

            print "elapsed time: {} sec\n".format(time.time()-start)
            print "gamma-deg: {}\n".format(
                fdm.get_property_value("ic/gamma-deg"))

    data = {}
    data['gamma_table'] = gamma_table
    return data


bada_data = generate_bada_data(
    fdm=FDM737(),
    vels=np.linspace(700,800,2),
    alts=np.linspace(10000,30000,2))

print bada_data['gamma_table']
