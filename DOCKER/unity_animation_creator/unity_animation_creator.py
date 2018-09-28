#BBD's Krita Script Starter Feb 2018
from krita import *
from PyQt5.QtWidgets import *
from krita import *
from PyQt5.QtCore import QStandardPaths, QSettings
import PyQt5.uic as uic

DOCKER_NAME = 'Unity Animation Creator'
DOCKER_ID = 'pykrita_unity_animation_creator'

class Unity_animation_creator(DockWidget):

	def CheckDocument(self):
		self.document = Krita.instance().activeDocument()
		if self.document is None:
			return
		else:
			strFramesToShow = self.lineEdit_FrameCount.text()
			try: 
				int(strFramesToShow)
			except ValueError:
				return
			
			self.FramesToShow = int(strFramesToShow)
			self.CreateNewFrame()

	def CreateNewFrame(self):
		root = self.document.rootNode()
		aboveNum = 0
		if (len(root.childNodes()) > 0):
			aboveNum = len(root.childNodes()) - 1
		else:
			aboveNum = None		
		
		root.addChildNode(self.document.createNode("Frame_" + str(len(root.childNodes()) + 1), "grouplayer"), root.childNodes()[aboveNum])
		root.childNodes()[len(root.childNodes()) - 1].addChildNode(self.document.createNode("Frame_" + str(len(root.childNodes())) + "_Child", "paintlayer"), None)
		
		#NEED TO FIX KRITA NOT UPDATING OPACITY IN CANVAS
		#COULD BE A DRIVER/OpenGL ISSUE. RESEARCH MORE
		#IF SO, NOT MUCH CAN BE DONE
		children = root.childNodes()		
		i = len(children) - 1
		o = 1
		while (i >= 0):
			if(o < self.FramesToShow):
				children[i].setOpacity(255 / o)
			else:
				children[i].setOpacity(255)
				children[i].setVisible(False)
				
			i -= 1
			o += 1	
			
		self.document.setActiveNode(root.childNodes()[len(root.childNodes()) - 1].childNodes()[0])

	def __init__(self):
		super().__init__()
		self.setWindowTitle(DOCKER_NAME)
		mainWidget = QWidget(self)
		self.setWidget(mainWidget) 
		
		mainLayout = QVBoxLayout(mainWidget)
		
		hLayout_FrameCount = QHBoxLayout()
		hLayout_CreateFrame = QHBoxLayout()
		mainLayout.addLayout(hLayout_FrameCount)
		mainLayout.addLayout(hLayout_CreateFrame)
		
		label_FrameCount = QLabel("Number of Frames to Show:")
		self.lineEdit_FrameCount = QLineEdit("5", mainWidget)
		button_CreateFrame = QPushButton("Create New Frame", mainWidget)
		
		hLayout_FrameCount.addWidget(label_FrameCount)
		hLayout_FrameCount.addWidget(self.lineEdit_FrameCount)
		hLayout_CreateFrame.addWidget(button_CreateFrame)		
		
		button_CreateFrame.clicked.connect(self.CheckDocument)

	def canvasChanged(self, canvas):
		pass

instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID, 
												DockWidgetFactoryBase.DockRight, 
												Unity_animation_creator)

instance.addDockWidgetFactory(dock_widget_factory)
