from stl import mesh
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import copy as cp
import math
from skimage.draw import polygon,ellipsoid
from skimage import measure

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
        while i < len1:
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


        za=za+1
        a=a+compteur+1
    return Zones

def FindContour(Zones):
    ListeContour=[]
    ij=-1
    while ij<len(Zones)-1:

        ij = ij+1
        IndexContour=[]
        IndexContour.append(0)
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
            numberContour=1
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
                        for il in range(len(A[ii])):
                            if A[ii,il] == True:
                                Test=Test+1
                            if B[ii,il] == True:
                                Test2=Test2+1
                            if C[ii,il] == True:
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
        if numberContour>1:
            Contour1=[]
            IndexContour.append(len(Contour))
            for l in range(len(IndexContour)-1):
                Contour1.append(Contour[IndexContour[l]:IndexContour[l+1]])
            for i in range(IndexContour[1],len(Contour)):
                 Contour=np.delete(Contour,IndexContour[1],axis=0)
        if numberContour==1:
            Contour1=[]
            Contour1.append(Contour)
#Tri Contour
        for KON in range(len(Contour1)):
            Contour=Contour1[KON]
            if len(Contour)!=0:
                IsFollow1=Contour[0,3:6]
                p=0
                while p<len(Contour)-1:

                    p=p+1
                    BisFollow=False
                    for i in range(p,len(Contour)):
                        IsFollow2=Contour[i,0:3]
                        IsFollow3=Contour[i,3:6]
                        A =np.array([IsFollow1 == IsFollow2,IsFollow1 == IsFollow3])
                        for ii in range(len(A)):
                            Test=0
                            for il in range(len(A[ii])):
                                if A[ii,il] == True:
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

def Projection(ListeContour):
    ListeProjete=[]
    ListC2=cp.deepcopy(ListeContour)
    ListC3=[]
    ListC4=[]
    if len(ListC2)!=0:
        ListC3=ListC2[0]
        if ListC3[0][0,0]==ListC3[0][1,0]:
            ListC3[0]=Organization(ListC3[0])
        ListC4=ListeContour[0]
        if ListC4[0][0,0]==ListC4[0][1,0]:
            ListC4[0]=Organization(ListC4[0])
    if len(ListC2)>0:
        for i in range(1,len(ListC2)):
            ListC3=ListC3+ListC2[i]
            if ListC3[i][0,0]==ListC3[i][1,0]:
                ListC3[i]=Organization(ListC3[0])
            ListC4=ListC4+ListeContour[i]
            if ListC4[i][0,0]==ListC4[i][1,0]:
                ListC4[i]=Organization(ListC4[i])
    for ij in range(len(ListC3)):
        for i in range(len(ListC3[ij])):
            ListC3[ij][i][2]=0
            ListC3[ij][i][5]=0
    for i in range(len(ListC2)):
        ListeProjete1=[]
        ListeProjete1.append(ListC4[i])
        ListeProjete1.append(ListC3[i])
        ListeProjete.append(ListeProjete1)

    return ListeProjete

def Organization(Contour):
    A=Contour[0]
    A=np.reshape(A,newshape=(1,6))
    Contour=np.delete(Contour,0,axis=0)
    c=np.append(Contour,A,axis=0)
    return c
