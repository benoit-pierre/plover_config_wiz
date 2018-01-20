from PyQt5.QtWidgets import QLabel, QGridLayout

from . import WizardPage
from .serial import scan


class SerialDetectPage(WizardPage):

    def __init__(self):
        super().__init__()
        self.setTitle('Serial Port')
        self.setSubTitle('Auto-Detection')
        grid = QGridLayout(self)
        self.label = QLabel(self)
        self.label.setWordWrap(True)
        grid.addWidget(self.label, 0, 0, 1, 1)
        self.available_ports = []
        self.step = 'start'

    def _refresh(self):
        if self.step == 'start':
            text = (
                'Please make sure the machine is <b>disconnected</b>, '
                'and click the "Next" button.'
            )
        elif self.step == 'finish':
            text = (
                'Please make sure the machine is <b>connected</b>, '
                'and click the "Next" button.'
            )
        elif self.step == 'failed':
            text = (
                'Auto-detection failed!'
            )
        else:
            raise ValueError(self.step)
        self.label.setText(text)

    def initializePage(self):
        self.step = 'start'
        self._refresh()

    def validatePage(self):
        if self.step == 'start':
            self.available_ports = scan()
            self.step = 'finish'
        elif self.step == 'finish':
            new_ports = list(sorted(set(scan()) - set(self.available_ports)))
            if new_ports:
                wizard = self.wizard()
                wizard.config['machine_specific_options']['port'] = new_ports[0]
                return True
            self.step = 'failed'
        elif self.step == 'failed':
            pass
        else:
            raise ValueError(self.step)
        self._refresh()
        return False
