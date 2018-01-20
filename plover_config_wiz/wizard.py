from importlib import import_module

from PyQt5.QtWidgets import QWizard

from plover.gui_qt.tool import Tool

from . import RESOURCE_DIR, resource_path


class ConfigWiz(QWizard, Tool):

    TITLE = 'Config Wiz'
    ROLE = 'config_wiz'
    ICON = str(resource_path('icon.svg'))

    PAGES = [
        line.strip().split() for line in '''

        machine py

        serial py
        serial_detect py skip_history

        plugin py

        test py

        '''.strip().split('\n')

        if line.strip()
    ]

    def __init__(self, engine):
        super().__init__(engine)
        self.engine = engine
        self._page = {}
        self._page_name = {-1: ''}
        self._page_id = {}
        self._skip_history = set()
        for md_file in RESOURCE_DIR.glob('*.md'):
            self._new_page(md_file.stem, 'md')
        for page_params in self.PAGES:
            page_name, page_type, *page_params = page_params
            page_params = {
                param: True
                for param in page_params
            }
            self._new_page(page_name, page_type, **page_params)
        self.machine = None
        self.config = None
        self.currentIdChanged.connect(self.on_id_changed)
        self.setStartId(self._page_id['machine'])

    def _new_page(self, page_name, page_type, skip_history=False):
        page_title = page_name.replace('_', ' ').title()
        page_module_name = '.' + page_name
        page_class_name = page_title.replace(' ', '') + 'Page'
        page_package = 'plover_config_wiz.page'
        if page_type == 'py':
            page_module = import_module(page_module_name, page_package)
            page_class = getattr(page_module, page_class_name)
            page = page_class()
        elif page_type == 'md':
            page_module = import_module('.info', page_package)
            page_class = getattr(page_module, 'InfoPage')
            page = page_class()
            page.setTitle(page_title)
            page.resource = 'resource:' + page_name + '.md'
        else:
            raise ValueError(page_type)
        page_id = self.addPage(page)
        self._page[page_id] = page
        self._page_name[page_id] = page_name
        self._page_id[page_name] = page_id
        if skip_history:
            self._skip_history.add(page_id)

    def pageId(self, page_name):
        return self._page_id[page_name]

    def nextId(self):
        page_id = self.currentId()
        page_name = self._page_name[page_id]
        next_id = super().nextId()
        if next_id != -1:
            return next_id
        if self.machine is None:
            return -1
        next_page = self.machine.workflow.get(page_name)
        if next_page is not None:
            return self._page_id[next_page]
        test_id = self._page_id['test']
        if page_id < test_id:
            return test_id
        return -1

    def initializePage(self, page_id, ignore=True):
        if ignore:
            return
        super().initializePage(page_id)

    def on_id_changed(self, page_id):
        available = set(self.pageIds())
        for missing in set(self._page) - available:
            if missing > page_id:
                self.setPage(missing, self._page[missing])
        for skip_history in set(self._skip_history) & available:
            if skip_history < page_id:
                self.removePage(skip_history)
        self.initializePage(page_id, ignore=False)
