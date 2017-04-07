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

    def sparql_query(self, sparql):
        """Adapter function for retrieving the result of sparql query

        :param sparql: code of sparql query
        :return: array of rdf triples
        """
        qt = self.CreateQueryTransaction(self.ss_handle)
        results = qt.sparql_query(sparql)
        self.CloseQueryTransaction(qt)
        return results

    def save_user(self, user):
        """Function provides interface for saving instance of class Page to SIB as couple of rdf triples.

        :param page: page to save in SIB
        """
        t = RDFTransactionList()

        t.setType(self.ns + "user" + user.uuid, self.ns + "User")
        t.add_literal(self.ns + "user" + user.uuid, self.ns + "hasId", user.uuid)
        t.add_literal(self.ns + "user" + user.uuid, self.ns + "hasName", user.name)
        t.add_literal(self.ns + "user" + user.uuid, self.ns + "hasSurname", user.surname)
        t.add_literal(self.ns + "user" + user.uuid, self.ns + "hasPatronymic", user.patronymic)
        t.add_literal(self.ns + "user" + user.uuid, self.ns + "hasCity", user.city["long_name"])

        l = self.CreateInsertTransaction(self.ss_handle)
        l.send(t.get())
        self.CloseInsertTransaction(l)

    def get_users(self):
        """Get all users from SIB

        :return: list of instances of class User
        """
        # Dictionary with key - user_uri in sib, value - instance of class User
        users = dict()

        # Getting all users id with users uri
        with open(config.get("sparql", "dir") + "users_id.rq") as f:
            # rdf triples (user_uri, hasId, user_id)
            rdf_triples = self.sparql_query(f.read())
            for triple in rdf_triples:
                # for each user id create empty instance of class User
                users[triple[0][2]] = User("", "", "", "", "", "")

        # Getting users info in rdf triples
        with open(config.get("sparql", "dir") + "users_info.rq") as f:
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


if __name__ == "__main__":
    sib_adapter = SIBAdapter(config.get("sib", "ip"), config.getint("sib", "port"),
                             config.get("sib", "space_name"), config.get("sib", "namespace"))
    sib_adapter.join_sib()

    user = User(uuid.uuid4(), "Sergey", "Titov", "Alekseevich", "Petrozavodsk", Status.PENDING)
    sib_adapter.save_user(user)

    sib_adapter.leave_sib()
