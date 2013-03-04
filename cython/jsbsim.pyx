from libcpp cimport bool
from libcpp.string cimport string

cdef extern from "JSBSim/FGFDMExec.h" namespace "JSBSim":
    cdef cppclass c_FGFDMExec "JSBSim::FGFDMExec":
        c_FGFDMExec(int root, int fdmctr)
        void Unbind()
        void Run()
        void RunIC()
        bool LoadModel(string model,
                       bool add_model_to_path)
        bool LoadModel(string aircraft_path,
                       string engine_path,
                       string systems_path,
                       string model,
                       bool add_model_to_path)
        bool LoadScript(string script, double delta_t, string initfile)
        bool SetEnginePath(string path)
        bool SetAircraftPath(string path)
        bool SetSystemsPath(string path)
        void SetRootDir(string path) 
        string GetEnginePath()
        string GetAircraftPath()
        string GetSystemsPath()
        string GetRootDir()
        double GetPropertyValue(string property)
        void SetPropertyValue(string property, double value)
        string GetModelName()
        bool SetOutputDirectives(string fname)
        void ForceOutput(int idx=0)
        void SetLoggingRate(double rate)
        bool SetOutputFileName(string fname)
        string GetOutputFileName()
        void DoTrim(int mode)
        void DoSimplexTrim(int mode)
        void DoLinearization(int mode)
        void DisableOutput()
        void EnableOutput()
        void Hold()
        void EnableIncrementThenHold(int time_steps)
        void CheckIncrementalHold()
        void Resume()
        bool Holding()
        void ResetToInitialConditions()
        void SetDebugLevel(int level)
        string QueryPropertyCatalog(string check)
        void PrintPropertyCatalog()
        void SetTrimStatus(bool status)
        bool GetTrimStatus()
        string GetPropulsionTankReport()
        double GetSimTime() 
        double GetDeltaT()
        void SuspendIntegration()
        void ResumeIntegration()
        bool IntegrationSuspended()
        bool Setsim_time(double cur_time)
        void Setdt(double delta_t)
        double IncrTime() 
        int GetDebugLevel()   

# this is the python wrapper class
cdef class FGFDMExec:

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

    def run(self):
        self.thisptr.Run()

    def run_ic(self):
        self.thisptr.RunIC()

    def load_model(self, model, add_model_to_path = True):
        return self.thisptr.LoadModel(model, add_model_to_path)

    def load_model(self, model, aircraft_path,
                   engine_path, systems_path, add_model_to_path = True):
        return self.thisptr.LoadModel(model, add_model_to_path)

    def set_engine_path(self, path):
        return self.thisptr.SetEnginePath(path)

    def set_aircraft_path(self, path):
        return self.thisptr.SetAircraftPath(path)

    def set_systems_path(self, path):
        return self.thisptr.SetSystemsPath(path)

    def set_root_dir(self, path):
        self.thisptr.SetRootDir(path)

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
