from html import escape

from pkg_resources import Requirement

from PyQt5.QtWidgets import QLabel, QGridLayout

from plover_plugins_manager.local_registry import list_plugins

from . import WizardPage


class PluginPage(WizardPage):

    def __init__(self):
        super().__init__()
        self.setTitle('Plugin')
        grid = QGridLayout(self)
        self.label = QLabel(self)
        self.label.setWordWrap(True)
        grid.addWidget(self.label, 0, 0, 1, 1)
        self._plugin_installed = False

    def initializePage(self):
        self._plugin_installed = False
        available_plugins = list_plugins()
        machine = self.wizard().machine
        req = Requirement.parse(machine.plugin)
        plugin_str = f'<b>{req.name}</b> plugin'
        if req.specifier:
            plugin_str += f' (version: <code>{req.specifier}</code>)'
        paragraph_list = [
            f'You need the {plugin_str} installed to use '
            f'the <b>{escape(machine.name)}</b> machine.'
        ]
        plugin = available_plugins.get(req.key)
        if plugin is None:
            paragraph_list.append(
                'Please install it and restart the configuration process.'
            )
        else:
            assert len(plugin) == 1
            plugin = plugin[0]
            paragraph_list.append(
                f'You have version: <code>{escape(plugin.version)}</code>.'
            )
            if plugin.parsed_version in req.specifier:
                paragraph_list.append(
                    'You\'re all set!'
                )
                self._plugin_installed = True
            else:
                paragraph_list.append(
                    'Please update to a compatible version, '
                    'and restart the configuration process.'
                )
        self.label.setText('<br><br>'.join(paragraph_list))

    def validatePage(self):
        return self._plugin_installed
