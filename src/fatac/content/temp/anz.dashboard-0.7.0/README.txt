=====================
 anz.dashboard README
=====================

:author:    jiangdongjin
:contact:   eastxing@gmail.com
:date:      2010/09/27
:abstract: This is a netvibes and iGoogle like dashboard implementation on
           Plone.

.. contents::
.. sectnum::

Introduction
============
anz.dashboard is a netvibes and iGoogle like dashboard implementation.

Overview
========
anz.dashboard add a new Plone content type 'Anz dashboard'. A dashboard
object can contain any number of pages, a page can contain any number of
columns, a column can contain any number of widgets. So you can use
dashboard to render complex composite page or external data source.

Now anz.dashboard carried the following widgets:

- static text widget
  render static HTML contents that edit with a WYSIWYG editor by dashboard
  owner.
- calender widget
  show events information in calendar.
- weather widget
  show weather of specific city.
- rss feed widget
  show contents get from any rss feed.
- folder contents widget
  show contents under specific folders.

Requirements
============
Plone 3.0 or later

Installation
============
To install anz.dashboard into the global Python environment (or a
workingenv), using a traditional Zope 2 instance, you can do this:

* When you're reading this you have probably already run 
  ``easy_install anz.dashboard``. Find out how to install setuptools
  (and EasyInstall) here:
  http://peak.telecommunity.com/DevCenter/EasyInstall

* Create a file called ``anz.dashboard-configure.zcml`` in the
  ``/path/to/instance/etc/package-includes`` directory.  The file
  should only contain this::

    <include package="anz.dashboard" />

Alternatively, if you are using zc.buildout and the
plone.recipe.zope2instance recipe to manage your project, you can do this:

* Add ``anz.dashboard`` to the list of eggs to install, e.g.:

::

    [buildout]
    ...
    eggs =
        ...
        anz.dashboard
       
* Tell the plone.recipe.zope2instance recipe to install a ZCML slug:

::

    [instance]
    recipe = plone.recipe.zope2instance
    ...
    zcml =
        anz.dashboard

anz.dashboard
=====================

      
* Re-run buildout, e.g. with:

::

    $ ./bin/buildout
        
You can skip the ZCML slug if you are going to explicitly include the
package from another package's configure.zcml file.

In Plone just add "anz.dashboard" product with quick_installer, or install
"anz.dashboard" by portal_setup.

Use cases
=========
- Used to build personal web portal
- Used to build complex composite page
- Used to render informations come from external site or web services

Features
========
* 'tab' or 'tile' layout
  You can choose 'tile mode' or 'tab mode'. With 'tile mode', all pages
  are shown in one page, from top to bottom, it is useful for you to make
  very complex composite page. With 'tab mode', you can switch pages using
  the top tab links.

* any number of pages or columns
  You can create any number of pages, and add any number of columns to a
  page.

* persistent drag&drop
  all widgets can moved with drag&drop functionality in the column, from
  column to column or from page to page(under 'tile' mode). 

* change column width by drag&drop
  easily change column width by drag&drop a column splitter.

* persistent collapse/expand:
  all widgets can be set to collapse or expand.

* edit widget preference
  all widgets provide some preferences, you can set it as your like.

* full Ajax support
  full Ajax operation support, give you smoothly use experience. 

ToDo
====
- more widgets 
- more widget color theme
