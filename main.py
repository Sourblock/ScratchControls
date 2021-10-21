#from modules.scraper import scrape
from PyQt5 import uic
from PyQt5 import uic, QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QModelIndex, QTimer
import pandas as pd
import numpy as np
import sys
import os 
import time
from encoding_and_decoding import encode, decode
from scratchman import ScratchMan
from pathlib import Path
from datetime import datetime
import requests



class WorkerThread(QtCore.QThread):
    updateSignal = QtCore.pyqtSignal()
    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.parent = parent

    def run(self):
        while True:
            while self.parent.const_update_check.isChecked() :
                print("Constant update !")
                self.updateSignal.emit()
                time.sleep(10)
            
            time.sleep(0.1)


class SplashWindow(QMainWindow):
    def __init__(self):
        super(SplashWindow, self).__init__()
        file = os.path.join(Path(__file__).resolve().parent, "Screen.ui")
        uic.loadUi(file, self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.counter = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.forward)
        self.timer.start(20)

    def forward(self) :
        self.counter += 1
        self.progressBar.setValue(self.counter)
        if self.counter == 100 :
            self.timer.stop()
            self.close()
            time.sleep(0.5)
            self.window = MainWindow()
            self.window.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        file = os.path.join(Path(__file__).resolve().parent, "app.ui")
        uic.loadUi(file, self)
        self.wt = WorkerThread(self)
        self.binit()
        self.wt.start()
        
        

    def binit(self) :
        self.linkevents()
        self.scratch_man = ScratchMan()
        self.can_fill_vars = True
        self.use_def_name = True
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

    def linkevents(self):
        self.login_btn.clicked.connect(self.performLogin)
        self.cloud_vars_btn.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(2))
        self.logout_btn.clicked.connect(self.performLogout)
        self.back_home_btn.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(1))
        self.setvar_save_btn.clicked.connect(self.updateVar)
        self.createvar_save_btn.clicked.connect(self.createVar)
        self.setvar_project_combo.currentIndexChanged.connect(self.refreshVariableCombos)
        self.setvar_var_combo.currentIndexChanged.connect(self.refreshVarValue)
        self.use_def_name_check.toggled.connect(self.useDefVsCusName)
        self.add_user_var_btn.clicked.connect(self.addVarFromUser)
        self.customapi_req_btn.clicked.connect(self.getCusAPIResponse) 
        self.customapi_save_btn_2.clicked.connect(self.saveCusAPIVar) 
        self.customapi_project_combo_2.currentIndexChanged.connect(self.refreshVariableCombosCus)
        self.customapi_var_combo_2.currentIndexChanged.connect(self.refreshVarValueCus)
        self.wt.updateSignal.connect(self.addVarFromUser)

    def saveCusAPIVar(self) :
        project_id = self.projects[self.customapi_project_combo_2.currentText()]
        var_name = self.customapi_var_combo_2.currentText()
        value = encode(self.customapi_value_input_2.text())
        if self.scratch_man.createNewVar(project_id, var_name, value) :
            QMessageBox.about(self, "Information", "Variable updated !")
            self.refreshProjectCombos()
        else :
            QMessageBox.about(self, "Creation error", "Variable not updated !")

    def getCusAPIResponse(self):
        url = self.customapi_url_input.text()
        data = self.getDataFromUrl(url)
        self.customapi_resp_out.setPlainText(str(data))

    def getDataFromUrl(self, url) :
        res = requests.get(url)
        return res.json()

    def addVarFromUser(self) :
        project_id = self.projects[self.user_var_project_combo.currentText()]
        var_coice = self.user_var_name_combo.currentIndex()
        if var_coice == 0 :
            value = self.scratch_man.getFollowersCount()
        elif var_coice == 1 :
            value = self.scratch_man.getFollowingCount()
        elif var_coice == 2 :
            value = self.scratch_man.getLoveCount()
        elif var_coice == 3 :
            value = self.scratch_man.getViewsCount()
        elif var_coice == 4 :
            value = self.scratch_man.getFavoritesCount()
        elif var_coice == 5 :
            value = self.scratch_man.getStatus()
        elif var_coice == 6 :
            value = self.scratch_man.getCountry()
        else:
            value = self.scratch_man.getJoinDate()

        value = encode(str(value))
        if self.use_def_name :
            name = self.user_var_name_combo.currentText()
        else :
            name = self.usercar_custom_name_input.text()

        if self.scratch_man.createNewVar(project_id, name, value) :
            print("Information:", "Variable created !")
            self.refreshProjectCombos()
        else :
            print("Creation error:", "Variable not created !")



    def useDefVsCusName(self) :
        if self.use_def_name_check.isChecked() :
            self.label_9.setEnabled(False)
            self.usercar_custom_name_input.setEnabled(False)
            self.use_def_name = True
        else :
            self.label_9.setEnabled(True)
            self.usercar_custom_name_input.setEnabled(True)
            self.use_def_name = False

    def refreshProjectsCount(self):
        self.projects_btn.setText(str(len(self.projects)))

    def refreshFavoritesCount(self):
        count = self.scratch_man.getFavoritesCount()
        self.favorite_btn.setText(str(count))

    def refreshViewsCount(self):
        count = self.scratch_man.getViewsCount()
        self.views_btn.setText(str(count))

    def refreshLoveCount(self) :
        count = self.scratch_man.getLoveCount()
        self.loves_btn.setText(str(count))

    def refreshMessageCount(self) :
        count = self.scratch_man.getMessageCount()
        self.messages_btn.setText(str(count))

    def refreshFollowersCount(self):
        count = self.scratch_man.getFollowersCount()
        self.followers_btn.setText(str(count))

    def refreshFollowingCount(self):
        count = self.scratch_man.getFollowingCount()
        self.following_btn.setText(str(count))

    def createVar(self) :
        project_id = self.projects[self.createvar_project_combo.currentText()]
        var_name = self.createvar_name_input.text()
        value = encode(self.createvar_value_input.text())
        if self.scratch_man.createNewVar(project_id, var_name, value) :
            QMessageBox.about(self, "Information", "Variable created !")
            self.refreshProjectCombos()
        else :
            QMessageBox.about(self, "Creation error", "Variable not created !")

    def updateVar(self) :
        project_id = self.projects[self.setvar_project_combo.currentText()]
        var_name = self.setvar_var_combo.currentText()
        value = encode(self.setvar_value_input.text())
        if self.scratch_man.setCloudVar(project_id, var_name, value) :
            QMessageBox.about(self, "Information", "Variable value updated !")
            self.refreshProjectCombos()
        else :
            QMessageBox.about(self, "Update error", "Error accured!")
    
    def performLogin(self) :
        username = self.username_input.text()
        password = self.password_input.text()

        if self.scratch_man.login(username, password) :
            self.refreshProjectCombos()
            self.refreshMessageCount()
            self.refreshFollowersCount()
            self.refreshFollowingCount()
            self.refreshLoveCount()
            self.refreshViewsCount()
            self.refreshFavoritesCount()
            self.refreshProjectsCount()
            self.username_input.clear()
            self.password_input.clear()
            self.stackedWidget.setCurrentIndex(1)
        else :
            QMessageBox.about(self, "Login error", "Please check username, password")

    def refreshVariableCombosCus(self) :
        if not self.can_fill_vars :
            return

        self.customapi_var_combo_2.clear()
        project_title = self.customapi_project_combo_2.currentText()
        self.vars = self.scratch_man.getAllVars(self.projects[project_title])
        for var in self.vars :
            self.customapi_var_combo_2.addItem(var)

        self.refreshVarValueCus()

    def refreshVarValueCus(self) :
        project_id = self.projects[self.createvar_project_combo.currentText()]
        var_name2 = self.customapi_var_combo_2.currentText()
        try :
            self.customapi_value_input_2.setText(decode(self.scratch_man.getVarValue(project_id, var_name2)[0]))
        except Exception as e:
            print(e)
            self.customapi_value_input_2.clear()

    def refreshVariableCombos(self) :
        if not self.can_fill_vars :
            return

        self.setvar_var_combo.clear()
        project_title = self.setvar_project_combo.currentText()
        self.vars = self.scratch_man.getAllVars(self.projects[project_title])
        for var in self.vars :
            self.setvar_var_combo.addItem(var)

        self.refreshVarValue()

    def refreshVarValue(self) :
        project_id = self.projects[self.createvar_project_combo.currentText()]
        var_name = self.setvar_var_combo.currentText()
        try :
            self.setvar_value_input.setText(decode(self.scratch_man.getVarValue(project_id, var_name)[0]))
        except Exception as e:
            print(e)
            self.setvar_value_input.clear()

    def refreshProjectCombos(self) :
        self.can_fill_vars = False
        self.setvar_project_combo.clear()
        self.createvar_project_combo.clear()
        self.user_var_project_combo.clear()
        self.customapi_project_combo_2.clear()
        self.projects = self.scratch_man.getAllProjects()
        for title in self.projects.keys() :
            self.setvar_project_combo.addItem(title)
            self.createvar_project_combo.addItem(title)
            self.user_var_project_combo.addItem(title)
            self.customapi_project_combo_2.addItem(title)
        self.can_fill_vars = True
        self.refreshVariableCombos()
        self.refreshVariableCombosCus()

    def performLogout(self) :
        self.scratch_man.logout()
        self.stackedWidget.setCurrentIndex(0)



if __name__ == "__main__":
    app = QApplication([])

    splash = SplashWindow()
    splash.show()
    sys.exit(app.exec())    