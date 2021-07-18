import pandas as pd

from modules.interface.MainWindowInterface import Ui_Dialog
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtGui

from modules.logic.MongoDBManager.MongoManager import MongoManager
from modules.DBDoesNotExistMessageBox.DBDoesNotExistMessageBox import MessageBox
from modules.logic.PandasWidgetModel.PandasWidgetModel import DataFrameModel


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, config_path: str):
        # init interface
        super(MainWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # add radio buttons in group
        self.radiobutton_group = [
            self.ui.radioButton_extramural,
            self.ui.radioButton_daytime,
            self.ui.radioButton_daytime1,
            self.ui.radioButton_remotely,
            self.ui.radioButton_extramural1]

        # set pandas table as widget
        self.pandas_model = DataFrameModel()
        self.ui.tableWidget.setModel(self.pandas_model)

        # dialog box
        self.__db_not_exist_message_box = MessageBox()
        # error message
        self.err_msg = QtWidgets.QErrorMessage()

        # init mongoDB manager
        self.__init_mongo_manager(config_path)

        # push buttons connects
        self.ui.pushButton.clicked.connect(self.add_educational_program)
        self.ui.pushButton_2.clicked.connect(self.find_educational_program)



    def add_educational_program(self):
        # get selected type of education
        education_type = ''
        for i in self.radiobutton_group:
            if i.isChecked():
                education_type = i.text()

        # form document and insert in mongoDB
        doc = {
            "speciality": self.ui.lineEdit_specialty.text().strip(),
            "rec_year": self.ui.lineEdit_set_year.text().strip(),
            "qualification": self.ui.lineEdit_qualification.text().strip(),
            "studying_period": self.ui.lineEdit_training_period.text().strip(),
            "reg_num": self.ui.lineEdit_registration_number.text().strip(),
            "education_type": education_type.strip()
        }

        # check fields on completeness
        is_completeness = True
        for _, i in doc.items():
            if len(i) == 0:
                is_completeness = False
                break

        # add document if fields is completeness, else show error message
        if is_completeness:
            self.__mongo_manager.add_document(doc)
        else:
            self.err_msg.showMessage("Не заполненно одно из полей.")



    def find_educational_program(self):
        query = {
            "speciality": self.ui.lineEdit_specialty_Search.text(),
            "rec_year": self.ui.lineEdit__set_year_search.text()
        }

        # check fields on completeness
        is_completeness = True
        for _, i in query.items():
            if len(i) == 0:
                is_completeness = False
                break

        # find document if fields is completeness, else show error message
        result = None
        if is_completeness:
            result = self.__mongo_manager.find(query)
        else:
            self.err_msg.showMessage("Не заполненно одно из полей.")


        # place data in table
        if result is not None:
            # rename columns and set in table
            result = result.rename(columns={
                "Специальность": "speciality",
                "rec_year": "Год набора",
                "qualification": "Квалификация",
                "studying_period": "Период обучения",
                "reg_num": "Номер регистрации",
                "education_type": "Форма получения образования"
            })
            self.pandas_model.setDataFrame(result)
        elif result == 'Not found':
            self.err_msg.showMessage("Учебные планы не найдены.")


    def __init_mongo_manager(self, config_path: str):
        # create manager
        self.__mongo_manager = MongoManager(dbconfig_path=config_path)

        # check if database and collection exist
        if not self.__mongo_manager.db_is_exist or not self.__mongo_manager.col_is_exist:
            clicked_button = self.__db_not_exist_message_box.exec()
            if clicked_button == QMessageBox.Close:
                QtCore.QTimer.singleShot(0, self.close)
            elif clicked_button == QMessageBox.Ok:
                self.__mongo_manager.create_database_and_collection()







