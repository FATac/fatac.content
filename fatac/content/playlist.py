from zope import schema
from plone.directives import form
from five import grok
from plone.memoize.instance import memoize
from fatac.content import PlaylistMessageFactory as _
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage
from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName
from groupSelectWidget import GroupsSelectionWidgetFactory
from plone.indexer import indexer
from fatac.theme.browser.funcionsCerca import funcionsCerca
from fatac.theme.browser.genericView import genericView
from fatac.theme.browser.vistesCerca import resultatsView
import json


class IPlaylist(form.Schema, IImageScaleTraversable):
    """ Playlist Schema
    """

    # Imatge de la Playlist
    descImage = NamedBlobImage(
        title=_(u"Playlist Image"),
        description=_(u"Add a Playlist Image that represents your playlist"),
        required=False,
        )

   # form.write_permission(track="fatac.ModRelField")
   # form.read_permission(track="fatac.ModRelField")

    # Llista d'objectes de la playlist que serveix per ordenar
    orderedList = schema.List(
        title=_(u"Ordered List To Play"),
        description=_(u"This is a list that has the order of the DB objects"),
        default=[],
        value_type=schema.TextLine(),
        required=False,
        )

    # Llista del grups en els que es pot llistar aquesta Playlist
    form.widget(visibleInGroupsList=GroupsSelectionWidgetFactory)
    visibleInGroupsList = schema.List(
        title=_(u"List of Groups that has this Playlist"),
        description=_(u"This is a list of the Groups that can show this playlist"),
        required=False,
        value_type=schema.TextLine(title=u"Visible in Groups"),
        )

    #Amaguem els camps a l'edicio
    form.omitted('orderedList')


@indexer(IPlaylist)
def vigListIndexer(playlist):
    """ Index en el Cataleg del camp 'visibleInGroupsList'
    """
    if playlist.visibleInGroupsList != None:
        return playlist.visibleInGroupsList
    else:
        return []
grok.global_adapter(vigListIndexer, name="visibleInGroupsList")


@grok.subscribe(IPlaylist, IObjectAddedEvent)
def autoPublishPlaylist(playlist, event):
    """ Publica la Playlist un cop s'ha creat.
    """
    wtool = getToolByName(playlist, 'portal_workflow')
    wtool.doActionFor(playlist, "publish")


class returnOrderedList(grok.View):
    """ Async View
        Retorna la llista d'objectes que te la playlist per poder ordenar
    """

    grok.context(IPlaylist)
    grok.require('zope2.View')
    grok.name('returnOrderedList')

    def render(self):
        """ Render the settings as inline Javascript object in HTML <head>
        """

        request = self.request
        context = self.context

        settings = self.llistaObjectes(request, context)
        json_snippet = json.dumps(settings)

        request.response.setHeader("content-type", "application/json")
        return json_snippet

    @memoize
    def llistaObjectes(self, request, context):
        """ Retorna la llista d'objectes del camp orderedList
        """

        llista_ids = []
        if context.orderedList != [] and context.orderedList != None:
            for element in context.orderedList:
                llista_ids.append(element[1])

        return {
            "Ids": llista_ids
        }


class View(grok.View, funcionsCerca):
    """ Main View
    """

    grok.context(IPlaylist)
    grok.require('zope2.View')
    grok.name('view')


class playlistView(grok.View, resultatsView):
    """ Pinta els resultats i les dades referents a la paginacio i les opcions
        de visualitzacio.
    """

    grok.context(IPlaylist)
    grok.require('zope2.View')
    grok.name('playlistView')
    grok.template('playlistView')

    def retDadesResultats(self):
        """ Crida la vista displayResultatsPaginaView i retorna l'html generat
        """

        request = self.request
        request.set('sorting', 'False')
        portal = getToolByName(self, 'portal_url')
        portal = portal.getPortalObject()
        path = '/'.join(self.context.getPhysicalPath())
        html = portal.unrestrictedTraverse(path + '/displayResultsPlaylistView')()
        return html


class displayResultsPlaylistView(grok.View, funcionsCerca):
    """ pinta l'html corresponent als resultats de la pagina actual (sense
        controls de visualitzacio)
    """

    grok.context(IPlaylist)
    grok.require('zope2.View')
    grok.name('displayResultsPlaylistView')
    grok.template('displayResultsPlaylistView')

    def retNumPagina(self):
        """ retorna el numero de pagina que cal pintar pintar
        """
        parametres_visualitzacio = self.retParametresVisualitzacio()
        return int(parametres_visualitzacio['pagina_actual'])

    def retDades(self):
        """ retorna l'html dels resultats de la pagina actual
        (nomes els resultats en si, no els controls de visualitzacio)
        """
        #TODO: per testejar descomentar seguent linia i comentar la resta
        #return self.retNumPagina()
        portal = getToolByName(self, 'portal_url')
        portal = portal.getPortalObject()
        path = '/'.join(self.context.getPhysicalPath())
        html = portal.unrestrictedTraverse(path + '/genericPlaylistview')()
        return html


class genericPlaylistview(grok.View, genericView):

    grok.context(IPlaylist)
    grok.require('zope2.View')
    grok.name('genericPlaylistview')
    grok.template('genericPlaylistview')

    def __init__(self, context, request):
        super(grok.View, self).__init__(context, request)
        super(genericView, self).__init__(context, request)


    def dades_genericview_header(self):
        """ funcions que retornen les dades necessaries per pintar cada vista
        """
        orderedList = self.context.orderedList

        dades_json = self.retSectionHeader()  # retorna diccionari
        resultat = []
        if dades_json:
            i = 0
            for objecte in dades_json:
                id_objecte = self.idobjectes[i]
                i += 1
                if objecte and 'sections' in objecte:
                    titol_objecte = self.getTitolObjecte(objecte['sections'])

                    dades = []
                    for seccio in objecte['sections']:
                        if seccio['name'] == 'header':
                            for dada in seccio['data']:
                                dades.append(self.llegirDada(dada))

                    # Treiem l'ordre que te cada element
                    order = 0
                    for obj in orderedList:
                        if id_objecte == obj[1]:
                            order = obj[0]

                    dades_objecte = {'id': id_objecte,
                                     'titol': titol_objecte,
                                     'classe': objecte['className'],
                                     'thumbnail_classe': self.getThumbnailClasse(objecte['className']),
                                     'thumbnail_objecte': self.getThumbnailObjecte(id_objecte),
                                     'dades_header': dades,
                                     'order': order}
                    resultat.append(dades_objecte)

        if resultat != []:
            # Ordenem els resultats segons l'ordre que s'ha fet des de la pantalla d'ordenacio
            orderedResultat = sorted(resultat, key=lambda k: int(k['order']))
            return orderedResultat
        else:
            return resultat


class sortingView(grok.View, funcionsCerca):
    """ Sorting View
    """

    grok.context(IPlaylist)
    grok.require('zope2.View')
    grok.name('sortingView')
    grok.template('sortingView')


class orderPlaylistView(grok.View, resultatsView):
    """ View for sorting Playlist elements
    """

    grok.context(IPlaylist)
    grok.require('zope2.View')
    grok.name('orderPlaylistView')
    grok.template("orderPlaylistView")

    def retDadesResultats(self):
        """ Crida la vista displayResultatsPaginaView i retorna l'html generat
        """

        request = self.request
        request.set('sorting', 'True')
        portal = getToolByName(self, 'portal_url')
        portal = portal.getPortalObject()
        path = '/'.join(self.context.getPhysicalPath())
        html = portal.unrestrictedTraverse(path + '/displayResultsPlaylistView')()
        return html


class updateList(grok.View):
    """ View for the updateList Method
    """

    grok.context(IPlaylist)
    grok.require('zope2.View')
    grok.name('updateList')

    def update(self):

        context = self.context
        newOrder = self.request.get('order')
        oldList = context.orderedList
        newList = []
        index = 0
        for element in newOrder:
            for oldElement in oldList:
                if str(element) == str(oldElement[0]):
                    newList.append([index, oldElement[1]])
                    index += 1

        if newList != []:
            context.orderedList = newList

    def render(self):
        print 'orderedList field Updated.'


class deleteObjectId(grok.View):
    """ View for removing an ID from the orderedList
    """

    grok.context(IPlaylist)
    grok.require('zope2.View')
    grok.name('deleteObjectId')

    def update(self):
        context = self.context
        objToDelete = self.request.get('objectId')
        oldList = context.orderedList
        newList = []
        index = 0
        for oldElement in oldList:
            if objToDelete != oldElement[1]:
                newList.append([index, oldElement[1]])
                index += 1

        if newList != []:
            context.orderedList = newList

    def render(self):
        print 'ID removed successfully'
