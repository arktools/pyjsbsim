from libcpp.string cimport string
cimport jsbsim

cdef class FGFDMExec:
    cdef c_FGFDMExec *thisptr      # hold a C++ instance which we're wrapping
    def __cinit__(self):
        self.thisptr = new c_FGFDMExec(0,0)
        a = setEnginePath("hello")
        print 'a: ', a
    def __dealloc__(self):
        del self.thisptr
    def __repr__(self):
        return "FGFDMExec"
    def setEnginePath(self,path):
        return self.thisptr.SetEnginePath(path)
