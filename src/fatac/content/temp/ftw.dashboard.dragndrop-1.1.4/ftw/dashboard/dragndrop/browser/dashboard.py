from plone.app.layout.dashboard.dashboard import DashboardView


class FTWDashBoard(DashboardView):
    """ Improve the default Plone Dashboard """

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
        return getattr(self.context.portal_properties, 'ftw.dashboard', None)
