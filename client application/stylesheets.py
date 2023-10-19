light_style_sheet = """
    QWidget{background:transparent}
    QMainWindow{background-color: qlineargradient(y1: 0, y2: 1, stop: 0 #f8f4f4, stop: 1 #e4e0e0)}
    QTabWidget::pane {border:0px;background:transparent;} 
    QTabBar::tab {background: rgb(10,10,10);border:none;padding:12px;color:#AAA;}
    QTabBar::tab:hover {background:rgb(10,10,10);color:white;}
    QTabBar::tab:selected {background:rgb(23,23,23);color:white;}
"""

dark_style_sheet = """
    QWidget{background:transparent}
    QMainWindow{background-color: qlineargradient(y1: 0, y2: 1, stop: 0 #202020, stop: 1 #1b1b1b)}
    QTabWidget::pane {border:0px;transparent;} 
    QTabBar::tab {background: rgb(10,10,10);border:none;padding:12px;color:#AAA;}
    QTabBar::tab:hover {background:rgb(10,10,10);color:white;}
    QTabBar::tab:selected {background:rgb(23,23,23);color:white;}
"""