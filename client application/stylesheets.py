light_style_sheet = """
    TitleBarButton {
     qproperty-normalColor: black;
     qproperty-hoverColor: black;
     qproperty-hoverBackgroundColor: #ddd;
    }
    QWidget{background:transparent}
    *[MainWindow="true"]{background-color: qlineargradient(y1: 0, y2: 1, stop: 0 #f8f4f4, stop: 1 #e4e0e0)}
    QMainWindow[loginForm="true"]{background:qlineargradient(y1: 0, y2: 1, stop: 0 #f8f4f4, stop: 1 rgba(228, 224, 224,50));border-bottom-left-radius:5px}
    
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

    QPushButton[topMenuButton="true"]{color:#777;border:none;font-size:12px;font-family:verdana;margin-left:8px;margin-right:8px;margin-bottom:9px;margin-top:-5px;font-weight:1;}
    QPushButton:hover[topMenuButton="true"]{color:#333}
    QPushButton:pressed[topMenuButton="true"]{border-bottom:1px solid #666;color:#000;margin-top:-4px;padding-top:1px}
    QPushButton[topMenuButton="true"][selected="true"]{color:#5b2efc;border-bottom:3px solid #5b2efc;margin-top:-2px;padding-top:0px;}

    QPushButton[addTaskButton="true"]{background:#5b2efc;border:none;border-radius:14px;color:white;font-size:18px;margin-right:5px;margin-left:5px;}
    QPushButton[addTaskButton="true"]:hover{background:#4b1eec;}
    QPushButton[addTaskButton="true"]:pressed{background:#3b0edc;color:#ddd}

    QLabel[title="true"]{color:black;margin-left:10px;font-size:20px;font-weight:1;font-family:verdana}
    QLabel[username_title]{padding:0;font-family:verdana;font-size:12px;color:rgba(0,0,0,170);margin-left:10px;}
    QLabel[username_title]:hover{color:rgba(0,0,0,255)}
    QWidget[searchBar="true"]{border:1px solid #EEE;margin-top:5px;border-radius:17px}
    QWidget[searchBar="true"][focused="true"]{border:1px solid #222;}
    
    QLineEdit{color:#222;font-family:verdana;font-size:14px;margin-right:30px}
    
    QPushButton[settings="true"]{color:black;font-size:16px;border:1px solid #ddd;border-radius:10px;background:white;padding:12px;}
    
    QLineEdit[loginButton="true"]{background:qlineargradient(x1: 1, x2: 0, stop: 0 rgba(255,255,255,0.5), stop: 1 rgba(255,255,255,0.2));padding:5px;padding-left:10px;border-radius:14px;margin-left:5px}
    QPushButton[loginButton="true"]{background:qlineargradient(x1: 1, x2: 0, stop: 0 rgba(255,255,255,0.5), stop: 1 rgba(255,255,255,0.2));padding:5px;padding-left:10px;border-radius:14px;margin-left:5px;color:#444;margin-right:30px}
    
    QLabel[TimeLeft3]{
        color: #c42b1c;
    }
    QLabel[TimeLeft2]{
        color: #9d5d00;
    }
    QLabel[TimeLeft1]{
        color: #9d5d00;
    }
    QLabel[TimeLeft0]{
        color: #0f7b0f;
    }
    QLabel[TimeLeft4]{
        color: #666;
    }
    QLabel[status0]{background:black;color:white;border-radius:8px;font-family:verdana;margin:5px;padding:5px;font-size:11px;}
    QLabel[status1]{background:#5b2efc;color:white;border-radius:8px;font-family:verdana;margin:5px;padding:5px;font-size:11px;}
    QLabel[status2]{background:#0f7b0f;color:white;border-radius:8px;font-family:verdana;margin:5px;padding:5px;font-size:11px;}
    QLabel[status3]{background:#c42b1c;color:white;border-radius:8px;font-family:verdana;margin:5px;padding:5px;font-size:11px;}
    
    QTableWidget{border:0px solid}
    QTableWidget::item{border-top:1px solid #eee;font-family:verdana;}
    QTableView::item:selected {background-color: #7b4eff;color:white;}
    QHeaderView::section{background:white;border:none;border-right:1px solid #eee;margin-bottom:5px;}

    QTableCornerButton::section {background-color:transparent;}
    
    QLabel[calendarLabel]{font-weight:bold;font-family:arial;color:#5b2efc}
    
    QHeaderView::section{padding-bottom:5px;margin-bottom:0px;border-bottom:1px solid #ddd}
    QTableWidget[calendarTable]::item{border:none;border-right:1px solid #eee;border-bottom:1px solid #f2f2f2}
    
    QLabel[taskCalendarItem]{background:#5b2efc;color:white;border-radius:15px;padding:2px;margin:1px;font-family:arial;font-size:12px;}
    
    QPushButton[weekArrow]{color:black;border-radius:11px;font-size:12px;}
    QPushButton[weekArrow]:pressed{margin-right:1px;}
    
    QPushButton[signupFormButton]{color:gray;font-size:12px;text-align:left;margin-left:15px;margin-top:5px;}
"""

dark_style_sheet = """
    TitleBarButton {
     qproperty-normalColor: white;
     qproperty-hoverColor: white;
     qproperty-hoverBackgroundColor: #444;
    }
    QWidget{background:transparent}
    *[MainWindow="true"]{background-color: qlineargradient(y1: 0, y2: 1, stop: 0 #202020, stop: 1 #1b1b1b)}
    QMainWindow[loginForm="true"]{background:qlineargradient(y1: 0, y2: 1, stop: 0 #202020, stop: 1 rgba(27, 27, 27, 50));border-bottom-left-radius:5px}
   
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
    
    QScrollBar:horizontal{background-color: rgb(12,12,12);height: 10px;margin:2px;border: 1px transparent #2A2929;border-radius: 3px;}
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
    QLabel[username_title]{padding:0;font-family:verdana;font-size:12px;color:rgba(255,255,255,170);margin-left:10px;}
    QLabel[username_title]:hover{color:rgba(255,255,255,255)}
    QWidget[searchBar="true"]{border:1px solid #333;margin-top:5px;border-radius:17px}
    QWidget[searchBar="true"][focused="true"]{border:1px solid #C8C8C8;}
    
    QLineEdit{color:white;font-family:verdana;font-size:14px;margin-right:30px}
    
    QPushButton[settings="true"]{color:white;font-size:16px;border:1px solid #444;border-radius:10px;background:#252525;padding:12px}
    
    QLineEdit[loginButton="true"]{background:qlineargradient(x1: 1, x2: 0, stop: 0 rgba(255,255,255,0.2), stop: 1 rgba(255,255,255,0.1));padding:5px;padding-left:10px;border-radius:14px;margin-left:5px}
    QPushButton[loginButton="true"]{background:qlineargradient(x1: 1, x2: 0, stop: 0 rgba(255,255,255,0.2), stop: 1 rgba(255,255,255,0.1));padding:5px;padding-left:10px;border-radius:14px;margin-left:5px;color:#EEE;margin-right:30px}
    
    QLabel[TimeLeft3]{
        color: #ff99a4;
    }
    QLabel[TimeLeft2]{
        color: #fce100;
    }
    QLabel[TimeLeft1]{
        color: #fce100;
    }
    QLabel[TimeLeft0]{
        color: #6ccb5f;
    }
    QLabel[TimeLeft4]{
        color: #888;
    }
    QLabel[status0]{background:#EEE;color:black;border-radius:8px;font-family:verdana;margin:5px;padding:5px;font-size:11px;}
    QLabel[status1]{background:#916cee;color:white;border-radius:8px;font-family:verdana;margin:5px;padding:5px;font-size:11px;}
    QLabel[status2]{background:#6ccb5f;color:white;border-radius:8px;font-family:verdana;margin:5px;padding:5px;font-size:11px;}
    QLabel[status3]{background:#ff99a4;color:white;border-radius:8px;font-family:verdana;margin:5px;padding:5px;font-size:11px;}
    
    
    QTableWidget{border:0px solid}
    QTableWidget::item{border-top:1px solid #333;font-family:verdana;color:white;}
    QTableView::item:selected {background-color: #5b2efc;color:white;}
    QHeaderView::section{background:transparent;border:none;border-right:1px solid #333;margin-bottom:5px;color:white;}
    QTableCornerButton::section {background-color:transparent;}
    
    QLabel[calendarLabel]{font-weight:bold;font-family:arial;color:#916cee}
    
    QHeaderView::section{padding-bottom:5px;margin-bottom:0px;border-bottom:1px solid #333}
    QTableWidget[calendarTable]::item{border:none;border-right:1px solid #333;border-bottom:1px solid #444}
    
    QLabel[taskCalendarItem]{background:#916cee;color:white;border-radius:15px;padding:2px;margin:1px;font-family:arial;font-size:12px;}
    
    QPushButton[weekArrow]{color:white;border-radius:11px;font-size:12px;}
    QPushButton[weekArrow]:pressed{margin-right:1px;}
    
    QPushButton[signupFormButton]{color:gray;font-size:12px;text-align:left;margin-left:15px;margin-top:5px;}
"""