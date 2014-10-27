from __main__ import vtk, qt, ctk, slicer



#
# Load Files
#

class Interface:
  def __init__(self, parent):
    parent.title = "Overview Easy Clip Interface"
    parent.categories = ["Interface Easy Clip"]

    self.parent = parent

#
# qHelloPythonWidget
#

class InterfaceWidget:
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
      # Collapsible button -- Easy Clip Description
      self.loadCollapsibleButton = ctk.ctkCollapsibleButton()
      self.loadCollapsibleButton.text = "Scene"
      self.layout.addWidget(self.loadCollapsibleButton)

      # Layout within the laplace collapsible button
      self.loadFormLayout = qt.QFormLayout(self.loadCollapsibleButton)
      
      list_model = qt.QLabel("List of models:")
      self.loadFormLayout.addWidget(list_model)

#     inputModelSelectorFrame = qt.QFrame(self.parent)
#     inputModelSelectorFrame.setLayout(qt.QHBoxLayout())
#     self.parent.layout().addWidget(inputModelSelectorFrame)

#     inputModelSelector = slicer.qMRMLNodeAttributeTableView(inputModelSelectorFrame)
#     inputModelSelector.addAttribute()
#     inputModelSelector.accessibleName = True
      #inputModelSelector.setMRMLScene( slicer.mrmlScene )
      #self.loadFormLayout.addWidget(inputModelSelector)
      
      
      
      
      
      #inputList= qt.QListWidget(self.parent)
      #self.loadFormLayout.addWidget(inputList)
      
      inputSceneModel = slicer.qMRMLSceneModel()
      inputSceneModel.NodeTypes(1)
      #self.loadFormLayout.addWidget(inputSceneModel)
      
      
      
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
      #getCoordButton.connect('clicked(bool)', self.getCoordButtonClicked)
      
      # Add vertical spacer
      self.layout.addStretch(1)
      
      # SAVE PLANE BUTTON
      save = qt.QPushButton("Save plane")
      self.loadFormLayout.addWidget(save)
      #save.connect('clicked(bool)', self.saveClicked)
      
      # Add vertical spacer
      self.layout.addStretch(1)
      

      vbox = qt.QVBoxLayout()
      
      vbox.addWidget(self.redPlaneCheckBox)
      vbox.addWidget(self.yellowPlaneCheckBox)
      vbox.addWidget(self.greenPlaneCheckBox)
      vbox.addWidget(getCoordButton)
      vbox.addWidget(save)
      
      vbox.addStretch(1)
      groupBox.setLayout(vbox)


      groupBox3 = qt.QGroupBox("Clipping")
      self.loadFormLayout.addWidget(groupBox3)

      # CLIPPING BUTTONS
      buttonFrame = qt.QFrame(self.parent)
      buttonFrame.setLayout(qt.QHBoxLayout())
      self.layout.addWidget(buttonFrame)
          
          
      ClippingButton = qt.QPushButton("Clipping")
      buttonFrame.layout().addWidget(ClippingButton)
      #self.reloadButton.connect('clicked()', self.onReload)
          
      UndoButton = qt.QPushButton("Undo")
      buttonFrame.layout().addWidget(UndoButton)
      #self.reloadAndTestButton.connect('clicked()', self.onReloadAndTest)
          
      # Add vertical spacer
      self.layout.addStretch(1)
          
      # Set local var as instance attribute
      self.ClippingButton = ClippingButton
      self.UndoButton = UndoButton
      
      
      label2 = qt.QLabel("Choose the part you want to keep:")
      self.loadFormLayout.addWidget(label2)
      
      red_plane = qt.QCheckBox("Red Slice Clipping:")
      self.loadFormLayout.addWidget(red_plane)
      

      buttonFrame1 = qt.QFrame(self.parent)
      buttonFrame1.setLayout(qt.QHBoxLayout())
      self.layout.addWidget(buttonFrame1)
      radio_red1 = qt.QRadioButton("Negative")
      buttonFrame1.layout().addWidget(radio_red1)
      radio_red2 = qt.QRadioButton("Positive")
      buttonFrame1.layout().addWidget(radio_red2)


      yellow_plane = qt.QCheckBox("Yellow Slice Clipping:")
      self.loadFormLayout.addWidget(yellow_plane)


      buttonFrame2 = qt.QFrame(self.parent)
      buttonFrame2.setLayout(qt.QHBoxLayout())
      self.layout.addWidget(buttonFrame2)

      radio_yellow1 = qt.QRadioButton("Negative")
      buttonFrame2.layout().addWidget(radio_yellow1)
      radio_yellow2 = qt.QRadioButton("Positive")
      buttonFrame2.layout().addWidget(radio_yellow2)

      
      green_plane = qt.QCheckBox("Green Slice Clipping:")
      self.loadFormLayout.addWidget(green_plane)


      buttonFrame3 = qt.QFrame(self.parent)
      buttonFrame3.setLayout(qt.QHBoxLayout())
      self.layout.addWidget(buttonFrame3)

      radio_green1 = qt.QRadioButton("Negative")
      buttonFrame3.layout().addWidget(radio_green1)
      radio_green2 = qt.QRadioButton("Positive")
      buttonFrame3.layout().addWidget(radio_green2)

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








