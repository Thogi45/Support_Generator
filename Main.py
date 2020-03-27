import os,sys, glob
from stl import mesh, Mesh

LocateSTL=os.path.dirname(sys.argv[0])
print("----------------------------------------\n")
print("            SUPPORT GENERATOR              \n")
print("by Thomas Heissel and Thomas Girerd       ")
print("----------------------------------------\n")
print("You need to choose the STL file you want to generate supports with.")
files = os.listdir(LocateSTL)
i=1
stllist=[]
for name in files:
    if name.endswith(".stl")==True:
        print(name," ....... ",i)
        stllist.append(name)
        i=i+1
print("Look in another folder ....... ",0)
typea=0
OK=False
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
    if nbr>=1:
        print("You have selected: ", stllist[nbr-1])
        mesh.Mesh.from_file(stllist[nbr-1])
    else:
        print("You have selected: Look in another folder")
    Answer=input("Are you sure about your choice? YES/Y/y/yes/Yes: ")
    Yes=["YES","Y","y","yes","Yes"]
    if Answer not in Yes:
        OK=False
    else:
        OK=True
