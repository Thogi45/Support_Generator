import os,sys
from stl import mesh, Mesh
import glob
import time
path=os.path.dirname(sys.argv[0])

files = os.listdir(path)
i=1
stllist=[]
nbr=0
OK2=False
while OK2==False:
    i=1
    LocateSTL1="{0}/*.stl".format(path)
    Allfiles="{0}/*.*".format(path)
    Allfiles2="{0}/.*".format(path)

    Dir="{0}/*".format(path)
    STL=glob.glob(LocateSTL1)
    AllF=glob.glob(Allfiles)
    AllF2=glob.glob(Allfiles2)

    AllDF=glob.glob(Dir)
    AllDF=AllDF+AllF2
    AllF=AllF+AllF2
    for k in range(len(AllF)):
        AllDF.remove(AllF[k])
    print("STL AVAILABLE IN THE FOLDER: ", path)
    time.sleep(2)
    if len(STL)==0:
        print("NO STL FILE, please go to another folder")
    for name in STL:
        print(name," ....... ",i)
        i=i+1
    time.sleep(2)
    print("NAVIGATION INTO FOLDERS")
    for name in AllDF:
        print("Go into folder: ",name," ....... ",i)
        i=i+1
    print("Look back in another folder ....... ",0)
    typea=0
    OK=False
    time.sleep(2)
    while OK==False:
        typea=0
        while typea!=1:
             try:
                nbr=int(input(("Select a number for what do you want to do: ")))
                if nbr>=0 and nbr<=i-1:
                    typea=1
                else:
                    print("Enter a integer between ",0," and ",i-1)
             except:#Mais si l'utilisateur à rentrer autre chose que un entier alors on lui affiche "Veuillez entrer un nombre" et la boucle recommence.
                print("Enter a integer between ",0," and ",i-1)
        if nbr>=1 and nbr<=len(STL):
            print("You have selected: ", STL[nbr-1])
            STL1=STL[nbr-1]
        elif nbr>len(STL) and nbr<=len(STL)+len(AllDF):
            print(nbr,len(STL))
            path=AllDF[nbr-len(STL)-1]
            files = os.listdir(path)
            test=os.listdir(path)
            print(files)
            print(test)
        else:
            print("You have selected: Look in another folder")
            path=os.path.dirname(path)
            files = os.listdir(path)
            test=os.listdir(path)
            print(files)
            print(test)


        Answer=input("Are you sure about your choice? YES/Y/y/yes/Yes: ")
        Yes=["YES","Y","y","yes","Yes"]
        if Answer not in Yes:
            OK=False
        else:
            if nbr>=1 and nbr<=len(STL):
                OK2=True
            OK=True

k=0

