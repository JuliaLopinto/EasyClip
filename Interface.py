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

      inputModelSelectorFrame = qt.QFrame(self.parent)
      inputModelSelectorFrame.setLayout(qt.QHBoxLayout())
      self.parent.layout().addWidget(inputModelSelectorFrame)

      inputModelSelector = slicer.qMRMLNodeAttributeTableView(inputModelSelectorFrame)
      inputModelSelector.addAttribute()
      inputModelSelector.accessibleName = True
      #inputModelSelector.setMRMLScene( slicer.mrmlScene )
      self.loadFormLayout.addWidget(inputModelSelector)
      
      # Add vertical spacer
      self.layout.addStretch(1)
      
      # Collapsible button -- Clipping part
      self.loadCollapsibleButton = ctk.ctkCollapsibleButton()
      self.loadCollapsibleButton.text = "Clipping"
      self.layout.addWidget(self.loadCollapsibleButton)

      # Layout within the laplace collapsible button
      self.loadFormLayout = qt.QFormLayout(self.loadCollapsibleButton)
      
      #--------------------------- Planes --------------------------#
      groupBox2 = qt.QGroupBox("Planes")
      self.loadFormLayout.addWidget(groupBox2)

      label = qt.QLabel("Choose the plane you want to use:")
      self.loadFormLayout.addWidget(label)

      redPlaneCheckBox = qt.QCheckBox("Red Plane")
      self.loadFormLayout.addWidget(redPlaneCheckBox)
      # Add vertical spacer
      self.layout.addStretch(1)
      
      # Set local var as instance attribute
      self.redPlaneCheckBox = redPlaneCheckBox
      
      yellowPlaneCheckBox = qt.QCheckBox("Yellow Plane")
      self.loadFormLayout.addWidget(yellowPlaneCheckBox)
      # Add vertical spacer
      self.layout.addStretch(1)
      
      # Set local var as instance attribute
      self.yellowPlaneCheckBox = yellowPlaneCheckBox
      
      greenPlaneCheckBox = qt.QCheckBox("Green Plane")
      self.loadFormLayout.addWidget(greenPlaneCheckBox)
      # Add vertical spacer
      self.layout.addStretch(1)
      
      # Set local var as instance attribute
      self.greenPlaneCheckBox = greenPlaneCheckBox
      
      #-------------------------- Buttons --------------------------#
      # GET COORDINATES BUTTON
      getCoordButton = qt.QPushButton("Get Coordinates")
      self.loadFormLayout.addWidget(getCoordButton)
      #getCoordButton.connect('clicked(bool)', self.getCoordButtonClicked)
      
      # Add vertical spacer
      self.layout.addStretch(1)
      
      # Set local var as instance attribute
      self.getCoordButton = getCoordButton
      
      
      # SAVE PLANE BUTTON
      save = qt.QPushButton("Save plane")
      self.loadFormLayout.addWidget(save)
      #save.connect('clicked(bool)', self.saveClicked)
      
      # Add vertical spacer
      self.layout.addStretch(1)
      
      # Set local var as instance attribute
      self.save = save

      vbox2 = qt.QVBoxLayout()
      vbox2.addWidget(label)
      vbox2.addWidget(redPlaneCheckBox)
      vbox2.addWidget(yellowPlaneCheckBox)
      vbox2.addWidget(greenPlaneCheckBox)
      vbox2.addWidget(getCoordButton)
      vbox2.addWidget(save)
      vbox2.addStretch(1)
      groupBox2.setLayout(vbox2)


      # Add vertical spacer
      self.layout.addStretch(1)

      # Set local var as instance attribute
      self.groupBox2 = groupBox2


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
      
      radio_red1 = qt.QRadioButton("Negative")
      self.loadFormLayout.addWidget(radio_red1)
      radio_red2 = qt.QRadioButton("Positive")
      self.loadFormLayout.addWidget(radio_red2)
      
      yellow_plane = qt.QCheckBox("Yellow Slice Clipping:")
      self.loadFormLayout.addWidget(yellow_plane)
      
      radio_yellow1 = qt.QRadioButton("Negative")
      self.loadFormLayout.addWidget(radio_yellow1)
      radio_yellow2 = qt.QRadioButton("Positive")
      self.loadFormLayout.addWidget(radio_yellow2)
      
      green_plane = qt.QCheckBox("Green Slice Clipping:")
      self.loadFormLayout.addWidget(green_plane)
      
      radio_green1 = qt.QRadioButton("Negative")
      self.loadFormLayout.addWidget(radio_green1)
      radio_green2 = qt.QRadioButton("Positive")
      self.loadFormLayout.addWidget(radio_green2)

      vbox3 = qt.QVBoxLayout()

      vbox3.addWidget(label2)
      vbox3.addWidget(red_plane)
      vbox3.addWidget(radio_red1)
      vbox3.addWidget(radio_red2)
      vbox3.addWidget(yellow_plane)
      vbox3.addWidget(radio_yellow1)
      vbox3.addWidget(radio_yellow2)
      vbox3.addWidget(green_plane)
      vbox3.addWidget(radio_green1)
      vbox3.addWidget(radio_green2)

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
        
        
        reloadButton = qt.QPushButton("Reload")
        buttonFrame.layout().addWidget(reloadButton)
        #self.reloadButton.connect('clicked()', self.onReload)

        reloadAndTestButton = qt.QPushButton("Reload and Test")
        buttonFrame.layout().addWidget(reloadAndTestButton)
        #self.reloadAndTestButton.connect('clicked()', self.onReloadAndTest)

        # Add vertical spacer
        self.layout.addStretch(1)
      
        # Set local var as instance attribute
        self.reloadButton = reloadButton
        self.reloadAndTestButton = reloadAndTestButton




      # Collapsible button -- Clipping part
      self.loadCollapsibleButton = ctk.ctkCollapsibleButton()
      self.loadCollapsibleButton.text = "Advanced"
      self.layout.addWidget(self.loadCollapsibleButton)
          
      # Layout within the laplace collapsible button
      self.loadFormLayout = qt.QFormLayout(self.loadCollapsibleButton)

      #----------------- Information about planes ------------------#

      #-------------------- Loading CSV files ----------------------#



    def onReload(self,moduleName="Interface"):
        """Generic reload method for any scripted module.
        ModuleWizard will subsitute correct default moduleName.
        """
        import imp, sys, os, slicer
    
        widgetName = moduleName + "Widget"
    
        filePath = eval('slicer.modules.%s.path' % moduleName.lower())
        p = os.path.dirname(filePath)
        if not sys.path.__contains__(p):
            sys.path.insert(0,p)
    
                                            
        parent = slicer.util.findChildren(name='%s Reload' % moduleName)[0].parent()
        for child in parent.children():
            try:
                child.hide()
            except AttributeError:
                pass
                                            
        item = parent.layout().itemAt(0)
        while item:
            parent.layout().removeItem(item)
            item = parent.layout().itemAt(0)
                                            
        globals()[widgetName.lower()] = eval('globals()["%s"].%s(parent)' % (moduleName, widgetName))
        globals()[widgetName.lower()].setup()

    



