# -*- encoding: utf-8 -*-

from zope.interface import implements
from interfaces import IPortalUser
from plone.app.portlets.interfaces import IDefaultDashboard
from plone.app.portlets.dashboard import DefaultDashboard
from plone.app.portlets import portlets
from plone.app.layout.dashboard.dashboard import DashboardView
from plone.app.controlpanel.interfaces import IPloneControlPanelView
from plone.app.controlpanel.security import ISecuritySchema
from Products.Five.browser import BrowserView
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from ZTUtils import make_query
from Products.PluggableAuthService.interfaces.plugins import IRolesPlugin
from zope.component import adapts, getAdapter, getMultiAdapter
from itertools import chain
from AccessControl import getSecurityManager
from Products.CMFCore.permissions import ManagePortal
from plone.protect import CheckAuthenticator
from Products.CMFPlone import PloneMessageFactory as _
from five import grok
from Products.CMFPlone.utils import normalizeString
from Products.statusmessages.interfaces import IStatusMessage
from zExceptions import Forbidden

from fatac.content import portletPlaylists, portletMyFiles, portletMyGroups
from fatac.core.utils import crearObjecte


class FatacPortalDefaultDashboard(DefaultDashboard):
    """ A new custom default dashboard for users.
    """
    implements(IDefaultDashboard)
    adapts(IPortalUser)

    def __call__(self):
        #news = portlets.news.Assignment()
        recent = portlets.recent.Assignment()
        calendar = portlets.calendar.Assignment()
        #search = portlets.search.Assignment()
        playlists = portletPlaylists.Assignment()
        mygroups = portletMyGroups.Assignment()
        myfiles = portletMyFiles.Assignment()

        return {
            'plone.dashboard1': (playlists,),
            'plone.dashboard2': (recent,),
            'plone.dashboard3': (mygroups,),
            'plone.dashboard4': (calendar, myfiles),
        }


class FatacDashboardCommon(BrowserView):

    def searchPlaylistsResults(self, groupmembers, groupname):
        context = self.context
        pc = getToolByName(context, 'portal_catalog')
        results = pc.searchResults(portal_type='fatac.playlist',
                                   originalGroup=groupname,
                                   Creator=groupmembers,
                                   sort_on='modified',
                                   sort_order='reverse',)
        return results

    def searchActivityResults(self, groupmembers, groupname):
        context = self.context
        pc = getToolByName(context, 'portal_catalog')
        results = pc.searchResults(portal_type=['fatac.playlist', 'plone.Comment'],
                                                      originalGroup=groupname,
                                                      Creator=groupmembers,
                                                      sort_on='modified',
                                                      sort_order='reverse',)
        return results

    def retornaCountGroupMembers(self, groupname):
        gtool = getToolByName(self.context, 'portal_groups')
        group = gtool.getGroupById(groupname)
        members = group.getGroupMembers()
        return len(members)

    def retornaCountGroupPlaylists(self, groupmembers, groupname):
        return len(self.searchPlaylistsResults(groupmembers, groupname))

    def retornaCountGroupActivity(self, groupmembers, groupname):
        return len(self.searchActivityResults(groupmembers, groupname))


class FatacDashBoard(DashboardView):
    """ Improve the default Plone Dashboard
    """

    #__call__ = ViewPageTemplateFile('templates/filtresview.pt')

    def registered_portlelts(self):
        """ Returns the registered portlets in a list with 2 item tuple
        [('id', 'user friendly'), ( 'id2', 'Another Portlet')] """
        props = self.dashboard_props()
        ret = []
        if props:
            portlets = props.addable_portlets
            for portlet in portlets:
                if ':' in portlet:
                    parts = portlet.split(':')
                    id_ = parts[0]
                    title = ''.join(parts[1:])
                else:
                    id_ = title = portlet
                ret.append(dict(id=id_, title=title))
        return ret

    def dashboard_props(self):
        return getattr(self.context.portal_properties, 'fatac.dashboard', None)

    def retornaCountGrups(self, memberid):
        gtool = getToolByName(self.context, 'portal_groups')
        mgroups = gtool.getGroupsByUserId(memberid)
        if len(mgroups) > 0:
            return len(mgroups) - 1  # For not to count the built-in "Authenticated Users"
        else:
            return len(mgroups)  # I'm Zope admin and I have no built-in groups

    def retornaCountPlaylists(self, memberid):
        catalog = getToolByName(self.context, 'portal_catalog')
        playlists = catalog.searchResults(portal_type='fatac.playlist', Creator=memberid)
        return len(playlists)

    def retornaCountActivitat(self, memberid):
        catalog = getToolByName(self.context, 'portal_catalog')
        activitat = catalog.searchResults(portal_type=['fatac.playlist', 'File', 'plone.Comment'], Creator=memberid)
        return len(activitat)

    def retornaCountGroupMembers(self, groupname):
        gtool = getToolByName(self.context, 'portal_groups')
        group = gtool.getGroupById(groupname)
        members = group.getGroupMembers()
        return len(members)

    def retornaCountGroupPlaylists(self, groupname):
        gtool = getToolByName(self.context, 'portal_groups')
        group = gtool.getGroupById(groupname)
        members = group.getGroupMembers()
        catalog = getToolByName(self.context, 'portal_catalog')
        playlists = catalog.searchResults(portal_type='fatac.playlist', Creator=members)
        return len(playlists)

    def retornaCountGroupActivity(self, groupname):
        gtool = getToolByName(self.context, 'portal_groups')
        group = gtool.getGroupById(groupname)
        members = group.getGroupMembers()
        catalog = getToolByName(self.context, 'portal_catalog')
        activitat = catalog.searchResults(portal_type=['fatac.playlist', 'plone.Comment'], Creator=members)
        return len(activitat)

    def retornaPlaylists(self):
        """ retorna una llista de diccionaris amb títol, descripció, url, i
        llista de ids de totes les playlists creades per l'usuari
        """

        llistat = []
        mt = getToolByName(self.context, 'portal_membership')
        if not mt.isAnonymousUser():  # the user has not logged in
            member = mt.getAuthenticatedMember()
        playlists = self.context.portal_catalog.searchResults(portal_type='fatac.playlist',
                                                              Creator=member.getId(),
                                                              sort_on='modified',
                                                              sort_order='reverse')
        for playlist in playlists:
            obj = playlist.getObject()
            # passem de [[0, 'id1'], [1, 'id2'], [2, 'id3'], ...] a 'id1,id2,id3,id4'
            ids = ','.join([a[1] for a in obj.orderedList])
            dada = {'nom': playlist.id, 'tipus': 'objects', 'valor': ids}
            llistat.append({'titol': playlist.Title,
                            'id': playlist.id,
                            'descripcio': playlist.Description,
                            'url': playlist.getURL(),
                            'dada': dada})

        return llistat

    def returnUserPlaylists(self):
        pc = getToolByName(self.context, 'portal_catalog')
        portal_state = getMultiAdapter((self.context, self.request), name="plone_portal_state")
        member = portal_state.member()
        playlist_search = pc.searchResults(portal_type='fatac.playlist',
                                             Creator=member.getId(),
                                             sort_on='modified',
                                             sort_order='reverse',)
        playlists = []
        for playlist in playlist_search:
            obj = playlist.getObject()
            playlists.append(dict(id=playlist.id,
                                 Title=playlist.Title,
                                 objects=','.join([a[1] for a in sorted(obj.orderedList, key=lambda x: x[0])]))
                                )
        return playlists


class groupActivity(FatacDashboardCommon):
    """ Returns The group activity content
    """


class groupPlaylists(FatacDashboardCommon):
    """ View related group-playlists.pt """


class deleteUserGroup(grok.View):
    """ View for deleting Group of the User
    """
    grok.context(FatacPortalDefaultDashboard)
    grok.require('zope2.View')
    grok.name('deleteUserGroup')

    def update(self):
        groupId = self.request.get('groupId')

        if groupId != None:
            #Get the current member
            mt = getToolByName(self.context, 'portal_membership')
            if not mt.isAnonymousUser():  # the user has not logged in
                member = mt.getAuthenticatedMember()
                username = member.getUserName()

                #if not member.canAdministrateGroup():
                #    raise Unauthorized, "You cannot remove a member from the group."

                # If user can remove from Group -> Remove User From Group
                if member.canRemoveFromGroup(groupId):
                    gtool = getToolByName(self.context, 'portal_groups')
                    gtool.removePrincipalFromGroup(member.getId(), groupId)
                    self.context.plone_utils.addPortalMessage(_(u'Changes made.'))
                    print 'User ' + username + ' deleted from Group: ' + groupId
        else:
            print 'No group ID'

    def render(self):
        #Get the current member
        mt = getToolByName(self.context, 'portal_membership')
        if mt.isAnonymousUser():  # the user has not logged in
            print 'User not logged in (deleteUserGroup)'


class ControlPanelView(BrowserView):
    """ A simple view to be used as a basis for control panel screens.
    """

    implements(IPloneControlPanelView)


class UsersGroupsControlPanelView(ControlPanelView):

    @property
    def portal_roles(self):
        pmemb = getToolByName(aq_inner(self.context), 'portal_membership')
        return [r for r in pmemb.getPortalRoles() if r != 'Owner']

    @property
    def many_users(self):
        pprop = getToolByName(aq_inner(self.context), 'portal_properties')
        return pprop.site_properties.many_users

    @property
    def many_groups(self):
        pprop = getToolByName(aq_inner(self.context), 'portal_properties')
        return pprop.site_properties.many_groups

    @property
    def email_as_username(self):
        return getAdapter(aq_inner(self.context), ISecuritySchema).get_use_email_as_login()

    def makeQuery(self, **kw):
        return make_query(**kw)

    def membershipSearch(self, searchString='', searchUsers=True, searchGroups=True, ignore=[]):
        """ Search for users and/or groups, returning actual member and group items
            Replaces the now-deprecated prefs_user_groups_search.py script
        """
        groupResults = userResults = []

        gtool = getToolByName(self, 'portal_groups')
        mtool = getToolByName(self, 'portal_membership')

        searchView = getMultiAdapter((aq_inner(self.context), self.request), name='pas_search')

        if searchGroups:
            groupResults = searchView.merge(chain(*[searchView.searchGroups(**{field: searchString}) for field in ['id', 'title']]), 'groupid')
            groupResults = [gtool.getGroupById(g['id']) for g in groupResults if g['id'] not in ignore]
            groupResults.sort(key=lambda x: x is not None and normalizeString(x.getGroupTitleOrName()))

        if searchUsers:
            userResults = searchView.merge(chain(*[searchView.searchUsers(**{field: searchString}) for field in ['login', 'fullname', 'email']]), 'userid')
            userResults = [mtool.getMemberById(u['id']) for u in userResults if u['id'] not in ignore]
            userResults.sort(key=lambda x: x is not None and x.getProperty('fullname') is not None and normalizeString(x.getProperty('fullname')) or '')

        return groupResults + userResults

    def atoi(self, s):
        try:
            return int(s)
        except ValueError:
            return 0

    @property
    def is_zope_manager(self):
        return getSecurityManager().checkPermission(ManagePortal, self.context)

    # The next two class methods implement the following truth table:
    #
    # MANY USERS/GROUPS SEARCHING       CAN LIST USERS/GROUPS   RESULT
    # False             False           False                   Lists unavailable
    # False             False           True                    Show all
    # False             True            False                   Show matching
    # False             True            True                    Show matching
    # True              False           False                   Too many to list
    # True              False           True                    Lists unavailable
    # True              True            False                   Show matching
    # True              True            True                    Show matching

    # TODO: Maybe have these methods return a text message (instead of a bool)
    # corresponding to the actual result, e.g. "Too many to list", "Lists unavailable"

    @property
    def show_group_listing_warning(self):
        if not self.searchString:
            acl = getToolByName(self, 'acl_users')
            if acl.canListAllGroups():
                if self.many_groups:
                    return True
        return False

    @property
    def show_users_listing_warning(self):
        if not self.searchString:
            acl = getToolByName(self, 'acl_users')
            # XXX Huh? Is canListAllUsers broken?
            if not acl.canListAllUsers():
                if self.many_users:
                    return True
        return False


class ManageGroupsPanel(UsersGroupsControlPanelView):

    def __call__(self):
        form = self.request.form
        submitted = form.get('form.submitted', False)
        search = form.get('form.button.Search', None) is not None
        findAll = form.get('form.button.FindAll', None) is not None
        self.searchString = not findAll and form.get('searchstring', '') or ''
        self.searchResults = []
        self.newSearch = False

        if search or findAll:
            self.newSearch = True

        if submitted:
            if form.get('form.button.Modify', None) is not None:
                self.manageGroup([group[len('group_'):] for group in self.request.keys() if group.startswith('group_')],
                                 form.get('delete', []))

        # Only search for all ('') if the many_users flag is not set.
        if not(self.many_groups) or bool(self.searchString):
            self.searchResults = self.doSearch(self.searchString)

        return self.index()

    def doSearch(self, searchString):
        """ Search for a group by id or title
        """
        acl = getToolByName(self, 'acl_users')
        rolemakers = acl.plugins.listPlugins(IRolesPlugin)

        searchView = getMultiAdapter((aq_inner(self.context), self.request), name='pas_search')

        # First, search for inherited roles assigned to each group.
        # We push this in the request so that IRoles plugins are told provide
        # the roles inherited from the groups to which the principal belongs.
        self.request.set('__ignore_group_roles__', False)
        self.request.set('__ignore_direct_roles__', True)
        inheritance_enabled_groups = searchView.merge(chain(*[searchView.searchGroups(**{field: searchString}) for field in ['id', 'title']]), 'id')
        allInheritedRoles = {}
        for group_info in inheritance_enabled_groups:
            groupId = group_info['id']
            group = acl.getGroupById(groupId)
            group_info['title'] = group.getProperty('title', group_info['title'])
            allAssignedRoles = []
            for rolemaker_id, rolemaker in rolemakers:
                allAssignedRoles.extend(rolemaker.getRolesForPrincipal(group))
            allInheritedRoles[groupId] = allAssignedRoles

        # Now, search for all roles explicitly assigned to each group.
        # We push this in the request so that IRoles plugins don't provide
        # the roles inherited from the groups to which the principal belongs.
        self.request.set('__ignore_group_roles__', True)
        self.request.set('__ignore_direct_roles__', False)
        explicit_groups = searchView.merge(chain(*[searchView.searchGroups(**{field: searchString}) for field in ['id', 'title']]), 'id')

        # Tack on some extra data, including whether each role is explicitly
        # assigned ('explicit'), inherited ('inherited'), or not assigned at all (None).
        results = []
        for group_info in explicit_groups:
            groupId = group_info['id']
            group = acl.getGroupById(groupId)
            group_info['title'] = group.getProperty('title', group_info['title'])

            explicitlyAssignedRoles = []
            for rolemaker_id, rolemaker in rolemakers:
                explicitlyAssignedRoles.extend(rolemaker.getRolesForPrincipal(group))

            roleList = {}
            for role in self.portal_roles:
                canAssign = group.canAssignRole(role)
                if role == 'Manager' and not self.is_zope_manager:
                    canAssign = False
                roleList[role] = {'canAssign': canAssign,
                                'explicit': role in explicitlyAssignedRoles,
                                'inherited': role in allInheritedRoles[groupId]}

            canDelete = group.canDelete()
            if roleList['Manager']['explicit'] or roleList['Manager']['inherited']:
                if not self.is_zope_manager:
                    canDelete = False

            group_info['roles'] = roleList
            group_info['can_delete'] = canDelete
            results.append(group_info)
        # Sort the groups by title
        sortedResults = searchView.sort(results, 'title')

        # Reset the request variable, just in case.
        self.request.set('__ignore_group_roles__', False)
        return sortedResults

    def manageGroup(self, groups=[], delete=[]):
        CheckAuthenticator(self.request)
        context = aq_inner(self.context)

        groupstool = context.portal_groups
        utils = getToolByName(context, 'plone_utils')
        groupstool = getToolByName(context, 'portal_groups')

        message = _(u'No changes made.')

        for group in groups:
            roles = [r for r in self.request.form['group_' + group] if r]
            group_obj = groupstool.getGroupById(group)
            current_roles = group_obj.getRoles()
            if not self.is_zope_manager:
                # don't allow adding or removing the Manager role
                if ('Manager' in roles) != ('Manager' in current_roles):
                    raise Forbidden

            groupstool.editGroup(group, roles=roles, groups=())
            message = _(u'Changes saved.')

        if delete:
            for group_id in delete:
                group = groupstool.getGroupById(group_id)
                if 'Manager' in group.getRoles() and not self.is_zope_manager:
                    raise Forbidden

            groupstool.removeGroups(delete)
            message = _(u'Group(s) deleted.')

        utils.addPortalMessage(message)


class UserMembershipControlPanel(UsersGroupsControlPanelView):

    def update(self):
        self.gtool = getToolByName(self, 'portal_groups')
        self.mtool = getToolByName(self, 'portal_membership')

        if not self.mtool.isAnonymousUser():  # the user has not logged in
            self.member = self.mtool.getAuthenticatedMember()
            self.userid = self.member.getId()

            form = self.request.form
            findMembers = self.request.get('fm')

            self.searchResults = []
            self.searchString = ''
            self.newSearch = False

            if form.get('form.submitted', False):
                if findMembers:
                    groupname = form.get('groupname', None)
                    delete = form.get('delete', [])
                    if delete:
                        for userid in delete:
                            self.gtool.removePrincipalFromGroup(userid, groupname, self.request)
                        self.context.plone_utils.addPortalMessage(_(u'Changes made.'))

                    add = form.get('add', [])
                    if add:
                        for userid in add:
                            member = self.mtool.getMemberById(userid)
                            if 'Manager' in member.getRoles() and not self.is_zope_manager:
                                raise Forbidden

                            self.gtool.addPrincipalToGroup(userid, groupname, self.request)
                        self.context.plone_utils.addPortalMessage(_(u'Changes made.'))
                else:
                    delete = form.get('delete', [])
                    if delete:
                        for groupname in delete:
                            self.gtool.removePrincipalFromGroup(self.userid, groupname, self.request)
                        self.context.plone_utils.addPortalMessage(_(u'Changes made.'))

                    add = form.get('add', [])
                    if add:
                        for groupname in add:
                            group = self.gtool.getGroupById(groupname)
                            if 'Manager' in group.getRoles() and not self.is_zope_manager:
                                raise Forbidden

                            self.gtool.addPrincipalToGroup(self.userid, groupname, self.request)
                        self.context.plone_utils.addPortalMessage(_(u'Changes made.'))

            search = form.get('form.button.Search', None) is not None
            findAll = form.get('form.button.FindAll', None) is not None and not self.many_groups

            self.searchString = not findAll and form.get('searchstring', '') or ''

            if findMembers:
                if findAll or not self.many_users or self.searchString != '':
                    self.searchResults = self.getPotentialMembers(self.searchString)
            else:
                if findAll or not self.many_groups or self.searchString != '':
                    grupsPotencials = self.getPotentialGroups(self.searchString)
                    if (grupsPotencials != None and grupsPotencials != []):
                        for grup in grupsPotencials:
                            if grup.getId() not in ["Administrators", "Site Administrators"]:
                                self.searchResults.append(grup)
                    else:
                        self.searchResults = grupsPotencials

            if search or findAll:
                self.newSearch = True

            self.groups = self.getGroups()

    def __call__(self):
        self.update()
        return self.index()

    def getGroups(self):
        groupResults = [self.gtool.getGroupById(m) for m in self.gtool.getGroupsForPrincipal(self.member)]
        groupResults.sort(key=lambda x: x is not None and normalizeString(x.getGroupTitleOrName()))
        return filter(None, groupResults)

    def getPotentialGroups(self, searchString):
        ignoredGroups = [x.id for x in self.getGroups() if x is not None]
        return self.membershipSearch(searchString, searchUsers=False, ignore=ignoredGroups)

    def getPotentialMembers(self, searchString):
        ignoredGroups = [x.id for x in self.getGroups() if x is not None]
        return self.membershipSearch(searchString, searchUsers=True, searchGroups=False, ignore=ignoredGroups)

    def retornaCountGrups(self, memberid):
        gtool = getToolByName(self.context, 'portal_groups')
        mgroups = gtool.getGroupsByUserId(memberid)
        if len(mgroups) > 0:
            return len(mgroups) - 1  # For not to count the built-in "Authenticated Users"
        else:
            return len(mgroups)  # I'm Zope admin and I have no built-in groups

    def retornaCountPlaylists(self, memberid):
        catalog = getToolByName(self.context, 'portal_catalog')
        playlists = catalog.searchResults(portal_type='fatac.playlist', Creator=memberid)
        return len(playlists)

    def retornaCountActivitat(self, memberid):
        catalog = getToolByName(self.context, 'portal_catalog')
        activitat = catalog.searchResults(portal_type=['fatac.playlist', 'File'], Creator=memberid)
        return len(activitat)

    def retornaCountGroupMembers(self, groupname):
        gtool = getToolByName(self.context, 'portal_groups')
        group = gtool.getGroupById(groupname)
        members = group.getGroupMembers()
        return len(members)

    def retornaCountGroupPlaylists(self, groupname):
        gtool = getToolByName(self.context, 'portal_groups')
        group = gtool.getGroupById(groupname)
        members = group.getGroupMembers()
        catalog = getToolByName(self.context, 'portal_catalog')
        playlists = catalog.searchResults(portal_type='fatac.playlist', Creator=members)
        return len(playlists)

    def retornaCountGroupActivity(self, groupname):
        gtool = getToolByName(self.context, 'portal_groups')
        group = gtool.getGroupById(groupname)
        members = group.getGroupMembers()
        catalog = getToolByName(self.context, 'portal_catalog')
        activitat = catalog.searchResults(portal_type=['fatac.playlist', 'plone.Comment'], Creator=members)
        return len(activitat)


class GroupDetailsControlPanel(UsersGroupsControlPanelView):

    #index = ViewPageTemplateFile('browser/usergroups_groupdetails.pt')

    def __call__(self):

        context = aq_inner(self.context)
        ploneview = getMultiAdapter((self.context, self.request), name=u'plone')

        self.gtool = getToolByName(context, 'portal_groups')
        self.gdtool = getToolByName(context, 'portal_groupdata')
        self.regtool = getToolByName(context, 'portal_registration')
        self.groupname = getattr(self.request, 'groupname', None)
        self.grouproles = self.request.set('grouproles', [])
        self.group = self.gtool.getGroupById(self.groupname)
        self.grouptitle = self.groupname
        if self.group is not None:
            self.grouptitle = self.group.getGroupTitleOrName()

        self.request.set('grouproles', self.group.getRoles() if self.group else [])

        flagAdded = False

        submitted = self.request.form.get('form.submitted', False)
        if submitted:
            CheckAuthenticator(self.request)

            msg = _(u'No changes made.')
            self.group = None

            title = self.request.form.get('title', None)
            description = self.request.form.get('description', None)

            #addname = self.request.form.get('addname', None)
            addname = ploneview.normalizeString(title)

            if addname:
                if not self.regtool.isMemberIdAllowed(addname):
                    msg = _(u'The group name you entered is not valid.')
                    IStatusMessage(self.request).add(msg, 'error')
                    return self.index()

                success = self.gtool.addGroup(addname, (), (), title=title,
                                              description=description,
                                              REQUEST=self.request)
                if not success:
                    msg = _(u'Could not add group ${name}, perhaps a user or group with '
                            u'this name already exists.', mapping={u'name': addname})
                    IStatusMessage(self.request).add(msg, 'error')
                    return self.index()
                else:
                    portal = getToolByName(self, 'portal_url').getPortalObject()
                    # Si no existeix la carpeta de grup la creem
                    if addname not in portal.Groups.objectIds():
                        crearObjecte(portal.Groups, addname, 'Folder', title, description)
                        newgroup = portal.Groups[addname]
                        # Giving the group permissions to the recently created folder
                        newgroup.manage_setLocalRoles(addname, ['Owner'])
                        newgroup.indexObject()

                    # Afegim el creador a la llista de managers del grup
                    flagAdded = True

                self.group = self.gtool.getGroupById(addname)
                msg = _(u'Group ${name} has been added.',
                        mapping={u'name': addname})

            elif self.groupname:
                self.gtool.editGroup(self.groupname, roles=None, groups=None,
                                     title=title, description=description,
                                     REQUEST=context.REQUEST)
                self.group = self.gtool.getGroupById(self.groupname)
                msg = _(u'Changes saved.')

            else:
                msg = _(u'Group name required.')

            processed = {}
            for id, property in self.gdtool.propertyItems():
                processed[id] = self.request.get(id, None)

            if self.group:
                # Si hem creat un nou grup, afegim a l'usuari en la llista i dins del grup per defecte
                if flagAdded:
                    self.mtool = getToolByName(context, 'portal_membership')
                    self.userid = self.mtool.getAuthenticatedMember().getId()
                    processed['delegated_group_member_managers'] = [self.userid]
                    self.gtool.addPrincipalToGroup(self.userid, self.group.getId(), self.request)
                    context.plone_utils.addPortalMessage(_(u'Changes made.'))
                self.group.setGroupProperties(processed)

            IStatusMessage(self.request).add(msg, type=self.group and 'info' or 'error')
            if self.group and not self.groupname:
                target_url = '%s/%s' % (self.context.absolute_url(), '@@manage-groups')
                self.request.response.redirect(target_url)
                return ''

        return self.index()

    def getCreateGroupFields(self):
        """ Rearrange and choose the fields we want to be shown when creating a group"""
        context = aq_inner(self.context)
        self.gdtool = getToolByName(context, 'portal_groupdata')
        fields = [fields for fields in self.gdtool.propertyMap() if fields['id'] != 'email']
        return tuple(fields)
