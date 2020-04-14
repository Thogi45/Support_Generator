from stl import mesh
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

mesh = mesh.Mesh.from_file("C:\\Users\\DCLIC\\PycharmProjects\\Support_Generator\\Demi_Cercle.stl")
normal = mesh.normals
vertices = np.array([[0.,0.,0.,1.,0.,0.,0.,1.,0.],[1.,0.,0.,0.,1.,0.,1.,1.,0],[2.,1.,0.,1.,1.,0.,1.,2.,0],[-1.,0.,0.,0.,-1.,0.,0.,0.,0.],[2.,2.,0.,2.,1.,0.,1.,2.,0.]])

'''[array([ 5., -5., 10.,  0., -5., 10.,  5.,  5., 10.,  5.,  5., 10.,  0.,
       -5., 10.,  0.,  5., 10.]), array([ 5.00000000e+00, -1.00000000e+01,  3.55271402e-14,  0.00000000e+00,
       -1.00000000e+01,  3.55271402e-14,  5.00000000e+00, -5.00000000e+00,
        0.00000000e+00,  5.00000000e+00, -5.00000000e+00,  0.00000000e+00,
        0.00000000e+00, -1.00000000e+01,  3.55271402e-14,  0.00000000e+00,
       -5.00000000e+00,  0.00000000e+00]), array([  5.,  -5.,  25.,   0.,  -5.,  25.,   5., -10.,  25.,   5., -10.,
        25.,   0.,  -5.,  25.,   0., -10.,  25.]), array([ 5.,  5., 15.,  0.,  5., 15.,  5., -5., 15.,  5., -5., 15.,  0.,
        5., 15.,  0., -5., 15.]), array([ 5., 10., 25.,  0., 10., 25.,  5.,  5., 25.,  5.,  5., 25.,  0.,
       10., 25.,  0.,  5., 25.]), array([ 5.,  5.,  0.,  0.,  5.,  0.,  5., 10.,  0.,  5., 10.,  0.,  0.,
        5.,  0.,  0., 10.,  0.])]
        [np.array([[ 5., -5., 10.,  0., -5., 10.,  5.,  5., 10.], [5.,  5., 10.,  0.,-5., 10.,  0.,  5., 10.]]), np.array([ [5.00000000e+00, -1.00000000e+01,  3.55271402e-14,  0.00000000e+00,-1.00000000e+01,  3.55271402e-14,  5.00000000e+00, -5.00000000e+00,0.00000000e+00],[  5.00000000e+00, -5.00000000e+00,  0.00000000e+00,0.00000000e+00, -1.00000000e+01,  3.55271402e-14,  0.00000000e+00,-5.00000000e+00,  0.00000000e+00]]), np.array([[5.,  -5.,  25.,   0.,  -5.,  25.,   5., -10.,  25.],[5., -10.,25.,   0.,  -5.,  25.,   0., -10.,  25.]]), np.array([[5.,  5., 15.,  0.,  5., 15.,  5., -5., 15.], [ 5., -5., 15.,  0.,5., 15.,  0., -5., 15.]]), np.array([[5., 10., 25.,  0., 10., 25.,  5.,  5., 25.],[5.,  5., 25.,  0.,10., 25.,  0.,  5., 25.]]), np.array([[5.,  5.,  0.,  0.,  5.,  0.,  5., 10.,  0.],[5., 10.,  0.,  0.,5.,  0.,  0., 10.,  0.]])]
'''
'''np.array([[2.,0.,0.,4.,0.,0.,1.,1.,1.],[1.,0.,0.,0.,1.,0.,1.,1.,0],[0.,0.,0.,0.,1.,0.,1.,0.,0],[2.,0.,0.,1.,0.,0.,1.,1.,1.],[1.,-1.,0.,1.,0.,0.,0.,0.,2.]])
'''


print(len(vertices))

def AreasWithSameAngle(vertices):
    a=0
    plan=vertices
    Zones=[]
    supp=0
    compteur=0
    za=0
    while a < len(vertices):
        PetitZone=[]
        zi=0
        ref=plan[0,0:9]
        plan=np.delete(plan,0,axis=0)
        PetitZone.append(ref)
       # Zones[za,zi]=ref
        v1=np.array([ref[0]-ref[3],ref[1]-ref[4],ref[2]-ref[5]])
        v2=np.array([ref[0]-ref[6],ref[1]-ref[7],ref[2]-ref[8]])
        normal1=np.cross(v1,v2)
        Pref=ref[0:3]
        len1= len(plan)
        i=0
        compteur=0
        while i < len1 :
            P1=plan[0,0:3]
            P2=plan[0,3:6]
            P3=plan[0,6:9]
            v3=np.array([P1[0]-Pref[0],P1[1]-Pref[1],P1[2]-Pref[2]])
            v4=np.array([P2[0]-Pref[0],P2[1]-Pref[1],P2[2]-Pref[2]])
            v5=np.array([P3[0]-Pref[0],P3[1]-Pref[1],P3[2]-Pref[2]])
            if np.dot(v3,normal1)==0 and (np.dot(v4,normal1)==0 and np.dot(v5,normal1)==0) :
                zi=zi+1
                PetitZone.append(plan[0,0:9])
              #  Zones[za,zi]=plan[0,0:9]
                plan=np.delete(plan,0,axis=0)
                compteur=compteur+1
            i=i+1
        Zones.append(PetitZone)

        print(a)
        za=za+1
        a=a+compteur+1
    return Zones

def FindContour(Zones):
    ListeContour=[]
    for ij in range(len(Zones)):
        shapes=np.shape(Zones[ij])
        Contour=np.zeros((shapes[0]*3,6))
        SmallZone=Zones[ij]
        p=0
        for a in range(len(SmallZone)):

            IsExt=SmallZone[a][0:6]
            BIsExt=True
            IsExt2=SmallZone[a][3:9]
            BIsExt2=True
            IsExt3=np.concatenate((SmallZone[a][0:3],SmallZone[a][6:9]))
            BIsExt3=True

            for i in range(len(SmallZone)):
                if i!=a:
                    IsExt4=SmallZone[i][0:6]
                    IsExt5=SmallZone[i][3:9]
                    IsExt6=np.concatenate((SmallZone[i][0:3],SmallZone[i][6:9]))
                    IsExt7=np.concatenate((SmallZone[i][3:6],SmallZone[i][0:3]))
                    IsExt8=np.concatenate((SmallZone[i][6:9],SmallZone[i][0:3]))
                    IsExt9=np.concatenate((SmallZone[i][6:9],SmallZone[i][3:6]))
                    A =np.array([IsExt == IsExt4,IsExt == IsExt5,IsExt == IsExt6,IsExt == IsExt7,IsExt == IsExt8,IsExt == IsExt9])
                    B =np.array([IsExt2 == IsExt4,IsExt2 == IsExt5,IsExt2 == IsExt6,IsExt2 == IsExt7,IsExt2 == IsExt8,IsExt2 == IsExt9])
                    C =np.array([IsExt3 == IsExt4,IsExt3 == IsExt5,IsExt3 == IsExt6,IsExt3 == IsExt7,IsExt3 == IsExt8,IsExt3 == IsExt9])
                    for ii in range(len(A)):
                        Test=0
                        Test2=0
                        Test3=0
                        for ij in range(len(A[ii])):
                            if A[ii,ij] == True:
                                Test=Test+1
                            if B[ii,ij] == True:
                                Test2=Test2+1
                            if C[ii,ij] == True:
                                Test3=Test3+1
                        if Test==6:
                            BIsExt=False
                        if Test2==6:
                            BIsExt2=False
                        if Test3==6:
                            BIsExt3=False

            if BIsExt==True:
                Contour[p,0:6]=IsExt
                p=p+1
            if BIsExt2==True:
                Contour[p,0:6]=IsExt2
                p=p+1
            if BIsExt3==True:
                Contour[p,0:6]=IsExt3
                p=p+1
        for i in range(p,shapes[0]*3):
            Contour=np.delete(Contour,p,axis=0)

        if len(Contour)!=0:
            IsFollow1=Contour[0,3:6]
            p=0
            while p<len(Contour):
                p=p+1
                BisFollow=False
                for i in range(p,len(Contour)):
                    IsFollow2=Contour[i,0:3]
                    IsFollow3=Contour[i,3:6]
                    A =np.array([IsFollow1 == IsFollow2,IsFollow1 == IsFollow3])
                    for ii in range(len(A)):
                        Test=0
                        for ij in range(len(A[ii])):
                            if A[ii,ij] == True:
                                Test=Test+1
                        if Test==3:
                            BisFollow=True
                            k=ii
                            a=i
                if k==0 and BisFollow==True:
                   Contour=np.insert(Contour,p,Contour[a],axis=0)
                   Contour=np.delete(Contour,a+1,axis=0)
                   IsFollow1=Contour[p,3:6]
                if k==1 and BisFollow==True:
                    Sauv=Contour[a,0:3]
                    Sauv2=Contour[a,3:6]
                    Sauv=np.concatenate((Sauv2,Sauv))
                    Contour=np.insert(Contour,a,Sauv,axis=0)
                    Contour=np.delete(Contour,a+1,axis=0)
                    Contour=np.insert(Contour,p,Contour[a],axis=0)
                    Contour=np.delete(Contour,a+1,axis=0)
                    IsFollow1=Contour[p,3:6]
            ListeContour.append(Contour)
    return ListeContour

Zones = AreasWithSameAngle(vertices)
ListeContour = FindContour(Zones)

#ListeCarre=[np.array([[ 5., -5., 10.,  0., -5., 10.,  5.,  5., 10.], [5.,  5., 10.,  0.,-5., 10.,  0.,  5., 10.]]), np.array([ [5.00000000e+00, -1.00000000e+01,  3.55271402e-14,  0.00000000e+00,-1.00000000e+01,  3.55271402e-14,  5.00000000e+00, -5.00000000e+00,0.00000000e+00],[  5.00000000e+00, -5.00000000e+00,  0.00000000e+00,0.00000000e+00, -1.00000000e+01,  3.55271402e-14,  0.00000000e+00,-5.00000000e+00,  0.00000000e+00]]), np.array([[5.,  -5.,  25.,   0.,  -5.,  25.,   5., -10.,  25.],[5., -10.,25.,   0.,  -5.,  25.,   0., -10.,  25.]]), np.array([[5.,  5., 15.,  0.,  5., 15.,  5., -5., 15.], [ 5., -5., 15.,  0.,5., 15.,  0., -5., 15.]]), np.array([[5., 10., 25.,  0., 10., 25.,  5.,  5., 25.],[5.,  5., 25.,  0.,10., 25.,  0.,  5., 25.]]), np.array([[5.,  5.,  0.,  0.,  5.,  0.,  5., 10.,  0.],[5., 10.,  0.,  0.,5.,  0.,  0., 10.,  0.]])]
#shapes1=np.shape(ListeCarre[0])


#ListeContour= FindContour(ListeCarre)
Index=[]
for ij in range(len(ListeContour)):
    SmallIndex=[]
    for i in range(1,len(ListeContour[ij])):
        v1=np.array([ListeContour[ij][i][3]-ListeContour[ij][i][0],ListeContour[ij][i][4]-ListeContour[ij][i][1],ListeContour[ij][i][5]-ListeContour[ij][i][2]])
        v2=np.array([ListeContour[ij][i-1][3]-ListeContour[ij][i-1][0],ListeContour[ij][i-1][4]-ListeContour[ij][i-1][1],ListeContour[ij][i-1][5]-ListeContour[ij][i-1][2]])
        if np.dot(np.array([v1[0],v1[1],0]),np.array([1,0,0]))/np.linalg.norm([v1[0],v1[1],0])==np.dot(np.array([v2[0],v2[1],0]),np.array([1,0,0]))/np.linalg.norm([v2[0],v2[1],0]):
            if np.dot(np.array([v1[0],v1[1],v1[2]]),np.array([0,0,1]))/np.linalg.norm([v1[0],v1[1],v1[2]])==np.dot(np.array([v2[0],v2[1],v2[2]]),np.array([0,0,1]))/np.linalg.norm([v2[0],v2[1],v2[2]]):
                ListeContour[ij][i-1][3:6]=ListeContour[ij][i][3:6]
                SmallIndex.append(i)
    Index.append(SmallIndex)

for ij in range(len(Index)):
    j=len(Index[ij])
    while j!=0:
        ListeContour[ij]=np.delete(ListeContour[ij],Index[ij][j-1],axis=0)
        j=j-1

vertices=ListeContour[0]
MaxX=vertices[0,0]
MinX=vertices[0,0]
PointMaxX=vertices[0,0:3]
PointMinX=vertices[0,0:3]
MaxY=vertices[0,1]
MinY=vertices[0,1]
PointMaxY=vertices[0,0:3]
PointMinY=vertices[0,0:3]
for ij in range(len(vertices)):
    if vertices[ij,0]>=MaxX:
        MaxX=vertices[ij,0]
        PointMaxX=vertices[ij,0:3]
    if vertices[ij,0]<=MinX:
        MinX=vertices[ij,0]
        PointMinX=vertices[ij,0:3]
    if vertices[ij,0]>=MaxY:
        MaxY=vertices[ij,0]
        PointMaxY=vertices[ij,0:3]
    if vertices[ij,0]<=MinY:
        MinY=vertices[ij,0]
        PointMinY=vertices[ij,0:3]


Precision=100


while (vertices[j,0]!=PointMinX[0] or vertices[j,1]!=PointMinX[1]):
    j=j+1

Start=vertices[j,0:3]
CurrentPoint1=Start
CurrentPoint2=Start
Points1=[]
Points2=[]
Points1.append(Start)
Points2.append(Start)
xp1=Start[0]
A=Start[1]-MinY
B=MaxY-MinY
'''''''''''
if isinstance(A/B*Precision,int):
    yp1=Start[1]
    yp2=Start[1]
else:
    yp1=math.ceil(A/B*Precision)*B/Precision+MinY
    yp2=math.floor(A/B*Precision)*B/Precision+MinY
'''''
Points1=[]
Points2=[]
Points1.append(Start)
Points2.append(Start)
if j == 0 :
    NextPoint1=vertices[j+1,0:3]
    a1=j+1
    NextPoint2=vertices[len(vertices)-1,0:3]
    a2=len(vertices)-1
if j== len(vertices)-1:
    NextPoint1=vertices[0,0:3]
    a1=0
    NextPoint2=vertices[j-1,0:3]
    a2=j-1
if j!=len(vertices)-1 and j!=0:
    NextPoint1=vertices[j+1,0:3]
    NextPoint2=vertices[j-1,0:3]
    a1=j+1
    a2=j-1
print(a1)
distanceMax=np.linalg.norm([Start[0]-NextPoint1[0],Start[1]-NextPoint1[1],0])
End = NextPoint1
for i in range(len(vertices)):
    if distanceMax<=np.linalg.norm([Start[0]-vertices[i,0],Start[1]-vertices[i,1],0]):
        End = vertices[i,0:3]
        distanceMax=np.linalg.norm([Start[0]-vertices[i,0],Start[1]-vertices[i,1],0])

i=1
while i!=101:
    xp1=xp1+1/Precision*(MaxX-MinX)
    if xp1>NextPoint1[0]:
        CurrentPoint1=NextPoint1
        if a1>=len(vertices)-1:
            a1=0
        else:
            a1=a1+1
        NextPoint1=vertices[a1,0:3]
    if xp1>NextPoint2[0]:
        CurrentPoint2=NextPoint2
        if a2<=0:
            a2=len(vertices)-1
        else:
            a2=a2-1
        NextPoint2=vertices[a2,0:3]
    VNP1=np.array([NextPoint1[0]-CurrentPoint1[0],NextPoint1[1]-CurrentPoint1[1],0])
    VNP2=np.array([NextPoint2[0]-CurrentPoint2[0],NextPoint2[1]-CurrentPoint2[1],0])
    if np.dot(VNP1,[1,0,0])==0:
        CurrentPoint1=NextPoint1
        if a1>=len(vertices)-1:
            a1=0
        else:
            a1=a1+1
        NextPoint1=vertices[a1,0:3]
    if np.dot(VNP2,[1,0,0])==0:
        CurrentPoint2=NextPoint2
        if a2<=0:
            a2=len(vertices)-1
        else:
            a2=a2-1
        NextPoint2=vertices[a2,0:3]
    if i==34:
        k=0
    VNP1=np.array([NextPoint1[0]-CurrentPoint1[0],NextPoint1[1]-CurrentPoint1[1],0])
    VNP2=np.array([NextPoint2[0]-CurrentPoint2[0],NextPoint2[1]-CurrentPoint2[1],0])
    COS1=np.dot(VNP1,[1,0,0])/np.linalg.norm(VNP1)
    COS2=np.dot(VNP2,[1,0,0])/np.linalg.norm(VNP2)
    if NextPoint1[1]>=CurrentPoint1[1]:
        yp1=CurrentPoint1[1]+(xp1-CurrentPoint1[0])*np.tan(np.arccos(COS1))
    else:
        yp1=CurrentPoint1[1]-(xp1-CurrentPoint1[0])*np.tan(np.arccos(COS1))
    if NextPoint2[1]>=CurrentPoint2[1]:

        yp2=CurrentPoint2[1]+(xp1-CurrentPoint2[0])*np.tan(np.arccos(COS2))
    else:
        yp2=CurrentPoint2[1]-(xp1-CurrentPoint2[0])*np.tan(np.arccos(COS2))
    Points1.append(np.array([xp1,yp1,0]))
    Points2.append(np.array([xp1,yp2,0]))
    print(i)
    i=i+1





for ij in range(len(ListeContour)):
    for i in range(len(ListeContour[ij])-1):
        plt.plot([ListeContour[ij][i][0],ListeContour[ij][i+1][0]] ,[ListeContour[ij][i][1],ListeContour[ij][i+1][1]])

    plt.plot([ListeContour[ij][i+1][0],ListeContour[ij][0][0]] ,[ListeContour[ij][i+1][1],ListeContour[ij][0][1]])
    plt.xlim(-15,30)
    plt.ylim(-15,30)
    plt.show()


### Projection à faire
ListeProjete=[]
ListeProjete.append(ListeContour)
ListeProjete.append(ListeContour)
for ij in range(len(ListeContour)):
    for i in range(len(ListeContour[ij])):
        if ListeContour[ij][i][2]!=0:
            ListeProjete[1][ij][i][2]=0
        if ListeContour[ij][i][5]!=0:
            ListeProjete[1][ij][i][5]=0
k=0



### Fonctions
### Affichage graphe plus cool


