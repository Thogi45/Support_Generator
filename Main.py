import os,sys, glob

from stl import mesh, Mesh
import subprocess

LocateSTL=os.path.dirname(sys.argv[0])
print("----------------------------------------\n")
print("            SUPPORT GENERATOR              \n")
print("by Thomas Heissel and Thomas Girerd       ")
print("----------------------------------------\n")
print("You need to choose the STL file you want to generate supports with.")

import Support_finder


