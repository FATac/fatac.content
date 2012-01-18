# python
import pprint
from copy import deepcopy

# zope
from zope.interface import implements

# archetypes
from Products.Archetypes.public import *
from Products.Archetypes.utils import DisplayList

# atct
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema

# products
from anz.dashboard.config import PROJECTNAME
from anz.dashboard.interfaces import IDashboard
from anz.dashboard import MSG_FACTORY as _

DashboardSchema = ATContentTypeSchema.copy() + Schema((
	# provide a method to view and modify layout config
	StringField('config',
		widget=TextAreaWidget(
			lable='Config',
			description=_(u'debug only. do not touch this if you do not know detail about it.'),
			visible={'edit':'invisible', 'view':'invisible'},
			size=20)
	),
	StringField('pageLayout',
		default='tile',
		vocabulary=DisplayList((
			('tile', _(u'page_layout_tile', default='Tile mode')),
			('tab', _(u'page_layout_tab', default='Tab mode')),
			)),
		widget=SelectionWidget(
			label=_(u'label_page_layout_mode', default='Page layout mode'),
			description=_(u'help_page_layout_mode', default='''\
            You can choose 'tile mode' or
			'tab mode'. With 'tile mode', all pages are shown in one page, from
			top to bottom, it is useful for you to make very complex composite
			page. With 'tab mode', you can switch pages using the top tab
			links.'''),
			i18n_domain='anz.dashboard')
	),
	)
)

class Dashboard( ATCTContent ):
	''' Dashboard is a content type to build composite page. '''
	implements( IDashboard )
	
	schema = DashboardSchema
	portal_type = meta_type = 'Anz Dashboard'
	archetype_name = 'Anz Dashboard'
	
	defaultPageConfig =  {
		'columns': [],
		'title': 'untitled page',
		'width':'100%'
	}
	
	defaultColumnConfig = {
		'width': '0.5',
		'style': 'padding:5px 0 5px 5px',
		'widgets':[]
	}
	
	defaultWidgetCfg = {
		'id': '',
		'color': '',
		'style': '',
		'collapse': 0,
		'options': { 'title': 'Un-titled widget' }
	}
	
	def __init__( self, oid, **kw ):
		super(Dashboard, self).__init__(oid, **kw)
		self._layoutCfg = []
		
		# add a page with 2 columns default
		self._layoutCfg.append( deepcopy(self.defaultPageConfig) )
		self._layoutCfg[0]['columns'].append( deepcopy(self.defaultColumnConfig) )
		self._layoutCfg[0]['columns'].append( deepcopy(self.defaultColumnConfig) )
		
		self._p_changed = True
	
	def getConfig( self, retStr=True ):
		''' '''
		return retStr and pprint.pformat(self._layoutCfg) or self._layoutCfg

	def setConfig( self, value ):
		if value:
			value = value.replace('\n', ' ').replace('\r', '')
			self._layoutCfg = eval( value )

registerType( Dashboard, PROJECTNAME )
