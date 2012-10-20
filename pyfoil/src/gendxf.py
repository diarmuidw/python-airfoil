#!Joseph Moster
#Copyright 2011

import csv
import sys
import getopt
import os.path


import sdxf
#http://www.kellbot.com/sdxf-python-library-for-dxf/


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
    
    d=sdxf.Drawing()
    d.layers.append(sdxf.Layer(name="textlayer",color=3))
    d.layers.append(sdxf.Layer(name="drawinglayer",color=2))
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
            d.layers.append(sdxf.Point(points=(row[0], row[1]), layer="drawinglayer"))
        line=1            
    print linePoints
    d.append(sdxf.Text('Hello World!',point=(3,0),layer="textlayer"))
    d.layers.append(sdxf.Layer(name="drawinglayer",color=2))
    d.append(sdxf.Text('BLUEKULU!',point=(20,20),layer="drawinglayer"))
    #d.layers.append(sdxf.LineList(points=linePoints, layer="drawinglayer"))
    

    (root, ext) = os.path.splitext(outputfilename)
    saveName = root+'.dxf'    
    d.saveas(saveName)
 
if __name__ == "__main__":
	main(sys.argv[1:])

#python foil2svg1.py -c 3 -f ../../0010.dat -o ../../0010.svg

