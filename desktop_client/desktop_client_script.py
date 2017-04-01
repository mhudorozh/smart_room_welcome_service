#!/usr/bin/python
# -*- coding: utf-8 -*-

from smart_m3.m3_kp import *
from smart_m3.RDFTransactionList import *
import uuid

import webbrowser
import time

NS = "http://cs.karelia.ru/smartroom_welcome_service#"


class PageViewer:
    def __init__(self, node):
        self.node = node

    def handle(self, added, removed):
        print "Added:"
        print added
        print "Removed: "
        print removed


class SIBAdapter(KP):
    def __init__(self, server_ip, server_port):
        KP.__init__(self, str(uuid.uuid4()) + "DesktopClient")
        self.ss_handle = ("X", (TCPConnector, (server_ip, server_port)))

    def join_sib(self):
        self.join(self.ss_handle)

    def leave_sib(self):
        self.leave(self.ss_handle)

    def create_subscription(self, trip, handler):
        self.st = self.CreateSubscribeTransaction(self.ss_handle)
        initial_results = self.st.subscribe_rdf(trip, handler)
        print initial_results

    def create_map_page_subscription(self):
        trip = [Triple(URI(NS + "MapPage_1"), URI(NS + "hasContent"), None)]
        sibAdapter.create_subscription(trip, PageViewer(self))


if __name__ == "__main__":
    sibAdapter = SIBAdapter("127.0.0.1", 10010)
    sibAdapter.join_sib()
    sibAdapter.create_map_page_subscription()

    while True:
        line = raw_input('\nType "exit" to exit the program\n')
        if line.lower() == "exit":
            break

    sibAdapter.leave_sib()
