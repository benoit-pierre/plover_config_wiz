from PyQt5.QtWidgets import QWizardPage


class WizardPage(QWizardPage):

    def nextId(self):
        return -1
