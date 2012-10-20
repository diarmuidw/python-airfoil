#!Joseph Moster
#Copyright 2011

import csv
import sys
import getopt
import os.path

from pysvg.shape import *
from pysvg.builders import *


#def ComplexShapes():
def main(argv):                         
    filename = './ag03.dat'
    chord = 10
                      
    try:
        opts, args = getopt.getopt(argv, "c:f:", ["chord=", "filename="])
    except getopt.GetoptError:          
        usage()                         
        sys.exit(2)
    
    for opt, arg in opts:                
        if opt in ("-c", "chord="):      
            chord = float(arg)               
        elif opt in ("-f", "filename="): 
            filename = str(arg)             

    
    
    #I found the below constant on the internet,  this could use verification
    scale = 100 
    xOffset = 0 
    yOffset = 0 
    
    pts = ""
    line= 0
    # Read airfoil data
    spamReader = csv.reader(open(filename, 'rb'), delimiter=' ', quotechar='|', skipinitialspace="true")
    for row in spamReader:
        #Skip the first line of header information
        if(line!=0):
            #Format and store in a string
            pts+= str((float(row[0])*chord+xOffset)*scale)+","+str((float(row[1])*-chord+yOffset)*scale)+"  "
        line=1            

    oh=ShapeBuilder()
    mySVG=svg("test")
    #Create a polyline using the formatted airfoil data string
    pl=oh.createPolyline(points=pts,strokewidth=1, stroke='blue')
    mySVG.addElement(pl)

    (root, ext) = os.path.splitext(filename)
    saveName = root+'.svg'    
    mySVG.save(saveName)
 
if __name__ == "__main__":
    main(sys.argv[1:])



