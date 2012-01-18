Introduction
============

The ftw.dashboard.dragndrop - packet add persistent dragndrop functionality to standard plone dashboard.
Additional it add icons for fold, edit and close/remove functionality

How to use ftw.dashboard.dragndrop
==================================

1.) Install the ftw.dashboard.dragndrop product with the portal_setup tool.

2.) Customize the properties (addablePortlets)

3.) Use

Properties:
-----------

dashboardEditable: 
True: the dashboard allways show in the editmode, all functionalities are available 
False: in the standard view (/dashboard) only the dragndrop and the fold functionality are available. In the manage-dashbord View all functionalities are available  

columnNumber: 
Number of Dashboard-Columns. 
(if more than 4 columns, you have to added a new PortletManger)

addablePortlets: 
the portlets wich show in the add portlet Dropdown
You can use "portlet.Calendar" or "portlet.Calendar:Portlet Calendar", after colon is a user friendly name - added in release 1.1

Provided features:
==================

ftw.dashboard.dragndrop provides the following features:

persistent dragndrop
    all portlets can moved with dragndrop functionality from column to column and also in the column
persistent fold:
    all portlets have an icon on the top (triangle) wich provide the persistent fold function
edit portlet 
    all portlets have an icon on the top (pensil) wich links to the respective Edit Page.
close/remove portlet
    all portlets have an icon on the top (cross) wich remove the respective portlet from the dashboard

Copyright and credits
=====================

ftw.dashboard.dragndrop is copyright 2009 by 4teamwork_ , and is licensed under the GPL. See LICENSE.txt for details.

.. _4teamwork: http://www.4teamwork.ch/
