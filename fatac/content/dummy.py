from zope import schema
from plone.directives import form
from five import grok
from fatac.content import PlaylistMessageFactory as _
import json
from fatac.theme.browser.genericView import genericView


class IDummy(form.Schema):
    """ Dummy Schema
    """

    tagList = schema.List(
        title=_(u"Tag List"),
        description=_(u"This is a list of tags that have this image"),
        default=[],
        value_type=schema.TextLine(),
        required=False,
        )


class View(grok.View, genericView):
    """ Main View
    """
    grok.context(IDummy)
    grok.require('zope2.View')
    grok.name('view')
    #grok.template("dummy_view")

    def __init__(self, context, request):
        super(grok.View, self).__init__(context, request)
        super(genericView, self).__init__(context, request)


class loadTags(grok.View):
    """ Metode que retorna els tags
    """
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
    """ Metode que guarda els Tags
    """

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
    """ Metode que elimina el Tag
    """

    grok.context(IDummy)
    grok.require('zope2.View')
    grok.name('deleteTag')

    def render(self):
        print "Delete Tag!"
        return """ """
