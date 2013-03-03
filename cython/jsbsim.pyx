from libcpp cimport bool
from libcpp.string cimport string

# the c++ adaptor class
cdef extern from "FGFDMExec.h" namespace "JSBSim":
    cdef cppclass c_FGFDMExec "JSBSim::FGFDMExec":

        ###########################################
        # ctor
        ###########################################
        c_FGFDMExec(int root, int fdmctr)

        ###########################################
        # run functions
        ###########################################
        void Run()
        void RunIC()

        ###########################################
        # load functions
        ###########################################
        bool LoadModel(string model,
                       bool add_model_to_path)

        bool LoadModel(string aircraft_path,
                       string engine_path,
                       string systems_path,
                       string model,
                       bool add_model_to_path)
        bool LoadScript(string script, double delta_t, string initfile)

        ###########################################
        # set functions
        ###########################################
        bool SetEnginePath(string path)
        bool SetAircraftPath(string path)
        bool SetSystemsPath(string path)
        void SetRootDir(string path) 
        
        ###########################################
        # get functions
        ###########################################
        string GetEnginePath()
        string GetAircraftPath()
        string GetSystemsPath()
        string GetRootDir()
        string GetModelName()

# this is the python wrapper class
cdef class FGFDMExec:

    ###########################################
    #python basics
    ###########################################

    cdef c_FGFDMExec *thisptr      # hold a C++ instance which we're wrapping

    def __cinit__(self):
        self.thisptr = new c_FGFDMExec(0,0)

    def __dealloc__(self):
        del self.thisptr

    def __repr__(self):
        return "FGFDMExec \n" \
            "root dir\t:\t{}\n" \
            "aircraft path\t:\t{}\n" \
            "engine path\t:\t{}\n" \
            "systems path\t:\t{}\n" \
                .format(
                self.get_root_dir(),
                self.get_aircraft_path(),
                self.get_engine_path(),
                self.get_systems_path())

    ###########################################
    # run functions
    ###########################################

    def run(self):
        self.thisptr.Run()

    def run_ic(self):
        self.thisptr.RunIC()

    ###########################################
    # load functions
    ###########################################

    def load_model(self, model, add_model_to_path = True):
        return self.thisptr.LoadModel(model, add_model_to_path)

    def load_model(self, model, aircraft_path,
                   engine_path, systems_path, add_model_to_path = True):
        return self.thisptr.LoadModel(model, add_model_to_path)

    ###########################################
    # set functions
    ###########################################
    def set_engine_path(self, path):
        return self.thisptr.SetEnginePath(path)

    def set_aircraft_path(self, path):
        return self.thisptr.SetAircraftPath(path)

    def set_systems_path(self, path):
        return self.thisptr.SetSystemsPath(path)

    def set_root_dir(self, path):
        self.thisptr.SetRootDir(path)

    ###########################################
    # get funtions
    ###########################################
    
    def get_engine_path(self):
        return self.thisptr.GetEnginePath()

    def get_aircraft_path(self):
        return self.thisptr.GetAircraftPath()

    def get_systems_path(self):
        return self.thisptr.GetSystemsPath()

    def get_root_dir(self):
        return self.thisptr.GetRootDir()

    def get_model_name(self):
        return self.thisptr.GetModelName()
