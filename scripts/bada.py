import time
from math import pi, sin
import pickle
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

    def __init__(self, flight_levels, file_name):
        self.flight_levels = flight_levels
        self.file_name = file_name
        self.cruise = {}
        self.climb = {}
        self.descent = {}

    def save(self):
        pickle.dump(self, open(self.file_name,"wb"))

    def __repr__(self):

        ptf_template = open("bada_ptf.template","rb").read()

        ptf_row_format = "{flight_level:3} |"\
            "{cruise_tas:5d} {cruise_fuelrate_low:6.1f} {cruise_fuelrate_nom:6.1f} {cruise_fuelrate_high:6.1f} |"\
            "{climb_tas:5d} {climb_roc_low:5d} {climb_roc_nom:4d} {climb_roc_high:4d} {climb_fuelrate_nom:8.1f}  |"\
            "{descent_tas:5d} {descent_rod:6d} {descent_fuelrate:7.1f}\n"\
            "    |                           |                                |                     \n"

        modes = ["low", "nom", "high"]
        table = ""

        # conversions
        pps2kgpm = 27.2155422
        fps2fpm = 60
        lbs2kg = 0.453592

        # write table entries
        # TODO multi engine, fuel flow rate
        for fl in self.flight_levels:
            fl_str = str(fl)
            table += ptf_row_format.format(
                    flight_level=int(fl),
                    cruise_tas=int(self.cruise[fl_str]["nom"]["ic/vt-kts"]),
                    cruise_fuelrate_low=pps2kgpm*
                        self.cruise[fl_str]["low"]["propulsion/engine/fuel-flow-rate-pps"],
                    cruise_fuelrate_nom=pps2kgpm*
                        self.cruise[fl_str]["nom"]["propulsion/engine/fuel-flow-rate-pps"],
                    cruise_fuelrate_high=pps2kgpm*
                        self.cruise[fl_str]["high"]["propulsion/engine/fuel-flow-rate-pps"],
                    climb_tas=int(self.climb[fl_str]["nom"]["ic/vt-kts"]),
                    climb_roc_low= int(
                        sin(pi/180*self.climb[fl_str]["low"]["ic/gamma-deg"])*
                        self.climb[fl_str]["nom"]["ic/vt-fps"]*fps2fpm),
                    climb_roc_nom= int(
                        sin(pi/180*self.climb[fl_str]["nom"]["ic/gamma-deg"])*
                        self.climb[fl_str]["nom"]["ic/vt-fps"]*fps2fpm),
                    climb_roc_high= int(
                        sin(pi/180*self.climb[fl_str]["high"]["ic/gamma-deg"])*
                        self.climb[fl_str]["high"]["ic/vt-fps"]*fps2fpm),
                    climb_fuelrate_nom=pps2kgpm*
                        self.climb[fl_str]["nom"]["propulsion/engine/fuel-flow-rate-pps"],
                    descent_tas=int(self.descent[fl_str]["ic/vt-kts"]),
                    descent_rod=-int(
                        sin(pi/180*self.descent[fl_str]["ic/gamma-deg"])*
                        self.descent[fl_str]["ic/vt-fps"]*fps2fpm),
                    descent_fuelrate=pps2kgpm*
                        self.descent[fl_str]["propulsion/engine/fuel-flow-rate-pps"],
                )

        fl_key = self.cruise.keys()[0]
        alts = [] 
        for fl in self.cruise.keys():
            alts.append(100*float(fl))
        max_alt=max(alts)

        return ptf_template.format(
            table=table,
            date=time.strftime("%b %d %Y"),
            name=self.file_name,

            climb_cas_low=int(self.climb[fl_key]["low"]["ic/vc-kts"]),
            climb_cas_high=int(self.climb[fl_key]["high"]["ic/vc-kts"]),
            climb_mach=self.climb[fl_key]["nom"]["ic/mach"],

            cruise_cas_low=int(self.cruise[fl_key]["low"]["ic/vc-kts"]),
            cruise_cas_high=int(self.cruise[fl_key]["high"]["ic/vc-kts"]),
            cruise_mach=self.cruise[fl_key]["nom"]["ic/mach"],

            descent_cas_low=int(self.descent[fl_key]["ic/vc-kts"]),
            descent_cas_high=int(self.descent[fl_key]["ic/vc-kts"]),
            descent_mach=self.descent[fl_key]["ic/mach"],

            low_mass=int(self.cruise[fl_key]["low"]["inertia/weight-lbs"]*lbs2kg),
            nom_mass=int(self.cruise[fl_key]["nom"]["inertia/weight-lbs"]*lbs2kg),
            high_mass=int(self.cruise[fl_key]["high"]["inertia/weight-lbs"]*lbs2kg),

            max_alt=int(max_alt),
        )

    @classmethod
    def from_fdm(cls, fdm, flight_levels, file_name):

        data = cls(flight_levels, file_name);
        solver = BinarySolver(verbose=False)

        for fl in flight_levels:

            # flight level as string
            fl_str = str(fl)

            # calculate altitude from flight level
            alt = 100*fl
            # can't fly on ground
            if alt <= 10: alt = 100
            fdm.set_property_value("ic/h-agl-ft", alt)

            print "=================================="
            print "flight level: {}\n".format(fl)
            print "=================================="

            # cruise
            data.cruise[fl_str] = {}
            fdm.set_property_value("ic/gamma-deg", 0)
            for mode in ["low", "nom", "high"]:
                start = time.time()
                fdm.setup_bada_trim(mode)
                try:
                    fdm.do_simplex_trim(0)
                except RuntimeError as e:
                    print e
                    break
                # run once to calculate fuel flow rate
                fdm.run()

                data.cruise[fl_str][mode] = fdm.get_property_catalog("/")

                #print "i: {} pps: {}\n".format(i,
                    #data.cruise[fl_str][mode]["propulsion/engine/fuel-flow-rate-pps"])

                print "\ncruise {} trim finished:\n" \
                    "elapsed time\t: {} sec\n".format(mode,
                    time.time()-start)

            # max climb rate
            data.climb[fl_str] = {}
            for mode in ["low", "nom", "high"]:
                start = time.time()
                fdm.setup_bada_trim(mode)
                try:
                    solver.solve(TrimPropertyProblem("ic/gamma-deg",fdm),
                        prob_type="max", x_guess=0, x_min=0, x_max=50, tol=0.1)
                except RuntimeError as e:
                    print e
                    break
                fdm.run()
                data.climb[fl_str][mode] = fdm.get_property_catalog("/")
                print "\nmax climb {} trim finished:\n" \
                    "elapsed time\t: {} sec\ngamma\t: {}\n".format(
                        mode,
                        time.time()-start,
                        fdm.get_property_value("ic/gamma-deg"))

            # max descent rate
            data.descent[fl_str] = {}
            start = time.time()
            fdm.setup_bada_trim("nom")
            try:
                solver.solve(TrimPropertyProblem("ic/gamma-deg",fdm),
                    prob_type="min", x_guess=0, x_min=-50, x_max=0, tol=0.1)
            except RuntimeError as e:
                print e
                break
            fdm.run()
            data.descent[fl_str] = fdm.get_property_catalog("/")
            print "\nmax descent trim finished:\n" \
                "elapsed time\t: {} sec\ngamma\t: {}\n".format(
                time.time()-start, fdm.get_property_value("ic/gamma-deg"))

            # save data after each step
            data.save()

        return data
