
from tkinter import *
from tkinter import filedialog
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import Support_Generator
from stl import mesh, Mesh
import os,sys

class Interface(Frame):

    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""

    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, bg= 'navy', **kwargs)

        self.pack()
        self.STL = ""
        self.angle_verif = DoubleVar()
        self.length_verif = DoubleVar()
        self.angle=0.0
        # Création de nos widgets
        self.message3=Label(self,text="Choose the Length for the Bridge Rule (must be between 4.5 to 5.5)",anchor=W)
        self.message3.config(width=len(self.message3["text"]))
        self.message3.grid(column=0,row=3,pady=5)
        self.message = Label(self,justify=LEFT, text="Choose a STL file",anchor=W,width=len(self.message3["text"]))
        self.message.grid(column=0,row=1,pady=5)
        self.message1 = Label(self, text="",bg='white',width=10)
        self.message1.grid(column=1,row=1,pady=5,columnspan=3)
        self.bouton_OK = Button(self, text="Validate", command=self.disp)
        self.bouton_OK.grid(column=6,row=1,pady=5)
        self.bouton_Plot = Button(self, text="View", command=self.View)
        self.bouton_Plot.grid(column=7,row=1,pady=5)
        self.bouton_Browse = Button(self, text="Browse",command=self.click)
        self.bouton_Browse.grid(column=5,row=1,pady=5)
        self.message4=Label(self,text="Choose the Overhang Angle (must be between 40 to 50)",anchor=W, width=len(self.message3["text"]))
        self.message4.grid(column=0,row=2,pady=5)
        self.angle_texte = Entry(self,textvariable = self.angle_verif)
        self.angle_texte.grid(column=1,row=2,pady=5,columnspan=3)
        self.bouton_OK2 = Button(self, text="Validate", command=self.disp2)
        self.bouton_OK2.grid(column=5,row=2,columnspan=2,pady=5)

        self.angle_texte = Entry(self,textvariable = self.length_verif)
        self.angle_texte.grid(column=1,row=3,pady=5,columnspan=3)
        self.bouton_OK3 = Button(self, text="Validate", command=self.disp3)
        self.bouton_OK3.grid(column=5,row=3,columnspan=2,pady=5)
        self.support = Label(self,justify=LEFT, text="Choose your support shape",anchor=W,width=len(self.message3["text"]))
        self.support.grid(row=4,rowspan=2,column=0,pady=5)
        self.canvas = Canvas(self,width=32,height=32)
        self.canvas.create_rectangle(2,2,30,30,fill="black")
        self.canvas.grid(row=4,column=1,padx=5)
        self.canvas2 = Canvas(self,width=32,height=32)
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
        self.canvas2.grid(row=4,column=2,padx=2)
        self.canvas3 = Canvas(self,width=32,height=32)
        self.canvas3.create_line(5,2,5,29,fill="black")
        self.canvas3.create_line(15,2,15,29,fill="black")
        self.canvas3.create_line(25,2,25,29,fill="black")
        self.canvas3.create_line(2,15,29,15,fill="black")
        self.canvas3.create_line(2,5,29,5,fill="black")
        self.canvas3.create_line(2,25,29,25,fill="black")
        self.canvas3.grid(row=4,column=3,padx=2)

    def click(self):
        """Il y a eu un clic sur le bouton.
        On change la valeur du label message."""
        self.message1["text"]=filedialog.askopenfilename(title="Choose a STL file",filetypes=[("STL","*.stl")])
        self.message1["width"]=len(self.message1["text"])
    def disp(self):
        if self.message1["text"]!="":
            self.bouton_OK["fg"] = 'green'
            self.STL = self.message1["text"]
        else:
            self.bouton_OK["fg"] = 'red'
            self.STL = self.message1["text"]
    def disp2(self):
         try:
            nbr=self.angle_verif.get()
            if nbr>=40 and nbr<=50:
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
            else:
                self.bouton_OK3['fg']="red"
         except:#Mais si l'utilisateur à rentrer autre chose que un entier alors on lui affiche "Veuillez entrer un nombre" et la boucle recommence.
            self.bouton_OK3['fg']="red"
    def View(self):
        if self.bouton_OK["fg"] == 'green':
            my_mesh= mesh.Mesh.from_file(self.STL)
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
        else:
            self.bouton_OK["fg"] = 'red'



fenetre = Tk()
fenetre.title('Support Generator')
interface = Interface(fenetre)

interface.mainloop()
carot=interface.STL


print(carot)

