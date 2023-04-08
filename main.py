import sys
from PySide6.QtWidgets import QApplication, QGraphicsItem
from PySide6.QtGui import QPixmap
from PySide6 import QtGui, QtWidgets, QtCore
import os
QtGui.QImageReader.setAllocationLimit(0)

class GraphicsDualPixmapItem(QGraphicsItem):
    def __init__(self, image1: QPixmap, image2: QPixmap):
        super().__init__()

        self.image1 = image1
        self.image2 = image2

        assert self.image1.height() == self.image2.height(), f"Image1's height is {self.image1.height()} while Image2's height is {self.image2.height()}"
        assert self.image1.width() == self.image2.width(), f"Image1's width is {self.image1.width()} while Image2's width is {self.image2.width()}"
        
        self.width = self.image1.width()
        self.height = self.image1.height()

        self.VerticalBar_x = self.image1.width()//2

    def paint(self, painter:QtGui.QPainter, option:QtWidgets.QStyleOptionGraphicsItem, widget:QtWidgets.QWidget=None):
        painter.drawPixmap(0,0, self.VerticalBar_x, self.height, self.image1, 0,0, self.VerticalBar_x, self.height,)
        painter.drawPixmap(self.VerticalBar_x, 0, self.width - self.VerticalBar_x, self.height, self.image2, self.VerticalBar_x, 0, self.width - self.VerticalBar_x, self.height,)

    def boundingRect(self):
        return QtCore.QRectF(0,0,self.width, self.height)
    
    def mousePressEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent):
        scenePos = event.scenePos()
        x = scenePos.x()
        if x > 0 and x < self.width:
            self.VerticalBar_x = x
            self.update()

    def mouseMoveEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent):
        scenePos = event.scenePos()
        x = scenePos.x()
        if x > 0 and x < self.width:
            self.VerticalBar_x = x
            self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = QtWidgets.QGraphicsScene()
    view = QtWidgets.QGraphicsView()

        
    image1 = QPixmap('image1.png')
    image2 = QPixmap('image2.png')
    
    dualpixmapitem = GraphicsDualPixmapItem(image1, image2)
    scene.addItem(dualpixmapitem)
    view.setScene(scene)
    view.setRenderHint(QtGui.QPainter.Antialiasing)
    view.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
    view.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
    view.setOptimizationFlag(QtWidgets.QGraphicsView.DontAdjustForAntialiasing)
    view.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)

    view.fitInView(dualpixmapitem, QtCore.Qt.KeepAspectRatio)

    view.show()
    sys.exit(app.exec_())
