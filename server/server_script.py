#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import json


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
    access_token = 'AIzaSyAy8MoPJH-uh72zsxdnPqWbSyKCLq7jc_U'
    map_api_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'

    def __init__(self):
        pass

    @staticmethod
    def find_location(address):
        response = urllib.urlopen(GeoDecoder.map_api_url.format(address, GeoDecoder.access_token)).read()
        j = json.loads(response)
        long_name = j["results"][0]["address_components"][0]["long_name"]
        location = j["results"][0]["geometry"]["location"]
        return {"long_name": long_name, "lat": location["lat"], "lng": location["lng"]}


class SIBAdapter:
    def __init__(self):
        pass

    def connect_sib(self):
        print 'connecting sib...'
        print '...done'

    def register_ontology(self):
        print 'register adapter...'
        print '...done'

    def save_page(self, page):
        print 'saving page...'
        print page.name
        print page.content
        print '...done'


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
        self.sib_adapter = SIBAdapter()
        self.sib_adapter.connect_sib()
        self.sib_adapter.register_ontology()
        self.sib_adapter.save_page(MapBuilder.build(self.users))

    def register_user(self, uuid, name, short_city):
        for user in self.users:
            if user.uuid == uuid:
                print 'Error: request register user twice'
        user = User(uuid, name, GeoDecoder.find_location(short_city))
        self.users.append(user)
        self.sib_adapter.save_page(MapBuilder.build(self.users))
        self.sib_adapter.save_page(WelcomeBuilder.build(user))

if __name__ == "__main__":
    server = Server()
    server.register_user(1, 'gdhsnlvr', 'Petrozavodsk')
