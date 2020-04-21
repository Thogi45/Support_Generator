import os,sys, glob
import time
from stl import mesh, Mesh
import numpy as np
from Support_finder import support_45deg_rule
from Support_finder import needed_support_Bridge_rule
from Support_Generator import AreasWithSameAngle
from Support_Generator import FindContour
from Support_Generator import Projection
from Support_Shape import line_support
from Support_Shape import Rectangular_simple_support
from Support_Shape import gridxy
from Support_Shape import ZigZag
from Support_Shape import plot
from Hello import ShapeChoice



print("----------------------------------------\n")
print("            SUPPORT GENERATOR              \n")
print("by Thomas Heissel and Thomas Girerd       ")
print("----------------------------------------\n")
print("You need to choose the STL file you want to generate supports with.")




import Locate_STL
my_mesh= mesh.Mesh.from_file(Locate_STL.STL1)
normal=my_mesh.normals
vertices= my_mesh.points
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
ListeContour=[]
for i in range(len(liste_support)):
    A=AreasWithSameAngle(liste_support[i])
    ListeContour.append(FindContour(A))
ListeProjete=Projection(ListeContour)

if len(ListeProjete)==0:
    print("you do not need any support")
else:
    Choice=ShapeChoice()
    print(ListeProjete[:][0][:][:])
    List_shape= np.shape(ListeProjete)
    print(List_shape)
    Faces=[]
    if Choice==1:
        for i in range (0,List_shape[0]):
            Rec=Rectangular_simple_support(ListeProjete[:][i][:][:])
            Faces.append(Rec)
        if List_shape[0]==1:
            Faces = Rec
        if List_shape[0]==2:
            Faces=np.concatenate((Faces[0],Faces[1]),axis=0)
        elif List_shape[0]==3:
            Faces=np.concatenate((Faces[0],Faces[1],Faces[2]),axis=0)
        elif List_shape[0]==4:
            Faces=np.concatenate((Faces[0],Faces[1],Faces[2],Faces[3]),axis=0)
        else:
            print("Pb, too much zones, modify code in main.py")
    elif Choice==2:
        for i in range (0,List_shape[0]):
            Rec=gridxy(ListeProjete[:][i][:][:],1)
            Faces.append(Rec)
        if List_shape[0]==1:
            Faces = Rec
        elif List_shape[0]==2:
            Faces=np.concatenate((Faces[0],Faces[1]),axis=0)
        elif List_shape[0]==3:
            Faces=np.concatenate((Faces[0],Faces[1],Faces[2]),axis=0)
        elif List_shape[0]==4:
            Faces=np.concatenate((Faces[0],Faces[1],Faces[2],Faces[3]),axis=0)
        else:
            print("Pb, too much zones, modify code in main.py")
    elif Choice==3:
        for i in range (0,List_shape[1]):
            Rec=ZigZag(ListeProjete[:][i][:][:],1)
            Faces.append(Rec)
        if List_shape[0]==1:
            Faces = Rec
        elif List_shape[0]==2:
            Faces=np.concatenate((Faces[0],Faces[1]),axis=0)
        elif List_shape[0]==3:
            Faces=np.concatenate((Faces[0],Faces[1],Faces[2]),axis=0)
        elif List_shape[0]==4:
            Faces=np.concatenate((Faces[0],Faces[1],Faces[2],Faces[3]),axis=0)
        else:
            print("Pb, too much zones, modify code in main.py")

plot(Faces,1,my_mesh)



