light_style_sheet = """
    QWidget{background:transparent}
    QMainWindow{background-color: qlineargradient(y1: 0, y2: 1, stop: 0 #f8f4f4, stop: 1 #e4e0e0)}
    QTabWidget::pane {border:0px;background:transparent;} 
    QTabBar::tab {background: rgb(10,10,10);border:none;padding:12px;color:#AAA;}
    QTabBar::tab:hover {background:rgb(10,10,10);color:white;}
    QTabBar::tab:selected {background:rgb(23,23,23);color:white;}
    QScrollArea{border:none;}
    QToolButton{background:transparent;border:none;font-family:verdana;font-weight:999;text-align:left;color:#000;font-size:12px;padding-left:15px;margin-top:14px;margin-bottom:14px}
    QToolButton[lastButton="true"]{margin-bottom:44px;margin-top:14px}
    QToolButton[firstButton="true"]{margin-top:44px;margin-bottom:14px}
    
    QScrollBar:vertical{background-color: rgb(194,194,194);width: 15px;margin: 15px 3px 15px 3px;border: 1px transparent #2A2929;border-radius: 4px;}
    QScrollBar::handle:vertical{background-color: #999;min-height: 5px;border-radius: 4px;}
    QScrollBar::sub-line:vertical{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:vertical{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on{height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on{height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{background: none;opacity: 0%;height: 0px;width:0px;}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{background: none;opacity: 0%;height: 0px;width:0px;}
    
    QLabel{color:white;font-family:Consolas;font-size:15px;border:0px solid black;background-color:transparent;padding:0px;padding-left:10px;padding-right:10px;margin:0px;text-indent:0px;}
    QLineEdit{border:0px solid black;margin:0px;padding:0px;font-family:Consolas;color:white;font-size:15px;padding-bottom:10px;text-indent:0px;margin-left:-2px;margin-top:-1px;}
    
    QLabel[title="true"]{color:black;margin-left:10px;font-size:20px;font-weight:1;font-family:verdana}
"""

dark_style_sheet = """
    QWidget{background:transparent}
    QMainWindow{background-color: qlineargradient(y1: 0, y2: 1, stop: 0 #202020, stop: 1 #1b1b1b)}
    QTabWidget::pane {border:0px;transparent;} 
    QTabBar::tab {background: rgb(10,10,10);border:none;padding:12px;color:#AAA;}
    QTabBar::tab:hover {background:rgb(10,10,10);color:white;}
    QTabBar::tab:selected {background:rgb(23,23,23);color:white;}
    QScrollArea{border:none;}
    QToolButton{background:transparent;border:none;font-family:verdana;font-weight:999;text-align:left;color:#fff;font-size:12px;padding-left:15px;margin-top:14px;margin-bottom:14px}
    QToolButton[lastButton="true"]{margin-bottom:44px;margin-top:14px}
    QToolButton[firstButton="true"]{margin-top:44px;margin-bottom:14px}
    
    QScrollBar:vertical{background-color: rgb(12,12,12);width: 15px;margin: 15px 3px 15px 3px;border: 1px transparent #2A2929;border-radius: 4px;}
    QScrollBar::handle:vertical{background-color: #333;min-height: 5px;border-radius: 4px;}
    QScrollBar::sub-line:vertical{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:vertical{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on{height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on{height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{background: none;opacity: 0%;height: 0px;width:0px;}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{background: none;opacity: 0%;height: 0px;width:0px;}
    
    QLabel{color:white;font-family:Consolas;font-size:15px;border:0px solid black;background-color:transparent;padding:0px;padding-left:10px;padding-right:10px;margin:0px;text-indent:0px;}
    QLineEdit{border:0px solid black;margin:0px;padding:0px;font-family:Consolas;color:white;font-size:15px;padding-bottom:10px;text-indent:0px;margin-left:-2px;margin-top:-1px;}

    QPushButton{color:white;}
    
    QLabel[title="true"]{color:white;margin-left:10px;font-size:20px;font-weight:1;font-family:verdana}
"""