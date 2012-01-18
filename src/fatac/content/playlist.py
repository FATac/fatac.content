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
from plone.dexterity.browser.add import DefaultAddForm, DefaultAddView
from plone.directives import dexterity
from z3c.form import button, field
from groupSelectWidget import GroupsSelectionWidgetFactory



class IPlaylist(form.Schema, IImageScaleTraversable):
    """
        Playlist Schema
    """

    # Imatge de la Playlist
    descImage = NamedBlobImage(
        title = _(u"Playlist Image"),
        description = _(u"Add a Playlist Image that represents your playlist"),
        required = False,
        )

   # form.write_permission(track="fatac.ModRelField")
   # form.read_permission(track="fatac.ModRelField")

    # Llista d'obectes relacionats amb la Playlist
    listToPlay = RelationList(
        title = _(u"List To Play"),
        description = _(u"This is a playlist to play"),
        default=[],
        value_type=RelationChoice(title=_(u"Objects to Play"), source=ObjPathSourceBinder()),
        required = False,
        )

    # Llista d'objectes de la playlist que serveix per ordenar
    orderedList = schema.List(
        title = _(u"Ordered List To Play"),
        description = _(u"This is a list that has the order of the listToPlay field"),
        default = [],
        value_type=schema.TextLine(),
        required = False,
        )

    # Llista del grups en els que es pot llistar aquesta Playlist
    form.widget(visibleInGroupsList = GroupsSelectionWidgetFactory)
    visibleInGroupsList = schema.List(
        title = _(u"List of Groups that has this Playlist"),
        description = _(u"This is a list of the Groups that can show this playlist"),
        required = False,
        value_type  = schema.TextLine(title=u"Visible in Groups"),
        )

    #Amaguem els camps a l'edicio
    form.omitted('listToPlay','orderedList')




@grok.subscribe(IPlaylist, IObjectAddedEvent)
def copyToOrderedList(playlist, event):
    """
        Metode que afegeix un objecte a la llista que es pot ordenar de la Playlist
    """
    orderedlist = []
    order = 0
    for item in playlist.listToPlay:
        orderedlist.append([order, item.to_object.getId()])
        order += 1

    playlist.orderedList = orderedlist


#myct1.setMyReferenceField(areferenceableobject)
#myct1.getMyReferenceField()

def set(self, value):
    """
        Sets the relationship target. Monkeypatches issues in original
        RelationListDataManager where manager assumes that every object has
        intid.
    """

    value = value or []
    new_relationships = []
    intids = getUtility(IIntIds)
    for item in value:
        try:
            to_id = intids.getId(item)
        except KeyError:
            to_id = intids.register(item)
        new_relationships.append(RelationValue(to_id))
    super(RelationListDataManager, self).set(new_relationships)

RelationListDataManager.set = set




class View(grok.View):
    """
        Main View
    """
    grok.context(IPlaylist)
    grok.require('zope2.View')
    grok.name('view')




class updateList(grok.View):
    """
       View for the updateList Method
    """

    grok.context(IPlaylist)
    grok.require('zope2.View')
    grok.name('updateList')

    def update(self):
        context = self.context
        newOrder = self.request.get('order')
        oldList = context.orderedList
        newList = []
        for element in newOrder:
            for oldElement in oldList:
                if str(element) == str(oldElement[0]):
                    newList.append(oldElement)

        if newList != []:
            context.orderedList = newList

            #Check if we have removed elements from the list 
            #then we update the listToPlay reference field
            if (len(newList) != len(oldList)):
                idsList = []
                for i in newList:
                    idsList.append(i[1])

                newRelationList = []

                for item in context.listToPlay:
                    if item.to_object.id in idsList:
                        newRelationList.append(item)

                context.listToPlay = newRelationList

 
    def render(self):
        print 'orderedList field Updated.'



"""
class AddForm(dexterity.AddForm):

    grok.name('fatac.playlist')

    schema = IPlaylist
    

    def update(self):
        DefaultAddForm.update(self)

    def getBlockPlanJSON():
        return getBlockPlanJSON()


class AddView(DefaultAddView):
    form = AddForm
"""