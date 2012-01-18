import os


def compress( name, files ):
    for file in files:
        dest = open( name, 'a' )
        
        os.system( 'java -jar yuicompressor-2.4.2.jar %s -o tmp.txt' % file )
        f = open( 'tmp.txt', 'r' )
        
        # add file name first
        dest.write( '\n/* - %s - */\n' % file )
        dest.write( f.read() )
        
        dest.close()
        f.close()
        
        print 'compress %s' % file

if __name__ == '__main__':
    print 'start compress'
    layoutCSSFiles = [ 'anz_dashboard.css', 'carousel.css',
                       'TreeComboSuperBox.css', 'TabMoreMenu.css' ]
    compress( 'anz.dashboard.layout-min.css' , layoutCSSFiles )
    
    layoutJSFiles = [ 'anzi18n.js', 'Portal.js', 'PortalColumn.js',
                      'columnlayout-ux.js', 'carousel.js', 'XCheckbox.js',
                      'anz_widget.js', 'widget_static_text.js', 'widget_rss.js',
                      'widget_weather.js', 'widget_calendar.js', 'MultiSelect.js',
                      'TreeComboSuperBox.js', 'widget_folder_contents.js',
                      'widgetsview.js', 'TabMoreMenu.js', 'anz_dashboard.js' ]
    compress( 'anz.dashboard.layout-min.js' , layoutJSFiles )
    
    viewCSSFiles = [ 'anz_dashboard.css', 'carousel.css' ]
    compress( 'anz.dashboard.view-min.css' , viewCSSFiles )
    
    viewJSFiles = [ 'anzi18n.js', 'anz_widget.js', 'widget_static_text.js',
                    'widget_rss.js', 'widget_weather.js', 'widget_calendar.js',
                    'widget_folder_contents.js', 'anz_dashboard_view.js' ]
    compress( 'anz.dashboard.view-min.js' , viewJSFiles )
    
    print 'end compress'