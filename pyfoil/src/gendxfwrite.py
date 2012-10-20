#!Joseph Moster
#Copyright 2011

import csv
import sys
import getopt
import os.path


from dxfwrite import DXFEngine as dxf


def main(argv):                         
    filename = '../../ag03.dat'
    chord = 10
                      
    try:
        opts, args = getopt.getopt(argv, "c:f:o:", ["chord=", "filename=", "outputfilename="])
    except getopt.GetoptError:          
        usage()                         
        sys.exit(2)
    
    for opt, arg in opts:                
        if opt in ("-c", "chord="):      
            chord = float(arg)               
        elif opt in ("-f", "filename="): 
            filename = str(arg)    
        elif opt in ("-o", "outputfilename="): 
            outputfilename = str(arg)          

    #DXF related INIT
    (root, ext) = os.path.splitext(outputfilename)
    saveName = root+'.dxf'    
    drawing = dxf.drawing(saveName)
    #I found the below constant on the internet,  this could use verification
    scale = 100 
    xOffset = 0 
    yOffset = 0
    
    
    linePoints = []
    #pts = ""
    line= 0
    # Read airfoil data
    spamReader = csv.reader(open(filename, 'rb'), delimiter=' ', quotechar='|', skipinitialspace="true")
    for row in spamReader:
        #Skip the first line of header information
        if(line!=0):
            #Format and store in a string
            p= ((float(row[0])*chord+xOffset)*scale, (float(row[1])*-chord+yOffset)*scale)
            linePoints.append(p)
            
        line=1            
    print linePoints
    
    polyline= dxf.polyline(linetype='CONTINUOUS')
    polyline.add_vertices( linePoints )
    drawing.add(polyline)
    drawing.save()
    
    
    
if __name__ == "__main__":
	main(sys.argv[1:])

#python foil2svg1.py -c 3 -f ../../0010.dat -o ../../0010.svg

