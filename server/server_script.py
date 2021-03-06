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


class UserSubscriber:
    """Class receiver of the event about registering a new user"""

    def __init__(self, adapter, server):
        """Constructor
        
        :param adapter: instance of SIBAdapter joined to smart space 
        :param server: server to be notified
        """
        self.server = server
        self.adapter = adapter

    def handle(self, added, removed):
        """This function will be called when sib adapter catch event about new user
        
        :param added: rdf triple with user uri 
        :param removed: nothing, because we subscribing only on addition user, not removing, but still needed
            for correct prototype of called function from sib adapter
        :return: 
        """
        # Getting all users from SIB
        all_users = self.adapter.get_users()

        # Getting all processed users
        processed_users = self.server.users

        # Finding difference in O(n*m)
        new_users = []
        for user in all_users:
            was = False
            # Check is user has already been processed before
            for processed_user in processed_users:
                was |= processed_user.uuid == user.uuid
            # If not then add it to list of new users
            if not was:
                new_users.append(user)

        # If there is at most one new user, handling this new users
        if len(new_users) > 0:
            self.server.handle_new_users(new_users)


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

    def create_subscription(self, trip, handler):
        """Adapter function for creating subscription to rdf triple
        
        :param trip: rdf triple handler subscribe for
        :param handler: handler of triple's update event
        """
        self.st = self.CreateSubscribeTransaction(self.ss_handle)
        self.st.subscribe_rdf(trip, handler)

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

        print 'Saving page ' + self.ns + page.name
        print 'Content: ' + page.content
        t.setType(self.ns + page.name, self.ns + page.type)
        t.add_literal(self.ns + page.name, self.ns + "hasName", page.name)
        t.add_literal(self.ns + page.name, self.ns + "hasId", page.id)
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
        print 'Updating page ' + self.ns + page.name
        print 'New content: ' + page.content
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
        # Dictionary with key - user_uri in sib, value - instance of class User
        users = dict()

        # Getting all users id with users uri
        with open(config.get("sparql", "users_id_query")) as f:
            # rdf triples (user_uri, hasId, user_id)
            rdf_triples = self.sparql_query(f.read())
            for triple in rdf_triples:
                # for each user id create empty instance of class User
                users[triple[0][2]] = User("", "", "", "", "", "")

        # Getting users info in rdf triples
        with open(config.get("sparql", "users_info_query")) as f:
            # rdf triples (user_uri, type, attribute, value)
            rdf_triples = self.sparql_query(f.read())
            for triple in rdf_triples:
                # for each triple save attribute value to instance of class User
                if triple[2][2] == self.ns + "hasId":
                    users[triple[0][2]].uuid = triple[3][2]
                if triple[2][2] == self.ns + "hasName":
                    users[triple[0][2]].name = triple[3][2]
                if triple[2][2] == self.ns + "hasSurname":
                    users[triple[0][2]].surname = triple[3][2]
                if triple[2][2] == self.ns + "hasPatronymic":
                    users[triple[0][2]].patronymic = triple[3][2]
                if triple[2][2] == self.ns + "hasCity":
                    users[triple[0][2]].city['long_name'] = triple[3][2]
                if triple[2][2] == self.ns + "hasStatus":
                    users[triple[0][2]].status = triple[3][2]
            # return list of users
            return users.values()

    def create_user_subscription(self, handler):
        """Function for subscribing class handler to new user event
        
        :param handler: object that will be notified about new user event 
        """
        # None means any user
        trip = [Triple(None, URI("rdf:type"), URI(self.ns + "User"))]
        self.create_subscription(trip, handler)


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
        for user in users:
            page.content += str(user)
        page.content += "\n/* Version: " + str(uuid.uuid4()) + " */"
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
						
			file = open(config.get("html", "users_welcome"), 'r') 
			text = file.read() 
            file.close() 
            text = text.replace("username", user.name+" "+user.patronymic+" "+user.surname)
			text = text.replace("usercity", user.city)
		page.content = text
        return page


class Server:
    """Class server represent main logic module of welcome service. Server processes new user addition event and
    responds requests """

    def __init__(self):
        """Constructor of server with joining smart space"""

        # Joining smart space
        self.sib_adapter = SIBAdapter(config.get("sib", "ip"), config.getint("sib", "port"),
                                      config.get("sib", "space_name"), config.get("sib", "namespace"))
        self.sib_adapter.join_sib()

        # Pushing service ontology to SIB
        self.sib_adapter.register_ontology(config.get("ontology", "file"),
                                           config.get("ontology", "encoding"))

        self.sib_adapter.create_user_subscription(UserSubscriber(self.sib_adapter, self))

        # Getting all users registered before server start
        self.users = self.sib_adapter.get_users()
        # Saving map page with no registered users
        self.map_page = MapBuilder.build(self.users)
        self.sib_adapter.save_page(self.map_page)

    def close(self):
        self.sib_adapter.leave_sib()

    def handle_new_users(self, new_users):
        """Function for handling new users

        :param new_users: list of new users to process server
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

    while True:
        line = raw_input('\nType "exit" to exit the program\n')
        if line.lower() == "exit":
            break

    server.close()
