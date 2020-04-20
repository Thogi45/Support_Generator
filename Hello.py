def ShapeChoice():
    print("You will choose the shape you want")
    print("There are 3 types of shapes")
    print("1st Shape:    ___________")
    print("              |.........|")
    print("              |.........|")
    print("              |.........|")
    print("              |_________|\n")
    print("2nd Shape:    _|_|_|_|_|_")
    print("              _|_|_|_|_|_")
    print("              _|_|_|_|_|_")
    print("              _|_|_|_|_|_")
    print("               | | | | | \n")
    print("3rd Shape:     _________")
    print("               ________|")
    print("              |________ ")
    print("               ________|")
    print("              |_________")
    typea=0
    while typea!=1:
         try:
            nbr=int(input(("Select the shape you want to do (1,2 or 3):")))
            if nbr>=0 and nbr<=3:
                typea=1
            else:
                print("Enter a integer between ",0," and ",3)
         except:#Mais si l'utilisateur à rentrer autre chose que un entier alors on lui affiche "Veuillez entrer un nombre" et la boucle recommence.
            print("Enter a integer between ",0," and ",3)
    return nbr
