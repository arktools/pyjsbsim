cdef extern from "FGFDMExec.h" namespace "JSBSim":
    cdef cppclass c_FGFDMExec "JSBSim::FGFDMExec":
        c_FGFDMExec(int, int)

cdef class FGFDMExec:
    cdef c_FGFDMExec *thisptr      # hold a C++ instance which we're wrapping
    def __cinit__(self):
        self.thisptr = new c_FGFDMExec(0,0)
    def __dealloc__(self):
        del self.thisptr
    def __repr__(self):
        return "FGFDMExec"
