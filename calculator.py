#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import csv
import io
from PyQt5 import QtCore, Qt, uic, QtWidgets


class CalculatorWindow(QtWidgets.QWidget):

    def __init__(self):
        super(CalculatorWindow, self).__init__()
        uic.loadUi("calculator.ui", self)

        self.is_last_operation_calc = False

        # list of buttons defined in the .ui-file
        self.buttons = [
            self.button_0,
            self.button_1, self.button_2, self.button_3,
            self.button_4, self.button_5, self.button_6,
            self.button_7, self.button_8, self.button_9,
            self.button_plus, self.button_minus, self.button_multiply, self.button_divide,
            self.button_equals, self.button_clear, self.button_delete
        ]

        # list of keys corresponding to the defined buttons
        self.keys = {
            "0": 48,
            "1": 49, "2": 50, "3": 51,
            "4": 52, "5": 53, "6": 54,
            "7": 55, "8": 56, "9": 57,
            "plus": 43, "minus": 45, "multiply": 42, "divide": 47,
            "equals": 61, "clear": 16777223, "delete": 16777219
        }

        # make input field read-only to prevent unwanted input
        self.input.setReadOnly(True)

        self.connect_buttons()

    # connects the defined push buttons from the layout to the clicked signal
    def connect_buttons(self):
        for button in self.buttons:
            button.clicked.connect(self.button_click)

    # decorator function that logs clicks on ui push buttons
    def click_log():
        def dec(func):
            def inner_func(self):
                self.log_csv(["Button clicked", str(self.sender().objectName()), self.timestamp()])
                func(self)
            return inner_func
        return dec

    # decorator function that logs presses on keyboard keys
    def key_log():
        def dec(func):
            def inner_func(self, event):
                self.log_csv(["Key pressed", str(event.key()), self.timestamp()])
                func(self, event)
            return inner_func
        return dec

    # decorator function that logs calculations to be done after evaluate input is pressed
    def calc_log():
        def dec(func):
            def inner_func(self, calc_str):
                self.log_csv(["Calculation", str(calc_str)])
                return func(self, calc_str)
            return inner_func
        return dec

    def clear_after_calc_buttons():
        def dec(func):
            def inner_func(self):
                if(self.is_last_operation_calc):
                    print("Last operation was calculation; clearing input")
                    self.input.clear()
                    self.is_last_operation_calc = False
                return func(self)
            return inner_func
        return dec

    def clear_after_calc_keys():
        def dec(func):
            def inner_func(self, *args):
                if(self.is_last_operation_calc):
                    print("Last operation was calculation; clearing input")
                    self.input.clear()
                    self.is_last_operation_calc = False
                return func(self, *args)
            return inner_func
        return dec

    # slot function connected to the clicked signal of the push buttons
    @clear_after_calc_buttons()
    @click_log()
    def button_click(self):
        sender = self.sender()
        input_operators = self.buttons[:14]

        # if pushed button is a input operator, append the corresponding text to the input field
        if(sender in input_operators):
            self.input.insert(self.sender().text())

        # if the pushed button is the delete button, delete the last character from the input field
        if(sender == self.button_delete):
            self.input.backspace()

        # if the pushed button is the clear button, delete all characters from the input field
        if(sender == self.button_clear):
            self.input.clear()

        # if the pushed button is the = button, send the current text from the input field to the calculate function
        if(sender == self.button_equals):
            self.input.setText(str(self.calculate(self.input.text())))
            self.is_last_operation_calc = True

    # function that listens for input from the keyboard
    @clear_after_calc_keys()
    @key_log()
    def keyPressEvent(self, event):
        key = event.key()
        input_operators = list(self.keys.values())[:14]

        # if pushed key is a input operator, append the corresponding text to the input field
        if(key in input_operators):
            self.input.insert(event.text())

        # if the pushed key is the backspace key, delete the last character from the input field
        if(key == self.keys["delete"]):
            self.input.backspace()

        # if the pushed key is the clear key, delete all characters from the input field
        if(key == self.keys["clear"]):
            self.input.clear()

        # if the pushed key is the = key, send the current text from the input field to the calculate function
        if(key == self.keys["equals"]):
            self.input.setText(str(self.calculate(self.input.text())))
            self.is_last_operation_calc = True

    # function that evaluates a given input from the input field and prints the result of the evaluation to the display,
    # if it throws no error
    # @calc_log()
    def calculate(self, calc_str):
        result = "Math Error"
        try:
            result = eval(calc_str)
        except Exception as e:
            print("Exception occured: %s" % (str(e)))
            self.input.setText("Math Error")
        return result

    def timestamp(self):
        return QtCore.QDateTime.currentDateTime().toMSecsSinceEpoch()

    # convert log-data from list to csv-string and output it to stdout
    # https://stackoverflow.com/questions/9157314/how-do-i-write-data-into-csv-format-as-string-not-file
    def log_csv(self, data):
        si = io.StringIO()
        cw = csv.writer(si)
        cw.writerow(data)
        print(si.getvalue().strip("\r\n"))


# main loop to run the program
if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    win = CalculatorWindow()
    win.show()
sys.exit(app.exec_())
