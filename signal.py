from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject


class Signal(QObject):
	signal_dict = dict()
	
	time_exit = pyqtSignal()
	
	def __init__(self):
		super().__init__()
		
	def registSignal(self, class_name):
		print(class_name.__class__.__name__)
		if (class_name.__class__.__name__ == "TimeMeasure"):
			self.time_exit.connect(class_name.exit)
			
	def unregistSignal(self, class_name):
		if (class_name.__class__.__name__ == "TimeMeasure"):
			self.time_exit.disconnect(class_name.exit)
			
	def emit(self, function_name: str, *parameter):
		signal_object = eval("self.{}".format(function_name))
		signal_object.emit(*parameter)
