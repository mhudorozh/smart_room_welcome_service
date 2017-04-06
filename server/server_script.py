#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import json

from smart_m3.m3_kp import *
from smart_m3.RDFTransactionList import *
import uuid

NS = "http://cs.karelia.ru/smartroom_welcome_service#"
access_token = 'AIzaSyAy8MoPJH-uh72zsxdnPqWbSyKCLq7jc_U'
map_api_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'


class User:
    def __init__(self, uuid, name, city):
        self.uuid = uuid
        self.name = name
        self.city = city

    def __str__(self):
        return str(
            {
                "name": self.name,
                "city": self.city["long_name"],
                "lat": self.city["lat"],
                "lng": self.city["lng"]
            }
        )


class Page:
    def __init__(self, name, content):
        self.name = name
        self.content = content

    def __str__(self):
        return str(
            {
                "name": self.name,
                "content": self.content,
            }
        )


class GeoDecoder:
    def __init__(self):
        pass

    @staticmethod
    def find_location(address):
        response = urllib.urlopen(map_api_url.format(address, access_token)).read()
        j = json.loads(response)
        long_name = j["results"][0]["address_components"][0]["long_name"]
        location = j["results"][0]["geometry"]["location"]
        return {"long_name": long_name, "lat": location["lat"], "lng": location["lng"]}


class SIBAdapter(KP):
    def __init__(self, server_ip, server_port):
        KP.__init__(self, str(uuid.uuid4()) + "Server")
        self.ss_handle = ("X", (TCPConnector, (server_ip, server_port)))

    def join_sib(self):
        self.join(self.ss_handle)

    def leave_sib(self):
        self.leave(self.ss_handle)

    def update(self, i_trip, r_trip):
        upd = self.CreateUpdateTransaction(self.ss_handle)
        upd.update(i_trip, "RDF-M3", r_trip, "RDF-M3")
        self.CloseUpdateTransaction(upd)

    def register_ontology(self):
        l = self.CreateInsertTransaction(self.ss_handle)
        l.send('../ontology/ontology.owl', encoding="RDF-XML")
        self.CloseInsertTransaction(l)

    def sparql_query(self, sparql):
        print sparql
        qt = self.CreateQueryTransaction(self.ss_handle)
        results = qt.sparql_query(sparql)
        self.CloseQueryTransaction(qt)

        return results

    def save_map_page(self, page):
        t = RDFTransactionList()

        t.setType(NS + "MapPage_1", NS + "MapPage")
        t.add_literal(NS + "MapPage_1", NS + "hasContent", page.content)
        t.add_literal(NS + "MapPage_1", NS + "hasName", page.name)

        l = self.CreateInsertTransaction(self.ss_handle)
        l.send(t.get())
        self.CloseInsertTransaction(l)

    def save_user(self, name):
        t = RDFTransactionList()

        user_id = str(uuid.uuid4())
        user_uri = NS + "user" + user_id
        print user_uri
        t.setType(user_uri, NS + "User")
        t.add_literal(user_uri, NS + "hasId", user_id)
        t.add_literal(user_uri, NS + "hasStatus", "pending")
        t.add_literal(user_uri, NS + "hasName", name)

        l = self.CreateInsertTransaction(self.ss_handle)
        l.send(t.get())
        self.CloseInsertTransaction(l)

    def update_map_page(self, i_page, r_page):
        i_trip = [Triple(URI(NS + "MapPage_1"), URI(NS + "hasContent"), Literal(i_page.content))]
        r_trip = [Triple(URI(NS + "MapPage_1"), URI(NS + "hasContent"), Literal(r_page.content))]
        self.update(i_trip, r_trip)


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
        user = User(uuid, name, GeoDecoder.find_location(short_city))
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