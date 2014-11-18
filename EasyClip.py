from __main__ import vtk, qt, ctk, slicer

import numpy

#
# Load Files
#

class EasyClip:
    def __init__(self, parent):
        parent.title = "Easy Clip"
        parent.categories = ["Easy Clip"]
        parent.dependencies = []
        parent.contributors = ["Julia Lopinto"]
        parent.helpText = """
        This Module is used to clip one or differents 3D Models according to a predetermined plane.
        Plane can be saved to be reused for other models.
        After clipping, the models are closed and can be saved as new 3D Models.

        This is an alpha version of the module.
        It can't be used for the moment.
        """
        
        parent.acknowledgementText = """
            The tool is developped by Julia Lopinto (intern at the University of Michigan, School of Dentistry)
            """
        
        
        self.parent = parent

#
# qEasyClipWidget
#

class EasyClipWidget:
    def __init__(self, parent = None):
        
        # Developper mode :
        # change this to true to get reload and test buttons
        self.developerMode = True
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

        # #---------------------- RED SLICE -----------------------#
        # # Definition of the matrix for the Red Slice
        # self.test = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeRed')
        # self.matRed = self.test.GetSliceToRAS()
        #
        # # Matrix with the elements of SliceToRAS
        # self.m_Red = numpy.matrix([[self.matRed.GetElement(0,0), self.matRed.GetElement(0,1), self.matRed.GetElement(0,2), self.matRed.GetElement(0,3)],
        #                            [self.matRed.GetElement(1,0), self.matRed.GetElement(1,1), self.matRed.GetElement(1,2), self.matRed.GetElement(1,3)],
        #                            [self.matRed.GetElement(2,0), self.matRed.GetElement(2,1), self.matRed.GetElement(2,2), self.matRed.GetElement(2,3)],
        #                            [self.matRed.GetElement(3,0), self.matRed.GetElement(3,1), self.matRed.GetElement(3,2), self.matRed.GetElement(3,3)]])
        #
        # #---------------------- YELLOW SLICE ----------------------#
        # # Definition of the matrix for the Yellow Slice
        # self.test = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeYellow')
        # self.matYellow = self.test.GetSliceToRAS()
        #
        # # Matrix with the elements of SliceToRAS
        # self.m_Yellow = numpy.matrix([[self.matYellow.GetElement(0,0), self.matYellow.GetElement(0,1), self.matYellow.GetElement(0,2), self.matYellow.GetElement(0,3)],
        #                               [self.matYellow.GetElement(1,0), self.matYellow.GetElement(1,1), self.matYellow.GetElement(1,2), self.matYellow.GetElement(1,3)],
        #                               [self.matYellow.GetElement(2,0), self.matYellow.GetElement(2,1), self.matYellow.GetElement(2,2), self.matYellow.GetElement(2,3)],
        #                               [self.matYellow.GetElement(3,0), self.matYellow.GetElement(3,1), self.matYellow.GetElement(3,2), self.matYellow.GetElement(3,3)]])
        #
        # #---------------------- GREEN SLICE ----------------------#
        # # Definition of the matrix for the Green Slice
        # self.test = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeGreen')
        # self.matGreen = self.test.GetSliceToRAS()
        #
        # # Matrix with the elements of SliceToRAS
        # self.m_Green = numpy.matrix([[self.matGreen.GetElement(0,0), self.matGreen.GetElement(0,1), self.matGreen.GetElement(0,2), self.matGreen.GetElement(0,3)],
        #                              [self.matGreen.GetElement(1,0), self.matGreen.GetElement(1,1), self.matGreen.GetElement(1,2), self.matGreen.GetElement(1,3)],
        #                              [self.matGreen.GetElement(2,0), self.matGreen.GetElement(2,1), self.matGreen.GetElement(2,2), self.matGreen.GetElement(2,3)],
        #                              [self.matGreen.GetElement(3,0), self.matGreen.GetElement(3,1), self.matGreen.GetElement(3,2), self.matGreen.GetElement(3,3)]])
        #
        #---------------------- Coefficient ----------------------#
        # Definition of the coefficient to determine the plane equation
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

        # The Red Slice is the first slice determined on Slicer.
        # The others are defined from a transformation matrix applied on this one (RED SLICE)
        # Normal vector to the Red slice:
        self.n_vector = numpy.matrix([[0], [0], [1], [1]])
                                                                                              
        # point on the Red slice:
        self.A = numpy.matrix([[0], [0], [0], [1]])
                                                                                              

        ##########################################################
        #                         Interface                      #
        ##########################################################

        
        # Collapsible button -- Scene Description
        self.loadCollapsibleButton = ctk.ctkCollapsibleButton()
        self.loadCollapsibleButton.text = "Scene"
        self.layout.addWidget(self.loadCollapsibleButton)
        
        # Layout within the laplace collapsible button
        self.loadFormLayout = qt.QFormLayout(self.loadCollapsibleButton)

        #--------------------------- List of Models --------------------------#
        
        list_model = qt.QLabel("List of models:")
        self.loadFormLayout.addWidget(list_model)

        # /!\ TRY TO FIND AN OTHER SOLUTION TO DEFINE THE TABLE /!\
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

        #--------------------------- Clipping Part --------------------------#
        
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
        buttonFrame = qt.QFrame(self.parent)
        buttonFrame.setLayout(qt.QHBoxLayout())
        self.layout.addWidget(buttonFrame)
        
        # SAVE PLANE BUTTON
        save = qt.QPushButton("Save plane")
        buttonFrame.layout().addWidget(save)
        save.connect('clicked(bool)', self.savePlane)
        
        # READ PLANE BUTTON
        read = qt.QPushButton("Load plane")
        buttonFrame.layout().addWidget(read)
        read.connect('clicked(bool)', self.readPlane)
        
        # Add vertical spacer
        self.layout.addStretch(1)
        
        vbox = qt.QVBoxLayout()
        vbox.addWidget(self.redPlaneCheckBox)
        vbox.addWidget(self.yellowPlaneCheckBox)
        vbox.addWidget(self.greenPlaneCheckBox)
        vbox.addWidget(buttonFrame)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        
        
        # groupBox3 = qt.QGroupBox("Clipping")
        # self.loadFormLayout.addWidget(groupBox3)
        
        # CLIPPING BUTTONS
        self.groupBox1 = qt.QGroupBox("Red Slice Clipping")
        self.groupBox1.setCheckable(True)
        self.groupBox1.setChecked(False)

        self.radio_red_Neg= qt.QRadioButton("Negative")
        self.radio_red_Neg.setIcon(qt.QIcon(":/Icons/RedSpaceNegative.png"))

        self.radio_red_Pos = qt.QRadioButton("Positive")
        self.radio_red_Pos.setIcon(qt.QIcon(":/Icons/RedSpacePositive.png"))

        vbox = qt.QHBoxLayout()
        vbox.addWidget(self.radio_red_Neg)
        vbox.addWidget(self.radio_red_Pos)
        vbox.addStretch(1)

        self.groupBox1.setLayout(vbox)

        self.loadFormLayout.addWidget(self.groupBox1)

        self.groupBox2 = qt.QGroupBox("Yellow Slice Clipping")
        self.groupBox2.setCheckable(True)
        self.groupBox2.setChecked(False)

        self.radio_yellow_Neg= qt.QRadioButton("Negative")
        self.radio_yellow_Neg.setIcon(qt.QIcon(":/Icons/YellowSpaceNegative.png"))

        self.radio_yellow_Pos = qt.QRadioButton("Positive")
        self.radio_yellow_Pos.setIcon(qt.QIcon(":/Icons/YellowSpacePositive.png"))

        vbox = qt.QHBoxLayout()
        vbox.addWidget(self.radio_yellow_Neg)
        vbox.addWidget(self.radio_yellow_Pos)
        vbox.addStretch(1)

        self.groupBox2.setLayout(vbox)

        self.loadFormLayout.addWidget(self.groupBox2)

        self.groupBox3 = qt.QGroupBox("Green Slice Clipping")
        self.groupBox3.setCheckable(True)
        self.groupBox3.setChecked(False)

        self.radio_green_Neg= qt.QRadioButton("Negative")
        self.radio_green_Neg.setIcon(qt.QIcon(":/Icons/GreenSpaceNegative.png"))

        self.radio_green_Pos = qt.QRadioButton("Positive")
        self.radio_green_Pos.setIcon(qt.QIcon(":/Icons/GreenSpacePositive.png"))

        vbox = qt.QHBoxLayout()
        vbox.addWidget(self.radio_green_Neg)
        vbox.addWidget(self.radio_green_Pos)
        vbox.addStretch(1)

        self.groupBox3.setLayout(vbox)

        self.loadFormLayout.addWidget(self.groupBox3)


        buttonFrame = qt.QFrame(self.parent)
        buttonFrame.setLayout(qt.QHBoxLayout())
        self.loadFormLayout.addWidget(buttonFrame)

        self.ClippingButton = qt.QPushButton("Clipping")
        buttonFrame.layout().addWidget(self.ClippingButton)
        self.ClippingButton.connect('clicked()', self.ClippingButtonClicked)

        self.UndoButton = qt.QPushButton("Undo")
        buttonFrame.layout().addWidget(self.UndoButton)
        self.UndoButton.connect('clicked()', self.UndoButtonClicked)

        # Add vertical spacer
        self.layout.addStretch(1)
        
        
        # CLIPPING BUTTONS
        if self.developerMode:
            buttonFrame = qt.QFrame(self.parent)
            buttonFrame.setLayout(qt.QHBoxLayout())
            self.loadFormLayout.addWidget(buttonFrame)
            
            
            self.reloadButton = qt.QPushButton("Reload")
            buttonFrame.layout().addWidget(self.reloadButton)
            self.reloadButton.connect('clicked()', self.onReload)
            
            
            # Add vertical spacer
            self.layout.addStretch(1)


        #--------------------------- Advanced Part --------------------------#
        # In this part, the user will be able to load a CSV file with all the modules name.
        
        # Collapsible button -- Clipping part
        self.loadCollapsibleButton = ctk.ctkCollapsibleButton()
        self.loadCollapsibleButton.text = "Advanced"
        self.layout.addWidget(self.loadCollapsibleButton)
        
        # Layout within the laplace collapsible button
        self.loadFormLayout = qt.QFormLayout(self.loadCollapsibleButton)
    
        #-------------------- Loading CSV files ----------------------#


    def onReload(self,moduleName="EasyClip"):
        print ('Recharger la page ', moduleName)

    def redPlaneCheckBoxClicked(self):
        self.redslice = slicer.util.getNode('vtkMRMLSliceNodeRed')
        self.redslice.SetDimensions(600,300,1)
        self.redslice.UpdateMatrices()
        if self.redPlaneCheckBox.isChecked():
            self.redslice.SetWidgetVisible(True)
        if not self.redPlaneCheckBox.isChecked():
            self.redslice.SetWidgetVisible(False)
    
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

    def getCoord(self):
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
        self.d_yellow = self.n_NewYellowPlan[0]*self.A_NewYellowPlan[0] + self.n_NewYellowPlan[1]*self.A_NewYellowPlan[1]+self.n_NewYellowPlan[2]*self.A_NewYellowPlan[2]
    
        print "Yellow plan equation : \n", self.a_yellow, "* x + ", self.b_yellow, "* y + ", self.c_yellow, "* z + ", self.d_yellow," = 0 "
    
        # GREEN PLAN:
        self.n_NewGreenPlan = self.m_Green * self.n_vector
        print "n : \n", self.n_NewGreenPlan
    
        self.A_NewGreenPlan = self.m_Green * self.A
        print "A : \n", self.A_NewGreenPlan
    
        self.a_green = self.n_NewGreenPlan[0]
        self.b_green = self.n_NewGreenPlan[1]
        self.c_green = self.n_NewGreenPlan[2]
        self.d_green = self.n_NewGreenPlan[0]*self.A_NewGreenPlan[0] + self.n_NewGreenPlan[1]*self.A_NewGreenPlan[1] + self.n_NewGreenPlan[2]*self.A_NewGreenPlan[2]
    
        print "Green plan equation : \n", self.a_green, "* x + ", self.b_green, "* y + ", self.c_green, "* z + ", self.d_green," = 0 "

    def savePlane(self):
        filename = qt.QFileDialog.getSaveFileName(parent=self,caption='Save file')
        fichier = open(filename, "w")
        fichier.write("SliceToRAS Red Slice: \n")
        fichier.write(str(self.m_Red) + '\n')
        fichier.write('\n')
        
        fichier.write("SliceToRAS Yellow Slice: \n")
        fichier.write(str(self.m_Yellow) + '\n')
        fichier.write('\n')
            
        fichier.write("SliceToRAS Green Slice: \n")
        fichier.write(str(self.m_Green) + '\n')
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
    
    def readPlane(self):
        filename = qt.QFileDialog.getOpenFileName(parent=self,caption='Open file')
        print 'filename:', filename
        fichier2 = open(filename, 'r')
        fichier2.readline()
        NodeRed = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeRed')
        matRed = NodeRed.GetSliceToRAS()
        for i in range(0, 4):
            ligne = fichier2.readline()
            ligne = ligne.replace('[', '')
            ligne = ligne.replace('   ', ' ')
            ligne = ligne.replace(']', '')
            ligne = ligne.replace('\n', '')
            print ligne
            items = ligne.split()
            print items
            for j in range(0, 4):
                matRed.SetElement(i, j, float(items[j]))


        print matRed
        
        fichier2.readline()
        fichier2.readline()
        
        NodeYellow = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeYellow')
        matYellow = NodeYellow.GetSliceToRAS()
        for i in range(0, 4):
            ligne = fichier2.readline()
            ligne = ligne.replace('[', '')
            ligne = ligne.replace('   ', ' ')
            ligne = ligne.replace(']', '')
            ligne = ligne.replace('\n', '')
            print ligne
            items = ligne.split()
            print items
            for j in range(0, 4):
                matYellow.SetElement(i, j, float(items[j]))
        
        
        print matYellow
        
        fichier2.readline()
        fichier2.readline()
        
        NodeGreen = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeGreen')
        matGreen = NodeGreen.GetSliceToRAS()
        for i in range (0,4):
            ligne = fichier2.readline()
            ligne = ligne.replace('[', '')
            ligne = ligne.replace('   ', ' ')
            ligne = ligne.replace(']', '')
            ligne = ligne.replace('\n', '')
            print ligne
            items = ligne.split()
            print items
            for j in range(0, 4):
                matGreen.SetElement(i, j, float(items[j]))
        
        
        print matGreen
        fichier2.close()
        
        self.redslice = slicer.util.getNode('vtkMRMLSliceNodeRed')
        if self.redPlaneCheckBox.isChecked():
            self.redPlaneCheckBox.setCheckState(False)
            self.redslice.SetWidgetVisible(False)
        
        self.redPlaneCheckBox.setCheckState(True)
        self.redslice.SetWidgetVisible(True)

        # self.yellowslice = slicer.util.getNode('vtkMRMLSliceNodeYellow')
        # if self.yellowPlaneCheckBox.isChecked():
        #     self.yellowPlaneCheckBox.setCheckState(False)
        #     self.yellowslice.SetWidgetVisible(False)
        #
        # self.yellowPlaneCheckBox.setCheckState(True)
        # self.yellowslice.SetWidgetVisible(True)
        
        self.greenslice = slicer.util.getNode('vtkMRMLSliceNodeGreen')
        if self.greenPlaneCheckBox.isChecked():
            self.greenPlaneCheckBox.setCheckState(False)
            self.greenslice.SetWidgetVisible(False)
        
        self.greenPlaneCheckBox.setCheckState(True)
        self.greenslice.SetWidgetVisible(True)

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

        self.getCoord()
        numNodes = slicer.mrmlScene.GetNumberOfNodesByClass("vtkMRMLModelNode")
        for i in range(3, numNodes):
            mh = slicer.mrmlScene.GetNthNodeByClass(i, "vtkMRMLModelNode")
            self.model = slicer.util.getNode(mh.GetName())
            self.polyData = self.model.GetPolyData()
            PolyAlgorithm = vtk.vtkClipClosedSurface()
            PolyAlgorithm.SetInput(self.polyData)
        
            # Clipping in the direction of the normal vector
            self.plane_red = vtk.vtkPlane()
            self.plane_yellow = vtk.vtkPlane()
            self.plane_green = vtk.vtkPlane()
            
            self.planeCollection = vtk.vtkPlaneCollection()

            self.getCoord()
            #Condition for the red plane
            print self.m_Red
            print self.n_NewRedPlan
            if self.radio_red_Neg.isChecked():
                self.getCoord()
                self.plane_red.SetOrigin(self.A_NewRedPlan[0], self.A_NewRedPlan[1], self.A_NewRedPlan[2])
                if self.n_NewRedPlan[2] >= 0:
                    self.plane_red.SetNormal(-self.n_NewRedPlan[0], -self.n_NewRedPlan[1], -self.n_NewRedPlan[2])
                if self.n_NewRedPlan[2] < 0:
                    self.plane_red.SetNormal(self.n_NewRedPlan[0], self.n_NewRedPlan[1], self.n_NewRedPlan[2])
                self.planeCollection.AddItem(self.plane_red)
                print self.plane_red

            if self.radio_red_Pos.isChecked():
                self.getCoord()
                self.plane_red.SetOrigin(self.A_NewRedPlan[0], self.A_NewRedPlan[1], self.A_NewRedPlan[2])
                if self.n_NewRedPlan[2] >= 0:
                    self.plane_red.SetNormal(self.n_NewRedPlan[0], self.n_NewRedPlan[1], self.n_NewRedPlan[2])
                if self.n_NewRedPlan[2] < 0:
                    self.plane_red.SetNormal(-self.n_NewRedPlan[0], -self.n_NewRedPlan[1], -self.n_NewRedPlan[2])
                self.planeCollection.AddItem(self.plane_red)
                print self.plane_red

            #Condtion for the yellow plane
            print self.m_Yellow
            print self.n_NewYellowPlan
            if self.radio_yellow_Neg.isChecked():
                self.getCoord()
                self.plane_yellow.SetOrigin(self.A_NewYellowPlan[0], self.A_NewYellowPlan[1], self.A_NewYellowPlan[2])
                if self.n_NewYellowPlan[0] >= 0:
                    self.plane_yellow.SetNormal(-self.n_NewYellowPlan[0], -self.n_NewYellowPlan[1], -self.n_NewYellowPlan[2])
                if self.n_NewYellowPlan[0] < 0:
                    self.plane_yellow.SetNormal(self.n_NewYellowPlan[0], self.n_NewYellowPlan[1], self.n_NewYellowPlan[2])
                self.planeCollection.AddItem(self.plane_yellow)
                print self.plane_yellow

            if self.radio_yellow_Pos.isChecked():
                self.getCoord()
                self.plane_yellow.SetOrigin(self.A_NewYellowPlan[0], self.A_NewYellowPlan[1], self.A_NewYellowPlan[2])
                if self.n_NewYellowPlan[0] >= 0:
                    self.plane_yellow.SetNormal(self.n_NewYellowPlan[0], self.n_NewYellowPlan[1], self.n_NewYellowPlan[2])
                if self.n_NewYellowPlan[0] < 0:
                    self.plane_yellow.SetNormal(-self.n_NewYellowPlan[0], -self.n_NewYellowPlan[1], -self.n_NewYellowPlan[2])
                self.planeCollection.AddItem(self.plane_yellow)
                print self.plane_yellow

            #Condition for the green plane
            print self.m_Green
            print self.n_NewGreenPlan
            if self.radio_green_Neg.isChecked():
                self.getCoord()
                self.plane_green.SetOrigin(self.A_NewGreenPlan[0], self.A_NewGreenPlan[1], self.A_NewGreenPlan[2])
                if self.n_NewGreenPlan[1] >= 0:
                    self.plane_green.SetNormal(-self.n_NewGreenPlan[0], -self.n_NewGreenPlan[1], -self.n_NewGreenPlan[2])
                if self.n_NewGreenPlan[1] < 0:
                    self.plane_green.SetNormal(self.n_NewGreenPlan[0], self.n_NewGreenPlan[1], self.n_NewGreenPlan[2])
                self.planeCollection.AddItem(self.plane_green)
                print self.plane_green

            if self.radio_green_Pos.isChecked():
                self.getCoord()
                self.plane_green.SetOrigin(self.A_NewGreenPlan[0], self.A_NewGreenPlan[1], self.A_NewGreenPlan[2])
                if self.n_NewGreenPlan[1] > 0:
                    self.plane_green.SetNormal(self.n_NewGreenPlan[0], self.n_NewGreenPlan[1], self.n_NewGreenPlan[2])
                if self.n_NewGreenPlan[1] < 0:
                    self.plane_green.SetNormal(-self.n_NewGreenPlan[0], -self.n_NewGreenPlan[1], -self.n_NewGreenPlan[2])
                self.planeCollection.AddItem(self.plane_green)
                print self.plane_green
    
            clipper = vtk.vtkClipClosedSurface()
            clipper.SetClippingPlanes(self.planeCollection)
            clipper.SetInputConnection(PolyAlgorithm.GetOutputPort())
            clipper.SetGenerateFaces(1)
            clipper.SetScalarModeToLabels()
            clipper.Update()
            PolyDataNew = clipper.GetOutput()
            self.model.SetAndObservePolyData(PolyDataNew)

    def UndoButtonClicked(self):
        self.model.SetAndObservePolyData(self.polyData)
        self.groupBox1.setChecked(False)
        self.groupBox2.setChecked(False)
        self.groupBox3.setChecked(False)











