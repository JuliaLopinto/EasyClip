from __main__ import vtk, qt, ctk, slicer

import numpy

#
# Load Files
#

class EasyClip:
    def __init__(self, parent):
        parent.title = "Easy Clip Tool"
        parent.categories = ["Easy Clip"]
        
        self.parent = parent

#
# qHelloPythonWidget
#

class EasyClipWidget:
    def __init__(self, parent = None):
        
        self.developerMode = True # change this to true to get reload and test
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
        
        # Collapsible button -- Scene Description
        self.loadCollapsibleButton = ctk.ctkCollapsibleButton()
        self.loadCollapsibleButton.text = "Scene"
        self.layout.addWidget(self.loadCollapsibleButton)
        
        # Layout within the laplace collapsible button
        self.loadFormLayout = qt.QFormLayout(self.loadCollapsibleButton)
        
        list_model = qt.QLabel("List of models:")
        self.loadFormLayout.addWidget(list_model)
        
        inputModelList = slicer.qMRMLNodeAttributeTableView()
        numNodes = slicer.mrmlScene.GetNumberOfNodesByClass("vtkMRMLModelNode")
        for i in range (3,numNodes):
            mh = slicer.mrmlScene.GetNthNodeByClass(i,"vtkMRMLModelNode" )
            print mh.GetName()
            inputModelList.addAttribute()
            inputModelList.setAttribute(i-2, mh.GetName())
    
        self.loadFormLayout.addWidget(inputModelList)
        
        # Add vertical spacer
        self.layout.addStretch(1)
        
        # Collapsible button -- Clipping part
        self.loadCollapsibleButton = ctk.ctkCollapsibleButton()
        self.loadCollapsibleButton.text = "Clipping"
        self.layout.addWidget(self.loadCollapsibleButton)
        
        # Layout within the laplace collapsible button
        self.loadFormLayout = qt.QFormLayout(self.loadCollapsibleButton)
        
        #--------------------------- Planes --------------------------#
        
        label = qt.QLabel("Choose the plane you want to use:")
        self.loadFormLayout.addWidget(label)
        
        groupBox = qt.QGroupBox("Plane")
        self.loadFormLayout.addWidget(groupBox)
        
        self.redPlaneCheckBox = qt.QCheckBox("Red Plane")
        self.loadFormLayout.addWidget(self.redPlaneCheckBox)
        self.redPlaneCheckBox.connect('clicked(bool)', self.redPlaneCheckBoxClicked)
        
        # Add vertical spacer
        self.layout.addStretch(1)
        
        
        self.yellowPlaneCheckBox = qt.QCheckBox("Yellow Plane")
        self.loadFormLayout.addWidget(self.yellowPlaneCheckBox)
        self.yellowPlaneCheckBox.connect('clicked(bool)', self.yellowPlaneCheckBoxClicked)
        
        # Add vertical spacer
        self.layout.addStretch(1)
        
        
        self.greenPlaneCheckBox = qt.QCheckBox("Green Plane")
        self.loadFormLayout.addWidget(self.greenPlaneCheckBox)
        self.greenPlaneCheckBox.connect('clicked(bool)', self.greenPlaneCheckBoxClicked)
        # Add vertical spacer
        self.layout.addStretch(1)
        
        
        #-------------------------- Buttons --------------------------#
        # GET COORDINATES BUTTON
        getCoordButton = qt.QPushButton("Get Coordinates")
        self.loadFormLayout.addWidget(getCoordButton)
        getCoordButton.connect('clicked(bool)', self.getCoordButtonClicked)
        
        # Add vertical spacer
        self.layout.addStretch(1)
        
        # SAVE PLANE BUTTON
        save = qt.QPushButton("Save plane")
        self.loadFormLayout.addWidget(save)
        save.connect('clicked(bool)', self.saveClicked)
        
        # READ PLANE BUTTON
        read = qt.QPushButton("Read plane")
        self.loadFormLayout.addWidget(read)
        read.connect('clicked(bool)', self.readFile)
        
        # Add vertical spacer
        self.layout.addStretch(1)
        
        
        vbox = qt.QVBoxLayout()
        
        vbox.addWidget(self.redPlaneCheckBox)
        vbox.addWidget(self.yellowPlaneCheckBox)
        vbox.addWidget(self.greenPlaneCheckBox)
        vbox.addWidget(getCoordButton)
        vbox.addWidget(save)
        vbox.addWidget(read)
        
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        
        
        groupBox3 = qt.QGroupBox("Clipping")
        self.loadFormLayout.addWidget(groupBox3)
        
        # CLIPPING BUTTONS
        buttonFrame = qt.QFrame(self.parent)
        buttonFrame.setLayout(qt.QHBoxLayout())
        self.layout.addWidget(buttonFrame)
        
        
        self.ClippingButton = qt.QPushButton("Clipping")
        buttonFrame.layout().addWidget(self.ClippingButton)
        self.ClippingButton.connect('clicked()', self.ClippingButtonClicked)
        
        self.UndoButton = qt.QPushButton("Undo")
        buttonFrame.layout().addWidget(self.UndoButton)
        self.UndoButton.connect('clicked()', self.UndoButtonClicked)
        
        # Add vertical spacer
        self.layout.addStretch(1)
        
        
        label2 = qt.QLabel("Choose the part you want to keep:")
        self.loadFormLayout.addWidget(label2)
        
        red_plane = qt.QCheckBox("Red Slice Clipping:")
        self.loadFormLayout.addWidget(red_plane)
        
        
        buttonFrame1 = qt.QFrame(self.parent)
        buttonFrame1.setLayout(qt.QHBoxLayout())
        self.layout.addWidget(buttonFrame1)
        self.radio_red_Neg = qt.QRadioButton("Negative")
        buttonFrame1.layout().addWidget(self.radio_red_Neg)
        self.radio_red_Pos = qt.QRadioButton("Positive")
        buttonFrame1.layout().addWidget(self.radio_red_Pos)
        
        self.radio_red_Neg.connect('clicked(bool)', self.radio_redClicked)
        self.radio_red_Pos.connect('clicked(bool)', self.radio_redClicked)
        
        
        yellow_plane = qt.QCheckBox("Yellow Slice Clipping:")
        self.loadFormLayout.addWidget(yellow_plane)
        
        
        buttonFrame2 = qt.QFrame(self.parent)
        buttonFrame2.setLayout(qt.QHBoxLayout())
        self.layout.addWidget(buttonFrame2)
        
        self.radio_yellow_Neg = qt.QRadioButton("Negative")
        buttonFrame2.layout().addWidget(self.radio_yellow_Neg)
        self.radio_yellow_Pos = qt.QRadioButton("Positive")
        buttonFrame2.layout().addWidget(self.radio_yellow_Pos)
        
        self.radio_yellow_Neg.connect('clicked(bool)', self.radio_YellowClicked)
        self.radio_yellow_Pos.connect('clicked(bool)', self.radio_YellowClicked)
        
        
        green_plane = qt.QCheckBox("Green Slice Clipping:")
        self.loadFormLayout.addWidget(green_plane)
        
        
        buttonFrame3 = qt.QFrame(self.parent)
        buttonFrame3.setLayout(qt.QHBoxLayout())
        self.layout.addWidget(buttonFrame3)
        
        self.radio_green_Neg= qt.QRadioButton("Negative")
        buttonFrame3.layout().addWidget(self.radio_green_Neg)
        self.radio_green_Pos = qt.QRadioButton("Positive")
        buttonFrame3.layout().addWidget(self.radio_green_Pos)
        
        self.radio_green_Neg.connect('clicked(bool)', self.radio_GreenClicked)
        self.radio_green_Pos.connect('clicked(bool)', self.radio_GreenClicked)
        
        vbox3 = qt.QVBoxLayout()
        
        vbox3.addWidget(label2)
        vbox3.addWidget(red_plane)
        vbox3.addWidget(buttonFrame1)
        vbox3.addWidget(yellow_plane)
        vbox3.addWidget(buttonFrame2)
        vbox3.addWidget(green_plane)
        vbox3.addWidget(buttonFrame3)
        
        
        vbox3.addWidget(buttonFrame)
        
        vbox3.addStretch(1)
        groupBox3.setLayout(vbox3)
        
        
        # Add vertical spacer
        self.layout.addStretch(1)
        
        # Set local var as instance attribute
        self.groupBox3 = groupBox3
        
        
        # CLIPPING BUTTONS
        if self.developerMode:
            buttonFrame = qt.QFrame(self.parent)
            buttonFrame.setLayout(qt.QHBoxLayout())
            self.layout.addWidget(buttonFrame)
            
            
            self.reloadButton = qt.QPushButton("Reload")
            buttonFrame.layout().addWidget(self.reloadButton)
            self.reloadButton.connect('clicked()', self.onReload)
            
            
            # Add vertical spacer
            self.layout.addStretch(1)
        
        # Collapsible button -- Clipping part
        self.loadCollapsibleButton = ctk.ctkCollapsibleButton()
        self.loadCollapsibleButton.text = "Advanced"
        self.layout.addWidget(self.loadCollapsibleButton)
        
        # Layout within the laplace collapsible button
        self.loadFormLayout = qt.QFormLayout(self.loadCollapsibleButton)
    
    #----------------- Information about planes ------------------#
    
    #-------------------- Loading CSV files ----------------------#
    
    
    
    def onReload(self,moduleName="Interface"):
        globals()[moduleName] = slicer.util.reloadScriptedModule(moduleName)
    
    
    def redPlaneCheckBoxClicked(self):
        redslice = slicer.util.getNode('vtkMRMLSliceNodeRed')
        if self.redPlaneCheckBox.isChecked():
            redslice.SetWidgetVisible(True)
        if not self.redPlaneCheckBox.isChecked():
            redslice.SetWidgetVisible(False)
    
    def yellowPlaneCheckBoxClicked(self):
        yellowslice = slicer.util.getNode('vtkMRMLSliceNodeYellow')
        if self.yellowPlaneCheckBox.isChecked():
            yellowslice.SetWidgetVisible(True)
        if not self.yellowPlaneCheckBox.isChecked():
            yellowslice.SetWidgetVisible(False)
    
    def greenPlaneCheckBoxClicked(self):
        greenslice = slicer.util.getNode('vtkMRMLSliceNodeGreen')
        if self.greenPlaneCheckBox.isChecked():
            greenslice.SetWidgetVisible(True)
        if not self.greenPlaneCheckBox.isChecked():
            greenslice.SetWidgetVisible(False)


    def getCoordButtonClicked(self):
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
        fichier.write("SliceToRAS Red Slice: \n")
        fichier.write(str(self.m_Red) +'\n')
        fichier.write('\n')
        
        fichier.write("SliceToRAS Yellow Slice: \n")
        fichier.write(str(self.m_Yellow) +'\n')
        fichier.write('\n')
            
        fichier.write("SliceToRAS Green Slice: \n")
        fichier.write(str(self.m_Green) +'\n')
        fichier.write('\n')
        
        fichier.write("Coefficients for the Red plane: \n")
        fichier.write("a:" + str(self.a_red) + '\n')
        fichier.write("b:" + str(self.b_red) + '\n')
        fichier.write("c:" + str(self.c_red) + '\n')
        fichier.write("d:" + str(self.d_red) + '\n')
        
        fichier.write('\n')
        fichier.write("Coefficients for the Yellow plane: \n")
        fichier.write("a:" + str(self.a_yellow) + '\n')
        fichier.write("b:" + str(self.b_yellow) + '\n')
        fichier.write("c:" + str(self.c_yellow) + '\n')
        fichier.write("d:" + str(self.d_yellow) + '\n')
        
        fichier.write('\n')
        fichier.write("Coefficients for the Green plane: \n")
        fichier.write("a:" + str(self.a_green) + '\n')
        fichier.write("b:" + str(self.b_green) + '\n')
        fichier.write("c:" + str(self.c_green) + '\n')
        fichier.write("d:" + str(self.d_green) + '\n')
            
            
        fichier.close()
    
    def readFile(self):
        fichier2=open('/Users/jlop/Desktop/PROJET_Julia/Codes_Python/plan_equation.txt','r')
        fichier2.readline()
        test = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeRed')
        matRed = test.GetSliceToRAS()
        for i in range (0,4):
        
            for j in range (0,4):
                ligne = fichier2.readline()
                ligne = ligne.replace('[','')
                ligne = ligne.replace('   ',' ')
                ligne = ligne.replace(']','')
                #ligne = ligne.replace('.',' ')
                print ligne
        fichier2.close()



    def radio_redClicked(self):
        if self.radio_red_Neg.isChecked():
            print "Keep the negative part of the red plane"
        
        if self.radio_red_Pos.isChecked():
            print "Keep the positive part of the red plane"

    def radio_YellowClicked(self):
        if self.radio_yellow_Neg.isChecked():
            print "Keep the negative part of the yellow plane"
    
        if self.radio_yellow_Pos.isChecked():
            print "Keep the positive part of the yellow plane"

    def radio_GreenClicked(self):
        if self.radio_green_Neg.isChecked():
            print "Keep the negative part of the green plane"
    
        if self.radio_green_Pos.isChecked():
            print "Keep the positive part of the green plane"


    def ClippingButtonClicked(self):
        
        numNodes = slicer.mrmlScene.GetNumberOfNodesByClass("vtkMRMLModelNode")
        for i in range (3,numNodes):
            mh = slicer.mrmlScene.GetNthNodeByClass(i,"vtkMRMLModelNode" )
            self.model = slicer.util.getNode(mh.GetName())
            self.polyData = self.model.GetPolyData()
            PolyAlgorithm = vtk.vtkClipClosedSurface()
            PolyAlgorithm.SetInputData(self.polyData)
        
            # Clipping in the direction of the normal vector
            plane = vtk.vtkPlane()
        
            #Condition for the red plane
            if self.radio_red_Neg.isChecked():
                plane.SetOrigin(self.A_NewRedPlan[0],self.A_NewRedPlan[1],self.A_NewRedPlan[2])
                plane.SetNormal(-self.n_NewRedPlan[0],-self.n_NewRedPlan[1],(self.matRed.GetElement(3,2)-self.n_NewRedPlan[2])/self.A_NewRedPlan[2])

    
            if self.radio_red_Pos.isChecked():
                plane.SetOrigin(self.A_NewRedPlan[0],self.A_NewRedPlan[1],self.A_NewRedPlan[2])
                plane.SetNormal(self.n_NewRedPlan[0],self.n_NewRedPlan[1],(-self.matRed.GetElement(3,2)+self.n_NewRedPlan[2])/self.A_NewRedPlan[2])
                

            #Condtion for the yellow plane
            if self.radio_yellow_Neg.isChecked():
                plane.SetOrigin(self.A_NewYellowPlan[0],self.A_NewYellowPlan[1],self.A_NewYellowPlan[2])
                plane.SetNormal((self.matYellow.GetElement(3,2)-self.n_NewYellowPlan[0])/self.A_NewYellowPlan[0],-self.n_NewYellowPlan[1],-self.n_NewYellowPlan[2])

            if self.radio_yellow_Pos.isChecked():
                plane.SetOrigin(self.A_NewYellowPlan[0],self.A_NewYellowPlan[1],self.A_NewYellowPlan[2])
                plane.SetNormal((-self.matYellow.GetElement(3,2)+self.n_NewYellowPlan[0])/self.A_NewYellowPlan[0],self.n_NewYellowPlan[1],self.n_NewYellowPlan[2])

            #Condition for the green plane
            if self.radio_green_Neg.isChecked():
                plane.SetOrigin(self.A_NewGreenPlan[0],self.A_NewGreenPlan[1],self.A_NewGreenPlan[2])
                plane.SetNormal(self.n_NewGreenPlan[0],-(self.matGreen.GetElement(3,2)-self.n_NewGreenPlan[1]),self.n_NewGreenPlan[2])
        
            if self.radio_green_Pos.isChecked():
                plane.SetOrigin(self.A_NewGreenPlan[0],self.A_NewGreenPlan[1],self.A_NewGreenPlan[2])
                plane.SetNormal(-self.n_NewGreenPlan[0],(self.matGreen.GetElement(3,2)-self.n_NewGreenPlan[1]),-self.n_NewGreenPlan[2])


        
            planeCollection = vtk.vtkPlaneCollection()
            planeCollection.AddItem(plane)
    
            clipper = vtk.vtkClipClosedSurface()
            clipper.SetClippingPlanes(planeCollection)
            clipper.SetInputConnection(PolyAlgorithm.GetOutputPort())
            clipper.SetGenerateFaces(1)
            clipper.SetScalarModeToLabels()
            clipper.Update()
            PolyDataNew = clipper.GetOutput()
            self.model.SetAndObservePolyData(PolyDataNew)
                
                
    def UndoButtonClicked(self):
        
        self.model.SetAndObservePolyData(self.polyData)







