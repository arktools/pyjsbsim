from libcpp.string cimport string

cdef extern from "FGFDMExec.h" namespace "JSBSim":
    cdef cppclass c_FGFDMExec "JSBSim::FGFDMExec":
        c_FGFDMExec(int root, int fdmctr)
        bool SetEnginePath(string path)
