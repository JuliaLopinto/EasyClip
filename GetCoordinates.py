#! /usr/bin/python
# -*- coding: utf-8 -*-

from __main__ import vtk, qt, slicer, ctk

import numpy

m_Red = numpy.matrix([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
m_Green = numpy.matrix([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
m_Yellow = numpy.matrix([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
#
# Test : Get the coordinates of the modified slice by clipping
#

class GetCoordinates:
    def __init__(self, parent):
        parent.title = "TestCoordinates"
        parent.categories = ["GetCoordinates"]

        self.parent = parent

class GetCoordinatesWidget:
    def __init__(self, parent = None):
        if not parent:
            self.parent = slicer.qMRMLWidget()
            self.parent.setLayout(qt.QVBoxLayout())
            self.parent.setMRMLScene(slicer.mrmlScene)
        else:
            self.parent = parent
        self.layout = self.parent.layout()
        if not parent:
            self.setup()
            self.parent.show()

    def setup(self):
        ##########################################################
        #                   Global Variable                      #
        ##########################################################
        
        
        #---------------------- RED SLICE -----------------------#
        self.test = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeRed')
        self.matRed = self.test.GetSliceToRAS()
        
        # Matrix with the elements of SliceToRAS
        self.m_Red = numpy.matrix([[self.matRed.GetElement(0,0), self.matRed.GetElement(0,1), self.matRed.GetElement(0,2), self.matRed.GetElement(0,3)],
                                   [self.matRed.GetElement(1,0), self.matRed.GetElement(1,1), self.matRed.GetElement(1,2), self.matRed.GetElement(1,3)],
                                   [self.matRed.GetElement(2,0), self.matRed.GetElement(2,1), self.matRed.GetElement(2,2), self.matRed.GetElement(2,3)],
                                   [self.matRed.GetElement(3,0), self.matRed.GetElement(3,1), self.matRed.GetElement(3,2), self.matRed.GetElement(3,3)]])
                              
                              
                            
        #---------------------- YELLOW SLICE ----------------------#
        self.test = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeYellow')
        self.matYellow = self.test.GetSliceToRAS()
            
                              
        # Matrix with the elements of SliceToRAS
        self.m_Yellow = numpy.matrix([[self.matYellow.GetElement(0,0), self.matYellow.GetElement(0,1), self.matYellow.GetElement(0,2), self.matYellow.GetElement(0,3)],
                                      [self.matYellow.GetElement(1,0), self.matYellow.GetElement(1,1), self.matYellow.GetElement(1,2), self.matYellow.GetElement(1,3)],
                                      [self.matYellow.GetElement(2,0), self.matYellow.GetElement(2,1), self.matYellow.GetElement(2,2), self.matYellow.GetElement(2,3)],
                                      [self.matYellow.GetElement(3,0), self.matYellow.GetElement(3,1), self.matYellow.GetElement(3,2), self.matYellow.GetElement(3,3)]])
            
                                                       
        #---------------------- GREEN SLICE ----------------------#
        self.test = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeGreen')
        self.matGreen = self.test.GetSliceToRAS()
            
                                                       
        # Matrix with the elements of SliceToRAS
        self.m_Green = numpy.matrix([[self.matGreen.GetElement(0,0), self.matGreen.GetElement(0,1), self.matGreen.GetElement(0,2), self.matGreen.GetElement(0,3)],
                                     [self.matGreen.GetElement(1,0), self.matGreen.GetElement(1,1), self.matGreen.GetElement(1,2), self.matGreen.GetElement(1,3)],
                                     [self.matGreen.GetElement(2,0), self.matGreen.GetElement(2,1), self.matGreen.GetElement(2,2), self.matGreen.GetElement(2,3)],
                                     [self.matGreen.GetElement(3,0), self.matGreen.GetElement(3,1), self.matGreen.GetElement(3,2), self.matGreen.GetElement(3,3)]])
        
        #---------------------- Coefficient ----------------------#
        self.a_red = 0
        self.b_red = 0
        self.c_red = 0
        self.d_red = 0
        
        self.a_yellow = 0
        self.b_yellow = 0
        self.c_yellow = 0
        self.d_yellow = 0
        
        self.a_green = 0
        self.b_green = 0
        self.c_green = 0
        self.d_green = 0
        
        # Normal vector to the Red slice:
        self.n_vector = numpy.matrix([[0],[0],[1],[1]])
        
        # point on the Red slice:
        self.A = numpy.matrix([[0],[0],[0],[1]])
        
        # Instantiate and connect widgets ...

        # Collapsible button
        sampleCollapsibleButton = ctk.ctkCollapsibleButton()
        sampleCollapsibleButton.text = "A collapsible button"
        self.layout.addWidget(sampleCollapsibleButton)


        # Layout within the sample collapsible button
        sampleFormLayout = qt.QFormLayout(sampleCollapsibleButton)

        # Get Coordinates button
        getCoordButton = qt.QPushButton("Get Coordinates")
        sampleFormLayout.addWidget(getCoordButton)
        getCoordButton.connect('clicked(bool)', self.getCoordButtonClicked)

        # Add vertical spacer
        self.layout.addStretch(1)

        # Set local var as instance attribute
        self.getCoordButton = getCoordButton
    
        # Save
        save = qt.QPushButton("Save plan")
        sampleFormLayout.addWidget(save)
        save.connect('clicked(bool)', self.saveClicked)
    
        # Add vertical spacer
        self.layout.addStretch(1)
    
        # Set local var as instance attribute
        self.save = save

        # Get Coordinates button
        getClippingRed = qt.QPushButton("Clipping Red Plane")
        sampleFormLayout.addWidget(getClippingRed)
        getClippingRed.connect('clicked(bool)', self.getClippingClickedRed)

        # Add vertical spacer
        self.layout.addStretch(1)
    
        # Set local var as instance attribute
        self.getClippingRed = getClippingRed
    
        # Get Coordinates button
        getClippingYellow = qt.QPushButton("Clipping Yellow Plane")
        sampleFormLayout.addWidget(getClippingYellow)
        getClippingYellow.connect('clicked(bool)', self.getClippingClickedYellow)
    
        # Add vertical spacer
        self.layout.addStretch(1)
    
        # Set local var as instance attribute
        self.getClippingYellow = getClippingYellow
    
        # Get Coordinates button
        getClippingGreen = qt.QPushButton("Clipping Green Plane")
        sampleFormLayout.addWidget(getClippingGreen)
        getClippingGreen.connect('clicked(bool)', self.getClippingClickedGreen)
    
        # Add vertical spacer
        self.layout.addStretch(1)
    
        # Set local var as instance attribute
        self.getClippingGreen = getClippingGreen
    
        # reload button
        # (use this during development, but remove it when delivering
        #  your module to users)
        #self.reloadButton = qt.QPushButton("Reload")
        #self.reloadButton.toolTip = "Reload this module."
        #self.reloadButton.name = "TestCoordinates Reload"
        #sampleFormLayout.addWidget(self.reloadButton)
        #self.reloadButton.connect('clicked()', self.onReload)
    

    def getCoordButtonClicked(self):
        
        
        #------------------- PLAN -----------------#

        # AXES FOR THE PLAN :

        #           |z
        #           |
        #           |________y
        #          /
        #         /
        #        /x

        # YELLOW PLAN : the equation is the coordinates on the x axis
        # GREEN PLAN : the equation is the coordinates on the y axis
        # RED PLAN : the equation is the coordinates on the z axis

        # RED PLAN:
        self.n_NewRedPlan = self.m_Red * self.n_vector
        print "n : \n", self.n_NewRedPlan
        
        self.A_NewRedPlan = self.m_Red * self.A
        print "A : \n", self.A_NewRedPlan
        
        self.a_red = self.n_NewRedPlan[0]
        self.b_red = self.n_NewRedPlan[1]
        self.c_red = self.n_NewRedPlan[2]
        self.d_red = self.n_NewRedPlan[0]*self.A_NewRedPlan[0] + self.n_NewRedPlan[1]*self.A_NewRedPlan[1] + self.n_NewRedPlan[2]*self.A_NewRedPlan[2]
        
        print "Red plan equation : \n", self.a_red ,"* x + ", self.b_red , "* y + ", self.c_red , "* z + ", self.d_red ," = 0 "
        
        # YELLOW PLAN:
        self.n_NewYellowPlan = self.m_Yellow * self.n_vector
        print "n : \n", self.n_NewYellowPlan

        self.A_NewYellowPlan = self.m_Yellow * self.A
        print "A : \n", self.A_NewYellowPlan
        
        self.a_yellow = self.n_NewYellowPlan[0]
        self.b_yellow = self.n_NewYellowPlan[1]
        self.c_yellow = self.n_NewYellowPlan[2]
        self.d_yellow = self.n_NewYellowPlan[0]*self.A_NewYellowPlan[0] + self.n_NewYellowPlan[1]*self.A_NewYellowPlan[1] + self.n_NewYellowPlan[2]*self.A_NewYellowPlan[2]
        
        print "Yellow plan equation : \n", self.a_yellow ,"* x + ", self.b_yellow , "* y + ", self.c_yellow , "* z + ", self.d_yellow ," = 0 "

        # GREEN PLAN:
        self.n_NewGreenPlan = self.m_Green * self.n_vector
        print "n : \n", self.n_NewGreenPlan

        self.A_NewGreenPlan = self.m_Green * self.A
        print "A : \n", self.A_NewGreenPlan

        self.a_green = self.n_NewGreenPlan[0]
        self.b_green = self.n_NewGreenPlan[1]
        self.c_green = self.n_NewGreenPlan[2]
        self.d_green = self.n_NewGreenPlan[0]*self.A_NewGreenPlan[0] + self.n_NewGreenPlan[1]*self.A_NewGreenPlan[1] + self.n_NewGreenPlan[2]*self.A_NewGreenPlan[2]

        print "Green plan equation : \n", self.a_green ,"* x + ", self.b_green , "* y + ", self.c_green , "* z + ", self.d_green ," = 0 "



    def saveClicked(self):
        NomFichier = '/Users/jlop/Desktop/PROJET_Julia/Codes_Python/plan_equation.txt'
        fichier = open(NomFichier,"w")
        fichier.write("Plan equation for the Green Slice \n")
        fichier.write("SliceToRAS Red Slice: \n")
        fichier.write(str(self.m_Red) +'\n')
        fichier.write('\n')
        fichier.write("Coefficients for the plan: \n")
        fichier.write("a:" + str(self.a_red) + '\n')
        fichier.write("b:" + str(self.b_red) + '\n')
        fichier.write("c:" + str(self.c_red) + '\n')
        fichier.write("d:" + str(self.d_red) + '\n')
        
        fichier.write("SliceToRAS Yellow Slice: \n")
        fichier.write(str(self.m_Yellow) +'\n')
        fichier.write('\n')
        fichier.write("Coefficients for the plan: \n")
        fichier.write("a:" + str(self.a_yellow) + '\n')
        fichier.write("b:" + str(self.b_yellow) + '\n')
        fichier.write("c:" + str(self.c_yellow) + '\n')
        fichier.write("d:" + str(self.d_yellow) + '\n')
        
        
        fichier.write("SliceToRAS Green Slice: \n")
        fichier.write(str(self.m_Green) +'\n')
        fichier.write('\n')
        fichier.write("Coefficients for the plan: \n")
        fichier.write("a:" + str(self.a_green) + '\n')
        fichier.write("b:" + str(self.b_green) + '\n')
        fichier.write("c:" + str(self.c_green) + '\n')
        fichier.write("d:" + str(self.d_green) + '\n')
        
        
        fichier.close()
        
        
    def getClippingClickedRed(self):
        model = slicer.util.getNode('Model_GM_T0_Reg_MD_novo')
        polyData = model.GetPolyData()
            
        PolyAlgorithm = vtk.vtkClipClosedSurface()
        PolyAlgorithm.SetInput(polyData)
            
        plane = vtk.vtkPlane()
        plane.SetOrigin(self.A_NewRedPlan[0],self.A_NewRedPlan[1],self.A_NewRedPlan[2])
        plane.SetNormal(self.n_NewRedPlan[0],self.n_NewRedPlan[1],-self.n_NewRedPlan[2])
            
        planeCollection = vtk.vtkPlaneCollection()
        planeCollection.AddItem(plane)
            
        clipper = vtk.vtkClipClosedSurface()
        clipper.SetClippingPlanes(planeCollection)
        clipper.SetInputConnection(PolyAlgorithm.GetOutputPort())
        clipper.SetGenerateFaces(1)
        clipper.SetScalarModeToLabels()
        clipper.Update()
        PolyDataNew = clipper.GetOutput()
            
        model.SetAndObservePolyData(PolyDataNew)


    def getClippingClickedYellow(self):
        model = slicer.util.getNode('Model_GM_T0_Reg_MD_novo')
        polyData = model.GetPolyData()
    
        PolyAlgorithm = vtk.vtkClipClosedSurface()
        PolyAlgorithm.SetInput(polyData)
    
        plane = vtk.vtkPlane()
        plane.SetOrigin(self.A_NewYellowPlan[0],self.A_NewYellowPlan[1],self.A_NewYellowPlan[2])
        plane.SetNormal(self.n_NewYellowPlan[0],self.n_NewYellowPlan[1],self.n_NewYellowPlan[2])
    
        planeCollection = vtk.vtkPlaneCollection()
        planeCollection.AddItem(plane)
    
        clipper = vtk.vtkClipClosedSurface()
        clipper.SetClippingPlanes(planeCollection)
        clipper.SetInputConnection(PolyAlgorithm.GetOutputPort())
        clipper.SetGenerateFaces(1)
        clipper.SetScalarModeToLabels()
        clipper.Update()
        PolyDataNew = clipper.GetOutput()
    
        model.SetAndObservePolyData(PolyDataNew)

    def getClippingClickedGreen(self):
        model = slicer.util.getNode('Model_GM_T0_Reg_MD_novo')
        polyData = model.GetPolyData()
    
        PolyAlgorithm = vtk.vtkClipClosedSurface()
        PolyAlgorithm.SetInput(polyData)
    
        plane = vtk.vtkPlane()
        plane.SetOrigin(self.A_NewGreenPlan[0],self.A_NewGreenPlan[1],self.A_NewGreenPlan[2])
        plane.SetNormal(self.n_NewGreenPlan[0],self.n_NewGreenPlan[1],self.n_NewGreenPlan[2])
        
        planeCollection = vtk.vtkPlaneCollection()
        planeCollection.AddItem(plane)
    
        clipper = vtk.vtkClipClosedSurface()
        clipper.SetClippingPlanes(planeCollection)
        clipper.SetInputConnection(PolyAlgorithm.GetOutputPort())
        clipper.SetGenerateFaces(1)
        clipper.SetScalarModeToLabels()
        clipper.Update()
        PolyDataNew = clipper.GetOutput()
    
        model.SetAndObservePolyData(PolyDataNew)



    
    
    



