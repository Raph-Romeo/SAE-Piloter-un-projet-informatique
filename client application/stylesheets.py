light_style_sheet = """
    TitleBarButton {
     qproperty-normalColor: black;
     qproperty-hoverColor: black;
     qproperty-hoverBackgroundColor: #ddd;
    }
    QWidget{background:transparent}
    *[MainWindow="true"]{background-color: qlineargradient(y1: 0, y2: 1, stop: 0 #f8f4f4, stop: 1 #e4e0e0)}
    QTabWidget::pane {border:0px;background:transparent;} 
    QTabBar::tab {background: rgb(10,10,10);border:none;padding:12px;color:#AAA;}
    QTabBar::tab:hover {background:rgb(10,10,10);color:white;}
    QTabBar::tab:selected {background:rgb(23,23,23);color:white;}
    QScrollArea{border:none;}
    QToolButton{background:transparent;border:none;font-family:verdana;font-weight:999;text-align:left;color:#777;font-size:12px;padding-left:15px;margin-top:14px;margin-bottom:14px}
    QToolButton[lastButton="true"]{margin-bottom:44px;margin-top:14px}
    QToolButton[firstButton="true"]{margin-top:44px;margin-bottom:14px}
    QToolButton[selected="true"]{border-left:3px solid #5b2efc;padding-left:12px;color:#5b2efc}
    QToolButton:hover[selected="false"]{color:#333}
    QToolButton:pressed[selected="false"]{border-left:1px solid #666;padding-left:13px;color:#000}

    QScrollBar:vertical{background-color: rgb(194,194,194);width: 15px;margin: 15px 3px 15px 3px;border: 1px transparent #2A2929;border-radius: 4px;}
    QScrollBar::handle:vertical{background-color: #999;min-height: 5px;border-radius: 4px;}
    QScrollBar::sub-line:vertical{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:vertical{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on{height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on{height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{background: none;opacity: 0%;height: 0px;width:0px;}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{background: none;opacity: 0%;height: 0px;width:0px;}
    
    QScrollBar:horizontal{background-color: rgba(194,194,194,80);height: 10px;margin:2px;border: 1px transparent #2A2929;border-radius: 3px;}
    QScrollBar::handle:horizontal{background-color: #999;min-height: 5px;width:5px;border-radius: 3px;}
    QScrollBar::sub-line:horizontal{margin: 3px 0px 3px 0px;height: 5px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:horizontal{margin: 3px 0px 3px 0px;height: 5px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::sub-line:horizontal:hover,QScrollBar::sub-line:horizontal:on{height: 4px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on{height: 4px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal{background: none;opacity: 0%;height: 4px;width:0px;}
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal{background: none;opacity: 0%;height: 4px;width:0px;}

    QLabel{color:black;font-family:Consolas;font-size:15px;border:0px solid black;background-color:transparent;padding:0px;padding-left:10px;padding-right:10px;margin:0px;text-indent:0px;}
    QLineEdit{border:0px solid black;margin:0px;padding:0px;font-family:Consolas;color:white;font-size:15px;padding-bottom:10px;text-indent:0px;margin-left:-2px;margin-top:-1px;}

    QMainWindow[tasksTopMenu="true"]{background:#FFF;border-radius:10px;margin-right:20px;}
    QWidget[tasksContentWindow="true"]{background:#FFF;border-radius:10px;margin-right:20px;margin-top:5px;margin-bottom:30px}

    QPushButton[topMenuButton="true"]{color:#777;border:none;font-size:12px;font-family:verdana;margin-left:8px;margin-right:8px;margin-bottom:9px;margin-top:-5px}
    QPushButton:hover[topMenuButton="true"]{color:#333}
    QPushButton:pressed[topMenuButton="true"]{border-bottom:1px solid #666;color:#000;margin-top:-4px;padding-top:1px}
    QPushButton[topMenuButton="true"][selected="true"]{color:#5b2efc;border-bottom:3px solid #5b2efc;margin-top:-2px;padding-top:0px}

    QPushButton[addTaskButton="true"]{background:#5b2efc;border:none;border-radius:14px;color:white;font-size:18px;margin-right:5px;margin-left:5px;}
    QPushButton[addTaskButton="true"]:hover{background:#4b1eec;}
    QPushButton[addTaskButton="true"]:pressed{background:#3b0edc;color:#ddd}

    QLabel[title="true"]{color:black;margin-left:10px;font-size:20px;font-weight:1;font-family:verdana}
    QWidget[searchBar="true"]{border:1px solid #EEE;margin-top:5px;border-radius:17px}
    QWidget[searchBar="true"][focused="true"]{border:1px solid #222;}
    
    QLineEdit{color:#222;font-family:verdana;font-size:14px;margin-right:30px}
    
    QPushButton[settings="true"]{color:black;font-size:16px;border:1px solid #ddd;border-radius:10px;background:white;padding:12px;}
    
    QTableWidget{border:0px solid}
    QTableWidget::item{border-top:1px solid #eee;font-family:verdana;}
    QTableView::item:selected {background-color: #7b4eff;color:white;}
    QHeaderView::section{background:white;border:none;border-right:1px solid #eee;margin-bottom:5px;font-weight:normal;}
    QHeaderView::section:active{font-weight:normal}
"""

dark_style_sheet = """
    TitleBarButton {
     qproperty-normalColor: white;
     qproperty-hoverColor: white;
     qproperty-hoverBackgroundColor: #444;
    }
    QWidget{background:transparent}
    *[MainWindow="true"]{background-color: qlineargradient(y1: 0, y2: 1, stop: 0 #202020, stop: 1 #1b1b1b)}
    QTabWidget::pane {border:0px;transparent;} 
    QTabBar::tab {background: rgb(10,10,10);border:none;padding:12px;color:#AAA;}
    QTabBar::tab:hover {background:rgb(10,10,10);color:white;}
    QTabBar::tab:selected {background:rgb(23,23,23);color:white;}
    QScrollArea{border:none;}
    QToolButton{background:transparent;border:none;font-family:verdana;font-weight:999;text-align:left;color:#ddd;font-size:12px;padding-left:15px;margin-top:14px;margin-bottom:14px}
    QToolButton[lastButton="true"]{margin-bottom:44px;margin-top:14px}
    QToolButton[firstButton="true"]{margin-top:44px;margin-bottom:14px}
    QToolButton[selected="true"]{border-left:3px solid #916cee;padding-left:12px;color:#916cee}
    QToolButton:hover[selected="false"]{color:#fff}
    QToolButton:pressed[selected="false"]{border-left:1px solid #777;padding-left:13px;color:#fff}
    
    QScrollBar:vertical{background-color: rgb(12,12,12);width: 15px;margin: 15px 3px 15px 3px;border: 1px transparent #2A2929;border-radius: 4px;}
    QScrollBar::handle:vertical{background-color: #333;min-height: 5px;border-radius: 4px;}
    QScrollBar::sub-line:vertical{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:vertical{margin: 3px 0px 3px 0px;height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on{height: 0px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on{height: 0px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{background: none;opacity: 0%;height: 0px;width:0px;}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{background: none;opacity: 0%;height: 0px;width:0px;}
    
    QScrollBar:horizontal{background-color: rgba(12,12,12);height: 10px;margin:2px;border: 1px transparent #2A2929;border-radius: 3px;}
    QScrollBar::handle:horizontal{background-color: #333;min-height: 5px;width:5px;border-radius: 3px;}
    QScrollBar::sub-line:horizontal{margin: 3px 0px 3px 0px;height: 5px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:horizontal{margin: 3px 0px 3px 0px;height: 5px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::sub-line:horizontal:hover,QScrollBar::sub-line:horizontal:on{height: 4px;width: 0px;subcontrol-position: top;subcontrol-origin: margin;}
    QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on{height: 4px;width: 0px;subcontrol-position: bottom;subcontrol-origin: margin;}
    QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal{background: none;opacity: 0%;height: 4px;width:0px;}
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal{background: none;opacity: 0%;height: 4px;width:0px;}

    
    QLabel{color:white;font-family:Consolas;font-size:15px;border:0px solid black;background-color:transparent;padding:0px;padding-left:10px;padding-right:10px;margin:0px;text-indent:0px;}
    QLineEdit{border:0px solid black;margin:0px;padding:0px;font-family:Consolas;color:white;font-size:15px;padding-bottom:10px;text-indent:0px;margin-left:-2px;margin-top:-1px;}

    QMainWindow[tasksTopMenu="true"]{background:#252525;border-radius:10px;margin-right:20px}
    QWidget[tasksContentWindow="true"]{background:#252525;border-radius:10px;margin-right:20px;margin-top:5px;margin-bottom:30px}

    QPushButton[topMenuButton="true"]{color:#ddd;border:none;font-size:12px;font-family:verdana;margin-left:8px;margin-right:8px;margin-bottom:9px;margin-top:-5px}
    QPushButton:hover[topMenuButton="true"]{color:#fff}
    QPushButton:pressed[topMenuButton="true"]{border-bottom:1px solid #777;color:#fff;margin-top:-4px;padding-top:1px}
    QPushButton[topMenuButton="true"][selected="true"]{color:#916cee;border-bottom:3px solid #916cee;margin-top:-2px;padding-top:0px}
    
    QPushButton[addTaskButton="true"]{background:#916cee;border:none;border-radius:14px;color:#222;font-size:18px;margin-left:5px;margin-right:5px;}
    QPushButton[addTaskButton="true"]:hover{background:#815cde;}
    QPushButton[addTaskButton="true"]:pressed{background:#714cce;color:#000}
    
    QLabel[title="true"]{color:white;margin-left:10px;font-size:20px;font-weight:1;font-family:verdana}
    QWidget[searchBar="true"]{border:1px solid #333;margin-top:5px;border-radius:17px}
    QWidget[searchBar="true"][focused="true"]{border:1px solid #C8C8C8;}
    
    QLineEdit{color:white;font-family:verdana;font-size:14px;margin-right:30px}
    
    QPushButton[settings="true"]{color:white;font-size:16px;border:1px solid #111;border-radius:10px;background:#252525;padding:12px}
    
    QTableWidget{border:0px solid}
    QTableWidget::item{border-top:1px solid #333;font-family:verdana;font-weight:bold;color:white;}
    QTableView::item:selected {background-color: #5b2efc;color:white;}
    QHeaderView::section{background:transparent;border:none;border-right:1px solid #333;margin-bottom:5px;font-weight:normal;color:white;}
    QHeaderView::section:active{font-weight:normal}
"""