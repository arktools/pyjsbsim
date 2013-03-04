import devpath
from pyjsbsim.jsbsim import FGFDMExec

fdm = FGFDMExec()

fdm.set_root_dir("/usr/local/share/JSBSim/")
fdm.set_aircraft_path("aircraft")
fdm.set_engine_path("engine")
fdm.set_systems_path("systems")
fdm.load_model("737")

print 'catalog\n', fdm.query_property_catalog("/")

fdm.set_property_value("ic/vt-fps", 750.0)
fdm.set_property_value("ic/h-agl-ft", 30000.0)
fdm.set_property_value("ic/gamma-deg", 30000.0)
fdm.set_property_value("ic/lat-gc-deg", 47.0)
fdm.set_property_value("ic/lon-gc-deg", 122.0)
fdm.set_property_value("ic/phi-deg", 0.0)
fdm.set_property_value("ic/theta-deg", 0.0)
fdm.set_property_value("ic/psi-deg", 0.0)

vels = [700, 710, 720, 730, 1000, 700]
for i in range(len(vels)):
    fdm.set_property_value("ic/vt-fps", vels[i])
    trimComplete = False
    try:
        fdm.do_simplex_trim(0)
        trimComplete = True
    except:
        pass

    if trimComplete:
        print "trim ok"
