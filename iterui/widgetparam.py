# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShowResult.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QWidget,QDialog,QApplication, QHBoxLayout, QVBoxLayout
from Ui_WidgetParam import Ui_WidgetParam
from data_handling.activationdata import OneSpectrumActivationData
from PyQt5.QtWidgets import QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class WidgetParam(QWidget, Ui_WidgetParam):
    param_names = ['total_activity(Bq)',
                   'total_heat(kW)',
                   'dose_rate(Sv/kg)',
                   'ingestion_dose(Sv/kg)']
    cooling_times = [1, 1.0e5, 1.0e6, 1.0e7, 1.0e8, 1.0e9, 1.5e9]

    def __init__(self, parent=None):
        super(WidgetParam, self).__init__(parent)
        self.setupUi(self)
        self.act_data = None
        self.initialize_canvas_parameters()
        self.axes = [None, None, None, None]
        self.checkButtons = [self.checkBoxAct, self.checkBoxHeat, self.checkBoxDose, self.checkBoxIng]

    def ui_to_data(self, act_data: OneSpectrumActivationData):
        # show parameters of 6 cooling times
        self.act_data = act_data
        for i in range(0, len(act_data.all_steps_activation_data)):
            one_step_data = act_data.all_steps_activation_data[i]

            for j in range(0, 4):
                val = act_data.all_steps_activation_data[i].parameters[WidgetParam.param_names[j]]
                new_item = QTableWidgetItem('{0}'.format(val))
                self.tableWidgetParams.setItem(i,j+1,new_item)
        # plot data to plot widge
        self.initialize_figs_parameters()

    def initialize_canvas_parameters(self):
        self.figure = Figure(figsize=(8, 6), dpi=100, tight_layout=True)
        self.figure.set_facecolor('#F5F5F5')
        self.figure.subplots_adjust(left=0.08, top=0.92, bottom=0.1)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout(self.framePlot)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas,self.framePlot)
        self.horizontalLayoutBelowPlot.addWidget(self.toolbar)

    def initialize_figs_parameters(self):
        self.canvas.figure.clf()
        checked_button_num = 0
        for i in range(0,4):
            if self.checkButtons[i].isChecked():
                checked_button_num += 1
        if checked_button_num is 0:
            return
        idx = 1
        if checked_button_num % 2 is 0:
            totalnum = checked_button_num * 50 + 20
        else:
            totalnum = checked_button_num*100+10
        for i in range(0, 4):
            if self.checkButtons[i].isChecked():
                self.axes[i] = self.figure.add_subplot(totalnum + idx)
                self.draw_axe(i)
                idx += 1
        self.canvas.draw()

    @pyqtSlot()
    def on_checkBoxAct_clicked(self):
        self.update()
        self.initialize_figs_parameters()

    @pyqtSlot()
    def on_checkBoxHeat_clicked(self):
        self.update()
        self.initialize_figs_parameters()

    @pyqtSlot()
    def on_checkBoxDose_clicked(self):
        self.update()
        self.initialize_figs_parameters()

    @pyqtSlot()
    def on_checkBoxIng_clicked(self):
        self.update()
        self.initialize_figs_parameters()

    def draw_axe(self, idx):
        assert(self.checkButtons[idx].isChecked())
        values = []
        for i in range(0, len(self.act_data.all_steps_activation_data)):
            one_step_data = self.act_data.all_steps_activation_data[i]
            values.append(one_step_data.parameters[WidgetParam.param_names[idx]])
        assert(self.axes[idx] is not None)
        cur_axe = self.axes[idx]
        Font = {'family': 'Tahoma',
                'weight': 'bold', 'size': 10}
        # Abscissa
        cur_axe.set_xlim([1, 2e9])
        cur_axe.set_xticks(WidgetParam.cooling_times)
        cur_axe.set_xticklabels(WidgetParam.cooling_times, fontdict=Font)
        cur_axe.set_xlabel("Cooling time (s)", fontdict=Font)
        cur_axe.set_ylim([min(values), max(values)*1.5])
        # Ordinate
        cur_axe.set_ylabel(WidgetParam.param_names[idx], fontdict=Font)
        cur_axe.grid(True)  # Grid On
        cur_axe.plot(WidgetParam.cooling_times, values)
        cur_axe.set_xscale('log')
        cur_axe.set_yscale('log')

