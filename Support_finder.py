from stl import mesh
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import math


#Plot normal to mesh

import Locate_STL
my_mesh= mesh.Mesh.from_file(Locate_STL.STL1)



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
ax.quiver(X2,Y2,Z2, U2,V2,W2)
ax.quiver(X3,Y3,Z3,U3,V3,W3)
ax.add_collection3d(mplot3d.art3d.Poly3DCollection(my_mesh.vectors))
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.xlim(-50,50)
plt.ylim(-50,50)
ax.set_zlim(0,50)

def support_45deg_rule (normal, vertices):
    '''
    45° rule for overhangs
    If an overhang tilts at an angle less than 45 degress from the vertical it requires 3D printing support structures.
    '''
    #angle between reference z-axis and normal

    Shape_normal= np.shape(normal)
    Shape_vertices=np.shape(vertices)
    Unit_vector_normals=np.zeros((Shape_normal[0], 3))
    dot_product=np.zeros((Shape_normal[0], 1))
    angle=np.zeros((Shape_normal[0],1))
    Vector_reference = np.array([[0],[0],[1]])

    #Mesh point that doesn't respect the 45° rule
    A=np.zeros((1,9))
    An=np.zeros((1,1))
    a=np.zeros((0,9))
    x=np.zeros((0,3))
    y=np.zeros((0,3))
    z=np.zeros((0,3))
    t=0
    for i in range (0,Shape_normal[0]):
        Unit_vector_normals[i,:]= normal[i,:]/np.linalg.norm(normal[i,:])
        dot_product[i,:]=np.dot(Unit_vector_normals[i,:],Vector_reference)
        angle[i,:]= np.arccos(dot_product[i,:])
        if np.abs(angle[i,:]) <= 0.785398 or (np.abs(angle[i,:]) >= 2.35619 and np.abs(angle[i,:]) <= 3.14159):
            b= np.array([vertices[i,:]])
            a=np.append(a,b,axis=0)
            t+=1
        else:
            angle[i,:]=An[0,0]
            pass
    Shape_support=np.shape(a)
    l=0
    for j in range (0, Shape_support[0]):
        for k in range (0, Shape_support[0]):
            d1=0
            d2=0
            d3=0
            if a[j,2]==a[j,5]==a[j,8]:
                a[j,:]=A[0,:]
            else:
                for l in range (0,2):
                    if a[j,2] != a[k,3*l+2]:
                        d1+=1
                    else:
                        pass
                    if a[j,5] != a[k,3*l+2]:
                        d2+=1
                    else:
                        pass
                    if a[j,8] != a[k,3*l+2]:
                        d3+=1
                    else:
                        pass
                if d1==2 and d2==2 and d3==2 and (a[j,2]!=0 or a[j,5]!=0 or a[j,8]!=0) and (a[k,2]!=0 or a[k,5]!=0 or a[k,8]!=0):
                    if ((a[j,0]==a[k,l*3] or a[j,1]==a[k,l*3+1]) and (a[j,3]==a[k,l*3] or a[j,4]==a[k,l*3+1]) and (a[j,6]==a[k,l*3] or a[j,7]==a[k,l*3+1]) for l in range (0,2)):
                        if j==k:
                            pass
                        elif (a[j,2]+a[j,5]+a[j,8])>(a[k,2]+a[k,5]+a[k,8]):
                            a[j,:]=A[0,:]
                            angle[j,:]=An[0,:]
                        else:
                            a[k,:]=A[0,:]
                            angle[j,:]=An[0,:]
                    else:
                        pass
                else:
                    pass
    a=a[~np.all(a == 0, axis=1)]
    a_shape=np.shape(a)
    normal_support = np.zeros((0,3))
    for i in range (0, Shape_vertices[0]):
        for j in range (0, a_shape[0]):
            if vertices[i,0]==a[j,0] and vertices[i,1]==a[j,1] and vertices[i,2]==a[j,2] and vertices[i,3]==a[j,3] and vertices[i,4]==a[j,4] and vertices[i,5]==a[j,5] and vertices[i,6]==a[j,6] and vertices[i,7]==a[j,7] and vertices[i,8]==a[j,8]:
                b= np.array([normal[i,:]])
                normal_support=np.append(normal_support,b,axis=0)
            else:
                pass

    Shape_normal_support=np.shape(normal_support)
    Unit_vector_normals_support=np.zeros((Shape_normal_support[0], 3))
    dot_product_support=np.zeros((Shape_normal_support[0], 1))
    angle_support=np.zeros((Shape_normal_support[0],1))

    for i in range (0, Shape_normal_support[0]):
        Unit_vector_normals_support[i,:]= normal_support[i,:]/np.linalg.norm(normal_support[i,:])
        dot_product_support[i,:]=np.dot(Unit_vector_normals_support[i,:],Vector_reference)
        angle_support[i,:]= np.arccos(dot_product_support[i,:])
    i=0
    m=0
    Required_support = ["a1","a2","a3","a4","a5","a6","a7","a8","a9","a10","a11","a12","a13","a14","a15","a16","a17","a18","a19","a20","a21","a22","a23","a24","a25","a26","a27","a28","a29","a30"]
    while i<a_shape[0]:
        if i==0:
            Required_support[m]=a[i,:]
            m+=1
        else:
            x1=x2=x3=0
            y1=y2=y3=0
            z1=z2=z3=0
            if a[i,0] != a[i-1,0]:
                x1+=1
            else:
                pass
            if a[i,3] != a[i-1,3]:
                x2+=1
            else:
                pass
            if a[i,6] != a[i-1,6]:
                x3+=1
            else:
                pass
            if a[i,1] != a[i-1,1]:
                y1+=1
            else:
                pass
            if a[i,4] != a[i-1,4]:
                y2+=1
            else:
                pass
            if a[i,7] != a[i-1,7]:
                y3+=1
            else:
                pass
            if a[i,2] != a[i-1,2]:
                z1+=1
            else:
                pass
            if a[i,5] != a[i-1,5]:
                z2+=1
            else:
                pass
            if a[i,8] != a[i-1,8]:
                z3+=1
            if angle_support[i] != angle_support[i-1]:
                Required_support[m]=a[i,:]
                m+=1
            elif (x1+x2+x3+y1+y2+y3+z1+z2+z3)>3:
                Required_support[m]=a[i,:]
                m+=1
            else:
                b=np.array(a[i,:])
                Required_support[m-1]=np.vstack((Required_support[m-1],b))
        i+=1
    Required_support=Required_support[0:m]
    return a

def needed_support_Bridge_rule (normal, vertices):
    '''
    5 mm rule for bridges
    If a bridge is more than 5 mm in length, it requires 3D printing support structure
    '''

    Shape_normal= np.shape(normal)
    Shape_vertices=np.shape(vertices)
    Unit_vector_normals=np.zeros((Shape_normal[0], 3))
    dot_product=np.zeros((Shape_normal[0], 1))
    angle=np.zeros((Shape_normal[0],1))
    Vector_reference = np.array([[0],[0],[1]])
    ab=np.zeros((0,9))
    for i in range (0,Shape_normal[0]):
        Unit_vector_normals[i,:]= normal[i,:]/np.linalg.norm(normal[i,:])
        dot_product[i,:]=np.dot(Unit_vector_normals[i,:],Vector_reference)
        angle[i,:]= np.arccos(dot_product[i,:])
        if np.abs(angle[i,:])==0 or np.abs(angle[i,:])==np.pi:
            b= np.array([vertices[i,:]])
            ab=np.append(ab,b,axis=0)
        else:
            pass
    print(ab)
    ab_shape=np.shape(ab)
    for j in range (0, ab_shape[0]):
        for k in range (0, ab_shape[0]):
            d1=0
            d2=0
            d3=0
            for l in range (0,2):
                if ab[j,2] != ab[k,3*l+2]:
                    d1+=1
                else:
                    pass
                if ab[j,5] != ab[k,3*l+2]:
                    d2+=1
                else:
                    pass
                if ab[j,8] != ab[k,3*l+2]:
                    d3+=1
                else:
                    pass

    Required_support = ["a1","a2","a3","a4","a5","a6","a7","a8","a9","a10","a11","a12","a13","a14","a15","a16","a17","a18","a19","a20","a21","a22","a23","a24","a25","a26","a27","a28","a29","a30"]
    i=0
    m=0
    while i<ab_shape[0]:
        if i==0:
            Required_support[m]=ab[i,:]
            m+=1
        else:
            x1=x2=x3=0
            y1=y2=y3=0
            z1=z2=z3=0
            if ab[i,0] != ab[i-1,0]:
                x1+=1
            else:
                pass
            if ab[i,3] != ab[i-1,3]:
                x2+=1
            else:
                pass
            if ab[i,6] != ab[i-1,6]:
                x3+=1
            else:
                pass
            if ab[i,1] != ab[i-1,1]:
                y1+=1
            else:
                pass
            if ab[i,4] != ab[i-1,4]:
                y2+=1
            else:
                pass
            if ab[i,7] != ab[i-1,7]:
                y3+=1
            else:
                pass
            if ab[i,2] != ab[i-1,2]:
                z1+=1
            else:
                pass
            if ab[i,5] != ab[i-1,5]:
                z2+=1
            else:
                pass
            if ab[i,8] != ab[i-1,8]:
                z3+=1
            else:
                pass
            if (x1+x2+x3+y1+y2+y3+z1+z2+z3)>3:
                Required_support[m]=ab[i,:]
                m+=1
            else:
                b=np.array(ab[i,:])
                Required_support[m-1]=np.vstack((Required_support[m-1],b))
        i+=1
    Required_support=Required_support[0:m]
    Shape_required_support=np.shape(Required_support)
    from Support_Generator import FindContour
    Contour = FindContour(Required_support)
    Shape_contour=np.shape(Contour)
    p=0
    #print(Contour[1,:,:])
    n=0
    for j in range(0,m):
        for k in range (0,m):
            if j != k:
                if (Contour[j][0][:2] == Contour[k][0][:2]).all() or (Contour[j][0][:2] == Contour[k][1][:2]).all() or (Contour[j][0][:2] == Contour[k][2][:2]).all() or (Contour[j][0][:2] == Contour[k][3][:2]).all():
                    if (Contour[j][1][:2] == Contour[k][0][:2]).all() or (Contour[j][1][:2] == Contour[k][1][:2]).all() or (Contour[j][1][:2] == Contour[k][2][:2]).all() or (Contour[j][1][:2] == Contour[k][3][:2]).all():
                        if (Contour[j][2][:2] == Contour[k][0][:2]).all() or (Contour[j][2][:2] == Contour[k][1][:2]).all() or (Contour[j][2][:2] == Contour[k][2][:2]).all() or (Contour[j][2][:2] == Contour[k][3][:2]).all():
                            if (Contour[j][3][:2] == Contour[k][0][:2]).all() or (Contour[j][3][:2] == Contour[k][1][:2]).all() or (Contour[j][3][:2] == Contour[k][2][:2]).all() or (Contour[j][3][:2] == Contour[k][3][:2]).all():
                                if Contour[j][0][2] <= 1e-5 or Contour[k][0][2] <= 1e-5:
                                    print(j,k)
                                    Required_support[j]=np.zeros((Shape_required_support[1],Shape_required_support[2]))
                                    Required_support[k]=np.zeros((Shape_required_support[1],Shape_required_support[2]))
                                elif Contour[j][0][2] > Contour[k][0][2]:
                                    Required_support[j]=np.zeros((Shape_required_support[1],Shape_required_support[2]))
                                else:
                                    Required_support[k]=np.zeros((Shape_required_support[1],Shape_required_support[2]))
                                '''Condition sur la distance'''
                                for l in range (0, Shape_contour[1]):
                                    for p in range (0, Shape_contour[1]):
                                        if Contour[j][0][0]!=Contour[j][l][0] and Contour[j][0][1]!=Contour[j][p][1]:
                                            if abs(Contour[j][0][0]-Contour[j][l][0])<=5 and abs(Contour[j][0][1]-Contour[j][p][1])<=5:
                                                Required_support[j]=np.zeros((Shape_required_support[1],Shape_required_support[2]))
            if (m % 2) == 0:
                pass
            else:
                Required_support[j]=np.zeros((Shape_required_support[1],Shape_required_support[2]))
                Required_support[k]=np.zeros((Shape_required_support[1],Shape_required_support[2]))
                n=0
    Required_support=Required_support[0:n]
    return Required_support
support_angle=support_45deg_rule(normal,vertices)
support_bridge=needed_support_Bridge_rule(normal,vertices)
print(support_bridge)

'''
figure2 = plt.figure(2)
ax2 = figure2.add_subplot(111, projection='3d')
verts=[[support_bridge[i,j*3:j*3+3] for j in range(3)] for i in range(support_bridge.shape[0])]
ax2.add_collection3d(Poly3DCollection(verts, alpha=0.25, facecolors='#800000'))
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_xlim(-50,50)
ax2.set_ylim(-50,50)
ax2.set_zlim(-50,50)

plt.show()'''
2
