from PyQt5.QtWidgets import QComboBox, QLabel, QGridLayout

from serial.tools.list_ports import comports

from . import WizardPage


def scan():
    return sorted(x[0] for x in comports())


class SerialPage(WizardPage):

    def __init__(self):
        super().__init__()
        self.setTitle('Serial Port')
        grid = QGridLayout(self)
        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setText(
            'Please select the serial port to use. If you\'re not sure, '
            'select \"Auto-detect\" and this wizard will attempt to '
            'automatically detect the correct port.'
        )
        grid.addWidget(self.label, 0, 0, 1, 1)
        self.port = QComboBox(self)
        self.port.addItem('Auto-detect')
        grid.addWidget(self.port, 1, 0, 1, 1)

    def initializePage(self):
        port = self.port.currentText()
        auto_detect = self.port.itemText(0)
        available_ports = [auto_detect] + list(scan())
        self.port.clear()
        self.port.addItems(available_ports)
        if port in available_ports:
            index = available_ports.index(port)
        else:
            index = 0
        self.port.setCurrentIndex(index)

    def validatePage(self):
        port = self.port.currentText()
        if port != 'Auto-detect':
            self.wizard().config['machine_specific_options']['port'] = port
        return True

    def nextId(self):
        port = self.port.currentText()
        if port != 'Auto-detect':
            return -1
        return self.wizard().pageId('serial_detect')
