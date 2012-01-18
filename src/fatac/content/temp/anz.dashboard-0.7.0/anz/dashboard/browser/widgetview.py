# python
import cjson

# zope
from Products.Five import BrowserView
from zope.interface import implements
from Acquisition import aq_parent, aq_inner, aq_base
from zope.i18n import translate

# cmf
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.ActionInformation import ActionInfo

# plone
from Products.CMFPlone.PloneBaseTool import getExprContext

# products
from anz.dashboard.interfaces import IWidgetView
from anz.dashboard import MSG_FACTORY as _

class WidgetView( BrowserView ):
	'''  '''
	implements( IWidgetView )
	
	def __init__( self, context, request ):
		super( WidgetView, self ).__init__( context, request )
		self.ec = getExprContext( context, object=None )
	
	def getWidgets( self,
					check_visibility=True,
					check_permissions=True,
					check_condition=True,
					retJson=True
					):
		''' Return a sequence of registered widgets' information.
        
        @param check_visibility
        if True, return only actions whose "visible" flag is set.
        
        @param check_permissions
        if True, return only actions for whose permissions the current user is
        authorized.
        
        @param check_condition
        if True, return only actions whose condition expression evaluates True.
        
        @param retJson
        format return value to json format or not
        
        @return
        a dict with widgets' information, format like:
        {
            'success': True,
            'msg': 'Get widgets success.',
            'widgets': [{
                'id': '',
                'title': '',
                'desc': '',
                'icon': ''
                },
                ...
                ]
        }
        '''
		context = self.context
		request = self.request
		ret = {}
		ret['widgets'] = []
		
		try:
			action_infos = self._getActions(
				check_visibility=check_visibility,
				check_permissions=check_permissions,
				check_condition=check_condition
				)
			
			for ai in action_infos:
				item = {}
				item['id'] = ai['id']
				item['title'] = translate( ai['title'], context=request )
				item['desc'] = translate( ai['description'], context=request )
				item['icon'] = ai['icon']
				
				ret['widgets'].append( item )
			
			ret['success'] = True
			ret['msg'] = translate( _(u'Get widgets success.'),
									context=request )
		except Exception, e:
			ret['success'] = False
			ret['msg'] = str(e)
		
		return retJson and cjson.encode(ret) or ret
	
	def getWidget( self,
				   id,
				   check_visibility=True,
				   check_permissions=True,
				   check_condition=True,
				   retJson=True
				   ):
		''' Return the specific widget's information.
		
		@param id
		id of the wanted widget
		
		@param check_visibility
        if True, return only action whose "visible" flag is set.
		
		@param check_permissions
        if True, return only action for whose permissions the current user is
		authorized.
		
		@param check_condition
        if True, return only action whose condition expression evaluates True.
        
        @param retJson
		format return value to json format or not
		
		@return
		a dict with the following format:
		{
		    'success': True,
			'msg': 'Get widget success.',
		    'id': '',
			'title': '',
			'desc': '',
			'icon': ''
		}
		
		'''
		context = self.context
		request = self.request
		ret = {}
		
		widgets = self.getWidgets( check_visibility=check_visibility,
								   check_permissions=check_permissions,
								   check_condition=check_condition,
								   retJson=False
								   )['widgets']
		
		for w in widgets:
			if w['id'] == id:
				ret['success'] = True
				ret['msg'] = translate( _(u'Get widget success.'),
										context=request )
				ret.update( w )
				break
		else:
			ret['success'] = False
			ret['msg'] = translate( _(u'No widget with id "${id}" found.'),
									mapping={'id':id},
									context=request )
		
		return retJson and cjson.encode(ret) or ret

	def _getActions( self,
					 check_visibility=True,
					 check_permissions=True,
					 check_condition=True
					 ):
		ret = []
		
		pa = getToolByName( self.context, 'portal_actions' )
		category = getattr( aq_inner(pa), 'dashboard_widgets', None )
		if category is not None:
			for action in category.listActions():
				ai = ActionInfo( action, self.ec )
				
				if check_visibility and not ai['visible']:
					continue
				if check_permissions and not ai['allowed']:
					continue
				if check_condition and not ai['available']:
					continue
				
				ret.append( ai )
		
		return ret