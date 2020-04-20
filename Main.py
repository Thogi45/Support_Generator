import os,sys, glob
import time
from stl import mesh, Mesh
import numpy as np



print("----------------------------------------\n")
print("            SUPPORT GENERATOR              \n")
print("by Thomas Heissel and Thomas Girerd       ")
print("----------------------------------------\n")
print("You need to choose the STL file you want to generate supports with.")


time.sleep(1)

import Locate_STL
my_mesh= mesh.Mesh.from_file(Locate_STL.STL1)
normal=my_mesh.normals
vertices= my_mesh.points
from Support_finder import support_45deg_rule
from Support_finder import needed_support_Bridge_rule
support_angle=support_45deg_rule(normal,vertices)
support_bridge=needed_support_Bridge_rule(normal,vertices)
i=0
p=len(support_bridge)
k=0;
while i<p:
    if all(support_bridge[k][0,0:9]== 0):
        del support_bridge[k]
    else:
        k=k+1

    p=p-1
liste_support=[]
liste_support=support_bridge+support_angle

from Support_Generator import AreasWithSameAngle
from Support_Generator import FindContour
from Support_Generator import Projection
ListeContour=[]
for i in range(len(liste_support)):
    A=AreasWithSameAngle(liste_support[i])
    ListeContour.append(FindContour(A))

'''ListeProjete=Projection(ListeContour)
print(ListeProjete[:][:][:][:])
ListeZone = np.concatenate((ListeProjete[0][0][:][:], ListeProjete[1][0][:][:]),axis=0)
print(ListeZone)
print(np.shape(ListeZone))

print(np.shape(ListeProjete[:][][:][:]))
print(np.shape(ListeProjete))'''

from Support_Shape import Rectangular_simple_support
from Support_Shape import plot
List_shape= np.shape(ListeProjete)
'''for i in range (0,List_shape[1]):
    Rec=Rectangular_simple_support(ListeProjete[:][i][:][:])
    print(ListeProjete[:][i][:][:])
    plot(Rec,1,my_mesh)'''

#Rec=Rectangular_simple_support(ListeProjete)
#plot(Rec,1,my_mesh)



