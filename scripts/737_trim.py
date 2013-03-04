import devpath
from pyjsbsim.jsbsim import FGFDMExec
from utils import BinarySolver
import time
import numpy as np
import pickle

class FDM737(FGFDMExec):

    def __init__(self):
        super(FDM737, self).__init__()

        self.set_root_dir("/usr/local/share/JSBSim/")
        self.set_aircraft_path("aircraft")
        self.set_engine_path("engine")
        self.set_systems_path("systems")
        self.load_model("737")
   
        #print self.query_property_catalog("/")

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
        self.fdm.set_property_value("ic/gamma-deg", param)
        # why is the negative sign there?
        print 'gamma: ', -self.fdm.get_property_value("ic/gamma-deg")

    def solve(self):
        result = {}
        try:
            self.fdm.do_simplex_trim(0)
            result['status'] = 'optimal'
        except RuntimeError as e:
            result['status'] = 'exception'
        return result

class BadaData(object):

    def __init__(self, vels, alts):
        self.vels = vels
        self.alts = alts
        self.catalog =[[0]*len(vels)]*len(alts)

    def __repr__(self):
        return "BADA Data:\n{}".format(str(self.catalog))

    @classmethod
    def from_fdm(cls, fdm, vels, alts):

        data = cls(vels, alts);
        solver = BinarySolver(verbose=False)

        for i_vel in range(len(vels)):
            fdm.set_property_value("ic/vt-fps", vels[i_vel])

            for i_alt in range(len(alts)):
                fdm.set_property_value("ic/h-agl-ft", alts[i_alt])

                print "vt-fps: {}\nh-agl-ft: {}\n".format(
                    fdm.get_property_value("ic/vt-fps"),
                    fdm.get_property_value("ic/h-agl-ft"))

                start = time.time()

                solver.solve(MaxFlightPathAngleProblem(fdm),
                    x_guess=0, x_min=-50, x_max=50, tol=0.1, speed=0.5)

                data.catalog[i_vel][i_alt] = fdm.get_property_catalog("/")

                print "elapsed time: {} sec\n".format(time.time()-start)
                print "gamma-deg: {}\n".format(fdm.get_property_value("ic/gamma-deg"))
        return data

bada_data_737 = BadaData.from_fdm(
    fdm=FDM737(),
    vels=np.linspace(700,800,1),
    alts=np.linspace(10000,30000,1))

pickle.dump(bada_data_737, open("save.bada_data_737","wb"))

bada_data_737 = pickle.load(open("save.bada_data_737","rb"))

print bada_data_737
