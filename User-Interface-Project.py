import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel,  QPushButton, 
    QVBoxLayout, QHBoxLayout, QWidget, QMenuBar, 
    QFileDialog, QTextEdit, QTabWidget, 
    QTabBar, QStatusBar
)

from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtCore import Qt

import os # Helpful in extracting file name

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Graphical User Interface')
        self.setMinimumSize(450, 400)


        menu = self.menuBar()

        file = menu.addMenu('File')

        new_action = QAction('New File', self)
        Open_action = QAction('Open File', self)
        Save_action = QAction('Save', self)
        Save_as_action = QAction('Save as', self)

        ###Now we need to add actions to the file menu

        file.addAction(new_action)
        file.addAction(Open_action)
        file.addAction(Save_action)
        file.addAction(Save_as_action)

        # Creating Home menu 


        Home = menu.addMenu('Home')
        action_1 = QAction('Font', self)
        action_2 = QAction('Cut', self)
        action_3 = QAction('Copy', self)
        action_4 = QAction('Paste', self)


        Home.addAction(action_1)
        Home.addAction(action_2)
        Home.addAction(action_3)
        Home.addAction(action_4)


        ## Create Edit Button on MenuBar

        Edit = menu.addMenu('Edit')

        cut_action  = QAction('Cut', self)

        copy_action = QAction('Copy', self)

        paste_action = QAction('Paste', self)


        Edit.addAction(cut_action)
        Edit.addAction(copy_action)
        Edit.addAction(paste_action)
        #Edit.addAction()

        help = menu.addMenu('Help')


        help_action = QAction('Help ?', self)
        contact_action = QAction('Contact Support', self)
        feedback_action = QAction('Feedback Column', self)

        help.addAction(help_action)
        help.addAction(contact_action)
        help.addAction(feedback_action)
        #help.addAction()



        #### Now we have created all the Menu Options , we should now connect it to our PC to open files or save files

        new_action.triggered.connect(self.new_file)
        Open_action.triggered.connect(self.opening_file)
        Save_action.triggered.connect(self.save_file)
        Save_as_action.triggered.connect(self.Save_as_file)


        #action_1.triggered.connect(self.save_file)
        #action_2.triggered.connect(self.save_file)
        #action_3.triggered.connect(self.save_file)
        #action_4.triggered.connect(self.save_file)


        #cut_action.triggered.connect(self.cut_file)
        #copy_action.triggered.connect(self.copy_file)
        #paste_action.triggered.connect(self.paste_file)

        '''
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout()

        

        close_button = QPushButton('Close', self)
        layout.addWidget(close_button, alignment= Qt.AlignmentFlag.AlignCenter)

        close_button.clicked.connect(self.close)


        central_widget.setLayout(layout)'''
        # Set the custom QMenuBar instance as the menu bar of the main window
        self.setMenuBar(menu)


        ##Adding the tab widget to Main Window

        self.tab_widget = QTabWidget()

        ## To keep record of file paths for each new tab

        self.file_paths = {}  # dictionary


        self.setCentralWidget(self.tab_widget)

        #status_bar = Q

        self.setStatusBar(QStatusBar(self))



        ### Creating shortcut keys checking -1

        Open_action.setShortcut(QKeySequence("Ctrl+O"))
        Save_action.setShortcut(QKeySequence("Ctrl+S"))



    def new_file(self):
        text_edit = QTextEdit()
        new_tab = self.tab_widget.addTab(text_edit, "Untitled")
        custom = self.create_custom_tab("Untitled", new_tab)

        # Keep track of file path (initially None for new files)
        self.tab_widget.tabBar().setTabButton(new_tab,QTabBar.ButtonPosition.RightSide,custom)


        self.file_paths[new_tab] = None
    def create_custom_tab(self, title, index):
        tab = QWidget()
        layout = QHBoxLayout()
        tab.setLayout(layout)

        label = QLabel()
        layout.addWidget(label)

        ### Creating close button

        close_but = QPushButton("x")
        close_but.setFixedSize(16, 16)
        #close_but.setFixedSize(close_but.sizeHint())
        close_but.setStyleSheet(" QPushButton {border : none; font-style: 'Aptos'} QPushButton:hover {color :'red'; font-weight : bold;} ")
        close_but.clicked.connect(lambda: self.close_tab(index))

        layout.addWidget(close_but)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        return tab
    
    def close_tab(self, index):
        self.tab_widget.removeTab(index)

        if index in self.file_paths:
            del self.file_paths[index]

        
    def opening_file(self):
        dialog = QFileDialog()
        file_path, _ = dialog.getOpenFileName(self, 'Open File', "", ("All Files (*);;Text Files (*.txt);;Python Files (*.py)" ))


        

        if file_path:  # Check if a file was selected
        # Create a new QTextEdit widget
            text_edit = QTextEdit()

        
        # Open the file and load its content into the text edit widget
        with open(file_path, 'r') as file:
            content = file.read()
            text_edit.setPlainText(content)

        
        ## Extracting Just the file name from the path
        file_name = os.path.basename(file_path)

        
        
        # Add the new tab with the file's content
        opening_tab = self.tab_widget.addTab(text_edit, file_name)
        self.tab_widget.setCurrentIndex(opening_tab)


        #open_tab_index = self.tab_widget.addTab(text_edit, file_name)
        custom = self.create_custom_tab(file_name, opening_tab)

        # Keep track of file path (initially None for new files)
        self.tab_widget.tabBar().setTabButton(opening_tab,QTabBar.ButtonPosition.RightSide,custom)

        # Keep track of the file path for this tab
        self.file_paths[opening_tab] = file_path



    def save_file(self):
        # First we need to check whether there is any open tab, if open is this a new file or already saved file

        current_index = self.tab_widget.currentIndex()
        #print(current_index)
        if current_index == -1:## It starts with 0, if it returns -1 then there is no file
            return None
        
        ## Then we check whether that is new or already saved file

        # We now check the file path, if not a saved one no path will be found, SO we have to call save_as functiom it will take care 

        file_path = self.file_paths.get(current_index)## It will search in the file_paths dictionary and return us

        if file_path is None:
            self.Save_as_file()
        
        else: #Save the file in same path
            text_edit = self.tab_widget.widget(current_index)
        

            content = text_edit.toPlainText()
            with open(file_path, 'w') as file:
                file.write(content)



        


    def Save_as_file(self):
        # Get the current tab index
        current_index = self.tab_widget.currentIndex()

        if current_index == -1:
            return
        
        dialog = QFileDialog()
        file_path, _ = dialog.getSaveFileName(self, 'Save File As', "", ("All Files (*);;Text Files (*.txt);;Python Files (*.py)" ))
        if file_path:
            print(f"Saved file as: {file_path}")
            text_edit = self.tab_widget.widget(current_index)
            content = text_edit.toPlainText()
            with open(file_path, 'w') as file:
                file.write(content)

            self.tab_widget.setTabText(current_index, file_path.split('/')[-1])
            self.file_paths[current_index] = file_path
            


        



    

app = QApplication(sys.argv)
w = MainWindow()
w.show()

app.exec()

