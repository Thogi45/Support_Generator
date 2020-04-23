from stl import mesh
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import math

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
                                            else:
                                                n+=1
                                                pass
            if (m % 2) == 0:
                pass
            else:
                Required_support[j]=np.zeros((Shape_required_support[1],Shape_required_support[2]))
                Required_support[k]=np.zeros((Shape_required_support[1],Shape_required_support[2]))
                n=0
    Required_support=Required_support[0:n]

    return Required_support

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
        if np.abs(angle[i,:]) >= 2.35619 and np.abs(angle[i,:]) <= 3.92699 and np.abs(angle[i,:]) != np.pi:
            b= np.array([vertices[i,:]])
            a=np.append(a,b,axis=0)
            t+=1
        else:
            angle[i,:]=An[0,0]
            pass
    Shape_support=np.shape(a)
    l=0
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
    Required_support = [1]*a_shape[0]
    while i<a_shape[0]:
        if i==0:
            #Required_support.append(a[i,:])
            Required_support[m]=np.array([a[i,:]])
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
                #Required_support.append(a[i,:])
                Required_support[m]=np.array([a[i,:]])
                m+=1
            elif (x1+x2+x3+y1+y2+y3+z1+z2+z3)>3:
                #Required_support.append(a[i,:])
                Required_support[m]=np.array([a[i,:]])
                m+=1
            else:
                b=np.array(a[i,:])
                Required_support[m-1]=np.vstack((Required_support[m-1],b))
        i+=1
    Required_support=Required_support[0:m]
    return Required_support
