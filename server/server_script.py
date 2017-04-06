#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import json
import ConfigParser

from smart_m3.m3_kp import *
from smart_m3.RDFTransactionList import *
import uuid

config = ConfigParser.ConfigParser()
config.read("config.ini")


class Status:
    """Enum of status values"""
    # Pending status means registration request was'nt processed
    PENDING = "pending"
    # Failed status means registration request was accepted, but server could not find location of user's city
    FAILED = "failed"
    # Ready status means registration request was accepted, everything fine
    READY = "ready"


class User:
    """Class of user profile"""

    def __init__(self, uuid, name, surname, patronymic, city, status):
        """Constructor of user

        :param uuid: unique identification of user
        :param name: name of user
        :param surname: surname of user
        :param patronymic: patronymic of user
        :param city: city user came from
        :param status: status of registration request
        """
        self.uuid = uuid
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.city = city
        self.status = status

    def __str__(self):
        """Function overloading string representation of user

        :return: string representation of user
        """
        return str(
            {
                "uuid": self.uuid,
                "name": self.name,
                "surname": self.surname,
                "patronymic": self.patronymic,
                "city": self.city["long_name"],
                "lat": self.city["lat"],
                "lng": self.city["lng"],
                "status": self.status
            }
        )


class Page:
    """Class of web page"""

    def __init__(self, name, content, type):
        """Constructor of page

        :param name: name of page
        :param content: html/css/js content of page
        :param type: rdf type of page
        """
        self.name = name
        self.content = content
        self.type = type

    def __str__(self):
        """Function overloading string representation of page

        :return: string representation of page
        """
        return str(
            {
                "name": self.name,
                "content": self.content,
                "type": self.type
            }
        )


def find_location(city_name):
    """Find location of city in world coordinates

    :param city_name: name of city, errors are permissible
    :return: dictionary with fields 'long_name' - correct name of city, 'lat' - latitude, 'lng' - longitude
    """
    request_rul = config.get("location_api", "api_url").format(city_name, config.get("location_api", "access_token"))

    response = urllib.urlopen(request_rul).read()
    j = json.loads(response)

    long_name = j["results"][0]["address_components"][0]["long_name"]
    location = j["results"][0]["geometry"]["location"]
    return {"long_name": long_name, "lat": location["lat"], "lng": location["lng"]}


class SIBAdapter(KP):
    """Class providing high-level methods for getting queries and communication with SIB. """

    def __init__(self, ip, port, space_name, ns):
        """Constructor of SIBAdapter without joining to sib

        :param ip: ip address of SIB
        :param port: port of SIB
        :param space_name: name of smart space to join
        :param ns: namespace of ontology
        """
        KP.__init__(self, str(uuid.uuid4()) + "Server")
        self.ss_handle = (space_name, (TCPConnector, (ip, port)))
        self.ns = ns

    def join_sib(self):
        """Adapter function for joining SIB"""
        self.join(self.ss_handle)

    def leave_sib(self):
        """Adapter function for leaving SIB"""
        self.leave(self.ss_handle)

    def update(self, i_trip, r_trip):
        """Adapter function for updating rdf triple

        :param i_trip: new version of rdf triple
        :param r_trie: old version of rdf triple
        """
        upd = self.CreateUpdateTransaction(self.ss_handle)
        upd.update(i_trip, "RDF-M3", r_trip, "RDF-M3")
        self.CloseUpdateTransaction(upd)

    def register_ontology(self, ontology_file_path, ontology_encoding="RDF-XML"):
        """Adapter function for loading project ontology to SIB

        :param ontology_file_path: path to ontology file of project
        :param ontology_encoding: encoding of ontology file (default "RDF-XML")
        """
        l = self.CreateInsertTransaction(self.ss_handle)
        l.send(ontology_file_path, encoding=ontology_encoding)
        self.CloseInsertTransaction(l)

    def sparql_query(self, sparql):
        """Adapter function for retrieving the result of sparql query

        :param sparql: code of sparql query
        :return: array of rdf triples
        """
        qt = self.CreateQueryTransaction(self.ss_handle)
        results = qt.sparql_query(sparql)
        self.CloseQueryTransaction(qt)
        return results

    def save_page(self, page):
        """Function provides interface for saving instance of class Page to SIB as couple of rdf triples.

        :param page: page to save in SIB
        """
        t = RDFTransactionList()

        t.setType(self.ns + page.name, self.ns + page.type)
        t.add_literal(self.ns + page.name, self.ns + "hasName", page.name)
        t.add_literal(self.ns + page.name, self.ns + "hasContent", page.content)

        l = self.CreateInsertTransaction(self.ss_handle)
        l.send(t.get())
        self.CloseInsertTransaction(l)

    def update_page_content(self, page, i_content, r_content):
        """Function provides interface for updating page content in SIB

        Updating performs with replacing triple with old page's content to new content
        With removing old rdf triples and inserting new rdf triples

        :param page: page to be updated
        :param i_content: page content to insert in SIB
        :param r_content: page content to remove from SIB
        """
        i_trip = [Triple(URI(self.ns + page.name), URI(self.ns + "hasContent"), Literal(i_content))]
        r_trip = [Triple(URI(self.ns + page.name), URI(self.ns + "hasContent"), Literal(r_content))]
        self.update(i_trip, r_trip)

    def update_user_status(self, user, i_status, r_status):
        """Function provides interface for updating user status in SIB

        Updating performs with replacing triple with old user's status to new status
        With removing old rdf triples and inserting new rdf triples

        :param user: user to be updated
        :param i_status: new status to be set
        :param r_status: old status to be removed
        :return:
        """
        i_trip = [Triple(URI(self.ns + "user:" + user.uuid), URI(self.ns + "hasStatus"), Literal(i_status))]
        r_trip = [Triple(URI(self.ns + "user:" + user.uuid), URI(self.ns + "hasStatus"), Literal(r_status))]
        self.update(i_trip, r_trip)

    def get_users(self):
        """Get all users from SIB

        :return: list of instances of class User
        """
        with open(config.get("files", "sparql_query_dir") + "users_id.rq") as f:
            rdf_triples = self.sparql_query(f.read())
            # TODO: write conversation from list of rdf triples to list of instances of class Users
            return []

class PageBuilder:
    def __init__(self):
        pass

    @staticmethod
    def build(users):
        return Page("undefined", "")


class MapBuilder(PageBuilder):
    @staticmethod
    def build(users):
        page = Page("map_page", "")
        page.content += 'var user_data = ['
        for user in users:
            page.content += str(user)
        page.content += '];'
        return page


class WelcomeBuilder(PageBuilder):
    @staticmethod
    def build(user):
        page = Page("welcome_page#" + str(user.uuid), "")
        page.content += 'var user_data = ['
        page.content += str(user)
        page.content += '];'
        return page


class Server:
    def __init__(self):
        self.users = []
        self.map_page = MapBuilder.build(self.users)
        self.sib_adapter = SIBAdapter("127.0.0.1", 10010)
        self.sib_adapter.join_sib()
        self.sib_adapter.register_ontology()
        self.sib_adapter.save_map_page(self.map_page)

    def register_user(self, uuid, name, short_city):
        for user in self.users:
            if user.uuid == uuid:
                print 'Error: request register user twice'
        user = User(uuid, name, find_location(short_city))
        self.users.append(user)
        self.sib_adapter.save_user(name)

        # updating map page
        updated_map_page = MapBuilder.build(self.users)
        self.sib_adapter.update_map_page(updated_map_page, self.map_page)
        self.map_page = updated_map_page


if __name__ == "__main__":
    server = Server()
    query = ("SELECT ?s ?p ?o WHERE {\n"
             "  ?s ?p ?o.\n"
             "  FILTER(?p = t:hasId)\n"
             "}")

    with open('../sparql/users_id.rq') as f:
        for res in server.sib_adapter.sparql_query(f.read()):
            print res
    with open('../sparql/users_info.rq') as f:
        for res in server.sib_adapter.sparql_query(f.read()):
            print res