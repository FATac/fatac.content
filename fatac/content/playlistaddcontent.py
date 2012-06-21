# -*- encoding: utf-8 -*-

from five import grok
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from zope.interface import Interface
import json


class retornaIdUltimaPlaylist(grok.View):
    """ View for the retornaIdUltimaPlaylist Method
    """

    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('retornaIdUltimaPlaylist')

    def render(self):
        """ Render the settings as inline Javascript object in HTML <head>
        """

        request = self.request
        context = self.context

        settings = self.retornaIdUltimaPlaylist(request, context)
        json_snippet = json.dumps(settings)

        request.response.setHeader("content-type", "application/json")
        return json_snippet

    def retornaIdUltimaPlaylist(self, request, context):
        """ Retorna l'id de la darrera playlist creda per l'usuari autenticat.
        """

        # Get the current member
        mt = getToolByName(context, 'portal_membership')
        if not mt.isAnonymousUser():
            member = mt.getAuthenticatedMember()

            # Search all the Playlist
            catalog = getToolByName(context, 'portal_catalog')
            search = catalog.searchResults({'portal_type': 'fatac.playlist', 'Creator': member.getId(), 'sort_on': 'created', 'sort_order': 'reverse'})[:1]
            for brain in search:
                return brain.id
        return None


class retornaPlaylists(grok.View):
    """ View for the llistaPlaylists Method
    """

    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('retornaPlaylists')

    def render(self):
        """ Render the settings as inline Javascript object in HTML <head>
        """

        request = self.request
        context = self.context

        settings = self.llistaPlaylists(request, context)
        json_snippet = json.dumps(settings)

        request.response.setHeader("content-type", "application/json")
        return json_snippet

    @memoize
    def llistaPlaylists(self, request, context):
        """ Retorna un diccionari amb una llista de ids i una llista de títols
        de les playlist creades per l'usuari autenticat.
        """

        # Get the current member
        mt = getToolByName(context, 'portal_membership')
        if not mt.isAnonymousUser():
            member = mt.getAuthenticatedMember()

            # Search all the Playlist
            catalog = getToolByName(context, 'portal_catalog')
            search = catalog.searchResults({'portal_type': 'fatac.playlist', 'Creator': member.getId()})

            llistaIds = []
            llistaTitols = []
            for brain in search:
                llistaIds.append(brain.id)
                llistaTitols.append(brain.Title)

            return {"ids": llistaIds, "titols": llistaTitols}
        return None


class actualitzaPlaylist(grok.View):
    """ View for the updatePlaylistObject Method
    """

    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('actualitzaPlaylist')

    def update(self):
        """ update method
        """

        self.updatePlaylistObject(self.context)

    def render(self):
        """ render method
        """

        print 'Playlist Updated.'

    @memoize
    def updatePlaylistObject(self, context):
        """ Afegeix l'id 'idObjecte' rebut per request a la playlist 'idPlaylist'
        rebuda per request, si l'objecte no existeix ja a la playlist.
        """

        idPlaylist = self.request.get('idPlaylist')
        idObjecte = self.request.get('idObjecte')

        #Search all the Playlist
        catalog = getToolByName(context, 'portal_catalog')
        search = catalog.searchResults({'portal_type': 'fatac.playlist', 'id': idPlaylist})

        playlist = search[0].getObject()
        newOrderedList = []

        if (playlist != None):
            # Check if new Object is in the Ordered List
            objectIsInOrderedList = False
            if (playlist.orderedList != None):
                for item in playlist.orderedList:
                    newOrderedList.append(item)
                    if (item[1] == idObjecte):
                        objectIsInOrderedList = True

            if (objectIsInOrderedList == False):
                newOrderedList.append([len(newOrderedList), idObjecte])
                playlist.orderedList = newOrderedList
