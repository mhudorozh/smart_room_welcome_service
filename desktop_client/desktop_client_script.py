#!/usr/bin/python
# -*- coding: utf-8 -*-

import webbrowser
import time


class SIBAdapter:
    def __init__(self):
        pass

    def connect_sib(self):
        print 'connecting sib...'
        print '...done'

    def register_ontology(self):
        print 'register adapter...'
        print '...done'

    def wait_for_page_change(self):
        time.sleep(5)
        return 'https://yandex.ru'


class PageViewer:
    def __init__(self):
        self.sib_adapter = SIBAdapter()
        self.sib_adapter.connect_sib()
        self.sib_adapter.register_ontology()

    def run(self):
        while True:
            url = self.sib_adapter.wait_for_page_change()
            webbrowser.open(url=url, autoraise=True)

if __name__ == "__main__":
    pageViewer = PageViewer()
    pageViewer.run()
