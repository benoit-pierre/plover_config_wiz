from types import SimpleNamespace
import json

from PyQt5.QtWidgets import QComboBox, QGridLayout, QLabel

from . import WizardPage
from .. import RESOURCE_DIR


class MachinePage(WizardPage):

    def __init__(self):
        super().__init__()
        self.setTitle('Machine')
        grid = QGridLayout(self)
        grid.setObjectName("gridLayout")
        self.machine = QComboBox(self)
        grid.addWidget(self.machine, 1, 0, 1, 1)
        label = QLabel(self)
        label.setWordWrap(True)
        label.setObjectName("label")
        label.setText('This wizard will help you setup your machine for use with Plover.\n'
                      '\n'
                      'Please select the type of machine you would like to use:')
        grid.addWidget(label, 0, 0, 1, 1)
        self._config = {}
        self._next_page = {}
        self._machine = {}
        for machine_json in sorted(RESOURCE_DIR.glob('*.json')):
            machine_id = machine_json.stem
            assert machine_id not in self._machine
            machine_spec = json.loads(machine_json.read_bytes())
            machine = SimpleNamespace(key=machine_id, name=machine_spec['name'],
                                      config=machine_spec.get('config', {}),
                                      plugin=machine_spec.get('plugin'),
                                      workflow=[])
            page_list = machine_spec.get('pages', [machine_id])
            if machine.plugin is not None and 'plugin' not in page_list:
                page_list.insert(0, 'plugin')
            machine.workflow = {
                page_name: page_list[n + 1]
                for n, page_name in enumerate(page_list[:-1])
            }
            machine.next_page = page_list[0] if page_list else None
            self._machine[machine_id] = machine
            self.machine.addItem(machine.name, machine)

    def initializePage(self):
        wizard = self.wizard()
        wizard.machine = None
        wizard.config = {
            'machine_specific_options': {}
        }

    def validatePage(self):
        wizard = self.wizard()
        machine = self.machine.currentData()
        wizard.machine = machine
        wizard.config.update(machine.config)
        return True

    def nextId(self):
        wizard = self.wizard()
        machine = self.machine.currentData()
        if machine.next_page is None:
            return -1
        return wizard.pageId(machine.next_page)
