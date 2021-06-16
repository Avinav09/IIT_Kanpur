import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, \
    QPushButton, QHBoxLayout, QVBoxLayout, QDialog, QLabel, QComboBox, QMessageBox
from PyQt5.QtGui import QStandardItemModel,QFont
import sqlite3
from PyQt5 import QtCore

# from PyQt5.QtGui import QDoubleValidator,


# class FloatDelegate(QItemDelegate):
#     def __init__(self, parent=None):
#         super().__init__()
#
#     def createEditor(self, parent, option, index):
#         editor = QLineEdit(parent)
#         editor.setValidator(QDoubleValidator())
#         return editor

global tablename

class TableWidget(QTableWidget):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.setStyleSheet('font-size: 15px;')

        # set table dimension
        nRows, nColumns = self.df.shape
        self.setColumnCount(nColumns)
        self.setRowCount(nRows)

        self.setHorizontalHeaderLabels(df.columns)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # self.setItemDelegateForColumn(1, FloatDelegate())

        # data insertion
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.setItem(i, j, QTableWidgetItem(str(self.df.iloc[i, j])))

        # self.cellChanged[int, int].connect(self.updateDF)

    # def updateDF(self, row, column):
    #     text = self.item(row, column).text()
    #     self.df.iloc[row, column] = text



class LoginDialog(QDialog):
    def __init__(self):
        super(LoginDialog, self).__init__()

        self.setFixedWidth(300)
        self.setFixedHeight(120)

        layout = QVBoxLayout()

        self.passinput = QLineEdit()
        self.passinput.setEchoMode(QLineEdit.Password)
        self.passinput.setPlaceholderText("Enter Password.")
        self.password = "covid"
        self.QBtn = QPushButton()
        self.QBtn.setText("Connect")
        self.setWindowTitle('Connect?')
        self.QBtn.clicked.connect(self.login)

        title = QLabel("Connection!")
        font = title.font()
        font.setPointSize(16)
        title.setFont(font)

        layout.addWidget(title)
        layout.addWidget(self.passinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def login(self):
        if(self.passinput.text() == self.password):
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Wrong Password')


class DFEditor(QWidget):

    # def connect_db(self):
    #     connection  = sqlite3.connect(r"C:\Users\avina\OneDrive\Desktop\COVID 19 Data\DB Browser SQLite\COVID19.db")
    #
    #
    #
    # con = sqlite3.connect(r"C:\Users\avina\OneDrive\Desktop\COVID 19 Data\DB Browser SQLite\COVID19.db")
    # cursor = con.cursor()
    # data = pd.read_sql_query("SELECT * from districtwise_data", con)
    # df = pd.DataFrame(data)
    # table_name = table_dialog()
    # table_name = table_dialog.ComboValue
    # print(table_name)
    # if table_name == 'Case Time Series Data':
    #     print(table_name)
    #     data = pd.read_sql_query("SELECT * from case_time_series", con)
    #     df = pd.DataFrame(data)
    #Verify that result of SQL query is stored in the dataframe
    # print(df.head())

    def __init__(self):
        super().__init__()
        self.resize(1800, 1000)

        mainLayout = QVBoxLayout()
        self.setFixedWidth(1500)
        self.setFixedHeight(800)

#########################################################################################################
        global tablename
        print("TableName : " + tablename)
        self.con = sqlite3.connect(r"C:\Users\avina\OneDrive\Desktop\COVID 19 Data\DB Browser SQLite\COVID19.db")
        self.cursor = self.con.cursor()
        self.data = pd.read_sql_query("SELECT * from " + tablename, self.con)
        # if tablename == 'District-Wise Table':
        #     self.data = pd.read_sql_query("SELECT * from districtwise_data", self.con)
        #     print(self.data)
        # # elif self.table_name.tables.currentText()== 'District-Wise Table':
        # #     self.data = pd.read_sql_query("SELECT * from districtwise_data", self.con)
        # # elif self.table_name.tables.currentText()== 'State-Wise Table':
        # #     self.data = pd.read_sql_query("SELECT * from statewise_data", self.con)
        # # else:
        # #     self.data = pd.read_sql_query("SELECT * from ICMR_test_report", self.con)


        self.df = pd.DataFrame(self.data)
        self.table_name = table_dialog()

#######################################################################################################################

        self.table = TableWidget(self.df)
        mainLayout.addWidget(self.table)

        button_print = QPushButton('Display DF')
        button_print.setStyleSheet('font-size: 15px')
        button_print.clicked.connect(self.print_DF_Values)
        mainLayout.addWidget(button_print)

        button_export = QPushButton('Export to CSV file')
        button_export.setStyleSheet('font-size: 15px')
        button_export.clicked.connect(self.export_to_csv)
        mainLayout.addWidget(button_export)

        self.setLayout(mainLayout)

    def print_DF_Values(self):
        print(self.table.df)

    def export_to_csv(self):
        self.table.df.to_csv('Data export.csv', index=False)
        print('CSV file exported.')




class table_dialog(QDialog):
    def __init__(self):
        super(table_dialog, self).__init__()

        self.setFixedWidth(300)
        self.setFixedHeight(120)

        mainlayout = QHBoxLayout()
        mainlayout.addStretch(1)

        self.model = QStandardItemModel()

        self.tables = QComboBox(self)
        self.tables.setFixedSize(250,40)
        self.tables.setFont(QFont("",12))
        self.tables.setModel(self.model)

        self.tables.addItem('case_time_series')
        self.tables.addItem('districtwise_data')
        self.tables.addItem('statewise_data')
        self.tables.addItem('ICMR_test_report')



        mainlayout.addWidget(self.tables, alignment=QtCore.Qt.AlignTop)
        self.setWindowTitle("COVID19 Database Tables")

        #create a button
        combo_button = QPushButton("Select Table")
        combo_button.setStyleSheet('font-size: 15px')
        combo_button.clicked.connect(self.ComboValue)
        mainlayout.addWidget(combo_button, alignment=QtCore.Qt.AlignBottom)

        self.setLayout(mainlayout)
        print(self.ComboValue() + '121')
    def ComboValue(self):
        global  tablename
        self.combovalue = str(self.tables.currentText())
        tablename = str(self.tables.currentText())
        print(self.combovalue)
        self.accept()
        return self.combovalue










if __name__ == '__main__':
    app = QApplication(sys.argv)
    passdlg = LoginDialog()
    tabledlg = table_dialog()

    if (passdlg.exec_() == QDialog.Accepted):
        tabledlg.show()

        if (tabledlg.exec_() == QDialog.Accepted):

            demo = DFEditor()
            demo.show()

    sys.exit(app.exec_())