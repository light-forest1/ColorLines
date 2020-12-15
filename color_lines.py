#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import datetime
#import subprocess
import re
import string
import codecs
import types
import random
#new 06.07.2018
# from libxmp.utils import file_to_dict
# from libxmp import XMPFiles, consts
#/new 06.07.2018
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtCore import Qt, pyqtSlot, QTimer, QSize

from PIL import Image

import networkx as nx


#new 08.07.2018

###
#План дій (08.07.2018):
#=========

#1) 
# (так) Можливість додавати декілька каталогів для роботи із файлами 
#зображень, 
# (ні) можливість вказувати глибину для каталогів.
# !!! При додаванні інформації з файлу, чий розмір менше 12 байт, 
# !!! виникає помилка.

#2) 
# (так) Кількість кожного ключового слова (якщо є однакові) для кожного 
#зображення (а не тільки загалом для всіх зображень у вказаних 
#каталогах), 
# (ні) можливість видаляти дублікати ключового слова для 
#зображення. 

#3) 
# (ні) Складання складних запитів із ключових слів для пошуку зображень.

#4) 
# (ні) Можливість додавати нові ключові слова для знайдених зображень, 
#заміняти або видаляти певні ключові слова.

#5) 
# (ні) Перегляд знайдених зображень, 
# (ні) копіювання у нове місце, видалення 
#зі старого місця. 

###

i_list = [0]

dirName = os.getcwd()
files_and_dirs_names = os.listdir(dirName)
files_names = []
print(files_names)

for item in files_and_dirs_names:
	if os.path.isfile(os.path.join(dirName, item)) and item != 'img.py':
		files_names.append(item)
print(files_names)

tab11Graph = nx.Graph()
tab11_Graph = nx.Graph()

tab11Btns = []

# colors = ['160, 0, 0', '255, 0, 0', '255, 255, 0', '0, 210, 0', '0, 200, 255', '0, 0, 255', '190, 0, 190', '0, 230, 230', '255, 150, 0', '30, 210, 77', '158, 86, 245', '255, 255, 160']
colors = ['160, 0, 0', '255, 0, 0', '255, 255, 0', '0, 230, 0', '0, 230, 230', '0, 0, 255', '190, 0, 190']
colors_icons = ['ball_gradient--dark_red.png','ball_gradient--red.png','ball_gradient--yellow.png','ball_gradient--green.png','ball_gradient--sky_blue.png','ball_gradient--blue.png','ball_gradient--violet.png']
colors_choosed_icons = ['ball_gradient--dark_red--choosed.png','ball_gradient--red--choosed.png','ball_gradient--yellow--choosed.png','ball_gradient--green--choosed.png','ball_gradient--sky_blue--choosed.png','ball_gradient--blue--choosed.png','ball_gradient--violet--choosed.png']

class Example(QWidget):

	def __init__(self):
		super().__init__()

		self.initUI()
		self.initGraph()

	def initUI(self):
		
		#prevBtn = QPushButton('<-', self)
		#nextBtn = QPushButton('->', self)
		
		#self.imgLbl = QLabel(self)
		#pixmap = QPixmap(files_names[0])
		#pixmap_new = pixmap.scaled(640, 480, Qt.KeepAspectRatio)
		#self.imgLbl.setPixmap(pixmap_new)
		
		#self.qTable = QTableWidget(self)
		#self.qTable.setRowCount(3)
		#self.qTable.setColumnCount(3)
		#for i in range(3):
			#chkBoxItem = QTableWidgetItem()
			#chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
			#chkBoxItem.setCheckState(Qt.Unchecked)
			#self.qTable.setItem(i, 0, chkBoxItem)
			#combo = QComboBox()
			#combo.addItems(['1 position', '2 position', '3 position'])
			#self.qTable.setCellWidget(i, 1, combo)
			#tableLbl = QLabel('Table Label')
			#self.qTable.setCellWidget(i, 2, tableLbl)
		
		self.tabs = QTabWidget()
		self.tab1 = QWidget()
		self.tab2 = QWidget()
		#self.tabs.resize(300,200)
		
		self.tabs.addTab(self.tab1, 'Tab 1')
		self.tabs.addTab(self.tab2, 'Tab 2')
		
		self.tab1.layout = QGridLayout(self)
		
		self.prevBtn = QPushButton('<-', self)
		self.nextBtn = QPushButton('->', self)
		self.lbl = QLabel('Some text')
		
		self.prevBtn.clicked.connect(self.prevBtnClicked)
		self.nextBtn.clicked.connect(self.nextBtnClicked)
		
		# Widgets to tab11
		
		# tab11Btns = []
		
		for i in range(9):
			tab11BtnsList = []
			for j in range(9):
				self.tab11Btn = QPushButton()
				self.tab11Btn.clicked.connect(self.tab11BtnClicked)
				self.tab11Btn.setProperty('x_tab11', j)
				self.tab11Btn.setProperty('y_tab11', i)
				self.tab11Btn.setProperty('node_num', i*9 + j)
				tab11BtnsList.append(self.tab11Btn)
			tab11Btns.append(tab11BtnsList)
		
		# / Widgets to tab11
		
		# 17.10.2018
		
		self.tab1Tabs = QTabWidget()
		self.tab11 = QWidget()
		self.tab12 = QWidget()
		
		self.tab1Tabs.addTab(self.tab11, 'Tab11')
		self.tab1Tabs.addTab(self.tab12, 'Tab12')
		
		self.tab11.layout = QGridLayout(self)
		
		
		self.tab12.layout = QGridLayout(self)
		
		
		self.tab11.layout.setSpacing(0)
		
		# Add widgets to tab11
		
		for i in range(len(tab11Btns)):
			for j in range(len(tab11Btns[i])):
				self.tab11.layout.addWidget(tab11Btns[i][j], i+1, j)
		
		# / Add widgets to tab11
		
		self.tab11.setLayout(self.tab11.layout)
		
		
		self.tab12.layout.setSpacing(5)
		
		
		self.tab12.setLayout(self.tab12.layout)
		
		# / 17.10.2018
		
		self.tab1.layout.setSpacing(5)
		
		self.tab1.layout.addWidget(self.prevBtn, 1, 0)
		self.tab1.layout.addWidget(self.nextBtn, 1, 1)
		# self.tab1.layout.addWidget(self.lbl, 2, 0)
		self.tab1.layout.addWidget(self.tab1Tabs, 2, 0)
		self.tab1.setLayout(self.tab1.layout)
		
		self.tab2.layout = QGridLayout(self)
		
		self.tab2Table = QTableWidget()
		self.tab2Table.setRowCount(50)
		self.tab2Table.setColumnCount(4)
		
		
		self.tab2.layout.addWidget(self.tab2Table, 1,0)
		
		self.tab2.setLayout(self.tab2.layout)
		
		
		
		#prevBtn.clicked.connect(self.prevBtnClicked)
		#nextBtn.clicked.connect(self.nextBtnClicked)
		
		#self.statusBar()

		grid = QGridLayout()
		grid.setSpacing(10)
		
		#grid.addWidget(prevBtn, 1, 0)
		#grid.addWidget(nextBtn, 1, 1)
		
		#grid.addWidget(self.qTable, 2, 0, 2, 2)
		grid.addWidget(self.tabs, 1, 0)		
		
		self.setLayout(grid)

		self.tableCellLbl = QLabel("<b>Якийсь</b> текст")
		self.tableCellLbl.setToolTip("<b>Якийсь</b> новий текст")
		# self.tab2Table.setItem(1,1, QTableWidgetItem(tr("<b>Якийсь</b> текст")))
		self.tab2Table.setCellWidget(1, 1, self.tableCellLbl)
		self.tab2Table.insertRow(2)

		cellLayout = QHBoxLayout()
		cellLayout.setSpacing(2)
		firstBtn = QPushButton('1', self)
		secondBtn = QPushButton('2', self)
		firstBtn.setProperty('num', 1)
		secondBtn.setProperty('num', 1)
		
		firstBtn.clicked.connect(self.firstBtnClicked)
		secondBtn.clicked.connect(self.secondBtnClicked)
		
		###
		# self.radio_button_1 = QRadioButton('and')
		# self.radio_button_1.setChecked(True)
		# self.radio_button_1.setProperty('btn_name', 'and')
		# self.radio_button_2 = QRadioButton('or')
		# self.radio_button_2.setProperty('btn_name', 'or')
		
		# self.button_group = QButtonGroup()
		# self.button_group.addButton(self.radio_button_1)
		# self.button_group.addButton(self.radio_button_2)
		
		# self.button_group.buttonClicked.connect(self._on_radio_button_clicked)
		###/
		cellLayout.addWidget(firstBtn)
		cellLayout.addWidget(secondBtn)
		
		###
		# cellRadioButtonsLayout = QHBoxLayout()
		# cellRadioButtonsLayout.setSpacing(2)
		# cellRadioButtonsLayout.addWidget(self.radio_button_1)
		# cellRadioButtonsLayout.addWidget(self.radio_button_2)
		
		# cellRadioButtons = QWidget()
		# cellRadioButtons.setProperty('radio_buttons_group', self.button_group)
		# cellRadioButtons.setLayout(cellRadioButtonsLayout)
		# self.tab2Table.setCellWidget(0, 0, cellRadioButtons)
		###/
		cellWidget = QWidget()
		cellWidget.setLayout(cellLayout)
		self.tab2Table.setCellWidget(2, 2, cellWidget)

		newButton = QPushButton('<b>Bold</b> font', self)
		newButton.clicked.connect(self.newButtonClicked)
		self.tab2Table.setCellWidget(1, 2, newButton)
		
		###
		self.secondButton = QPushButton('[AND] or')
		self.secondButton.setProperty('bool', 'and')
		self.secondButton.clicked.connect(self.secondButtonClicked)
		self.secondButton.setStyleSheet('background-color: rgb(255,255,170)')
		self.tab2Table.setCellWidget(2, 2, self.secondButton)
		###

		# self.tab2Table.cellPressed.connect(self.tab2TableCellActivated)
		
		self.buttonIcon = QIcon()
		self.buttonIcon.addFile('button_icon.png')
		newButton.setIcon(self.buttonIcon)
		
		# 30.10.2018
		
		self.tab2Table.setColumnWidth(0, 300)
		self.tab2Table.setShowGrid(False)
		
		# self.add_dir_to_copy_btn = QPushButton('Add directory to copy')
		# self.add_dir_to_copy_btn.clicked.connect(self.add_dir_to_copy_btn_clicked)
		# self.tab2Table.setCellWidget(0, 0, self.add_dir_to_copy_btn)
		
		# self.add_dir_to_receive_btn = QPushButton('Add directory to receive')
		# self.add_dir_to_receive_btn.clicked.connect(self.add_dir_to_receive_btn_clicked)
		# self.tab2Table.setCellWidget(2, 0, self.add_dir_to_receive_btn)
		
		# self.copy_dir_btn = QPushButton('Copy directory')
		# self.copy_dir_btn.clicked.connect(self.copy_dir_btn_clicked)
		# self.tab2Table.setCellWidget(4, 0, self.copy_dir_btn)
		
		# self.copy_progress = QProgressBar()
		# self.copy_progress.setMinimum(0)
		# self.copy_progress.setMaximum(100)
		# self.copy_progress.setValue(0)
		# self.tab2Table.setCellWidget(5, 0, self.copy_progress)
		
		# / 30.10.2018
		
		self.setGeometry(160, 160, 500, 500)
		self.setWindowTitle('Search Photos by XMP Tags')
		
		"""
		self.auto_start_timer = QtCore.QTimer()
		self.auto_start_timer.timeout.connect( lambda : self.copyfileobj( src=self.src, dst=self.dest, callback_progress=self.progress, callback_copydone=self.copydone )  )
		self.auto_start_timer.start(2000)
		"""
		
		self.show()

	
	#new 09.07.2018
	#def prevBtnClicked(self):
		
		#sender = self.sender()
		
		#if i_list[0] < len(files_names)-1:
			#i_list[0] += 1
		#else:
			#i_list[0] = 0
		##self.pixmap_new.load(files_names[i_list[0]])
		##self.imgLbl.setPixmap(self.pixmap_new)
		##pixmap = QPixmap(files_names[i_list[0]])
		##pixmap_new = pixmap.scaled(640, 480, Qt.KeepAspectRatio)
		##self.imgLbl.setPixmap(pixmap_new)
		
	#def nextBtnClicked(self):
		
		#sender = self.sender()

		#if i_list[0] > 0:
			#i_list[0] -= 1
		#else:
			#i_list[0] = len(files_names) - 1
		##pixmap = QPixmap(files_names[i_list[0]])
		##pixmap_new = pixmap.scaled(640, 480, Qt.KeepAspectRatio)
		##self.imgLbl.setPixmap(pixmap_new)

	def prevBtnClicked(self):
		sender = self.sender()
		self.lbl.setText('Previous Button was clicked')
		
	def nextBtnClicked(self):
		sender = self.sender()
		self.lbl.setText('Next Button was clicked')
		#self.tab2Table.setItem(0,0, QTableWidgetItem("Some text"))

	# def _on_radio_button_clicked(self, button):
		# if button.property('btn_name') == 'and':
			# # self.tab2Table.setItem(1,1, QTableWidgetItem('and pressed'))
			# print('and pressed')
		# elif button.property('btn_name') == 'or':
			# # self.tab2Table.setItem(1,1, QTableWidgetItem('or pressed'))
			# print('or pressed')

	def radio_button_and_clicked(self):
		sender = self.sender()
		button_num = sender.property('radio_btn_num')
		print('AND radio button No.' + str(button_num))
		
	def radio_button_or_clicked(self):
		sender = self.sender()
		button_num = sender.property('radio_btn_num')
		print('OR radio button No.' + str(button_num))
		
	def firstBtnClicked(self):
		sender = self.sender()
		btnWidget = self.tab2Table.cellWidget(2, 2)
		btnWidgetProperty = btnWidget.layout.firstBtn.property('num')
		btnWidget.layout.firstBtn.setProperty('num', btnWidgetProperty + 1)
		print('btnWidgetProperty is ' + str(btnWidgetProperty))
		self.tab2Table.setItem(1,1, QTableWidgetItem('1 btn clicked'))
		
		
	def secondBtnClicked(self):
		sender = self.sender()
		self.tab2Table.setItem(1,1, QTableWidgetItem('2 btn clicked'))

	def secondButtonClicked(self):
		sender = self.sender()
		boolProperty = sender.property('bool')
		if boolProperty == 'and':
			sender.setText('and [OR]')
			sender.setProperty('bool', 'or')
		elif boolProperty == 'or':
			sender.setText('[AND] or')
			sender.setProperty('bool', 'and')
		
		"""
		rand_int_list = []
		for i in range(3):
			rand_int_list.append(random.randint(0,255))
		
		sender.setStyleSheet('background-color: rgb(' + str(rand_int_list[0]) + ',' + str(rand_int_list[1]) + ',' + str(rand_int_list[2]) + ')')
		"""
		# self.newCellLbl = QLabel('<b>Новий</b> текст')
		self.plusCellBtn = QPushButton('+')
		self.minusCellBtn = QPushButton('-')
				
		self.cellLayout = QGridLayout(self)
		# cellLayout.addWidget(self.newCellLbl)
		self.cellLayout.addWidget(self.plusCellBtn, 0, 0)
		self.cellLayout.addWidget(self.minusCellBtn, 0, 1)
		
		cellWidget = QWidget()
		cellWidget.setLayout(self.cellLayout)
		self.cellLayout.setContentsMargins(0,0,0,0)
		self.cellLayout.setSpacing(0)
		
		# sender.setLayout(cellLayout)
		self.tab2Table.setCellWidget(2, 1, cellWidget)
		
		# sender.setText('New text')
		# sender.setStyleSheet('background-color: rgb(180,180,210); font-weight: bold')
		
	def newButtonClicked(self):
		sender = self.sender()
		# cellRadioWidget = self.tab2Table.cellWidget(0,0)
		#currBtn = self.button_group.checkedButton()
		# currBtnGroup = cellRadioWidget.property('radio_buttons_group')
		# currBtn = currBtnGroup.checkedButton()
		# print('currBtn is: ')
		# print(currBtn)
		# if currBtn.property('btn_name') == 'and':
			# print('and')
		# elif currBtn.property('btn_name') == 'or':
			# print('or')
		
		# image = Image.open('IMG_9133.JPG')
		
		# print('Image info is: ')
		# print(image.info)
		
		# self.tab2Table.cellPressed.connect(self.tab2TableCellActivated)
		self.tab2Table.itemSelectionChanged.connect(self.tab2TableItemSelChngd)
		# self.tab2Table.keyPressEvent = self.keyPressEvent
		self.tab2Table.keyPressEvent = self.keyPressEvent
		
		for i in range(10):
			"""
			self.radio_button_1 = QRadioButton('and')
			self.radio_button_1.setChecked(True)
			self.radio_button_1.setProperty('radio_btn_num', i)
			self.radio_button_2 = QRadioButton('or')
			self.radio_button_2.setProperty('radio_btn_num', i)
			
			# self.button_group = QButtonGroup()
			# self.button_group.addButton(self.radio_button_1)
			# self.button_group.addButton(self.radio_button_2)
			
			# self.button_group.buttonClicked.connect(self._on_radio_button_clicked)
			
			self.radio_button_1.clicked.connect(self.radio_button_and_clicked)
			self.radio_button_2.clicked.connect(self.radio_button_or_clicked)
			"""
			
			self.tab2TableItem = QTableWidgetItem('Text ' + str(i))
			# self.tab2TableItem.setBackground(QColor(205,255,218))
			if i % 2 == 0:
				self.tab2TableItem.setBackground(QColor(255,255,158))
				self.tab2TableItem.setForeground(QColor(0,134,104))
			else:
				self.tab2TableItem.setBackground(QColor(255,255,255))
				self.tab2TableItem.setForeground(QColor(0,0,230))
			
			self.tab2Table.setItem(i,0, self.tab2TableItem)
			
		
		# 25.09.2018
		
		# f = 'IMG_9133.JPG'
		# fd = open(f)
		# d = fd.read()
		# xmp_start = d.find('<x:xmpmeta')
		# xmp_end = d.find('</x:xmpmeta')
		# xmp_str = d[xmp_start:xmp_end+12]
		# print(xmp_str)
		
		"""
		with open('IMG_9133.JPG', "rb") as fin:
			img = fin.read()
		imgAsString = str(img)
		xmp_start = imgAsString.find('<x:xmpmeta')
		xmp_end = imgAsString.find('</x:xmpmeta')
		if xmp_start != xmp_end:
			xmpString = imgAsString[xmp_start:xmp_end + 12]
		
		print(type(imgAsString))
		print(type(xmpString))
		print(xmpString)
		self.tab2Table.setItem(1,1, QTableWidgetItem(xmpString))
		
		b = xmpString.encode('utf-8')
		print(b)
		print(type(b))
		
		print(b.decode("utf-8"))
		
		splitted_xmp = re.split(b'</rdf:li> <rdf:li>', b)
		
		for i in range(len(splitted_xmp)):
			new_str = splitted_xmp[i].decode()
			new_converted_str = codecs.escape_decode(bytes(new_str, "utf-8"))[0].decode("utf-8")
			print(new_converted_str)
			print(type(splitted_xmp[i]))
			self.tab2Table.setItem(i+5,1, QTableWidgetItem(new_converted_str))
		"""
		
		# print(xmpString.encode('utf-8'))
		# b = xmpString.encode()
		# print(b)
		# print(type(b))
		
		# print(b.decode())
		# print(type(b.decode()))
		
		
		
		# /25.09.2018

	def tab2TableItemSelChngd(self):
		sender = self.sender()
		
		print('Item selection changed')
		
		print('column=' + str(sender.currentColumn()))
		print('row=' + str(sender.currentRow()))
		i = sender.currentRow()
		# j = sender.currentColumn()
		
		self.cellLabel = self.tab2Table.cellWidget(i,0)
		
		if i % 2 == 0:
			self.tab2Table.setStyleSheet("QTableView {selection-background-color: rgb(135,212,243); selection-color:rgb(255,0,0);}")
		else:
			self.tab2Table.setStyleSheet("QTableView {selection-background-color: rgb(135,212,243); selection-color:rgb(255,255,255);}")
		
		self.tab2Table.selectRow(i)
		
	"""
	def tab2TableCellActivated(self, i, j):
		sender = self.sender()
		
		print('table cell activated')
		print('row num=' + str(i))
		print('col num=' + str(j))
	
		self.cellLabel = self.tab2Table.cellWidget(i,j)
		print(str(type(self.cellLabel)))
		
		if i % 2 == 0:
			self.tab2Table.setStyleSheet("QTableView {selection-background-color: rgb(135,212,243); selection-color:rgb(255,255,0);}")
		else:
			self.tab2Table.setStyleSheet("QTableView {selection-background-color: rgb(135,212,243); selection-color:rgb(255,255,255);}")
	"""
		
		# self.cellLabel.setStyleSheet('background-color: rgb(0,0,0); color: rgb(0,255,0)')
	
	# def add_dir_to_copy_btn_clicked(self):
		# sender = self.sender()
		
		# # foldername = QFileDialog.getExistingDirectory(self, "Open Folder", dirName, QFileDialog.ShowDirsOnly)
		# # foldername = QFileDialog.getOpenFileName(self, "Open Image File", dirName, '', 0)
		# foldername = "f:\z_iso\win10_home_sl_ru_x64.iso"
		
		# if foldername:
			# print('Foldername is ' + foldername)
			# self.tab2Table.setItem(1, 0, QTableWidgetItem(foldername))
			# self.src = foldername
	
	# def add_dir_to_receive_btn_clicked(self):
		# sender = self.sender()
		
		# # foldername = QFileDialog.getExistingDirectory(self, "Open Folder", dirName, QFileDialog.ShowDirsOnly)
		# # foldername = QFileDialog.getOpenFileName(self, "Open Image File", dirName)
		# # foldername = "c:\Users\v-user\Desktop\copied_photos\new_file.iso"
		# foldername = "f:\\new_file.iso"
		
		# if foldername:
			# print('Foldername is ' + foldername)
			# self.tab2Table.setItem(3, 0, QTableWidgetItem(foldername))
			# self.dest = foldername
	
	# def copy_dir_btn_clicked(self):
		# sender = self.sender()
		
		# self.auto_start_timer = QTimer()
		# self.auto_start_timer.timeout.connect( lambda : self.copyfileobj( src=self.src, dst=self.dest, callback_progress=self.progress, callback_copydone=self.copydone )  )
		# self.auto_start_timer.start(2000)
	
	
	# def progress(self, fsrc, fdst, copied):
		# size_src = os.stat( fsrc.name ).st_size
		# size_dst = os.stat( fdst.name ).st_size

		# float_src = float( size_src )
		# float_dst = float( size_dst )

		# percentage = int(float_dst/float_src*100)

		# try:
			# self.copy_progress.setValue( percentage )
		# except:
			# pass

		# app.processEvents()
	
	
	# def copydone(self, fsrc, fdst, copied):
		# self.copy_progress.setValue( 100 )
		# self.close()
	
	
	# def copyfileobj(self, src, dst, callback_progress, callback_copydone, length=8*1024):

		# # Prevent progress callback from being made each cycle
		# c = 0
		# c_max = 50

		# try:
			# self.auto_start_timer.stop()
		# except:
			# print('Error: could not stop QTimer')


		# # with open(src, 'r') as fsrc:
			# # with open(dst, 'w') as fdst:
				# # copied = 0
				# # while True:
					# # buf = fsrc.read(length)
					# # if not buf:
						# # break
					# # fdst.write(buf)
					# # copied += len(buf)
					# # c += 1
					# # if c == c_max:
						# # callback_progress(fsrc=fsrc, fdst=fdst, copied=copied)
						# # c = 0
				# # callback_copydone(fsrc=fsrc, fdst=fdst, copied=copied)
	
		# with open(src, 'r') as fsrc:
			# with open(dst, 'w') as fdst:
				# copied = 0
				# while True:
					# buf = fsrc.read(length)
					# if not buf:
						# break
					# fdst.write(buf)
					# copied += len(buf)
					# c += 1
					# if c == c_max:
						# callback_progress(fsrc=fsrc, fdst=fdst, copied=copied)
						# c = 0
				# callback_copydone(fsrc=fsrc, fdst=fdst, copied=copied)
	
	def keyPressEvent(self, e):
		print("event", e)
		
		i = self.tab2Table.currentRow()
		# j = self.tab2Table.currentColumn()
		
		if e.key() == Qt.Key_Insert:
			print('Key_Insert pressed')
					
			self.tab2Table.item(i,0).setForeground(QColor(0,255,0))
		
			# self.tab2Table.setItemSelected(self.tab2Table.item(i,j), False)
			# self.tab2Table.setItemSelected(self.tab2Table.item(i+1,j), True)
			
			self.tab2Table.setCurrentCell(i+1,0)
			self.tab2Table.selectRow(i+1)
		
		elif e.key() == Qt.Key_Up:
			print('Key_Up pressed')
			
			self.tab2Table.setCurrentCell(i-1,0)
			self.tab2Table.selectRow(i-1)
		
		elif e.key() == Qt.Key_Down:
			print('Key_Down pressed')
			
			self.tab2Table.setCurrentCell(i+1,0)
			self.tab2Table.selectRow(i+1)
		
		# if e.key()  == Qt.Key_Return :
			# print  ' return'
		# elif e.key() == Qt.Key_Enter :   
			# print ' enter'
	
	def tab11BtnClicked(self):
		sender = self.sender()
		
		x = sender.property('x_tab11')
		y = sender.property('y_tab11')
		
		print('Button x=' + str(sender.property('x_tab11')) + ', y=' + str(sender.property('y_tab11')) + ' pressed')

		if tab11Graph.graph['state'] == 0:
			if tab11Graph.nodes[y*9 + x]['color'] != 0:
				tab11Graph.nodes[y*9 + x]['is_choosed'] = True
				tab11_Graph.nodes[y*9 + x]['is_choosed'] = True
				tab11Graph.graph['is_current_node'] = True
				tab11Graph.graph['current_node_num'] = y*9 + x
				tab11Graph.graph['state'] = 1
				# sender.setText('*' + sender.text())
				# sender.setText('')
				self.tab11BtnIcon = QIcon()
				self.tab11BtnIcon.addFile(colors_choosed_icons[tab11Graph.nodes[y*9 + x]['color'] - 1])
				sender.setIcon(self.tab11BtnIcon)
				sender.setIconSize(QSize(48,48))
		if tab11Graph.graph['state'] == 1:
			if tab11Graph.nodes[y*9 + x]['color'] != 0 and tab11Graph.graph['current_node_num'] != y*9 + x:
				tab11Graph.nodes[y*9 + x]['is_choosed'] = True
				tab11Graph.nodes[tab11Graph.graph['current_node_num']]['is_choosed'] = False
				
				for i in range(9):
					for j in range(9):
						if i*9 + j == tab11Graph.graph['current_node_num']:
							# self.tab11BtnIcon = QIcon()
							# self.tab11BtnIcon.addFile('')
							# sender.setIcon(self.tab11BtnIcon)
							# tab11Btns[i][j].setIcon(QIcon())
							
							# tab11Btns[i][j].setText(str(tab11Graph.nodes[i*9 + j]['color']))
							# tab11Btns[i][j].setStyleSheet('background-color: rgb(' + colors[tab11Graph.nodes[i*9 + j]['color'] - 1] + ')')
							self.tab11BtnIcon = QIcon()
							self.tab11BtnIcon.addFile(colors_icons[tab11Graph.nodes[i*9 + j]['color'] - 1])
							tab11Btns[i][j].setIcon(self.tab11BtnIcon)
							tab11Btns[i][j].setIconSize(QSize(48,48))
				
				tab11Graph.graph['current_node_num'] = y*9 + x
				# sender.setText('*' + sender.text())
				# sender.setText('')
				self.tab11BtnIcon = QIcon()
				self.tab11BtnIcon.addFile(colors_choosed_icons[tab11Graph.nodes[y*9 + x]['color'] - 1])
				sender.setIcon(self.tab11BtnIcon)
				sender.setIconSize(QSize(48,48))
				
			if tab11Graph.nodes[y*9 + x]['color'] == 0:
				tab11GraphCopy = tab11Graph.copy()
				tab11GraphCopy.nodes[tab11GraphCopy.graph['current_node_num']]['color'] = 0
				
				for i in range(tab11GraphCopy.number_of_nodes()):
					if tab11GraphCopy.nodes[i]['color'] != 0:
						tab11GraphCopy.remove_node(i)
				
				pathBetweenNodes = True
				try:
					nx.shortest_path_length(tab11GraphCopy, tab11GraphCopy.graph['current_node_num'], y*9 + x)
				except nx.exception.NetworkXNoPath:
					pathBetweenNodes = False
					print('No path between nodes')
				
				if pathBetweenNodes == True:
					tab11Graph.nodes[y*9 + x]['is_choosed'] = True
					tab11Graph.nodes[tab11Graph.graph['current_node_num']]['is_choosed'] = False
					
					for i in range(9):
						for j in range(9):
							if i*9 + j == tab11Graph.graph['current_node_num']:
								# tab11Btns[i][j].setText('')
								tab11Btns[i][j].setIcon(QIcon())
								# tab11Btns[i][j].setStyleSheet('background-color: rgb(255, 255, 255)')
					
					tab11Graph.nodes[y*9 + x]['color'] = tab11Graph.nodes[tab11Graph.graph['current_node_num']]['color']
					# tab11Btns[y][x].setStyleSheet('background-color: rgb(' + colors[tab11Graph.nodes[tab11Graph.graph['current_node_num']]['color'] - 1] + ')')
					self.tab11BtnIcon = QIcon()
					self.tab11BtnIcon.addFile(colors_icons[tab11Graph.nodes[tab11Graph.graph['current_node_num']]['color'] - 1])
					sender.setIcon(self.tab11BtnIcon)
					sender.setIconSize(QSize(48,48))
					
					tab11Graph.nodes[tab11Graph.graph['current_node_num']]['color'] = 0
					tab11Graph.graph['current_node_num'] = y*9 + x
					# sender.setIcon(QIcon())
					# sender.setText(str(tab11Graph.nodes[y*9 + x]['color']))
					
					delete_one_color = False
					for i in range(5):
						for j in range(9):
							one_color_nodes_count = 1
							for k in range(9 - i - 1):
								if tab11Graph.nodes[(i+k+1)*9 + j]['color'] == tab11Graph.nodes[i*9 + j]['color'] and tab11Graph.nodes[i*9 + j]['color'] != 0:
									one_color_nodes_count += 1
								else:
									break
							if one_color_nodes_count >= 5:
								for k in range(one_color_nodes_count):
									tab11Graph.nodes[(i+k)*9 + j]['color'] = 0
									# tab11Btns[i+k][j].setText('')
									tab11Btns[i+k][j].setIcon(QIcon())
									# tab11Btns[i+k][j].setStyleSheet('background-color: rgb(255, 255, 255)')
								delete_one_color = True
								tab11Graph.graph['colored_nodes_count'] -= one_color_nodes_count
							if delete_one_color == True:
								break
						if delete_one_color == True:
							break
					
					for i in range(9):
						for j in range(5):
							one_color_nodes_count = 1
							for k in range(9 - j - 1):
								if tab11Graph.nodes[i*9 + j + k + 1]['color'] == tab11Graph.nodes[i*9 + j]['color'] and tab11Graph.nodes[i*9 + j]['color'] != 0:
									one_color_nodes_count += 1
								else:
									break
							if one_color_nodes_count >= 5:
								for k in range(one_color_nodes_count):
									tab11Graph.nodes[i*9 + j + k]['color'] = 0
									# tab11Btns[i][j+k].setText('')
									tab11Btns[i][j+k].setIcon(QIcon())
									# tab11Btns[i][j+k].setStyleSheet('background-color: rgb(255, 255, 255)')
								delete_one_color = True
								tab11Graph.graph['colored_nodes_count'] -= one_color_nodes_count
							if delete_one_color == True:
								break
						if delete_one_color == True:
							break
					
					for i in range(5):
						for j in range(5):
							one_color_nodes_count = 1
							
							if i > j:
								l = i
							else:
								l = j
							
							for k in range(9 - l - 1):
								if tab11Graph.nodes[(i+k+1)*9 + j + k + 1]['color'] == tab11Graph.nodes[i*9 + j]['color'] and tab11Graph.nodes[i*9 + j]['color'] != 0:
									one_color_nodes_count += 1
								else:
									break
							if one_color_nodes_count >= 5:
								for k in range(one_color_nodes_count):
									
									print('i=' + str(i))
									print('j=' + str(j))
									print('k=' + str(k))
									
									tab11Graph.nodes[(i+k)*9 + j + k]['color'] = 0
									# tab11Btns[i+k][j+k].setText('')
									tab11Btns[i+k][j+k].setIcon(QIcon())
									# tab11Btns[i+k][j+k].setStyleSheet('background-color: rgb(255, 255, 255)')
								delete_one_color = True
								tab11Graph.graph['colored_nodes_count'] -= one_color_nodes_count
							if delete_one_color == True:
								break
						if delete_one_color == True:
							break
					
					for i in range(5):
						for j in range(5):
							one_color_nodes_count = 1
							
							if i > (4 - j):
								l = i
							else:
								l = 4 - j
							
							for k in range(8 - l - 1):
								if tab11Graph.nodes[(i+k+1)*9 + j - k + 3]['color'] == tab11Graph.nodes[i*9 + j + 4]['color'] and tab11Graph.nodes[i*9 + j + 4]['color'] != 0:
									one_color_nodes_count += 1
								else:
									break
							if one_color_nodes_count >= 5:
								for k in range(one_color_nodes_count):
									
									print('i=' + str(i))
									print('j=' + str(j))
									print('k=' + str(k))
									
									tab11Graph.nodes[(i+k)*9 + j - k + 4]['color'] = 0
									# tab11Btns[i+k][j-k+4].setText('')
									tab11Btns[i+k][j-k+4].setIcon(QIcon())
									# tab11Btns[i+k][j-k+4].setStyleSheet('background-color: rgb(255, 255, 255)')
								delete_one_color = True
								tab11Graph.graph['colored_nodes_count'] -= one_color_nodes_count
							if delete_one_color == True:
								break
						if delete_one_color == True:
							break
					
					if delete_one_color == False:
						if tab11Graph.graph['colored_nodes_count'] < 81:
							for i in range(3):
								while True:
									rand_node = random.randint(0,80)
									rand_color = random.randint(1,7)
									if tab11Graph.nodes[rand_node]['color'] == 0:
										tab11Graph.nodes[rand_node]['color'] = rand_color
										tab11Graph.graph['colored_nodes_count'] += 1
										# if tab11Graph.graph['colored_nodes_count'] == 225:
											# break
										
										for j in range(9):
											for k in range(9):
												if j*9 + k == rand_node:
													# tab11Btns[j][k].setText(str(rand_color))
													# tab11Btns[j][k].setStyleSheet('background-color: rgb(' + colors[rand_color - 1] + ')')
													self.tab11BtnIcon = QIcon()
													self.tab11BtnIcon.addFile(colors_icons[rand_color - 1])
													tab11Btns[j][k].setIcon(self.tab11BtnIcon)
													tab11Btns[j][k].setIconSize(QSize(48,48))
										
										break
								if tab11Graph.graph['colored_nodes_count'] == 81:
									break
					
						for i in range(5):
							for j in range(9):
								one_color_nodes_count = 1
								for k in range(9 - i - 1):
									if tab11Graph.nodes[(i+k+1)*9 + j]['color'] == tab11Graph.nodes[i*9 + j]['color'] and tab11Graph.nodes[i*9 + j]['color'] != 0:
										one_color_nodes_count += 1
									else:
										break
								if one_color_nodes_count >= 5:
									for k in range(one_color_nodes_count):
										tab11Graph.nodes[(i+k)*9 + j]['color'] = 0
										tab11Btns[i+k][j].setIcon(QIcon())
										# tab11Btns[i+k][j].setText('')
										# tab11Btns[i+k][j].setStyleSheet('background-color: rgb(255, 255, 255)')
									delete_one_color = True
									tab11Graph.graph['colored_nodes_count'] -= one_color_nodes_count
								if delete_one_color == True:
									break
							if delete_one_color == True:
								break
					
						for i in range(9):
							for j in range(5):
								one_color_nodes_count = 1
								for k in range(9 - j - 1):
									if tab11Graph.nodes[i*9 + j + k + 1]['color'] == tab11Graph.nodes[i*9 + j]['color'] and tab11Graph.nodes[i*9 + j]['color'] != 0:
										one_color_nodes_count += 1
									else:
										break
								if one_color_nodes_count >= 5:
									for k in range(one_color_nodes_count):
										tab11Graph.nodes[i*9 + j + k]['color'] = 0
										tab11Btns[i][j+k].setIcon(QIcon())
										# tab11Btns[i][j+k].setText('')
										# tab11Btns[i][j+k].setStyleSheet('background-color: rgb(255, 255, 255)')
									delete_one_color = True
									tab11Graph.graph['colored_nodes_count'] -= one_color_nodes_count
								if delete_one_color == True:
									break
							if delete_one_color == True:
								break
					
						for i in range(5):
							for j in range(5):
								one_color_nodes_count = 1
								
								if i > j:
									l = i
								else:
									l = j
								
								for k in range(9 - l - 1):
									if tab11Graph.nodes[(i+k+1)*9 + j + k + 1]['color'] == tab11Graph.nodes[i*9 + j]['color'] and tab11Graph.nodes[i*9 + j]['color'] != 0:
										one_color_nodes_count += 1
									else:
										break
								if one_color_nodes_count >= 5:
									for k in range(one_color_nodes_count):
										
										print('i=' + str(i))
										print('j=' + str(j))
										print('k=' + str(k))
										
										tab11Graph.nodes[(i+k)*9 + j + k]['color'] = 0
										tab11Btns[i+k][j+k].setIcon(QIcon())
										# tab11Btns[i+k][j+k].setText('')
										# tab11Btns[i+k][j+k].setStyleSheet('background-color: rgb(255, 255, 255)')
									delete_one_color = True
									tab11Graph.graph['colored_nodes_count'] -= one_color_nodes_count
								if delete_one_color == True:
									break
							if delete_one_color == True:
								break
					
						for i in range(5):
							for j in range(5):
								one_color_nodes_count = 1
								
								if i > (4 - j):
									l = i
								else:
									l = 4 - j
								
								for k in range(9 - l - 1):
									if tab11Graph.nodes[(i+k+1)*9 + j - k + 3]['color'] == tab11Graph.nodes[i*9 + j + 4]['color'] and tab11Graph.nodes[i*9 + j + 4]['color'] != 0:
										one_color_nodes_count += 1
									else:
										break
								if one_color_nodes_count >= 5:
									for k in range(one_color_nodes_count):
										
										print('i=' + str(i))
										print('j=' + str(j))
										print('k=' + str(k))
										
										tab11Graph.nodes[(i+k)*9 + j - k + 4]['color'] = 0
										tab11Btns[i+k][j-k+4].setIcon(QIcon())
										# tab11Btns[i+k][j-k+4].setText('')
										# tab11Btns[i+k][j-k+4].setStyleSheet('background-color: rgb(255, 255, 255)')
									delete_one_color = True
									tab11Graph.graph['colored_nodes_count'] -= one_color_nodes_count
								if delete_one_color == True:
									break
							if delete_one_color == True:
								break
					
					tab11Graph.graph['state'] = 0

			
	
	def initGraph(self):
		for i in range(9):
			for j in range(9):
				tab11Graph.add_node(i*9 + j)
				tab11Graph.nodes[i*9 + j]['color'] = 0
				# Buttons on tab11
				tab11Btns[i][j].setFixedSize(48, 48)
				tab11Btns[i][j].setStyleSheet('background-color: rgb(210,210,210)')
				# / Buttons on tab11
				tab11Graph.nodes[i*9 + j]['is_choosed'] = False
				
				tab11_Graph.add_node(i*9 + j)
				tab11_Graph.nodes[i*9 + j]['color'] = 0
				tab11_Graph.nodes[i*9 + j]['is_choosed'] = False
				# Если i (номер строки) > 0, сформировать связь между этой вершиной 
				# и вершиной в том же столбце j, но в предыдущей строке i-1
				if i > 0:
					tab11Graph.add_edge(i*9 + j, (i-1)*9 + j)
					tab11_Graph.add_edge(i*9 + j, (i-1)*9 + j)
				# Если j (номер столбца) > 0, сформировать связь между этой вершиной 
				# и вершиной в той же строке i, но в предыдущем столбце j-1
				if j > 0:
					tab11Graph.add_edge(i*9 + j, i*9 + j - 1)
					tab11_Graph.add_edge(i*9 + j, i*9 + j - 1)
				
				# Формирование диагональных связей между вершинами (снизу слева - вверх направо) 
				# в графе tab11_Graph
				if i > 0 and j < 8:
					tab11_Graph.add_edge((i-1)*9 + j + 1, i*9 + j)
				# Формирование диагональных связей между вершинами (снизу справа - вверх налево) 
				# в графе tab11_Graph
				if i > 0 and j > 0:
					tab11_Graph.add_edge((i-1)*9 + j - 1, i*9 + j)
	
		print(tab11Graph.edges)
		
		# Создать 3 шара случайно выбранных цветов 
		# в случайно выбранных местах (среди свободных)
		for i in range(3):
			while True:
				# Случайным образом выбираем номер ячейки
				rand_node = random.randint(0,80)
				# Случайным образом выбираем номер цвета для шара
				rand_color = random.randint(1,7)
				# Если в ячейке, имеющей случайно выбранный номер, нет шара, 
				# то разместим его там
				if tab11Graph.nodes[rand_node]['color'] == 0:
					tab11Graph.nodes[rand_node]['color'] = rand_color
					tab11_Graph.nodes[rand_node]['color'] = rand_color
					break
		
		tab11Graph.graph['state'] = 0
		tab11Graph.graph['is_current_node'] = False
		tab11Graph.graph['current_node_num'] = 0
		tab11Graph.graph['colored_nodes_count'] = 3
		
		# Пройти по всем ячейкам. Если в графе tab11Graph вершина окрашена, 
		# то разместить в соответствующей ячейке шар определенного цвета
		for i in range(9):
			for j in range(9):
				if tab11Graph.nodes[i*9 + j]['color'] != 0:
					# tab11Btns[i][j].setText(str(tab11Graph.nodes[i*9 + j]['color']))
					# tab11Btns[i][j].setStyleSheet('background-color: rgb(' + colors[tab11Graph.nodes[i*9 + j]['color'] - 1] + ')')
					self.tab11BtnIcon = QIcon()
					self.tab11BtnIcon.addFile(colors_icons[tab11Graph.nodes[i*9 + j]['color'] - 1], size = QSize(48,48))
					tab11Btns[i][j].setIcon(self.tab11BtnIcon)
					tab11Btns[i][j].setIconSize(QSize(48,48))
		
if __name__ == '__main__':

	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
