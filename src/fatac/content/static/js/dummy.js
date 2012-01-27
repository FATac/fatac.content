$(document).ready(function() {

    //Get the current path
    var pathname = getPath();

    // Text Selection
    var selection = "";

    //Start Image Tagger
    imageTagger(pathname);

    //Start Contextual Menu
    contextMenu(pathname, selection);

});



// Parse url to get the correct path of the object
function getPath()
{
    //Get the current path
    var path = window.location.pathname;

    //Parse for different paths
    if (path.indexOf("view") != -1)
    {
        path = path.split("view")[0];
    }
    else if (path.indexOf("@@view") != -1)
    {
        path = path.split("@@view")[0];
    }
    else if (path[-1] != '/')
    {
        path = path + '/';
    }

    return path;
}


// Get User selected Text
function getSelected() {

/*
    // Update Contextual Menu if some text have been selected
    $('#description').click(function(e) {
        selection = getSelected();
        if (selection != "")
        {
            //updateContextMenu(pathname, selection);
            
        }
    });
*/

    if(window.getSelection) { return window.getSelection(); }
    else if(document.getSelection) { return document.getSelection(); }
    else 
    {
        var selection = document.selection && document.selection.createRange();
        if(selection.text) { return selection.text; }
        return false;
    }
    return false;
}


function contextMenu(pathname)
{
    var menu = [
                {"TRIA LA LLISTA ON VOLS FICAR AQUEST ELEMENT":{onclick:function(){},disabled:true}},
                $.contextMenu.separator,
    ];

    var titol;
    var idPlaylist;
    var menuDict = new Object();

    // Si no estem editant l'objecte fem la cerca de playlists i carreguem el menu contextual
    if (pathname.indexOf("@@edit") == -1 && pathname.indexOf("edit") == -1)
    {
        // Assign handlers immediately after making the request,
        // and remember the jqxhr object for this request
        $.getJSON(pathname + "returnPlaylists", function() { 
        })
        .error(function() { alert("No s'ha pogut carregar el menu contextual"); })
        .complete(function( data ) {

            
            var llistaPlaylists = jQuery.parseJSON( data.responseText );

            for (i=0; i<llistaPlaylists['Titols'].length; i++)
            {
                titol = llistaPlaylists['Titols'][i];
                idPlaylist = llistaPlaylists['Ids'][i];
                menuDict[titol] = function(menuItem,menu) {
                    $.ajax({url: pathname + "updatePlaylist?idPlaylist=" + idPlaylist, type: "post", error: function(){alert("Ha donat un error al afegir a la Playlist! No s'han guardat els canvis");}
                });};
            }

            if (llistaPlaylists['Titols'].length == 0)
            {
                menuDict['No hi han elements'] = {onclick:function(){},disabled:true};
            }

            menu.push(menuDict);

            $('.cmenu').contextMenu(menu,{theme:'default'});

        });
    }
    
}



function imageTagger(pathname)
{
    // When the DOM is ready, initialize the scripts.
    jQuery(function( $ ){
 
        // Set up the photo tagger.
        $( "div.photo-container" ).photoTagger({
 
            // The API urls.
            loadURL: pathname + "loadTags",
            saveURL: pathname + "saveTag",
            deleteURL: pathname + "deleteTag",
   
            // Default to turned on.
            isTagCreationEnabled: true,
        });
 
 
        // Hook up the enable create links.
        $( "a.enable-create" ).click(
            function( event ){
                // Prevent relocation.
                event.preventDefault();
 
                // Get the container and enable the tag
                // creation on it.
                $( this ).prevAll( "div.photo-container" )
                    .photoTagger( "enableTagCreation" );
                }
        );
 
 
        // Hook up the disabled create links.
        $( "a.disable-create" ).click(
            function( event ){
                // Prevent relocation.
                event.preventDefault();
 
                // Get the container and enable the tag
                // creation on it.
                $( this ).prevAll( "div.photo-container" )
                    .photoTagger( "disableTagCreation" );
            }
        );
 
 
        // Hook up the enable delete links.
        $( "a.enable-delete" ).click(
            function( event ){
                // Prevent relocation.
                event.preventDefault();
 
                // Get the container and enable the tag
                // deletion on it.
                $( this ).prevAll( "div.photo-container" )
                    .photoTagger( "enableTagDeletion" );
             }
        );
 
 
        // Hook up the disabled delete links.
            $( "a.disable-delete" ).click(
                function( event ){
                    // Prevent relocation.
                    event.preventDefault();
 
                    // Get the container and disabled the tag
                    // deletion on it.
                    $( this ).prevAll( "div.photo-container" )
                        .photoTagger( "disableTagDeletion" );
            }
        );
 
    });
}





