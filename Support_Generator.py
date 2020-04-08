from stl import mesh
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

mesh = mesh.Mesh.from_file("C:\\Users\\DCLIC\\PycharmProjects\\Support_Generator\\tessa_vase_filled.stl")
normal = mesh.normals
vertices = np.array([[2.,0.,0.,4.,0.,0.,1.,1.,1.],[1.,0.,0.,0.,1.,0.,1.,1.,0],[0.,0.,0.,0.,1.,0.,1.,0.,0],[2.,0.,0.,1.,0.,0.,1.,1.,1.],[1.,-1.,0.,1.,0.,0.,0.,0.,2.]])
'''np.array([[2.,0.,0.,4.,0.,0.,1.,1.,1.],[1.,0.,0.,0.,1.,0.,1.,1.,0],[0.,0.,0.,0.,1.,0.,1.,0.,0],[2.,0.,0.,1.,0.,0.,1.,1.,1.],[1.,-1.,0.,1.,0.,0.,0.,0.,2.]])
'''
figure = plt.figure()
axes = mplot3d.Axes3D(figure)
axes.set_xlabel('X')
axes.set_ylabel('Y')
axes.set_zlabel('Z')
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh.vectors))
scale = mesh.points.flatten('F')
axes.auto_scale_xyz(scale, scale, scale)
axes.set_title(mesh.name)
plt.show()
shapes=np.shape(vertices)
a=0
plan=vertices
Zones=[]
supp=0
compteur=0
za=0
print(len(vertices))
longueurV=len(vertices)
del vertices
while a < longueurV:
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

print("Toto")
ListeContour=[]
for ij in range(len(Zones)):
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
        print(ij)
        print(len(Zones))


print(Contour)
print(Contour[0:len(Contour),0])

for ij in range(len(ListeContour)):
    for i in range(len(ListeContour[ij])-1):
        plt.plot([ListeContour[ij][i][0],ListeContour[ij][i+1][0]] ,[ListeContour[ij][i][1],ListeContour[ij][i+1][1]])

    plt.plot([ListeContour[ij][i+1][0],ListeContour[ij][0][0]] ,[ListeContour[ij][i+1][1],ListeContour[ij][0][1]])
    plt.xlim(-50,50)
    plt.ylim(-50,50)
    plt.show()


### Projection à faire
### Fonctions
### Affichage graphe plus cool


