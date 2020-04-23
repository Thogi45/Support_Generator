import PyQt5
import PyQt5.QtWidgets
from tkinter import *
from tkinter import filedialog
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import Support_Generator
import mayavi
import vtk
from tvtk.api import tvtk
from mayavi import mlab
from stl import mesh


class Interface(Frame):

    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""

    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, **kwargs)
        self.config(background='light steel blue')
        self.pack()
        self.STL = ""
        self.OK = [False, False, False, False,False]
        self.angle_verif = DoubleVar()
        self.length_verif = DoubleVar()
        self.PA = DoubleVar()
        self.angle=0.0
        self.bridge=0.0
        self.shape = 0
        self.pathN = 0.0
        self.message3=Label(self,text="  Choose the Length for the Bridge Rule\n\n(must be between 4.5 to 5.5)",background='light steel blue')

        self.message3.grid(column=0,row=4,pady=5,sticky=W)
        self.photo = PhotoImage(file="Support_Generator.gif")
        self.canvasA = Canvas(self,width=532,height=60,highlightcolor='medium blue',highlightbackground='medium blue')
        self.canvasA.create_image(534/2,64/2,image=self.photo)
        self.canvasA.grid(row=0,column=0,columnspan=7)
        # Création de nos widgets

        self.message = Label(self,justify=LEFT, text="   Choose a STL file",background='light steel blue')
        self.message.grid(column=0,row=1,pady=0,rowspan=2,sticky=W)
        self.message1 = Label(self, text="",bg='white',width=10)
        self.message1.grid(column=1,row=1,pady=5,columnspan=3,rowspan=2)
        self.bouton_OK = Button(self, text="Validate", command=self.disp)
        self.bouton_OK.grid(column=5,row=2,pady=5,padx=5)
        self.bouton_Plot = Button(self, text="View", command=self.View)
        self.bouton_Plot.grid(column=6,row=1,pady=5,padx=5,rowspan=2)
        self.bouton_Browse = Button(self, text="Browse",command=self.click)
        self.bouton_Browse.grid(column=5,row=1,pady=5,padx=5)
        self.message4=Label(self,text="Choose the Overhang Angle\n\n        (must be between 40 to 50)",background='light steel blue')
        self.message4.grid(column=0,row=3,pady=5,sticky=W)
        self.angle_texte = Entry(self,textvariable = self.angle_verif)
        self.angle_texte.grid(column=1,row=3,pady=5,columnspan=3)
        self.bouton_OK2 = Button(self, text="Validate", command=self.disp2)
        self.bouton_OK2.grid(column=5,row=3,columnspan=2,pady=5)

        self.angle_texte = Entry(self,textvariable = self.length_verif)
        self.angle_texte.grid(column=1,row=4,pady=5,columnspan=3)
        self.bouton_OK3 = Button(self, text="Validate", command=self.disp3)
        self.bouton_OK3.grid(column=5,row=4,columnspan=2,pady=5)
        self.support = Label(self,justify=LEFT, text="  Choose your support shape",background='light steel blue')
        self.support.grid(row=5,rowspan=2,column=0,pady=5,sticky=W)
        self.canvas = Canvas(self,width=32,height=32,background='light steel blue',highlightbackground='light steel blue')
        self.canvas.create_rectangle(2,2,30,30,fill="black")
        self.canvas.grid(row=5,column=1)
        self.canvas2 = Canvas(self,width=32,height=32,background='light steel blue',highlightbackground='light steel blue')
        self.canvas2.create_line(2,2,29,2,fill="black")
        self.canvas2.create_line(2,2,2,6,fill="black")
        self.canvas2.create_line(2,6,29,6,fill="black")
        self.canvas2.create_line(29,6,29,10,fill="black")
        self.canvas2.create_line(29,10,2,10,fill="black")
        self.canvas2.create_line(2,10,2,14,fill="black")
        self.canvas2.create_line(2,14,29,14,fill="black")
        self.canvas2.create_line(29,14,29,18,fill="black")
        self.canvas2.create_line(2,18,29,18,fill="black")
        self.canvas2.create_line(2,18,2,22,fill="black")
        self.canvas2.create_line(2,22,29,22,fill="black")
        self.canvas2.create_line(29,22,29,26,fill="black")
        self.canvas2.create_line(2,26,29,26,fill="black")
        self.canvas2.create_line(2,26,2,30,fill="black")
        self.canvas2.create_line(2,30,29,30,fill="black")
        self.canvas2.grid(row=5,column=2,padx=2)
        self.canvas3 = Canvas(self,width=32,height=32,background='light steel blue',highlightbackground='light steel blue')
        self.canvas3.create_line(5,2,5,29,fill="black")
        self.canvas3.create_line(15,2,15,29,fill="black")
        self.canvas3.create_line(25,2,25,29,fill="black")
        self.canvas3.create_line(2,15,29,15,fill="black")
        self.canvas3.create_line(2,5,29,5,fill="black")
        self.canvas3.create_line(2,25,29,25,fill="black")
        self.canvas3.grid(row=5,column=3,padx=2)
        self.var_choix = StringVar()
        self.choix_1 = Radiobutton(self, text="", variable=self.var_choix, value=1,background='light steel blue')
        self.choix_2 = Radiobutton(self, text="", variable=self.var_choix, value=2,background='light steel blue')
        self.choix_3= Radiobutton(self, text="", variable=self.var_choix, value=3,background='light steel blue')
        self.choix_1.grid(row=6,column=1)
        self.choix_2.grid(row=6,column=2)
        self.choix_3.grid(row=6,column=3)
        self.bouton_OK4 = Button(self, text="Validate", command=self.disp4)
        self.bouton_OK4.grid(column=5,row=5,columnspan=2,rowspan=2,pady=5)
        self.path = Label(self,justify=LEFT, text="  Choose your path",background='light steel blue')
        self.path.grid(column=0,row=8,pady=5,sticky=W)
        self.path1 = Entry(self,textvariable = self.PA)
        self.path1.grid(column=1,row=8,pady=5,columnspan=3)
        self.bouton_OK5 = Button(self, text="Validate", command=self.disp5)
        self.bouton_OK5.grid(column=5,row=8,columnspan=2,pady=5)
        self.bouton_Generate = Button(self, text='Generate',command=self.generate)
        self.bouton_Generate.grid(column=2,row=9,columnspan=3,pady=5)
    def click(self):
        self.message1["text"]=filedialog.askopenfilename(title="Choose a STL file",filetypes=[("STL","*.stl")])
        self.message1["width"]=len(self.message1["text"])
    def disp(self):
        if self.message1["text"]!="":
            self.bouton_OK["fg"] = 'green'
            self.OK[0]=True
            self.STL = self.message1["text"]
        else:
            self.bouton_OK["fg"] = 'red'
            self.STL = self.message1["text"]
    def disp2(self):
         try:
            nbr=self.angle_verif.get()
            if nbr>=40 and nbr<=50:
                self.OK[1] = True
                self.bouton_OK2['fg']="green"
                self.angle = nbr
            else:
                self.bouton_OK2['fg']="red"
         except:#Mais si l'utilisateur à rentrer autre chose que un entier alors on lui affiche "Veuillez entrer un nombre" et la boucle recommence.
            self.bouton_OK2['fg']="red"
    def disp3(self):
         try:
            nbr=self.length_verif.get()
            if nbr>=4.5 and nbr<=5.5:
                self.bouton_OK3['fg']="green"
                self.OK[2] = True
            else:
                self.bouton_OK3['fg']="red"
         except:#Mais si l'utilisateur à rentrer autre chose que un entier alors on lui affiche "Veuillez entrer un nombre" et la boucle recommence.
            self.bouton_OK3['fg']="red"

    def disp4(self):
        try:
            nbr=self.var_choix.get()
            self.bouton_OK4['fg'] = "green"
            self.OK[3]=True
            if nbr=="":
                self.bouton_OK4['fg'] = "red"
        except:
            self.bouton_OK4['fg'] = "red"
    def disp5(self):
        try:
            nbr=float(self.PA.get())
            self.bouton_OK5['fg'] = "green"
            self.OK[4]=True
            self.pathN = nbr
            if nbr=="":
                self.bouton_OK5['fg'] = "red"
        except:
            self.bouton_OK5['fg'] = "red"
    def generate(self):
        i = 0
        for ij in range(len(self.OK)):
            if self.OK[ij]== True:
                i = i+1
        if i == 5:
            self.STL = self.message1["text"]
            self.angle = self.angle_verif.get()
            self.bridge = self.length_verif.get()
            self.shape = int(self.var_choix.get())
            my_mesh= mesh.Mesh.from_file(self.STL)
            normal=my_mesh.normals
            vertices=my_mesh.points
            from Support_finder import support_45deg_rule
            from Support_finder import needed_support_Bridge_rule
            support_angle=support_45deg_rule(normal,vertices,self.angle)
            support_bridge=needed_support_Bridge_rule(normal,vertices,self.bridge)
            i=0
            p=len(support_bridge)
            k=0
            while i<p:
                if all(support_bridge[k][0,0:9]== 0):
                    del support_bridge[k]
                else:
                    k=k+1
                p=p-1
            liste_support=[]
            liste_support=support_bridge+support_angle
            ListeContour=[]
            from Support_Generator import AreasWithSameAngle, FindContour, Projection
            from Support_Shape import thetraedral_simple_support, Rectangular_simple_support, gridxy, ZigZag, plot
            for i in range(len(liste_support)):
                A=AreasWithSameAngle(liste_support[i])
                ListeContour.append(FindContour(A))
            ListeProjete=Projection(ListeContour)
            ListeProjete_shape=np.shape(ListeProjete)
            if len(ListeProjete)==0:
                print("you do not need any support")
            else:
                n=0
                Faces=np.zeros((0,12))
                if ListeProjete_shape[2]==3:
                    while n <ListeProjete_shape[0]:
                        The=thetraedral_simple_support(ListeProjete[:][n][:][:])
                        Faces= np.append(Faces,The,axis=0)
                        n+=1
                    plot(Faces,my_mesh,-50,50,0,80)
                else:
                    if self.shape==1:
                        while n <ListeProjete_shape[0]:
                            Rec=Rectangular_simple_support(ListeProjete[:][n][:][:])
                            Faces= np.append(Faces,Rec,axis=0)
                            n+=1
                    elif self.shape==3:
                        while n <ListeProjete_shape[0]:
                            Grid=gridxy(ListeProjete[:][n][:][:],float(self.pathN))
                            Faces= np.append(Faces,Grid,axis=0)
                            n+=1
                    elif self.shape==2:
                        while n <ListeProjete_shape[0]:
                            ZZ=ZigZag(ListeProjete[:][n][:][:],float(self.pathN))
                            Faces= np.append(Faces,ZZ,axis=0)
                            n+=1
                    plot(Faces,my_mesh,-30,30,0,50)

    def View(self):
        if self.bouton_OK["fg"] == 'green':
            reader = tvtk.STLReader()
            reader.file_name = self.STL
            reader.update()
            surf = reader.output
            mlab.pipeline.surface(surf)
            mlab.show()
            k=0
            """""""""
            figure2 = plt.figure()
            axes = mplot3d.Axes3D(figure2)
            axes.add_collection3d(mplot3d.art3d.Poly3DCollection(my_mesh.vectors))
            axes.set_xlabel('X')
            axes.set_ylabel('Y')
            axes.set_zlabel('Z')
            scale = my_mesh.points.flatten('A')
            axes.auto_scale_xyz(scale, scale, scale)
            self.graph = FigureCanvasTkAgg(figure2,self)
            self.canvas4 = self.graph.get_tk_widget()
            self.canvas4.config(relief=GROOVE,borderwidth=5)
            self.canvas4.grid(column=8,row=1,rowspan=12,padx=10)
            """""
        else:
            self.bouton_OK["fg"] = 'red'



fenetre = Tk()
fenetre.title('Support Generator')
interface = Interface(fenetre)

interface.mainloop()
carot=interface.STL
print(carot)
carot = interface.angle
print(carot)
carot = interface.bridge
print(carot)
carot = interface.shape
print(carot)

