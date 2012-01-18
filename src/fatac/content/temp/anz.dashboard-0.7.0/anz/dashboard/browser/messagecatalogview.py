# python
import cjson

# zope
from Products.Five import BrowserView

from zope.interface import implements
from zope.component import queryUtility, getUtility

from zope.i18n.interfaces import ITranslationDomain
from zope.i18n.interfaces import IFallbackTranslationDomainFactory
from zope.i18n.interfaces import INegotiator

# products
from anz.dashboard import MSG_FACTORY as _
from anz.dashboard.interfaces import IMessageCatalogView

class MessageCatalogView( BrowserView ):
    ''' Provide functions to return message catalog. '''
    
    implements( IMessageCatalogView )
    
    def catalogMapping( self, domain, retJson=True ):
        ''' Return message catalog as a mapping.
        
        @param domain
        domain of the message catalog
        
        @param retJson
        format return value to json format or not( default True )
        
        @return
        a dict with the following format:
        {
            'success': True,
            'msg': 'Get message catalog mapping success.',
            'mapping': {
                u'text1': u'translated text1',
                u'text2': u'translated text2',
                ...
            }
        }
        
        '''
        context = self.context
        request = self.request
        ret = {}
        
        try:
            texts = {}
            
            # first try to get a zope.i18n.TranslationDomain instance
            util = queryUtility( ITranslationDomain, domain )
            if util is None:
                util = queryUtility( IFallbackTranslationDomainFactory )
                if util is not None:
                    util = util( domain )
            
            if util is not None:
                langs = util._catalogs.keys()
                
                # invoke local or global unnamed 'INegotiator' utilities
                negotiator = getUtility( INegotiator )
                
                # try to determine target language from negotiator utility
                target_language = negotiator.getLanguage( langs, request )
                
                # Get the translation
                catalog_names = util._catalogs.get(target_language)
                if catalog_names:
                    if len(catalog_names) == 1:
                        # this is a slight optimization for the case when
                        # there is a single catalog.
                        if util._data[catalog_names[0]]._catalog is None:
                            util._data[catalog_names[0]].reload()
                        texts = util._data[catalog_names[0]]._catalog._catalog
                    else:
                        for name in catalog_names:
                            catalog = util._data[name]
                            if catalog._catalog is None:
                                catalog.reload()
                            texts = catalog._catalog._catalog
                            if texts:
                                break
            
            if texts:
                texts.update( {u'': 'META'} )
            
                ret['success'] = True
                ret['msg'] = _(u'Get message catalog mapping success.')
            else:
                ret['success'] = False
                ret['msg'] = _(u'Get message catalog mapping failure.')
            ret['texts'] = texts
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)
        
        return retJson and cjson.encode(ret) or ret
