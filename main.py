#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 16:22:51 2020
@author: jacobwickline
"""

from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog, QAction,
                             QMessageBox)
from PyQt5.QtGui import (QImage, QPainter, QPen)
from PyQt5.QtCore import (Qt, QPoint)
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initializeUI()
        self.msg = QMessageBox()
        self.setMouseTracking(True)
        self.coordFile = open("Mouse Coordinates.txt", "w")

    def initializeUI(self):
        #Setting Window Settings
        self.setWindowTitle("CS 272 Final Project")
        self.setFixedSize(1024, 768)
        
        #Creating Blank Image
        self.canvas = QImage(self.size(), QImage.Format_RGB32)
        self.canvas.fill(Qt.white)
        
        #Creating Menu Bar
        menu = self.menuBar()
        fileMenu = menu.addMenu("File")
        brushSize = menu.addMenu("Brush Size")
        brushColor = menu.addMenu("Brush Color")
        
        #Adding Save Image Action
        saveAction = QAction("Save Image", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.triggered.connect(self.saveImage)
        fileMenu.addAction(saveAction)
        
        #Adding Clear Canvas Action
        clearAction = QAction("Clear Canvas", self)
        clearAction.setShortcut("Ctrl+C")
        clearAction.triggered.connect(self.clearCanvas)
        fileMenu.addAction(clearAction)
        
        #Adding Brush Size Actions
        brushSize_2 = QAction("2px", self)
        brushSize_2.triggered.connect(self.size_2)
        brushSize.addAction(brushSize_2)
        
        brushSize_4 = QAction("4px", self)
        brushSize_4.triggered.connect(self.size_4)
        brushSize.addAction(brushSize_4)
        
        brushSize_8 = QAction("8px", self)
        brushSize_8.triggered.connect(self.size_8)
        brushSize.addAction(brushSize_8)
        
        brushSize_16 = QAction("16px", self)
        brushSize_16.triggered.connect(self.size_16)
        brushSize.addAction(brushSize_16)
        
        #Adding Brush Color Actions
        brushColor_black = QAction("Black", self)
        brushColor_black.triggered.connect(self.color_black)
        brushColor.addAction(brushColor_black)
        
        brushColor_white = QAction("White", self)
        brushColor_white.triggered.connect(self.color_white)
        brushColor.addAction(brushColor_white)
        
        brushColor_red = QAction("Red", self)
        brushColor_red.triggered.connect(self.color_red)
        brushColor.addAction(brushColor_red)
                
        brushColor_green = QAction("Green", self)
        brushColor_green.triggered.connect(self.color_green)
        brushColor.addAction(brushColor_green)
        
        brushColor_blue = QAction("Blue", self)
        brushColor_blue.triggered.connect(self.color_blue)
        brushColor.addAction(brushColor_blue)
        
        brushColor_yellow = QAction("Yellow", self)
        brushColor_yellow.triggered.connect(self.color_yellow)
        brushColor.addAction(brushColor_yellow)
        
        #Creating Default Brush Settings
        self.currentColor = Qt.black
        self.currentSize = 2
        
        #This is for keeping track of the mouse's position once it has been clicked
        self.lastMousePos = QPoint()
        
        #This is for keeping track of how many times the mouse clicks happen in the app
        self.mousePressCount = 0
        
        #This keeps the user from drawing until the left mouse button is clicked
        self.draw = False

    #This will allow the user to save an image as a PNG, JPG/JPEG, or Another File
    def saveImage(self):
        filePath, _= QFileDialog.getSaveFileName(self, "Save Image", "",
                                                 "Portable Network Graphics File(*.png)"
                                                 ";;Joint Photographic Experts Group File(*.jpg *.jpeg)"
                                                 ";;All Files(*.*)")
        
        #This will return back if the user doesn't enter a location to
        if filePath == "":
            return
    
        self.canvas.save(filePath)
        
    #This will ask the user if they want to save their image before filling
    #the current image to white    
    def clearCanvas(self):
        self.msg.setWindowTitle("Save Before Clearing?")
        self.msg.setIcon(QMessageBox.Question)
        self.msg.setText("Do You Want to Save Before Clearing the Canvas?")
        self.msg.setStandardButtons(QMessageBox.No|QMessageBox.Yes)
        
        if(self.msg.exec_() == QMessageBox.Yes):
            self.saveImage()
            self.canvas.fill(Qt.white)
            self.update()
            
        else:
            self.canvas.fill(Qt.white)
            self.update()
            self.coordFile = open("Mouse Coordinates.txt", "w")
            self.coordFile.close()
            
    #These are the methods for changing the size of the brush
    def size_2(self):
        self.currentSize = 2
        
    def size_4(self):
        self.currentSize = 4
        
    def size_8(self):
        self.currentSize = 8
    
    def size_16(self):
        self.currentSize = 16
    
    #These are the methods for changing the color of the brush
    def color_black(self):
        self.currentColor = Qt.black
        
    def color_white(self):
        self.currentColor = Qt.white
        
    def color_red(self):
        self.currentColor = Qt.red
        
    def color_green(self):
        self.currentColor = Qt.green
        
    def color_blue(self):
        self.currentColor = Qt.blue
        
    def color_yellow(self):
        self.currentColor = Qt.yellow
            
    #This will detect if the mouse button is being pressed
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draw = True
            self.lastMousePos = event.pos()
        
        self.coordFile = open("Mouse Coordinates.txt" , "a")
        self.mousePressCount = self.mousePressCount + 1
        
        if(self.mousePressCount > 1):
            self.coordFile.write("\n\nMouse Coordinate Set: " + str(self.mousePressCount))
            
        else:
            self.coordFile.write("Mouse Coordinate Set: " + str(self.mousePressCount))

    #This will detect if the mouse is moving
    def mouseMoveEvent(self, event):
        if(event.buttons() & Qt.LeftButton) & self.draw:
            painter = QPainter(self.canvas)
            painter.setPen(QPen(self.currentColor, self.currentSize))
            painter.drawLine(self.lastMousePos, event.pos())
            self.lastMousePos = event.pos()
            self.update()
        
            self.coordFile = open("Mouse Coordinates.txt", "a")
            self.coordFile.write("\nMouse Coordinates: (x:%d , y:%d)" % (event.x(), event.y()))

    #This will detect if the mouse button has been released
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draw = False
            self.coordFile.close()

    #This will allow painting to happen on the canvas
    def paintEvent(self, event):
        canvasPainter  = QPainter(self)
        canvasPainter.begin(self)
        canvasPainter.drawImage(self.rect(),self.canvas)
        canvasPainter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
    