   $( document ).ready(function() {
        console.log( "document loaded" );


$("#result_from").change(function () {
	  var namefile = $("#result_from :selected").attr('value');
	  console.log(namefile)
	  $.ajax({dataType:"json", url: "https://raw.githubusercontent.com/rjru/EvolutionOfThemes/master/cytoscape/main_visual/data/"+namefile, success: function(result){
			  var cy = cytoscape({
			  container: document.getElementById('cy'),
			  elements: result,
			  // so we can see the ids
			  style: 
			  [
			    {
			      selector: 'node',
			      style:{
			            //'label': 'data(label)',
			            //'width': '0.5px',
			            //'height': '0.5px',
			            'width': '0.02em',
			            'height': '0.02em',
			            'color': 'yellow',
			            'background-fit': 'contain',
			            'background-clip': 'none',
			            'border-style': 'solid',
			            'border-width': '0.0002em',
			            'border-color': 'white',
			            //'font-size' : '0.5px',
			            'font-size' : '0.02em',
			            'background-color': 'data(class)'
			      		}
			    },
			    {
			      selector: 'node[class="grey"]',
			      style:{
			            //'label': 'data(label)',
			            //'width': '0.5px',
			            //'height': '0.5px',
			            'width': '0.01em',
			            'height': '0.01em',
			            'color': 'yellow',
			            'background-fit': 'contain',
			            'background-clip': 'none',
			            'border-style': 'solid',
			            'border-width': '0.0002em',
			            'border-color': 'white',
			            //'font-size' : '0.5px',
			            'font-size' : '0.02em',
			            'background-color': 'data(class)'
			      		}
			    },
			    {
			      selector: 'edge',
			      style: {

			            'text-background-color': 'yellow',
			            'text-background-opacity': 0.4,
			            //'width': '0.05em',
			            'width': '0.001em',
			            'control-point-step-size': '0.3em',
			            'line-color': 'black'
			             }
			    }
			  ],

			  layout: {
			          name: 'preset',
			          /*
			          positions: undefined, // map of (node id) => (position obj); or function(node){ return somPos; }
			          zoom: undefined, // the zoom level to set (prob want fit = false if set)
			          pan: undefined, // the pan level to set (prob want fit = false if set)
			          fit: true, // whether to fit to viewport
			          padding: 20, // padding on fit
			          animate: true, // whether to transition the node positions
			          animationDuration: 500, // duration of animation in ms if enabled
			          animationEasing: undefined, // easing of animation if enabled
			          animateFilter: function ( node, i ){ return true; }, // a function that determines whether the node should be animated.  All nodes animated by default on animate enabled.  Non-animated nodes are positioned immediately when the layout starts
			          ready: undefined, // callback on layoutready
			          stop: undefined, // callback on layoutstop
			          transform: function (node, position ){ return position; }, // transform a given node position. Useful for changing flow direction in discrete layouts 
			      	  */
			      	  }
			      //layout:{defaults}
			}); // fin citoscape

			//cy.add(data)
			//console.log(data.edges[0]["data"]["length"])

			var defaults = {
                name: 'cola',
                //avoidOverlap: true,
                //maxSimulationTime: 2,//800000, // max length in ms to run the layout
                //edgeLength: function( edge ){var len = parseFloat(edge.data('length')); return Math.sqrt(len); },
                //nodeSpacing: function( node ){ return 1; },
                //edgeLength
                //edgeSymDiffLength: undefined, // symmetric diff edge length in simulation
                //edgeJaccardLength: undefined
                //fit: false,
                //infinite: true
            };

            //cy.fit(); # holaaa
            //var ly = cy.$('node').not('[class="grey"]').layout(defaults) //{name: 'cola'}
            //ly.run();
			//cy.add(data)
			//cy.center();

			//cy.layout(defaults);

			cy.nodes().forEach(function(ele) {
			        ele.qtip({
			          content: {
			            id: 'ts',
			            text: $('#tss'),//timeSeriesView(ele.data("vectorTS")),//qtipText(ele),  data.edges
			            title: "Time series"//
			          },
			          style: {
			            classes: 'qtip-bootstrap'
			          },
			          position: {
			            my: 'bottom center',
			            at: 'top center',
			            target: ele
			          }
			        });
			      });

			function  timeSeriesView(objTS){
			  var cad ="";
			  for (prop in objTS) {
			    cad = String(objTS[prop])+cad;
			  }
			  return cad;
			}

			cy.on('click', 'node', function(evt){
			      ts = this.data("vectorTS");
			      console.log(ts);
			      ///*
			      $("#tss").html('');
			  var graph = new Rickshaw.Graph( {
			      element: document.querySelector("#tss"), 
			      width: 150, 
			      height: 50, 
			      series: [{
			          color: 'steelblue',
			          data: setFormat(ts)
			      }]
			  }); 

			  graph.render();
			  // */ 
			}); // fin click

			$('#config-toggle').on('click', function(){
			  $('body').toggleClass('config-closed');
			  cy.resize();
			});
			    
	},
	error:function (xhr, ajaxOptions, thrownError){
	    if(xhr.status==404) {
	    	  console.log("horror!")
			  var cy = cytoscape({
			  container: document.getElementById('cy'),
			  elements: undefined});
	    }
	}
	}); // fin ajax

});

	function setFormat(ts){
	  arrayTs = [];
	  for(e in ts){arrayTs.push({x:Number(e),y:ts[e]})}
	  return arrayTs;
	}   

    }); // fin document loaded
  /*
  $button.on('click', function(){
  	$.getJSON("data/syntetic_control_600.json", function (data) {
		var cy = cytoscape({
  container: document.getElementById('cy'),
  elements: data,
  // so we can see the ids
  style: 
  [
    {
      selector: 'node',
      style:{
            //'label': 'data(label)',
            //'width': '0.5px',
            //'height': '0.5px',
            'width': '0.015em',
            'height': '0.015em',
            'color': 'yellow',
            'background-fit': 'contain',
            'background-clip': 'none',
            'border-style': 'solid',
            'border-width': '0.0002em',
            'border-color': 'white',
            //'font-size' : '0.5px',
            'font-size' : '0.02em',
            'background-color': 'data(class)'
      		}
    },
    {
      selector: 'edge',
      style: {
            'text-background-color': 'yellow',
            'text-background-opacity': 0.4,
            //'width': '0.05em',
            'width': '0.0015em',
            'control-point-step-size': '0.3em'
             }
    }
  ],

  layout: {
          name: 'preset',
          positions: undefined, // map of (node id) => (position obj); or function(node){ return somPos; }
          zoom: undefined, // the zoom level to set (prob want fit = false if set)
          pan: undefined, // the pan level to set (prob want fit = false if set)
          fit: true, // whether to fit to viewport
          padding: 20, // padding on fit
          animate: true, // whether to transition the node positions
          animationDuration: 500, // duration of animation in ms if enabled
          animationEasing: undefined, // easing of animation if enabled
          animateFilter: function ( node, i ){ return true; }, // a function that determines whether the node should be animated.  All nodes animated by default on animate enabled.  Non-animated nodes are positioned immediately when the layout starts
          ready: undefined, // callback on layoutready
          stop: undefined, // callback on layoutstop
          transform: function (node, position ){ return position; }, // transform a given node position. Useful for changing flow direction in discrete layouts 
      	  }
      //layout:{defaults}
		});
  		cy.center();
  	});

  }); */
// fin del ajax
