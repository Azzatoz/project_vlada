from PyQt5 import QtCore, QtWidgets
from functools import partial
import os


class UiDocumentWindow(QtWidgets.QDialog):
    def __init__(self):
        super(UiDocumentWindow, self).__init__()

        self.paths_txt = "C:\\Users\\user\\PycharmProjects\\project_vlada\\paths.txt"
        self.paths_dict = self.load_paths()

        self.setObjectName("Dialog")
        self.resize(1200, 800)

        self.path_sale_word_line_edit = QtWidgets.QLineEdit(self)
        self.path_sale_word_line_edit.setGeometry(QtCore.QRect(40, 80, 381, 41))
        self.path_sale_word_line_edit.setObjectName("path_sale_word_line_edit")
        self.path_sale_word_line_edit.setReadOnly(True)
        self.path_sale_excel_line_edit = QtWidgets.QLineEdit(self)
        self.path_sale_excel_line_edit.setGeometry(QtCore.QRect(650, 80, 381, 41))
        self.path_sale_excel_line_edit.setObjectName("path_sale_excel_line_edit")
        self.path_sale_excel_line_edit.setReadOnly(True)
        self.path_write_downs_word_line_edit = QtWidgets.QLineEdit(self)
        self.path_write_downs_word_line_edit.setGeometry(QtCore.QRect(40, 190, 381, 41))
        self.path_write_downs_word_line_edit.setObjectName("path_write_downs_word_line_edit")
        self.path_write_downs_word_line_edit.setReadOnly(True)
        self.path_write_downs_excel_line_edit = QtWidgets.QLineEdit(self)
        self.path_write_downs_excel_line_edit.setGeometry(QtCore.QRect(650, 190, 381, 41))
        self.path_write_downs_excel_line_edit.setObjectName("path_write_downs_excel_line_edit")
        self.path_write_downs_excel_line_edit.setReadOnly(True)
        self.path_moving_word_line_edit = QtWidgets.QLineEdit(self)
        self.path_moving_word_line_edit.setGeometry(QtCore.QRect(40, 300, 381, 41))
        self.path_moving_word_line_edit.setObjectName("path_moving_word_line_edit")
        self.path_moving_word_line_edit.setReadOnly(True)
        self.path_moving_excel_line_edit = QtWidgets.QLineEdit(self)
        self.path_moving_excel_line_edit.setGeometry(QtCore.QRect(650, 300, 381, 41))
        self.path_moving_excel_line_edit.setObjectName("path_moving_excel_line_edit")
        self.path_moving_excel_line_edit.setReadOnly(True)
        self.path_acceptance_word_line_edit = QtWidgets.QLineEdit(self)
        self.path_acceptance_word_line_edit.setGeometry(QtCore.QRect(40, 410, 381, 41))
        self.path_acceptance_word_line_edit.setObjectName("path_acceptance_word_line_edit")
        self.path_acceptance_word_line_edit.setReadOnly(True)
        self.path_acceptance_excel_line_edit = QtWidgets.QLineEdit(self)
        self.path_acceptance_excel_line_edit.setGeometry(QtCore.QRect(650, 410, 381, 41))
        self.path_acceptance_excel_line_edit.setObjectName("path_acceptance_excel_line_edit")
        self.path_acceptance_excel_line_edit.setReadOnly(True)
        self.template_sale_word = QtWidgets.QPushButton(self)
        self.template_sale_word.setGeometry(QtCore.QRect(420, 80, 141, 41))
        self.template_sale_word.setObjectName("template_sale_word")
        self.template_sale_excel = QtWidgets.QPushButton(self)
        self.template_sale_excel.setGeometry(QtCore.QRect(1030, 80, 141, 41))
        self.template_sale_excel.setObjectName("template_sale_excel")
        self.template_acceptance_word = QtWidgets.QPushButton(self)
        self.template_acceptance_word.setGeometry(QtCore.QRect(420, 410, 141, 41))
        self.template_acceptance_word.setObjectName("template_acceptance_word")
        self.template_write_downs_word = QtWidgets.QPushButton(self)
        self.template_write_downs_word.setGeometry(QtCore.QRect(420, 190, 141, 41))
        self.template_write_downs_word.setObjectName("template_write_downs_word")
        self.template_moving_excel = QtWidgets.QPushButton(self)
        self.template_moving_excel.setGeometry(QtCore.QRect(1030, 300, 141, 41))
        self.template_moving_excel.setObjectName("template_moving_excel")
        self.template_acceptance_excel = QtWidgets.QPushButton(self)
        self.template_acceptance_excel.setGeometry(QtCore.QRect(1030, 410, 141, 41))
        self.template_acceptance_excel.setObjectName("template_acceptance_excel")
        self.template_moving_word = QtWidgets.QPushButton(self)
        self.template_moving_word.setGeometry(QtCore.QRect(420, 300, 141, 41))
        self.template_moving_word.setObjectName("template_moving_word")
        self.template_write_downs_excel = QtWidgets.QPushButton(self)
        self.template_write_downs_excel.setGeometry(QtCore.QRect(1030, 190, 141, 41))
        self.template_write_downs_excel.setObjectName("template_write_downs_excel")
        self.save_button = QtWidgets.QPushButton(self)
        self.save_button.setGeometry(QtCore.QRect(450, 590, 301, 41))
        self.save_button.setObjectName("save_button")

        self.re_translate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

        buttons = [self.template_sale_word, self.template_sale_excel, self.template_write_downs_word,
                   self.template_write_downs_excel, self.template_moving_word, self.template_moving_excel,
                   self.template_acceptance_word, self.template_acceptance_excel]
        for index, button in enumerate(buttons):
            button.clicked.connect(lambda clicked_button, i=index: self.open_file_dialog(i))
        self.save_button.clicked.connect(partial(self.save_paths, self.paths_dict))

        self.path_sale_word_line_edit.setText(self.paths_dict.get(0, ""))
        self.path_sale_excel_line_edit.setText(self.paths_dict.get(1, ""))
        self.path_write_downs_word_line_edit.setText(self.paths_dict.get(2, ""))
        self.path_write_downs_excel_line_edit.setText(self.paths_dict.get(3, ""))
        self.path_moving_word_line_edit.setText(self.paths_dict.get(4, ""))
        self.path_moving_excel_line_edit.setText(self.paths_dict.get(5, ""))
        self.path_acceptance_word_line_edit.setText(self.paths_dict.get(6, ""))
        self.path_acceptance_excel_line_edit.setText(self.paths_dict.get(7, ""))

    def re_translate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.template_sale_word.setText(_translate("Dialog", "Путь к файлу Word"))
        self.template_sale_excel.setText(_translate("Dialog", "Путь к файлу Excel"))
        self.template_acceptance_word.setText(_translate("Dialog", "Путь к файлу Word"))
        self.template_write_downs_word.setText(_translate("Dialog", "Путь к файлу Word"))
        self.template_moving_excel.setText(_translate("Dialog", "Путь к файлу Excel"))
        self.template_acceptance_excel.setText(_translate("Dialog", "Путь к файлу Excel"))
        self.template_moving_word.setText(_translate("Dialog", "Путь к файлу Word"))
        self.template_write_downs_excel.setText(_translate("Dialog", "Путь к файлу Excel"))
        self.save_button.setText(_translate("Dialog", "Сохранить"))

    def load_paths(self):
        paths_dict = {}
        if os.path.exists(self.paths_txt):
            with open(self.paths_txt, 'r') as file:
                for index, line in enumerate(file):
                    line = line.strip()
                    if line:
                        paths_dict[index] = line
        return paths_dict

    def open_file_dialog(self, index_clicked_button):
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выбрать файл", "",
                                                             "All Files (*);;Word Files (*.docx);;"
                                                             "Excel Files (*.xlsx)", options=options)

        if file_path:
            self.paths_dict[index_clicked_button] = file_path

            if index_clicked_button == 0:
                self.path_sale_word_line_edit.setText(file_path)
            elif index_clicked_button == 1:
                self.path_sale_excel_line_edit.setText(file_path)
            elif index_clicked_button == 2:
                self.path_write_downs_word_line_edit.setText(file_path)
            elif index_clicked_button == 3:
                self.path_write_downs_excel_line_edit.setText(file_path)
            elif index_clicked_button == 4:
                self.path_moving_word_line_edit.setText(file_path)
            elif index_clicked_button == 5:
                self.path_moving_excel_line_edit.setText(file_path)
            elif index_clicked_button == 6:
                self.path_acceptance_word_line_edit.setText(file_path)
            elif index_clicked_button == 7:
                self.path_acceptance_excel_line_edit.setText(file_path)

        return self.paths_dict

    def save_paths(self, paths_dict):
        existing_paths = self.load_paths()
        existing_paths.update(paths_dict)
        with open(self.paths_txt, 'w') as file:
            for filename, path in existing_paths.items():
                file.write(f"{path.replace('/', '\\\\')}\n")
        self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = UiDocumentWindow()
    ui.show()
    sys.exit(app.exec_())
