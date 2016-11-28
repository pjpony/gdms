/* This provides some default variables which should I think be moved to objects at some point soon */

/*Push button options for editing and so on primarily needed for touch devices where shift keys and the like are
  torture
 */
		var editmode = false;
        var newitems = false;

	$(".pushme").click(function () {
    var $element = $(this);
    $element.val(function(i, text) {
        editmode = !editmode;
        console.log (editmode);
        return text == $element.data('default-text') ? $element.data('new-text')
                                                     : $element.data('default-text');
    });
	});


/* This ocnverts the python date into javascript for the graph file which can then remain as a static javascript file
   in due course it may be better to load this via ajax - but for now need to understand difference between
   XML and XML(json)

   naming now using nodes instead of d3nodes and links instead of d3edges?? but currently got both as probably want to
   compare in a bit
 */

    {{from gluon.serializers import json}}
    var nodes = {{=XML(json(nodes))}};
    var links = {{=XML(json(links))}};
    var edges = [];


        /*var d3nodes  = [{"id":2,"title":"can I edit","x":230,"y":494},{"id":3,"title":"test","x":436,"y":309}]*/
        var d3nodes = {{=XML(d3nodes)}};
        var vieweventmap = false;
        var eventowner = false;
        var redraw = true;

        var d3edges = {{=XML(d3edges)}};

        console.log('nodes', nodes);
        console.log('d3node', d3nodes);
        console.log('links', links);
        console.log('d3edges', d3edges );


/* these are ajax functions and quite convenient to define here as then we get url syntax processing

 */
        function requestLink(sourceId,targetId)
        {
        ajax('{{=URL('network','linkrequest')}}'+'/'+sourceId+'/'+targetId+'/', ['bla'], 'ajaxlink');
        };

        function deleteLink(sourceId,targetId)
        {
        ajax('{{=URL('network','linkrequest')}}'+'/'+sourceId+'/'+targetId+'/delete/', ['bla'], 'ajaxlink');
        };

        function moveElement(sourceId, sourceposx, sourceposy)
        {
        ajax('{{=URL('event','move')}}'+'/'+0+'/'+sourceId+'/'+sourceposx+'/'+sourceposy+'/', ['bla'], 'ajaxlink');
        };

        var ajaxquesturl = "{{=URL('network','ajaxquest')}}?"

        function out(m) {
        $('#message').html(m);
        };