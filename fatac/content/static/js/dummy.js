$(document).ready(function() {

    //Get the current path
    var pathname = getPath();

    // Text Selection
    var selection = "";

    //Start Image Tagger
    imageTagger(pathname);

});

function mostrarAmagarAportacions() {
    // Fa que quan cliquem sobre un element amb classe num_aportacions es
    // mostri o s'amagui l'element amb id viewlet-below-content

    $('.num_aportacions').click(function(){
        $('#viewlet-below-content').slideToggle();
    });
}


function updateTips( t ) {
    tips
        .text( t )
        .addClass( "ui-state-highlight" );
    setTimeout(function() {
        tips.removeClass( "ui-state-highlight", 1500 );
    }, 500 );
}

function checkLength( o, n, min, max ) {
    if ( o.val().length > max || o.val().length < min ) {
        o.addClass( "ui-state-error" );
        updateTips( "Length of " + n + " must be between " +
            min + " and " + max + "." );
        return false;
    } else {
        return true;
    }
}


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
            isTagDeletionEnabled: true,
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





