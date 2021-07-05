from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
from PyQt5.QtGui import QImage


class Signal(QObject):
	appendTextBlind = pyqtSignal(str)
	appendTextDeaf = pyqtSignal(str)
	printImage = pyqtSignal(QImage)
	startRecord = pyqtSignal(bool)
	
	def __init__(self):
		super().__init__()
		
	def registSignal(self, class_ob):
		if (class_ob.__class__.__name__ == "BlindLayer"):
			self.appendTextBlind.connect(class_ob.appendTextBlind)
		elif (class_ob.__class__.__name__ == "DeafLayer"):
			self.printImage.connect(class_ob.printImage)
			self.startRecord.connect(class_ob.startRecord)
			self.appendTextDeaf.connect(class_ob.appendTextDeaf)
			
	def unregistSignal(self, class_name):
		if (class_name.__class__.__name__ == "BlindLayer"):
			self.appendTextBlind.disconnect(class_name.appendTextBlind)
		elif (class_ob.__class__.__name__ == "DeafLayer"):
			self.printImage.disconnect(class_ob.printImage)
			self.startRecord.disconnect(class_ob.startRecord)
			self.appendTextDeaf.disconnect(class_ob.appendTextDeaf)
			
	def emit(self, function_name: str, *parameter):
		signal_object = eval("self.{}".format(function_name))
		signal_object.emit(*parameter)
