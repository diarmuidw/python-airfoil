""" ============================================================================
Airfoil Class
-------------
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

============================================================================ """

# Module imports 
import math
from Tkinter import *

__author__ = "Robert Wolterman <robert.wolterman@gmail.com>"
__date__ = "22 September 2007"
__version__ = "$Revision:  $"

class Airfoil:
    """ Class to define the airfoil.  Able to:
    Create:
      - RW Series
      - NACA 4
      - NACA 5
      - Biconvex
      - Joukowski
    Modify:
      - Invert
      - Rotate
      - Scale
    """

    # ==========================================================================
    # INITIALIZATION FUNCTION 
    def __init__(self):
        """ Initialize the airfoil 
            We aren't initializing the shape list as you can regenerate the airfoil
            indefinitely
        """
        self.foilType = ""
        self.numPoints = ""
        self.numPan = ""
        self.cType = ""
    # ==========================================================================

    # ==========================================================================
    # UTILITY FUNCTIONS        
    def setFoil(self,npts,ctype):
        """ Sets the number of points and panels for the airfoil 
            npts - should only be an odd number
        """
        self.numPoints = npts
        self.numPan = self.numPoints - 1
        self.cType = ctype
        
    def insertCoords(self,npts,x,y):
        """ Creates an airfoil based on file input 
            - Special function for the airfoil generator program
        """
        self.numPoints = npts
        self.numPan = self.numPoints - 1
        self.cType = "FILE LOAD"
        self.shape = []
        # SET SHAPE
        for i in range(self.numPoints):
            self.shape.append( (x[i],y[i]) )

    def invert(self):
        """ Inverts the y coordinates of the already made airfoil """
        for i in range(len(self.shape)):
            x = self.shape[i][0]
            y = self.shape[i][1]
            self.shape[i] = (x,-y)
        
    def rotate(self,aoa):
        """ Rotates that airfoil be the given angle in degrees """
        # Convert the given angle of attack to radians
        aoa = math.radians(aoa)
        for i in range(len(self.shape)):
            ox = self.shape[i][0]
            oy = self.shape[i][1]
            x = ox*math.cos(aoa)+oy*math.sin(aoa)
            y = -ox*math.sin(aoa)+oy*math.cos(aoa)
            self.shape[i] = (x,y)
            
    def scale(self,ms):
        """ Scales the coordinates of the already made airfoil """
        for i in range(len(self.shape)):
            x = self.shape[i][0]
            y = self.shape[i][1]
            self.shape[i] = (ms*x,ms*y)

    # drawFoil
    def drawFoil(self,canvas,WINX,WINY):
        self.points = []
        self.lines = []
        for i in range(len(self.shape)-1,-1,-1):
            x =  WINX*self.shape[i][0] + (WINX/6 - (WINX*self.shape[i][0])/4)
            y = -WINX*self.shape[i][1] + (WINY/2 - (WINY*self.shape[i][1])/4)
            self.lines.append( (x,y) )
            self.shape.append(canvas.create_rectangle(x-.01,y-.01,x+.01,y+.01,fill="#FFFFFF",outline="#FFFFFF",activeoutline="#00ff00"))
            
        self.line = canvas.create_line(self.lines,fill="#FFFFFF")

    def xCoords(self):
        """ Creates the x coordinates based on self.cType 
        
            cType = equal    - equidistant points
                  = fullcos  - full cosine spacing
        """
        x = []
        if self.cType == 'equal':
            for i in range(1,self.numPoints+1):
                if i == 1 or i == self.numPoints:
                    x.append(1.0)
                elif i > 1 and i < (self.numPan/2)+1:
                    x.append(abs(abs(((i*1.0)-1.0)/((self.numPan*1.0)/2.0))-1.0))
                elif i > (self.numPan/2)+1 and i < self.numPoints:
                    x.append(abs(1.0 - abs(((i*1.0)-1.0)/((self.numPan*1.0)/2.0))))
                elif i == (self.numPan/2)+1:
                    x.append(0.0)
        
        elif self.cType == 'fullcos':
            x1 = []
            for i in range(1,self.numPoints/2+1):
                x1.append(1.0-math.cos((i-1.0)*math.pi/((self.numPoints/2)-1))/2.0 - .5)
            # Insert a point at i = 1.75
            x1.insert(1,1.0-math.cos((1.75-1.0)*math.pi/((self.numPoints/2)-1))/2.0 - .5)
            for i in range(len(x1)-1,-1,-1):
                x.append(x1[i])
            for i in range(1,len(x1)):
                x.append(x1[i])
                
        return x

    
    def NACAParts(self,nacades,type):
        """ Based on type, return the parts of the NACA 4 or 5 series """
        if type == 4:
            n1 = nacades/1000
            n2 = (nacades%1000)/100
            n3 = nacades - ((n1*1000)+(n2*100))
            return n1/100.0, n2/10.0, n3/100.0
            return mc, pc, tc
        elif type == 5:
            n1 = nacades/100
            n2 = nacades%100
            return n1, n2/100.0
    # ==========================================================================

    # ==========================================================================
    # AIRFOIL THICKNESS FUNCTIONS
    def thick45(self,x,tc):
        thick = []
        for i in range(1,self.numPoints+1):
            cx = x[i-1]
            thick.append((tc/0.2)*((0.2969*math.sqrt(cx)-(0.126*cx)-(0.3516*cx*cx)+(0.2843*cx*cx*cx)-(0.1015*cx*cx*cx*cx))))
        return thick
    # ==========================================================================

    # ==========================================================================
    # AIRFOIL CAMBER LINE FUNCTIONS
    def mclNACA4(self,x,mc,pc):
        """ Generates the Mean Camber Line shape for a NACA 4 airfoil """
        mcl = []
        for i in range(len(x)):
            cx = x[i]
            if cx > 0 and cx < pc:
                tmp = (mc/(pc*pc)) * ((2.0*pc*cx) - (cx*cx))
            else:
                tmp = (mc/((1.0-pc)*(1.0-pc))) * ((1.0 - 2.0*pc) + (2.0*pc*cx) - (cx*cx))
            mcl.append(tmp)
        return mcl

    def mclNACA5(self,x,n):
        """ Generates the Mean Camber Line shape for a NACA 5 airfoil 
            
            n - first three numbers in the NACA 5 series airfoil designation
        """
        mcl = []
        pc = 0
        mc = 0
        k = 0
        # Figure out mc, pc, and k
        if n == 210:
            pc = 0.05
            mc = 0.0580
            k = 361.4
        elif n == 220:
            pc = 0.10
            mc = 0.1260
            k = 51.64
        elif n == 230:
            pc = 0.15
            mc = 0.2025
            k = 15.957
        elif n == 240:
            pc = 0.20
            mc = 0.200
            k = 6.643
        elif n == 250:
            pc = 0.25
            mc = 0.3910
            k = 3.230
        
        for i in range(1,self.numPoints+1):
            cx = x[i-1]
            if cx > 0 and cx < pc:
                tmp = (k/6.0) * ((cx*cx*cx) - (3.0*mc*cx*cx)+(mc*mc)*(3.0-mc)*cx)
            else:
                tmp = (k/6.0) * (mc*mc*mc) * (1.0 - cx)
            mcl.append(tmp)
        return mcl
    # ==========================================================================

    # ==========================================================================
    # **************************************************************************
    # **************************************************************************
    # ==========================================================================

    # ==========================================================================
    # AIRFOIL CREATION FUNCTIONS  
    def genNACA4(self,nacades):
        """ Generates a NACA 4 Series airfoil 
            nacades - the airfoil designation, ie. 2412
                      will get broken apart into pieces
        """
        # Set airfoil type
        self.foilType = "NACA4"
        # Set shape
        self.shape = []
        # Initialize y
        y = []
        # Get mc,pc,tc from nacades
        mc, pc, tc = self.NACAParts(nacades,4)
        # Get X Coordinates
        x = self.xCoords()
        # Get NACA 4 Mean Camber Line
        ymcl = self.mclNACA4(x,mc,pc)
        # Get thickness distribution
        yt = self.thick45(x,tc)
        
        # Loop through and generate y values
        for i in range(1,self.numPoints+1):
            j = i-1
            if i == 1 or i == (self.numPan/2)+1 or i == self.numPoints+1:
                y.append(0.0)
            elif i > 1 and i < (self.numPan/2)+1:
                y.append(ymcl[j]-yt[j])
            elif i > (self.numPan/2)+1 and i < self.numPoints+1:
                y.append(ymcl[j]+yt[j])
        
        # Set airfoil shape
        for i in range(len(x)):
            self.shape.append( (x[i],y[i]) )

    def genNACA5(self,nacades):
        """ Generates a NACA 5 Series airfoil """
        # Set airfoil type
        self.foilType = "NACA5"
        # Set shape
        self.shape = []
        # Initialize y
        y = []
        # Break apart NACA designation
        n1, tc = self.NACAParts(nacades,5)
        # Get X Coordinates
        x = self.xCoords()
        # Get NACA 4 Mean Camber Line
        ymcl = self.mclNACA5(x,n1)
        # Get thickness distribution
        yt = self.thick45(x,tc)
        
        # Loop through and generate y values
        for i in range(1,self.numPoints+1):
            j = i-1
            if i == 1 or i == (self.numPan/2)+1 or i == self.numPoints+1:
                y.append(0.0)
            elif i > 1 and i < (self.numPan/2)+1:
                y.append(ymcl[j]-yt[j])
            elif i > (self.numPan/2)+1 and i < self.numPoints+1:
                y.append(ymcl[j]+yt[j])
        
        # Set airfoil shape
        for i in range(len(x)):
            self.shape.append( (x[i],y[i]) )
            
    def genBCX(self,tc):
        """ Generates a Biconvex airfoil of the given thickness to chord ratio """
        # Set airfoil type
        self.foilType = "BCX"
        # Set shape
        self.shape = []
        # Initialize y
        y = []
        # Get X Coordinates
        x = self.xCoords()
        
        # Loop through and generate y values
        for i in range(1,self.numPoints+1):
            j = i-1
            tmp = (x[j]-(1.0/2.0))**2 *tc*2.0 - tc/2.0
            if i == 1 or i == (self.numPan/2)+1 or i == self.numPoints+1:
                y.append(0.0)
            elif i > 1 and i < (self.numPan/2)+1:
                y.append(tmp)
            elif i > (self.numPan/2)+1 and i < self.numPoints+1:
                y.append(-tmp)
        
        # Set airfoil shape
        for i in range(len(x)):
            self.shape.append( (x[i],y[i]) )
     
    def genJoukowski(self,npts,mr,ml):
        """ Generates a Joukowski airfoil given mr and ml 
            Due to the use of c = 1 for the circle, mr and ml
            need to be limited to 0.4.
            
            This code will also translate the coordinates to the 
            [0,1] domain in x.
        """
        # Set airfoil type
        self.foilType = "JOUK"
        # Define lists
        self.shape = []
        xi = []
        eta = []
        x = []
        y = []
        # Set self.numPoints
        self.numPoints = npts
        # Calculate a
        a = math.sqrt((1.0-mr)*(1.0-mr) + ml*ml)
        # Set up xi and eta
        for i in range(1,self.numPoints+1):
            tr = math.radians(i-1.0)
            xi.append(mr+a*math.cos(tr))
            eta.append(ml+a*math.sin(tr))
        
        # Set x and y and fill in shape list
        for i in range(len(xi)):
            # CHORD = 1 For Unit Airfoil
            # X(I) = XI(I) + CHORD**2.0D0*XI(I)/(XI(I)**2.0D0+ETA(I)**2.0D0)
            # Y(I) = ETA(I) - CHORD**2.0D0*ETA(I)/(XI(I)**2.0D0+ETA(I)**2.0D0)
            x.append((xi[i]+1.0*xi[i]/(xi[i]*xi[i]+eta[i]*eta[i])))
            y.append((eta[i]-1.0*eta[i]/(xi[i]*xi[i]+eta[i]*eta[i])))
            
        mx = max(x) + abs(min(x))
        my = max(y)
        for i in range(len(x)):
            x[i] = x[i] / (2.0*mx)
            y[i] = y[i] / (2.0*my)
        
        mx2 = min(x)
        for i in range(len(x)):
            x[i] = x[i] - mx2
        
        for i in range(len(x)):
            self.shape.append( (x[i],y[i]) )
            
    # ==========================================================================                

    # ==========================================================================
    # DEBUG
    def output(self):
        #for i in range(len(self.x)):
        #    print self.x[i]
        for i in range(len(self.shape)):
            print self.shape[i][0], self.shape[i][1]
    def fileoutput(self, filename):
    
        #for i in range(len(self.x)):
        #    print self.x[i]
        f = open(filename, 'wb')
        f.write('airfoil\n')
        for i in range(len(self.shape)):
            print self.shape[i][0], self.shape[i][1]
            f.write('%s %s\n'%(self.shape[i][0], self.shape[i][1]))
        f.close()
    # ==========================================================================

if __name__ == "__main__":

    airfoil = Airfoil()
    airfoil.setFoil(201,"fullcos")
    
    airfoil.genNACA4(0010)
    #airfoil.genNACA5(21010)
    #airfoil.genJoukowski(361,-1./10.,1./10.)
    #airfoil.genBCX(.01)
    
    airfoil.output()
    
    #airfoil.rotate(5.0)
    #airfoil.scale(300.0)
    #airfoil.output()
    airfoil.fileoutput('../../0010.dat')

