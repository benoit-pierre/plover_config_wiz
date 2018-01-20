from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QGridLayout

from . import WizardPage
from ..markdown_widget import MarkdownWidget


class InfoPage(WizardPage):

    def __init__(self):
        super().__init__()
        grid = QGridLayout(self)
        self.info = MarkdownWidget(self)
        grid.addWidget(self.info, 0, 0, 1, 1)
        self.resource = None

    def initializePage(self):
        self.info.setSource(QUrl(self.resource))
