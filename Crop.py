from __main__ import vtk, qt, ctk, slicer
import numpy
#
# tool to crop the models vtk
#

class Crop:
  def __init__(self, parent):
    parent.title = "Clipping"
    parent.categories = ["Clipping"]

    self.parent = parent

#
# qCrop Widget
#

class CropWidget:
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
      # Collapsible button
      self.laplaceCollapsibleButton = ctk.ctkCollapsibleButton()
      self.laplaceCollapsibleButton.text = "A collapsible button"
      self.layout.addWidget(self.laplaceCollapsibleButton)

      # Layout within the laplace collapsible button
      sampleFormLayout = qt.QFormLayout(self.laplaceCollapsibleButton)

      # Get Coordinates button
      getClipping = qt.QPushButton("Preview")
      sampleFormLayout.addWidget(getClipping)
      getClipping.connect('clicked(bool)', self.getClippingClicked)

      # Add vertical spacer
      self.layout.addStretch(1)

      # Set local var as instance attribute
      self.getClipping = getClipping
      
      Scene = slicer.qMRMLSceneModel()
      Scene.NodeTypes(2)
      Scene.checkableColumn = True
    
      numNodes = slicer.mrmlScene.GetNumberOfNodesByClass("vtkMRMLModelNode")
      for i in range (3,numNodes):
          mh = slicer.mrmlScene.GetNthNodeByClass(i,"vtkMRMLModelNode" )
          print mh.GetName()
          Scene.insertRow(i-2, mh.GetName())
    
      
    
    #sampleFormLayout.addWidget(Scene)

    def getClippingClicked(self):
        #for i in range (3, self.numNodes):
        
        
        model = slicer.util.getNode("Model_GM_T0_Reg_MD_novo")
        poly = model.GetPolyData()


        nb_points = poly.GetNumberOfPoints()

        tab_points = poly.GetPoints()

        coord_points = numpy.zeros(3)
        IdList = vtk.vtkIdList()
        

        for i in range (0,nb_points):
            tab_points.GetPoint(i,coord_points)
            if coord_points[1]<=-10:
                IdList.InsertNextId(i)

        A = vtk.vtkDoubleArray()
        A.SetName('Clip')
        
        for i in range(0, nb_points):
            A.InsertNextValue(0)
        
        for i in range (0,IdList.GetNumberOfIds()):
            A.SetValue(IdList.GetId(i),1)
        
    
        point = poly.GetPointData()
        point.SetScalars(A)

        print A










