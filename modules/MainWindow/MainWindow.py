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
            self.ui.radioButton_daytime,
            self.ui.radioButton_extramural,
            self.ui.radioButton_extramural1,
            self.ui.radioButton_remotely,
            self.ui.radioButton_daytime1]

        # set pandas table as widget
        self.pandas_model = DataFrameModel()
        self.ui.tableWidget.setModel(self.pandas_model)

        # dialog box
        self.__db_not_exist_message_box = MessageBox()
        # message box
        self.__msg_box = QtWidgets.QMessageBox(self)

        # init mongoDB manager
        self.__init_mongo_manager(config_path)

        # push buttons connects
        self.ui.pushButton.clicked.connect(self.add_educational_program)
        self.ui.pushButton_2.clicked.connect(self.find_educational_program)


    def __reset_all_add_fields(self):
        # uncheck radio buttons
        for button in self.radiobutton_group:
            button.setCheckable(False)
            button.setCheckable(True)

        # clear add line edits
        self.ui.lineEdit_specialty.clear()
        self.ui.lineEdit_set_year.clear()
        self.ui.lineEdit_qualification.clear()
        self.ui.lineEdit_training_period.clear()
        self.ui.lineEdit_registration_number.clear()


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
            self.__reset_all_add_fields()
            # show msg box
            self.__show_add_document_msgbox()

        else:
            self.__show_empty_field_msgbox()


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
            self.__show_empty_field_msgbox()

        # place data in table
        if type(result) == pd.DataFrame:
            # rename columns and set in table
            result = result.rename(columns={
                "??????????????????????????": "speciality",
                "rec_year": "?????? ????????????",
                "qualification": "????????????????????????",
                "studying_period": "???????????? ????????????????",
                "reg_num": "?????????? ??????????????????????",
                "education_type": "?????????? ?????????????????? ??????????????????????"
            })
            self.pandas_model.setDataFrame(result)
        elif result == 'Not found':
            self.__show_not_found_msgbox()


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


    def __show_add_document_msgbox(self):
        self.__msg_box.setWindowTitle('???????????????????? ?????????????? ????????????')
        self.__msg_box.setText("???????????????? ?????????????? ????????.")
        self.__msg_box.show()

    def __show_empty_field_msgbox(self):
        self.__msg_box.setWindowTitle('???????????? ????????')
        self.__msg_box.setText("???? ?????????????????? ???????? ???? ??????????.")
        self.__msg_box.show()

    def __show_not_found_msgbox(self):
        self.__msg_box.setWindowTitle('???? ??????????????')
        self.__msg_box.setText("?????????????? ???????????????? ???? ????????????.")
        self.__msg_box.show()




