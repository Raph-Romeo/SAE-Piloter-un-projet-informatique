from PyQt5.QtGui import QIcon, QPixmap, QPainter


def color_icon(icon, color):
    pixmap = QPixmap(icon)
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()
    icon = QIcon(pixmap)
    return icon
