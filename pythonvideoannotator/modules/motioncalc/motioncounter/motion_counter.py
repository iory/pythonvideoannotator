import sys, os, shutil, re, pyforms, numpy as np, cv2
from pyforms 			 import BaseWidget
from pyforms.Controls 	 import ControlFile
from pyforms.Controls 	 import ControlPlayer
from pyforms.Controls 	 import ControlButton
from pyforms.Controls 	 import ControlNumber
from pyforms.Controls 	 import ControlSlider
from pyforms.Controls 	 import ControlCheckBox
from pyforms.Controls 	 import ControlText
from pyforms.Controls 	 import ControlCheckBoxList
from pythonvideoannotator.modules.motioncalc.motioncounter.motion_object import MotionObject
from PyQt4 import QtGui


class MotionCounter(BaseWidget):

	def __init__(self, parent=None):
		BaseWidget.__init__(self, 'Motion counter', parentWindow=parent)

		self.layout().setContentsMargins(10, 5, 10, 5)
		self.setMinimumHeight(300)
		self.setMinimumWidth(500)

		self._player			= ControlPlayer('Player')
		self._objects 			= ControlCheckBoxList('Objects')
		self._show_diff			= ControlCheckBox('Show diffs boxes')
		self._threshold_slider	= ControlSlider('Threshold', 5, 1, 255)
		self._radius_slider		= ControlSlider('Radius', 30, 1, 200)
		
		self._formset = [
			'_objects',
			'=',
			('_threshold_slider', '_radius_slider', '_show_diff'),
			'_player'
		]

		self._player.processFrame 	= self.__process_frame

		self._threshold_slider.changed 	= self.__threshold_changed_event
		self._radius_slider.changed 	= self.__radius_changed_event
		self._objects.changed 			= self.__objects_changed_evt

		self._objects_dict = {}
		self._selected_objs = []



	def __objects_changed_evt(self):
		self._selected_objs = [MotionObject(self._objects_dict[name]) for name in self._objects.value]

	@property
	def video_filename(self): return None
	@video_filename.setter
	def video_filename(self, value): self._player.value = value

	@property
	def objects(self): return self._selected_objs
	@objects.setter
	def objects(self, value):  self._objects.value = value
	

	def add_object_evt(self, obj): 			
		self._objects+= [obj.name, True]
		self._objects_dict[obj.name] = obj
		self.__objects_changed_evt()
		
	def remove_object_evt(self, obj, i): 
		self._objects-= i
		

	def __process_frame(self, frame):
		index = self._player.video_index
		
		for obj in self.objects: obj.process(index, frame)
		for obj in self.objects: obj.draw(index, frame, self._show_diff.value)

		return frame

	def __threshold_changed_event(self): self.threshold = self._threshold_slider.value
	def __radius_changed_event(self): 	 self.radius = self._radius_slider.value

	@property
	def radius(self): return self._radius_slider.value
	@radius.setter
	def radius(self, value): 
		for f in self.objects: f.radius = value

	@property
	def threshold(self): return self._threshold_slider.value
	@threshold.setter
	def threshold(self, value): 
		for f in self.objects: f.threshold = value




if __name__ == "__main__": pyforms.startApp(Main)