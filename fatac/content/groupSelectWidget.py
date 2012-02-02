import z3c.form.interfaces
import z3c.form.browser.textarea
import z3c.form.widget
from z3c.form import datamanager, interfaces, button, widget
from z3c.form.widget import MultiWidget
from zope import interface, component, schema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from operator import attrgetter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

"""
    * GroupSelecion Widget:
      Widget per a seleccionar els grups en els que es pot mostrar la Playlist

    * Funcionament:
      Al template (groupSelectWidget.pt) es crea una llista oculta per poder fer
      el recompte d'objectes que s'han d'afegir al valor del camp. Per tant, tenim
      que hi ha una llista origen "From", una llista de desti "TO" on van els elements
      de la llista original, i tenim una serie d'imputs "hidden" que es generen/eliminen
      automaticament (des de JavaScript) un cop s'apreta qualsevol boto d'afegir o 
      treure elments de les llistes "FROM"(>>) i "TO"(<<).
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
    klass = u'textarea-widget'
    items = ()

    showLabel = True # show labels for item subwidgets or not

    # Internal attributes
    _adapterValueAttributes = widget.MultiWidget._adapterValueAttributes + \
        ('showLabel',)

    def update(self):
        """See z3c.form.interfaces.IWidget."""
        # Ensure that updateWidgets is called.
        super(MultiWidget, self).update()
        if not self._widgets_updated:
            self.updateWidgets()

    def render(self):
        """
            Retorna el Template del widget
        """
        return self.input_template(self)

    def extract(self):
        """
            Captura els valors del form que s'han de guardar (quan fas submit)
        """
        super(MultiWidget, self).extract()
        if self.request.get(self.name) != None:
            self.value = self.request.get(self.name)
            return self.value
        else:
            return []

    def selectedItems(self):
        """
            Retorna la llista/valor guardat del camp
        """
        context = self.context
        try:
            return self.field.get(context)
        except:
            return []

    def notSelectedItems(self):
        """
            Retorna la llista de grups que es poden afegir al camp
        """
        context = self.context
        mtool = getToolByName(context, 'portal_membership')
        gtool = getToolByName(context, 'portal_groups')

        member = mtool.getAuthenticatedMember();
        groups = gtool.getGroupsByUserId(member.getId());

        try:
            fieldValue = self.field.get(context)
        except:
            fieldValue = None
        nselItems = [] # Llista de grups per afegir

        # Si hi havien valors guardats els filtem
        if fieldValue != None:
            for group in groups:
                if group.getId() not in fieldValue:
                    nselItems.append(group)

            return nselItems
        else:
            return groups


@component.adapter(schema.interfaces.ITextLine, interfaces.IFormLayer)
@interface.implementer(interfaces.ITextLinesWidget)
def GroupsSelectionWidgetFactory(field, request):
    """TextLines factory for GroupsSelectionWidget."""
    return widget.FieldWidget(field, GroupsSelectionWidget(request))