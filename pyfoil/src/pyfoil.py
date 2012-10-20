"""================================================ 
FOIL UI CLASS
-------------
Class to generate the UI for Airfoil Generator

Copyright: Robert Wolterman
Date:       09/08/2007

This file is part of Airfoil Generator.

Airfoil Generator is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Airfoil Generator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Airfoil Generator.  If not, see <http://www.gnu.org/licenses/>.

================================================"""

# MODULE IMPORTS
import Tkinter
import tkFileDialog
import airfoil

__author__ = "Robert Wolterman <robert.wolterman@gmail.com>"
__date__ = "22 September 2007"
__version__ = "$Revision:  $"

class UI(object):
    # INIT
    def __init__(self,root,windowName):
        """ INITIALIZE THE UI CLASS """
        # SET UP VARIABLES
        self.CWINX = 500
        self.CWINY = 350
        self.fileName = ""
        self.NPTS = ""
        self.foil = airfoil.Airfoil()
                
        # WIDGET VARIABLES
        self.foilNameLbl = Tkinter.StringVar()
        self.foilTypeOpt = Tkinter.StringVar()
        
        # INITIALIZE LABEL VALUES
        self.updateFoilName("")
        self.updateFoilType("n4")  # SET N4 AS DEFAULT
        
        # SET ROOT WINDOW NAME
        root.title(windowName)
        # SET WINDOW TO NOT RESIZE
        root.resizable(width="NO",height="NO")
        
        # SET UP MENU
        # CODE TAKEN FROM EFFBOT.ORG
        # MODIFIED FOR USE WITH THIS PROGRAM
        self.menuBar = Tkinter.Menu(root)
        
        # create a pulldown menu, and add it to the menu bar
        self.fileMenu = Tkinter.Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="Open", command=lambda: self.fileOpen(root))
        self.fileMenu.add_command(label="Save", command=lambda: self.fileSaveAs(root))
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=root.quit)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)

        # create more pulldown menus
        self.modifierMenu = Tkinter.Menu(self.menuBar, tearoff=0)
        self.modifierMenu.add_command(label="Invert", command=lambda: self.foilModsWrapper("invert"))
        self.modifierMenu.add_command(label="Scale", command=hello)
        self.modifierMenu.add_command(label="Rotate") #, command=lambda: self.foilModsWrapper("rotate"))
        self.menuBar.add_cascade(label="Modifiers", menu=self.modifierMenu)

        self.helpMenu = Tkinter.Menu(self.menuBar, tearoff=0)
        self.helpMenu.add_command(label="About", command=hello)
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)

        # display the menu
        root.config(menu=self.menuBar)
        
        # SET UP GUI
        # ======================================================================
        # FRAME FL - HOLDER FOR CANVAS
        self.FL = Tkinter.Frame(root,height=self.CWINY,width=self.CWINX)
        self.FL.pack(side=Tkinter.LEFT,fill=Tkinter.Y)
        
        # SETUP CANVAS
        self.plot = Tkinter.Canvas(self.FL,height=self.CWINY,width=self.CWINX,bg="#000000")
        self.plot.pack(side=Tkinter.TOP)
        
        # FRAME FLA - HOLDER FOR AIRFOIL BUTTONS THAT CONTROL FLIPBOOK
        self.FLA = Tkinter.Frame(self.FL,width=self.CWINX)
        self.FLA.pack(fill=Tkinter.X)
        
        # SET UP ANGLE OF ATTACK SLIDER IN FLA
        #self.foilRotate = Tkinter.Scale(self.FLA,from_=-50,to=50,resolution=1,label="Angle of Attack",orient=Tkinter.HORIZONTAL)
        #self.foilRotate.pack(side=Tkinter.LEFT,fill=Tkinter.X)
        
        # SETUP FOIL NAME LABEL
        self.lblFoilName = Tkinter.Label(self.FLA,justify="center",textvariable=self.foilNameLbl)
        self.lblFoilName.pack(side=Tkinter.LEFT,fill=Tkinter.X)

        # FRAME FLA - HOLDER FOR AIRFOIL BUTTONS THAT CONTROL FLIPBOOK
        self.FLB = Tkinter.Frame(self.FL,width=self.CWINX)
        self.FLB.pack(side=Tkinter.BOTTOM,fill=Tkinter.X)

        # FRAME FR - MAIN FRAME FOR FLIPPABLE FRAME AND BUTTONS
        self.FR = Tkinter.Frame(root,height=275,width=200)
        self.FR.pack(side=Tkinter.RIGHT,fill=Tkinter.Y)

        # CREATE FLIPPING FRAME HOLDER
        self.FRA = Tkinter.Frame(self.FR)
        self.FRA.pack(fill=Tkinter.BOTH)

        # CREATE FLIPPABLE FRAMES - DO NOT PACK FRAMES THEMSELVES, ONLY WIDGETS ON THEM
        # ==============================================
        
        # ==========================================================================
        # **************************************************************************
        # **************************************************************************
        # ==========================================================================
    
        # ==============================================
        # NACA 4 PAGE
        self.FRA2 = Tkinter.Frame(self.FRA)
    
        # NACA 4 MAX CAMBER SLIDER
        self.n4CPlace = Tkinter.Scale(self.FRA2,from_=2,to=9,resolution=1,label="Maximum Camber",orient=Tkinter.HORIZONTAL)
        self.n4CPlace.pack(side=Tkinter.TOP,fill=Tkinter.X)
        
        # NACA 4 MAX CAMBER POSITION SLIDER
        self.n4MCLPos = Tkinter.Scale(self.FRA2,from_=2,to=9,resolution=1,label="Max Camber Position",orient=Tkinter.HORIZONTAL)
        self.n4MCLPos.pack(side=Tkinter.TOP,fill=Tkinter.X)
    
        # NACA 4 AIRFOIL THICKNESS SLIDER
        self.n4TCRatio = Tkinter.Scale(self.FRA2,from_=0.02,to=0.99,resolution=.01,label="Airfoil Thickness Ratio",orient=Tkinter.HORIZONTAL)
        self.n4TCRatio.pack(side=Tkinter.TOP,fill=Tkinter.X)
        
        # PACK THE FLIPPING FRAME AND SET AS HIDDEN
        self.FRA2.pack(fill=Tkinter.BOTH, expand=1)
        self.active_fr = self.FRA2
    
        # ==============================================
        # NACA 5 PAGE
        self.FRA3 = Tkinter.Frame(self.FRA)
    
        # NACA 5 TYPE SLIDER
        self.n5MCLPos = Tkinter.Scale(self.FRA3,from_=210,to=250,resolution=10,label="NACA 5 Type",orient=Tkinter.HORIZONTAL)
        self.n5MCLPos.pack(side=Tkinter.TOP,fill=Tkinter.X)
    
        # NACA 5 AIRFOIL THICKNESS SLIDER
        self.n5TCRatio = Tkinter.Scale(self.FRA3,from_=0.02,to=0.99,resolution=.01,label="Airfoil Thickness Ratio",orient=Tkinter.HORIZONTAL)
        self.n5TCRatio.pack(side=Tkinter.TOP,fill=Tkinter.X)
        
        # PACK THE FLIPPING FRAME AND SET AS HIDDEN
        self.FRA3.pack(fill=Tkinter.BOTH, expand=1)
        self.FRA3.forget()
    
        # ==============================================
        # BICONVEX PAGE
        self.FRA4 = Tkinter.Frame(self.FRA)
    
        # BICONVEX THICKNESS SLIDER
        self.bxTCRatio = Tkinter.Scale(self.FRA4,from_=0.02,to=0.99,resolution=.01,label="Airfoil Thickness Ratio",orient=Tkinter.HORIZONTAL)
        self.bxTCRatio.pack(side=Tkinter.TOP,fill=Tkinter.X)
        
        # PACK THE FLIPPING FRAME AND SET AS HIDDEN
        self.FRA4.pack(fill=Tkinter.BOTH, expand=1)
        self.FRA4.forget()
        
        # ==============================================
        # JOUKOWSKI PAGE
        self.FRA5 = Tkinter.Frame(self.FRA)
        
        # JOUKOWSKI MR VALUE SLIDER - SET FOR CHORD = 1
        self.juMR = Tkinter.Scale(self.FRA5,from_=0.001,to=0.04,resolution=0.001,label="MR Value",orient=Tkinter.HORIZONTAL)
        self.juMR.pack(side=Tkinter.TOP,fill=Tkinter.X)
    
        # JOUKOWSKI ML VALUE SLIDER - SET FOR CHORD = 1
        self.juML = Tkinter.Scale(self.FRA5,from_=0.001,to=0.04,resolution=0.001,label="ML Value",orient=Tkinter.HORIZONTAL)
        self.juML.pack(side=Tkinter.TOP,fill=Tkinter.X)
        
        # PACK THE FLIPPING FRAME AND SET AS HIDDEN
        self.FRA5.pack(fill=Tkinter.BOTH, expand=1)
        self.FRA5.forget()

        # SET UP RADIO BUTTONS FOR AIRFOIL TYPE - PUT INTO FLB
        
        # ==========================================================================
        # **************************************************************************
        # **************************************************************************
        # ==========================================================================
        
        self.foilN4 = Tkinter.Radiobutton(self.FLB,text="NACA 4",variable=self.foilTypeOpt,value="n4",command=lambda: self.display(self.FRA2))
        self.foilN4.pack(side=Tkinter.LEFT,fill=Tkinter.X)
        
        self.foilN5 = Tkinter.Radiobutton(self.FLB,text="NACA 5",variable=self.foilTypeOpt,value="n5",command=lambda: self.display(self.FRA3))
        self.foilN5.pack(side=Tkinter.LEFT,fill=Tkinter.X)
        
        self.foilBX = Tkinter.Radiobutton(self.FLB,text="Biconvex",variable=self.foilTypeOpt,value="bx",command=lambda: self.display(self.FRA4))
        self.foilBX.pack(side=Tkinter.LEFT,fill=Tkinter.X)
        
        self.foilJU = Tkinter.Radiobutton(self.FLB,text="Joukowski",variable=self.foilTypeOpt,value="ju",command=lambda: self.display(self.FRA5))
        self.foilJU.pack(side=Tkinter.LEFT,fill=Tkinter.X)
        
        # FRAME FRB - RIGHT SUBFRAME FOR FOIL TYPES AND BUTTONS
        self.FRB = Tkinter.Frame(self.FR,bg="#FCFCFC")
        self.FRB.pack(side=Tkinter.BOTTOM,fill=Tkinter.X)
        
        # AIRFOIL NUMBER OF POINTS
        self.foilNPtsLbl = Tkinter.Label(self.FRB,justify="center",text="\nNumber of Points")
        self.foilNPtsLbl.pack(fill=Tkinter.X)
        self.foilNPts = Tkinter.Spinbox(self.FRB,from_=51,to=1001,increment=10,command=self.updateNPTS)
        self.foilNPts.pack(fill=Tkinter.X)
        # UPDATE NUMBER OF POINTS RIGHT AFTER CREATION
        self.updateNPTS()
        
        # SET UP COMMAND BUTTONS IN FRB
        self.spacerLbl = Tkinter.Label(self.FRB,justify="center")
        self.spacerLbl.pack(fill=Tkinter.X)
        self.btnGenFoil  = Tkinter.Button(self.FRB,text="Generate Airfoil",command=self.genFoil)
        self.btnGenFoil.pack(fill=Tkinter.X)
        # ======================================================================
        
    # updateFoilName
    def updateFoilName(self,inStr):
        """ UPDATES THE AIRFOIL NAME """
        self.foilNameLbl.set(inStr)

    # updateFoilType 
    def updateFoilType(self,inStr):
        """ UPDATES THE AIRFOIL TYPE """
        self.foilTypeOpt.set(inStr)
    
    # updateNPTS
    def updateNPTS(self):
        """ UPDATES THE NUMBER OF POINTS TO USE FOR AIRFOIL GENERATION """
        self.NPTS = self.foilNPts.get()
       
    # display
    def display(self,fr):
        """ Displays the frame selected by the radio button while hiding the
            current active frame
        """
        self.active_fr.forget()
        fr.pack(fill=Tkinter.BOTH, expand=1)
        self.active_fr = fr
        
    # genFoil
    def genFoil(self):
        """ Generates the airfoil and draws the shape """
        # SET AIRFOIL PARAMETERS - NUMBER OF POINTS AND SPACING
        self.foil.setFoil(int(self.NPTS),"fullcos")
        # FIGURE OUT WHAT AIRFOIL SHAPE WE ARE DOING
        # NACA 4 SERIES
        if self.foilTypeOpt.get() == "n4":
            # GET THE CURENT SLIDER VALUES
            cPlace = str(self.n4CPlace.get())
            mclpos = str(self.n4MCLPos.get())
            tc = str(self.n4TCRatio.get())
            tc = tc.split('.')
            nacades = cPlace+mclpos+tc[1]
            # GENERATE THE AIRFOIL SHAPE
            self.foil.genNACA4(int(nacades))
            # UPDATE THE AIRFOIL NAME LABEL
            self.updateFoilName("NACA "+nacades)
        # NACA 5 SERIES
        elif self.foilTypeOpt.get() == "n5":
            # GET THE CURRENT SLIDER VALUES
            mclpos = str(self.n5MCLPos.get())
            tc = str(self.n5TCRatio.get())
            tc = tc.split('.')
            nacades = mclpos+tc[1]
            # GENERATE THE AIRFOIL SHAPE
            self.foil.genNACA5(int(nacades))
            # UPDATE THE AIRFOIL NAME LABEL
            self.updateFoilName("NACA "+nacades)
        # BICONVEX
        elif self.foilTypeOpt.get() == "bx":
            # GET THE CURRENT SLIDER VALUE
            tc = self.bxTCRatio.get()
            # GENERATE THE AIRFOIL SHAPE
            self.foil.genBCX(float(tc))
            # UPDATE THE AIRFOIL NAME LABEL
            tc = tc*100
            self.updateFoilName("BICONVEC @ "+str(tc)+"% TC")
        # JUKOWSKI
        elif self.foilTypeOpt.get() == "ju":
            # GET THE CURRENT SLIDER VALUES
            mr = self.juMR.get()
            ml = self.juML.get()
            # GENERATE THE AIRFOIL SHAPE
            self.foil.genJoukowski(361,mr,ml)
            # UPDATE THE AIRFOIL NAME LABEL
            self.updateFoilName("JOUKOWSKI")
            
        # ==========================================================================
        # **************************************************************************
        # **************************************************************************
        # ==========================================================================
            
        # SET OLD SHAPE VARIABLE TO KEEP OLD VALUE WHEN ROTATING
        self.oldFoil = self.foil
        
        # DRAW THE AIRFOIL
        self.drawFoil()

    def drawFoil(self):
        """ This does the grunt work of drawing the airfoil """
        # SET LISTS TO HOLD POINTS PLOTTED AND ONE FOR LINE CREATION
        self.points = []
        self.lines = []
        # CLEAR THE CANVAS
        self.plot.delete("all")
        # LOOP THROUGH AND PLOT POINTS AS SMALL BOXES
        for i in range(len(self.foil.shape)-1,-1,-1):
            x =  self.CWINX*self.foil.shape[i][0] + (self.CWINX/6 - (self.CWINX*self.foil.shape[i][0])/4)
            # Y COORDINATE IS NEGATIVE DUE TO HOW AIRFOIL IS CREATED
            y = -self.CWINX*self.foil.shape[i][1] + (self.CWINY/2 - (self.CWINY*self.foil.shape[i][1])/4)
            # ADD TUPLE OF CURRENT X & Y TO LINES FOR THE AIRFOIL SHAPE
            self.lines.append( (x,y) )
            # PLOT THE CURRENT POINT
            self.points.append(self.plot.create_rectangle(x-.01,y-.01,x+.01,y+.01,fill="#FFFFFF",outline="#FFFFFF"))
        # PLOT THE AIRFOIL LINE
        self.line = self.plot.create_line(self.lines,fill="#FFFFFF")       
       
    # ==========================================================================
    # **************************************************************************
    # **************************************************************************
    # ==========================================================================

    def foilModsWrapper(self,opt):
        """ Modifies the airfoil based on the given option.
            Controlled by the menu bar
        """
        if opt == "invert":
            self.foil.invert()
        elif opt == "rotate":
            # USE OLD SHAPE TO NOT ROTATE ALREADY ROTATED AIRFOIL
            self.foil.shape = self.oldFoil.shape
            aoa = self.foilRotate.get()
            self.foil.rotate(aoa)
        
        # DRAW THE AIRFOIL
        self.drawFoil()   

    def fileSaveAs(self,root):
        """ Saves the file, either Tecplot, ICEM, or a simple data file """
        # SET FILETYPES
        filetypes = [ ('TecPlot File','*.tec'),('ICEM File','*.icem'),('Data File','*.dat')]
        # GET THE FILENAME FROM THE DIALOG WINDOW
        filename = tkFileDialog.asksaveasfilename(parent=root,filetypes=filetypes,title="Save Airfoil Coordinates")
        # OPEN THE FILE
        fole = open(filename,'w')
        # GET THE EXTENSION TO FIGURE OUT WHAT FILE TYPE TO WRITE
        ext = filename.split('.')[-1]
        # GET THE NUMBER OF POINTS AND PANELS OF THE AIRFOIL
        npts = self.foil.numPoints
        npan = self.foil.numPan
        
        # WRITE FILES
        if ext == 'tec' or ext == 'dat':
            if ext == 'tec':
                fole.write("VARIABLES=X,Y\n")
                fole.write('ZONE T="'+str(self.foilNameLbl.get())+'",I='+str(len(self.foil.shape))+',J=1,F=POINT\n')
            elif ext == 'dat':
                fole.write(" "+str(len(self.foil.shape))+"\n")
	        # WRITE COORDINATES
            for i in range(len(self.foil.shape)):
                x = str(self.foil.shape[i][0])
                y = str(self.foil.shape[i][1])
                fole.write("  "+x+"   "+y+"\n")
        elif ext == 'icem':
            npsec = npan/2+1
            fole.write(str(npsec)+"   2\n")
            # SECTION 1
            for i in range(npsec-1,-1,-1):
                x = str(self.foil.shape[i][0])
                y = str(self.foil.shape[i][1])
                fole.write("  "+x+"   "+y+"   0.000\n")
            # SECTION 2
            for i in range(npsec-1,npts):
                x = str(self.foil.shape[i][0])
                y = str(self.foil.shape[i][1])
                fole.write("  "+x+"   "+y+"   0.000\n")
        
        # CLOSE THE FILE
        fole.close()

    def fileOpen(self,root):
        """ Opens the file, either Tecplot, ICEM, or a simple data file and then draws the airfoil"""
        # SET FILETYPES
        filetypes = [ ('TecPlot File','*.tec'),('ICEM File','*.icem'),('Data File','*.dat')]
        # GET THE FILENAME FROM THE DIALOG WINDOW
        filename = tkFileDialog.askopenfilename(parent=root,filetypes=filetypes,title="Open Airfoil Coordinate File")
        # OPEN THE FILE
        file = open(filename,'r')
        # GET THE EXTENSION TO FIGURE OUT WHAT FILE TYPE TO WRITE
        ext = filename.split('.')[-1]
        # GET THE NUMBER OF POINTS AND PANELS OF THE AIRFOIL
        npts = self.foil.numPoints
        npan = self.foil.numPan
        
        # READ FILES
        if ext == 'tec' or ext == 'dat':
            # INITIALIZE X AND Y LISTS FOR ADDING TO AIRFOIL
            x = []
            y = []
            if ext == 'tec':
                tmp = file.readline()  # VARIABLE LINE
                header = file.readline()
                header = header.split(',')
                tecName = header[0].split('"')
                tecName = tecName[1]
                npts = header[1].split('=')
                npts = int(npts[1])
            elif ext == 'dat':
                npts = int(file.readline())
	        # READ COORDINATES
            for i in range(npts):
                line = file.readline()
                line = line.split()
                x.append(float(line[0]))
                y.append(float(line[1]))
        elif ext == 'icem':
            x = []
            y = []
            x2 = []
            y2 = []
            #npsec = npan/2+1
            header = file.readline()
            header = header.split()
            npsec = int(header[0])
            nsec = int(header[1])
            temp = file.readline()   # DON'T READ IN FIRST LINE OF ZERO
            # SECTION 1
            for i in range(int(npsec)-1):
                line = file.readline()
                line = line.split()
                x.append(float(line[0]))
                y.append(float(line[1]))
            # SECTION 2
            x.reverse()
            y.reverse()
            for i in range(int(npsec)):
                line = file.readline()
                line = line.split()
                x.append(float(line[0]))
                y.append(float(line[1]))
            npts = len(x)
        
        # CLOSE THE FILE
        file.close()
        # SET AIRFOIL SHAPE
        self.foil.insertCoords(npts,x,y)
        # UPDATE AIFROIL LABEL
        if ext not in [ 'dat', 'icem']:
            self.updateFoilName(tecName)
        else:
            self.updateFoilName("FILE LOADED AIRFOIL")
        # DRAW THE AIRFOIL
        self.drawFoil()


def hello():
    print "hello"

# *** TESTING *** 
if __name__ == "__main__":
    root = Tkinter.Tk()
    
    win = UI(root,"Airfoil Generator")
    root.mainloop()
    
    