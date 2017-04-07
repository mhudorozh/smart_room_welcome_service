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

    def __init__(self, uuid, name, surname, patronymic, city_name, status):
        """Constructor of user

        :param uuid: unique identification of user
        :param name: name of user
        :param surname: surname of user
        :param patronymic: patronymic of user
        :param city_name: city name user came from
        :param status: status of registration request
        """
        self.uuid = str(uuid)
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.city = {"long_name": city_name, "lat": 0, "lng": 0}
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

    def __init__(self, name, id, content, type):
        """Constructor of page

        :param name: name of page
        :param content: html/css/js content of page
        :param id: unique id of page
        :param type: rdf type of page
        """
        self.name = name
        self.id = id
        self.content = content
        self.type = type

    def __str__(self):
        """Function overloading string representation of page

        :return: string representation of page
        """
        return str(
            {
                "name": self.name,
                "id": self.id,
                "content": self.content,
                "type": self.type
            }
        )


def find_location(city_name):
    """Find location of city in world coordinates

    :param city_name: name of city, errors are permissible
    :return: dictionary with fields 'long_name' - correct name of city, 'lat' - latitude, 'lng' - longitude
    :raise AttributeError: if location of city didn't found
    :raise IOError: if no internet connection
    """
    request_rul = config.get("location_api", "url").format(city_name, config.get("location_api", "token"))
    response = urllib.urlopen(request_rul).read()
    j = json.loads(response)

    if j["status"] != "OK":
        raise AttributeError("Can't find location of city")

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
        t.add_literal(self.ns + page.id, self.ns + "hasId", page.id)
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
        with open(config.get("sparql", "dir") + "users_id.rq") as f:
            rdf_triples = self.sparql_query(f.read())
            # TODO: write conversation from list of rdf triples to list of instances of class Users
            return []


class MapBuilder:
    """Static class for building map page"""
    # Type of building page
    type = "MapPage"

    @staticmethod
    def build(users):
        """Static function for building map page

        :param users: users for whom the page is building
        :return: map page with cities of users
        """
        page = Page("map_page", "1", "", MapBuilder.type)
        # TODO: build map page

        return page


class WelcomeBuilder:
    """Static class for building welcome page"""
    # Type of building page
    type = "WelcomePage"

    @staticmethod
    def build(user):
        """Static function for building welcome page

        :param user: user for whom the page is building
        :return: welcome page for user
        """
        page = Page("welcome_page#" + user.uuid, user.uuid, "", WelcomeBuilder.type)
        # TODO: build map page

        return page


class Server:
    """Class server represent main logic module of welcome service. Server processes new user addition event and
    responds requests """

    def __init__(self):
        """Constructor of server with joining smart space"""
        self.users = []

        # Joining smart space
        self.sib_adapter = SIBAdapter(config.get("sib", "ip"), config.getint("sib", "port"),
                                      config.get("sib", "space_name"), config.get("sib", "namespace"))
        self.sib_adapter.join_sib()

        # Pushing service ontology to SIB
        self.sib_adapter.register_ontology(config.get("ontology", "file"),
                                           config.get("ontology", "encoding"))

        # Saving map page with no registered users
        self.map_page = MapBuilder.build(self.users)
        self.sib_adapter.save_page(self.map_page)

    def handle_new_users(self, new_users):
        """Function for handling new users

        :param users: list of new users to process server
        """
        # Finding location for each user
        for user in new_users:
            try:
                user.city = find_location(user.city["long_name"])
            except AttributeError:
                print "Can't find location of city" + user.city["long_name"]
                user.status = Status.FAILED
            except IOError:
                print "Can't connect to internet"
                user.status = Status.FAILED

        # Extend server processed users
        self.users.extend(new_users)

        # Updating map page content
        self.update_map_page(self.users)

        # Building welcome pages for every new user
        self.create_welcome_pages(new_users)

        # Changing status for each new user
        for user in new_users:
            # Status may be FAILED, in this case we can't set status to ready
            if user.status != Status.FAILED:
                user.status = Status.READY
            # Updating user registration status
            self.sib_adapter.update_user_status(user, user.status, Status.PENDING)

    def update_map_page(self, users):
        """Build and save map page for users

        :param users: list of users to be placed in map page
        """
        map_page = MapBuilder.build(users)
        self.sib_adapter.update_page_content(self.map_page, self.map_page.content, map_page.content)
        self.map_page = map_page

    def create_welcome_pages(self, new_users):
        """Build and save welcome page for each new user

        :param new_users: list of new users
        """
        for user in new_users:
            welcome_page = WelcomeBuilder.build(user)
            self.sib_adapter.save_page(welcome_page)


if __name__ == "__main__":
    server = Server()
    user = User(123, "Sergey", "Titov", "Alekseevich", "Konchezero", Status.PENDING)
