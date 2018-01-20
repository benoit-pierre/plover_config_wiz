from PyQt5.QtWidgets import QLabel, QPlainTextEdit, QSizePolicy, QVBoxLayout

from html import escape

from . import WizardPage


class TestPage(WizardPage):

    def __init__(self):
        super().__init__()
        self.setTitle('Testing')
        vbox = QVBoxLayout(self)
        self.results = QLabel(self)
        sizep = QSizePolicy(QSizePolicy.MinimumExpanding,
                            QSizePolicy.MinimumExpanding)
        sizep.setHorizontalStretch(0)
        sizep.setVerticalStretch(0)
        sizep.setHeightForWidth(self.results.sizePolicy().hasHeightForWidth())
        self.results.setSizePolicy(sizep)
        vbox.addWidget(self.results)
        label = QLabel(self)
        label.setWordWrap(True)
        label.setText('You can test you configuration by pressing '
                      'some keys and checking the output below:')
        vbox.addWidget(label)
        self.strokes = QPlainTextEdit(self)
        self.strokes.setReadOnly(True)
        vbox.addWidget(self.strokes)
        label = QLabel(self)
        label.setWordWrap(True)
        label.setText('Click the "Finish" button to save your '
                      'configuration and start using Plover.')
        vbox.addWidget(label)
        self._initial_config = {}

    def initializePage(self):
        engine = self.wizard().engine
        config = self.wizard().config
        machine = escape(config['machine_type'])
        text = '<b>Configuration:</b><ul>'
        text += f'<li><b>machine type:</b> {machine}</li>'
        options = config['machine_specific_options']
        if options:
            text += '<li><b>options:</b><ul>'
            for name, value in sorted(options.items()):
                text += f'<li>{escape(name)}: {escape(str(value))}'
            text += '</ul></li>'
        text += '</ul>'
        self.results.setText(text)
        if self._initial_config:
            return
        with engine:
            initial_config = engine.config
            self._initial_config = dict(
                machine_type=initial_config['machine_type'],
                machine_specific_options=initial_config['machine_specific_options'],
            )
            engine.set_output(False)
            engine.config = config
            engine.signal_stroked.connect(self.on_stroke)
        self.strokes.clear()

    def cleanupPage(self):
        engine = self.wizard().engine
        with engine:
            engine.signal_stroked.disconnect(self.on_stroke)
            engine.config = self._initial_config
        self._initial_config = {}

    def on_stroke(self, stroke):
        self.strokes.appendPlainText(stroke.rtfcre)
