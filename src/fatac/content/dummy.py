from zope import schema
from z3c.form import widget
from plone.directives import form
from zope.interface import Invalid
from plone.app.textfield import RichText
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from five import grok
from zope.component import getMultiAdapter
from plone.memoize.instance import memoize
from fatac.content import PlaylistMessageFactory as _
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage

from plone.app.relationfield.widget import RelationListDataManager
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from z3c.relationfield.relation import RelationValue

from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName

import json
from plone.app.layout.viewlets.interfaces import IHtmlHead
import urllib2






class IDummy(form.Schema, IImageScaleTraversable):
    """
    Dummy Schema
    """

    descImage = NamedBlobImage(
        title = _(u"Playlist Image"),
        description = _(u"Add a Playlist Image that represents your playlist"),
        required = False,
        )

    tagList = schema.List(
        title = _(u"Tag List"),
        description = _(u"This is a list of tags that have this image"),
        default = [],
        value_type=schema.TextLine(),
        required = False,
        )


class View(grok.View):
    """
    Main View
    """
    grok.context(IDummy)
    grok.require('zope2.View')
    grok.name('view')
    #grok.template("dummy_view")


class returnPlaylists(grok.View):
    """
       Async View
    """

    grok.context(IDummy)
    grok.require('zope2.View')
    grok.name('returnPlaylists')
    #grok.viewletmanager(IHtmlHead)

    #def update(self):
    #    self.llistaPlaylists = self.llistaPlaylists()

    def render(self):
        #print "S'ha demanat la llista de Playlists"
        """
        Render the settings as inline Javascript object in HTML <head>
        """
        request = self.request
        context = self.context

        settings = self.llistaPlaylists(request, context)
        json_snippet = json.dumps(settings)

        request.response.setHeader("content-type", "application/json")
        return json_snippet 

    @memoize
    def llistaPlaylists(self, request, context):
        #Get the current member
        mt = getToolByName(context, 'portal_membership')
        if not mt.isAnonymousUser(): # the user has not logged in
            member = mt.getAuthenticatedMember()
            username = member.getUserName()

        #Search all the Playlist
        catalog = getToolByName(context, 'portal_catalog')
        search = catalog.searchResults({'portal_type': 'fatac.playlist', 'Creator': member.getId()})
        
        llistaIds = []
        llistaTitols = []
        for brain in search:
            llistaIds.append(brain.id)
            llistaTitols.append(brain.Title)

        return {
            "Ids" : llistaIds,
            "Titols" : llistaTitols,
        }


class updatePlaylist(grok.View):
    """
       View for the updatePlaylist Method
    """

    grok.context(IDummy)
    grok.require('zope2.View')
    grok.name('updatePlaylist')

    def update(self):
        self.updatePlaylistObject(self.context)
        
    def render(self):
        print 'Playlist Updated.'

    @memoize
    def updatePlaylistObject(self, context):
        idPlaylist = self.request.get('idPlaylist')

        #Search all the Playlist
        catalog = getToolByName(context, 'portal_catalog')
        search = catalog.searchResults({'portal_type': 'fatac.playlist', 'id': idPlaylist})

        playlist = search[0].getObject()
        newOrderedList = []
        newRelationList = []

        if (playlist != None):
            # Check if new Object is in the Ordered List
            objectIsInOrderedList = False
            if (playlist.orderedList != None):
                for item in playlist.orderedList:
                    newOrderedList.append(item)
                    if (item[1] == context.getId()):
                        objectIsInOrderedList = True

            if (objectIsInOrderedList == False):
                newOrderedList.append([len(newOrderedList),context.getId()])
                playlist.orderedList = newOrderedList

            #Check if new Object is already in the playlist
            objectIsInPlaylist = False
            if (playlist.listToPlay != None):
                for item in playlist.listToPlay:
                    newRelationList.append(item)
                    if (item.to_object.id == context.id):
                        objectIsInPlaylist = True

            if (objectIsInPlaylist == False):
                intids = getUtility(IIntIds)
                try:
                    to_id = intids.getId(context)
                except KeyError:
                    to_id = intids.register(context)

                newRelationList.append(RelationValue(to_id))
                playlist.listToPlay = newRelationList



class loadTags(grok.View):
    grok.context(IDummy)
    grok.require('zope2.View')
    grok.name('loadTags')

    #Tag Data: id, x, y, width, height, message, photoID
    #tags = [{'id': '0', 'x': '0', 'y': '0', 'width': '300', 'height': '300', 'message': 'Hola caracola', 'photoID': 'photo1'}]

    def render(self):
        request = self.request
        context = self.context

        if (context.tagList != None):
            if (len(context.tagList) > 0):
                tags = []
    
                for tag in context.tagList:
                    subTag = tag.split(",")
                    tags.append({'id': subTag[0], 'x': subTag[1], 'y': subTag[2], 'width': subTag[3], 'height': subTag[4], 'message': subTag[5], 'photoID': subTag[6]})

                json_data = json.dumps(tags)

                print "Load Tags!"
                request.response.setHeader("content-type", "application/json")
                return json_data
            else:
                print "No hi han Tags per carregar"
                return []


class saveTag(grok.View):
    grok.context(IDummy)
    grok.require('zope2.View')
    grok.name('saveTag')

    def update(self):
        self.saveCurrentTag()

    def render(self):
        return """ """

    def saveCurrentTag(self):
        context = self.context
        request = self.request
        
        newTag = request.get('tag')
        print newTag

        currentTagList = []
        if (context.tagList != None):
            if (len(context.tagList) > 0):
                for tag in context.tagList:
                    currentTagList.append(tag)

        currentTagList.append(newTag)

        context.tagList = currentTagList 

        print "Save Tag!"


        #currentTagList.append([len(currentTagList), tag.x, tag.y, tag.width, tag.height, tag.message, tag.photoID])
        #url.id, url.x, url.y, url.width, url.height, url.message, url.photoID


class deleteTag(grok.View):
    grok.context(IDummy)
    grok.require('zope2.View')
    grok.name('deleteTag')

    def render(self):
        print "Delete Tag!"
        return """ """
