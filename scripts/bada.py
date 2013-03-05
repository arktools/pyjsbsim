import time
from utils import BinarySolver

class TrimPropertyProblem(object):

    def __init__(self, name, fdm):
        self.name = name
        self.fdm = fdm
        self.results = {}

    def setup(self, param):
        self.fdm.set_property_value(self.name, param)
        # XXX why is the minus sign needed here?
        #print self.name, -self.fdm.get_property_value(self.name)

    def solve(self):
        trimmed=False
        try:
            self.fdm.do_simplex_trim(0)
            trimmed=True
        except RuntimeError as e:
            #print e
            pass
        return trimmed

class BadaData(object):

    def __init__(self, vels, alts):
        self.vels = vels
        self.alts = alts
        self.cruise =[{}]*len(alts)
        self.climb =[{}]*len(alts)
        self.descent =[{}]*len(alts)

    def __repr__(self):
        return "BADA Data:\n"

    @classmethod
    def from_fdm(cls, fdm, vels, alts):

        data = cls(vels, alts);
        solver = BinarySolver(verbose=False)

        for i_alt in range(len(alts)):
            fdm.set_property_value("ic/h-agl-ft", alts[i_alt])

            print "vc-kts: {}\th-agl-ft: {}\n".format(
                fdm.get_property_value("ic/vc-kts"),
                fdm.get_property_value("ic/h-agl-ft"))

            # cruise
            fdm.set_property_value("ic/gamma-deg", 0)
            for mode in ["low", "nom", "high"]:
                start = time.time()
                fdm.setup_bada_trim(mode)
                fdm.do_simplex_trim(0)
                data.cruise[i_alt][mode] = fdm.get_property_catalog("/")
                print "\ncruise {} trim finished:\n" \
                    "elapsed time\t: {} sec\n".format(mode,
                    time.time()-start)

            # max climb rate
            for mode in ["low", "nom", "high"]:
                start = time.time()
                fdm.setup_bada_trim(mode)
                solver.solve(TrimPropertyProblem("ic/gamma-deg",fdm),
                    prob_type="max", x_guess=0, x_min=0, x_max=50, tol=0.1)
                data.climb[i_alt][mode] = fdm.get_property_catalog("/")
                print "\nmax climb {} trim finished:\n" \
                    "elapsed time\t: {} sec\ngamma\t: {}\n".format(
                        mode,
                        time.time()-start,
                        fdm.get_property_value("ic/gamma-deg"))

            # max decent rate
            start = time.time()
            fdm.setup_bada_trim("nom")
            solver.solve(TrimPropertyProblem("ic/gamma-deg",fdm),
                prob_type="min", x_guess=0, x_min=-50, x_max=0, tol=0.1)
            data.descent[i_alt] = fdm.get_property_catalog("/")
            print "\nmax descent trim finished:\n" \
                "elapsed time\t: {} sec\ngamma\t: {}\n".format(
                time.time()-start, fdm.get_property_value("ic/gamma-deg"))

        return data
