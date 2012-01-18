import z3c.form.interfaces
import z3c.form.browser.textarea
import z3c.form.widget
from z3c.form import datamanager, interfaces, button, widget
from z3c.form.widget import MultiWidget
from zope import interface, component, schema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from operator import attrgetter

from Products.CMFDynamicViewFTI.interfaces import IBrowserDefault
from five import grok
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.dexterity.browser.view import DefaultView

"""
    GroupSelecion Widget:
    Widget per a seleccionar els grups en els que es pot mostrar la Playlist
"""

class IGroupsSelectionWidget(interfaces.IMultiWidget):
    """Groups Selection widget."""

class GroupsSelectionWidget(MultiWidget):
    """This grid should be applied to an schema.List item which has
    schema.Object and an interface"""

    interface.implements(IGroupsSelectionWidget)
    input_template = ViewPageTemplateFile('browser/groupSelectWidget.pt')
    buttons = button.Buttons()

    prefix = 'widget'
    klass = u'multi-widget'
    items = ()

    showLabel = True # show labels for item subwidgets or not

    # Internal attributes
    _adapterValueAttributes = widget.MultiWidget._adapterValueAttributes + \
        ('showLabel',)


    #def updateActions(self):
    #    self.updateAllowAddRemove()
    #    if self.name is not None:
    #        self.prefix = self.name
    #    self.actions = component.getMultiAdapter(
    #        (self, self.request, self), interfaces.IActions)
    #    self.actions.update()


    def update(self):
        print self.value
        """See z3c.form.interfaces.IWidget."""
        # Ensure that updateWidgets is called.
        super(MultiWidget, self).update()
        if not self._widgets_updated:
            self.updateWidgets()

    def render(self):
        return self.input_template(self)
        

    #def setField(self, value):
        """
            The field information is passed to the widget after it is
            initialised.  Use this call to initialise the column
            definitions.
        """
        """
        self._field = value
        print "setfield"

        self.columns = []
        for name, field in getFieldsInOrder(self._field.value_type.schema):
            col = {
                'name': name,
                'label': field.title,
                'required': field.required,
                'mode': None,
            }
            self.columns.append(col)
        """


    #def getWidget(self, idx):
        """Create the object widget. This is used to avoid looking up
        the widget.
        """
        """
        valueType = self.field.value_type
        widget = component.getMultiAdapter((valueType, self.request), interfaces.ITextLinesWidget)

        widget.__parent__ = self

        widget.mode = self.mode
        widget.klass = 'groupselection-row'
        #set widget.form (objectwidget needs this)
        if interfaces.IFormAware.providedBy(self):
            widget.form = self.form
            interface.alsoProvides(
                widget, interfaces.IFormAware)
        widget.update()
        print "getWidget"
        return widget
        """

    #def updateWidgets(self):
        # if the field has configuration data set - copy it
    #    print "updateWidgets"
    #    super(GroupsSelectionWidget, self).updateWidgets()

    #def get(self, request):
    #    print "get"
    #    return self.field


@component.adapter(schema.interfaces.ITextLine, interfaces.IFormLayer)
@interface.implementer(interfaces.ITextLinesWidget)
def GroupsSelectionWidgetFactory(field, request):
    """TextLines factory for GroupsSelectionWidget."""
    return widget.FieldWidget(field, GroupsSelectionWidget(request))