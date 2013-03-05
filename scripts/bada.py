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

    def __init__(self, flight_levels):
        self.flight_levels = flight_levels
        self.cruise =[{}]*len(flight_levels)
        self.climb =[{}]*len(flight_levels)
        self.descent =[{}]*len(flight_levels)

    def __repr__(self):
        return "BADA Data:\n"

    @classmethod
    def from_fdm(cls, fdm, flight_levels):

        data = cls(flight_levels);
        solver = BinarySolver(verbose=False)

        for i_fl in range(len(flight_levels)):
            alt = 100*flight_levels[i_fl]
            # can't fly on ground
            if alt <= 10: alt = 100
            fdm.set_property_value("ic/h-agl-ft", alt)

            print "=================================="
            print "flight level: h-agl-ft {}\n".format(
                fdm.get_property_value("ic/h-agl-ft"))
            print "=================================="

            # cruise
            fdm.set_property_value("ic/gamma-deg", 0)
            for mode in ["low", "nom", "high"]:
                start = time.time()
                fdm.setup_bada_trim(mode)
                fdm.do_simplex_trim(0)
                data.cruise[i_fl][mode] = fdm.get_property_catalog("/")
                print "\ncruise {} trim finished:\n" \
                    "elapsed time\t: {} sec\n".format(mode,
                    time.time()-start)

            # max climb rate
            for mode in ["low", "nom", "high"]:
                start = time.time()
                fdm.setup_bada_trim(mode)
                solver.solve(TrimPropertyProblem("ic/gamma-deg",fdm),
                    prob_type="max", x_guess=0, x_min=0, x_max=50, tol=0.1)
                data.climb[i_fl][mode] = fdm.get_property_catalog("/")
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
            data.descent[i_fl] = fdm.get_property_catalog("/")
            print "\nmax descent trim finished:\n" \
                "elapsed time\t: {} sec\ngamma\t: {}\n".format(
                time.time()-start, fdm.get_property_value("ic/gamma-deg"))

        return data
