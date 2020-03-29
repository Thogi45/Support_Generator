from stl import mesh
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

#Plot normal to mesh
my_mesh= mesh.Mesh.from_file('C:\\Users\\thoma\\PycharmProjects\\Support_Generator\\Y_40.stl')
normal=my_mesh.normals
vertices= my_mesh.points
Shape_normal= np.shape(normal)
Normal_dir_start1= np.zeros((Shape_normal[0],6))
Normal_dir_start2= np.zeros((Shape_normal[0],6))
Normal_dir_start3= np.zeros((Shape_normal[0],6))
for i in range (0,Shape_normal[0]):
    Normal_dir_start1[i,:]= np.array([vertices[i,0], vertices[i,1], vertices[i,2],normal[i,0],normal[i,1],normal[i,2]])
    Normal_dir_start2[i,:]= np.array([vertices[i,3], vertices[i,4], vertices[i,5],normal[i,0],normal[i,1],normal[i,2]])
    Normal_dir_start3[i,:]= np.array([vertices[i,6], vertices[i,7], vertices[i,8],normal[i,0],normal[i,1],normal[i,2]])

X1,Y1,Z1,U1,V1,W1= zip(*Normal_dir_start1)
X2,Y2,Z2,U2,V2,W2= zip(*Normal_dir_start2)
X3,Y3,Z3,U3,V3,W3= zip(*Normal_dir_start3)
figure1 = plt.figure(1)
ax = figure1.add_subplot(111, projection='3d')
ax.quiver(X1,Y1,Z1,U1,V1,W1)
ax.quiver(X2,Y2,Z2,U2,V2,W2)
ax.quiver(X3,Y3,Z3,U3,V3,W3)
ax.add_collection3d(mplot3d.art3d.Poly3DCollection(my_mesh.vectors))
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.xlim(-50,50)
plt.ylim(-50,50)

def points_needed_support_45deg_rule (normal, vertices):
    #angle between reference z-axis and normal

    Shape_normal= np.shape(normal)
    Unit_vector_normals=np.zeros((Shape_normal[0], 3))
    dot_product=np.zeros((Shape_normal[0], 1))
    angle=np.zeros((Shape_normal[0],1))
    Vector_reference = np.array([[0],[0],[1]])

    #Mesh point that doesn't respect the 45° rule
    a=np.zeros((1,9))
    print(np.shape(Vector_reference))
    t=0
    for i in range (0,Shape_normal[0]):
        Unit_vector_normals[i,:]= normal[i,:]/np.linalg.norm(normal[i,:])
        dot_product[i,:]=np.dot(Unit_vector_normals[i,:],Vector_reference)
        angle[i,:]= np.arccos(dot_product[i,:])
        if np.abs(angle[i,:]) <= 0.785398 or (np.abs(angle[i,:]) >= 2.35619 and np.abs(angle[i,:]) <= 3.14159):
            t+=1
            b= np.array([vertices[i,:]])
            a=np.append(a,b,axis=0)
        else:
            pass
    return a

print(points_needed_support_45deg_rule (normal, vertices))
