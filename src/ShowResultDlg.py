# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QDialog, QApplication, QHBoxLayout
from Ui_ShowResultDlg import Ui_ShowResultDlg
from PyQt5 import Qt
from widgetparam import WidgetParam
from data_handling.material import *
import sys
import pickle
from PyQt5.QtGui import QIcon


class ShowResultDlg(QDialog, Ui_ShowResultDlg):
    def __init__(self, material, parent=None):
        super(ShowResultDlg, self).__init__(parent)
        self.setupUi(self)
        self.material = material
        self.material_name = material.name
        self.spectrum_name = material.spectrum
        self.data_to_uis()
        self.setWindowIcon(QIcon('fds.ico'))
        # self.setWindowFlags(Qt.WindowMinimizeButtonHint)c1

    def data_to_uis(self):
        self.Parameters.data_to_ui(self.material.activation_data.get_spectra_data(self.spectrum_name)
                                   ,self.material_name,self.spectrum_name,self.material)
        self.PathwayAnalysis.data_to_ui(self.material.activation_data.get_spectra_data(self.spectrum_name),self.material)
        self.PrimaryNuclides.data_to_ui(self.material.activation_data.get_spectra_data(self.spectrum_name))
        self.TransmutationGraph.data_to_ui(self.material.activation_data.get_spectra_data(self.spectrum_name))

#for testing
if __name__ is '__main__':
    app = QApplication(sys.argv)
    mat = None
    with open("C:/Users/ysp/Desktop/QT_practice/TestActivation.data", 'rb') as indata:
        mat = pickle.load(indata)
    showdlg = ShowResultDlg(mat, 1)
    showdlg.show()
    sys.exit(app.exec_())