from PyQt5.QtGui import QTextDocument
from PyQt5.QtCore import QUrl

from plover_plugins_manager.gui_qt.info_browser import InfoBrowser
from plover_plugins_manager.utils import description_to_html

from . import resource_path


class MarkdownWidget(InfoBrowser):

    def loadResource(self, resource_type, resource_url):
        if resource_url.scheme() == 'resource':
            resource_url = QUrl('file://' + str(resource_path(resource_url.path())))
        if resource_type == QTextDocument.ResourceType.UserResource:
            md = bytes(super().loadResource(resource_type, resource_url)).decode()
            css, html = description_to_html(md, 'text/markdown')
            return css + html
        return super().loadResource(resource_type, resource_url)

    def setSource(self, url, kind=QTextDocument.ResourceType.UserResource):
        assert (url.scheme() in 'resource' and url.path().endswith('.md')
                and kind == QTextDocument.ResourceType.UserResource)
        super().setSource(url, kind)
