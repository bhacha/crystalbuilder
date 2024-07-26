import importlib.util
#default path for current release 
spec_win = importlib.util.spec_from_file_location('lumapi', 'C:\\Program Files\\Lumerical\\v231\\api\\python\\lumapi.py')
#Functions that perform the actual loading
lumapi = importlib.util.module_from_spec(spec_win) #windows
spec_win.loader.exec_module(lumapi)

fdtd = lumapi.FDTD()

fdtd.addstructuregroup(name="A")

fdtd.addrect(name="in A")
