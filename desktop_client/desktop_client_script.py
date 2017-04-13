#!/usr/bin/python
# -*- coding: utf-8 -*-

from smart_m3.m3_kp import *
from smart_m3.RDFTransactionList import *
import uuid
import ConfigParser
import os
import webbrowser
import time

config = ConfigParser.ConfigParser()
config.read("config.ini")


class PageViewer:
    """Class receiver of the event about map page's content change"""

    def __init__(self, node):
        """Constructor of PageViewer
        
        :param node: sib adapter node joined in smart space
        """
        self.node = node

    def handle(self, added, removed):
        """This function will be called when sib adapter catch event about map page's content change
        
        :param added: rdf triple with new content of page 
        :param removed: old map page's content, not used, for correct prototype of called function from sib adapter
        :return: 
        """
        # Saving page content to local file
        with open('map_page.html', 'w') as f:
            f.write(str(added[0][2]))
        # Finding full path to saved page
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Opening map page in browser
        page_url = "file:///" + dir_path + "/map_page.html"
        webbrowser.open(url=page_url, autoraise=True)


class SIBAdapter(KP):
    """Class providing high-level methods for getting queries and communication with SIB. """

    def __init__(self, ip, port, space_name, ns):
        """Constructor of SIBAdapter without joining to sib

        :param ip: ip address of SIB
        :param port: port of SIB
        :param space_name: name of smart space to join
        :param ns: namespace of ontology
        """
        KP.__init__(self, str(uuid.uuid4()) + "DesktopClient")
        self.ss_handle = (space_name, (TCPConnector, (ip, port)))
        self.ns = ns

    def join_sib(self):
        """Adapter function for joining SIB"""
        self.join(self.ss_handle)

    def leave_sib(self):
        """Adapter function for leaving SIB"""
        self.leave(self.ss_handle)

    def create_subscription(self, trip, handler):
        """Adapter function for creating subscription to rdf triple

        :param trip: rdf triple handler subscribe for
        :param handler: handler of triple's update event
        """
        self.st = self.CreateSubscribeTransaction(self.ss_handle)
        self.st.subscribe_rdf(trip, handler)

    def sparql_query(self, sparql):
        """Adapter function for retrieving the result of sparql query

        :param sparql: code of sparql query
        :return: array of rdf triples
        """
        qt = self.CreateQueryTransaction(self.ss_handle)
        results = qt.sparql_query(sparql)
        self.CloseQueryTransaction(qt)
        return results

    def create_map_page_subscription(self, handler):
        """Function for subscribing class handler to map page's content change event

        :param handler: object that will be notified about map page's content change
        """
        # None means any content
        trip = [Triple(URI(self.ns + "map_page"), URI(self.ns + "hasContent"), None)]
        self.create_subscription(trip, handler)

if __name__ == "__main__":
    # Creating sib adapter
    sibAdapter = SIBAdapter(config.get("sib", "ip"), config.getint("sib", "port"),
                            config.get("sib", "space_name"), config.get("sib", "namespace"))

    # Joining smart space
    sibAdapter.join_sib()

    # Subscribing instance of PageViewer to map page content change
    sibAdapter.create_map_page_subscription(PageViewer(sibAdapter))

    while True:
        line = raw_input('\nType "exit" to exit the program\n')
        if line.lower() == "exit":
            exit(0)

    # Leaving sib
    sibAdapter.leave_sib()