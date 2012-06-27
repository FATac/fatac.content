/******
    Set up standard Plone popups

    Provides globals: common_content_filter

    Extends jQuery.tools.overlay.conf to set up common Plone effects and
    visuals.
******/


var common_content_filter = '#content>*:not(div.configlet),dl.portalMessage.error,dl.portalMessage.info';

jQuery.extend(jQuery.tools.overlay.conf,
    {
        fixed:false,
        speed:'fast',
        mask:{color:'#fff',opacity: 0.4,loadSpeed:0,closeSpeed:0}
    });


(function($) {

	// static constructs
	$.plonepopups = $.plonepopups || {};

    $.extend($.plonepopups,
        {
            // method to show error message in a noform
            // situation.
            noformerrorshow: function noformerrorshow(el, noform) {
                var o = $(el),
                    emsg = o.find('dl.portalMessage.error');
                if (emsg.length) {
                    o.children().replaceWith(emsg);
                    return false;
                } else {
                    return noform;
                }
            },
            // After deletes we need to redirect to the target page.
            redirectbasehref: function redirectbasehref(el, responseText) {
                var mo = responseText.match(/<base href="(\S+?)"/i);
                if (mo.length === 2) {
                    return mo[1];
                }
                return location;
            }
        });
})(jQuery);

jQuery(function($){

    if (jQuery.browser.msie && parseInt(jQuery.browser.version, 10) < 7) {
        // it's not realistic to think we can deal with all the bugs
        // of IE 6 and lower. Fortunately, all this is just progressive
        // enhancement.
        return;
    }

    // add new Playlist
    $('form[name=playlist_add]').prepOverlay(
        {
            subtype: 'ajax',
            filter: common_content_filter,
            formselector: 'form.kssattr-formname-++add++fatac.playlist',
            noform: function(el) {return $.plonepopups.noformerrorshow(el, 'redirect');},
            redirect: function () {return location.href;}
        }
    );

    // add new File
    $('form[name=file_add]').prepOverlay(
        {
            subtype: 'ajax',
            filter: common_content_filter,
            formselector: 'form[name="groups"]',
            noform: function(el) {return $.plonepopups.noformerrorshow(el, 'redirect');},
            redirect: function () {return location.href;}
        }
    );

    // Edit Group
    $('form[name=groups_edit]').prepOverlay(
        {
            subtype: 'ajax',
            filter: common_content_filter,
            formselector: 'form[name="groups"]',
            noform: function(el) {return $.plonepopups.noformerrorshow(el, 'redirect');},
            redirect: function () {return location.href;}
        }
    );

});

function removeSelectedGroup(idTagGroup)
{
    //Get the current path
    var pathname = window.location.pathname;

    //Parse for different paths
    if (pathname.indexOf("@@manage-groups") != -1)
    {
        pathname = pathname.split("@@manage-groups")[0];
    }
    else if (pathname[-1] != '/')
    {
        pathname = pathname + '/';
    }

    $( "#dialog-confirm" ).dialog({
        resizable: false,
        height:200,
        width:350,
        modal: true,
        buttons: {
            "Esborra aquest grup": function() {
                path = pathname + "@@deleteUserGroup?groupId=" + idTagGroup.replace("#","");
                $.ajax({url: path,
                        type: "post",
                        error: function() { alert("No s'ha eliminar el grup de l'usuari"); },
                        success: function() { window.location.href = pathname + "@@manage-groups";}
                      });
                $( this ).dialog( "close" );
            },
            "Cancel·la": function() {
                $( this ).dialog( "close" );
            }
        }
    });

    // path = pathname + "@@deleteUserGroup?groupId=" + idTagGroup.replace("#","");

    // $.ajax({url: path,
    //         type: "post",
    //         error: function() { alert("No s'ha eliminar el grup de l'usuari"); },
    //         success: function() { window.location.href = pathname + "@@manage-groups";}
    //       });

}

// Binding to the "trash" icon when managing groups
$(document).ready(function() {
    $(".dashboardListing").on("click", ".trashbin", function(event) {
        event.preventDefault();
        removeSelectedGroup($(this).attr("id"));
    })
})
