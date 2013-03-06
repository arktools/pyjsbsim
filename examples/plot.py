import devpath
from pyjsbsim import FGFDMExec
from pylab import *

# load
fdm = FGFDMExec(debug_level=0)
fdm.load_model("f16")

# trim
fdm.set_property_value("ic/h-agl-ft",1000)
fdm.set_property_value("ic/vc-kts",400)
fdm.set_property_value("ic/gamma-deg",0)
fdm.do_trim(0)

# simulate
(t,y) = fdm.simulate(
    t_final=10,
    dt=0.1,
    record_properties=["position/h-agl-ft", "attitude/theta-deg"])

# plot
title("test")
xlabel("t, sec")
ylabel("h-agl, ft")
plot(t,y["position/h-agl-ft"])
show()
