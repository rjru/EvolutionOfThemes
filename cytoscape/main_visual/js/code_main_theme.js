   $( document ).ready(function() {
        console.log( "document loaded" );


$("#result_from").change(function () {
	  var namefile = $("#result_from :selected").attr('value');
	  console.log(namefile)
	  $.ajax({dataType:"json", url: "../../clustering_process/result/"+namefile, success: function(result){
	  console.log(result)
			  var cy = cytoscape({
			  container: document.getElementById('cy'),
			  layout: {
			            name: 'preset'
			            },
			  elements: result,
			  // so we can see the ids
			  style:
			  [
			    {
			      selector: 'node',
			      style:{
			            'label': 'data(yearTheme)',
			            'width': '2em',
			            'height': '2em',
			            'color': 'black',
			            'background-fit': 'contain',
			            'background-clip': 'none',
			            'border-style': 'solid',
			            'border-width': '0.5em',
			            'border-color': 'white',
			            'font-size' : '2em',
			            'background-color': 'blue'//'data(class)'
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
			            'width': '0.5em',
			            'control-point-step-size': '0.3em',
			            'line-color': 'black'
			             }
			    }
			  ],
                /*
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
			      	  // */

			      //layout:{defaults}
			}); // fin citoscape

			//cy.add(data)
			//console.log(data.edges[0]["data"]["length"])

			var defaults = {
			  name: 'cola',
              animate: true, // whether to show the layout as it's running
              refresh: 1, // number of ticks per frame; higher is faster but more jerky
              maxSimulationTime: 4000, // max length in ms to run the layout
              ungrabifyWhileSimulating: false, // so you can't drag nodes during layout
              fit: true, // on every layout reposition of nodes, fit the viewport
              padding: 30, // padding around the simulation
              boundingBox: undefined, // constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
              nodeDimensionsIncludeLabels: undefined, // whether labels should be included in determining the space used by a node (default true)

              // layout event callbacks
              ready: function(){}, // on layoutready
              stop: function(){}, // on layoutstop

              // positioning options
              randomize: false, // use random node positions at beginning of layout
              avoidOverlap: true, // if true, prevents overlap of node bounding boxes
              handleDisconnected: true, // if true, avoids disconnected components from overlapping
              nodeSpacing: function( node ){ return 10; }, // extra spacing around nodes
              flow: undefined, // use DAG/tree flow layout if specified, e.g. { axis: 'y', minSeparation: 30 }
              alignment: undefined, // relative alignment constraints on nodes, e.g. function( node ){ return { x: 0, y: 1 } }

              // different methods of specifying edge length
              // each can be a constant numerical value or a function like `function( edge ){ return 2; }`
              edgeLength: undefined, // sets edge length directly in simulation
              edgeSymDiffLength: undefined, // symmetric diff edge length in simulation
              edgeJaccardLength: undefined, // jaccard edge length in simulation

              // iterations of cola algorithm; uses default values on undefined
              unconstrIter: undefined, // unconstrained initial layout iterations
              userConstIter: undefined, // initial layout iterations with user-specified constraints
              allConstIter: undefined, // initial layout iterations with all constraints including non-overlap

              // infinite layout options
              infinite: false // overrides all other options for a forces-all-the-time mode
  };

			var options = {
			  name: 'cose',

			  // Called on `layoutready`
			  ready: function(){},

			  // Called on `layoutstop`
			  stop: function(){},

			  // Whether to animate while running the layout
			  // true : Animate continuously as the layout is running
			  // false : Just show the end result
			  // 'end' : Animate with the end result, from the initial positions to the end positions
			  animate: true,

			  // Easing of the animation for animate:'end'
			  animationEasing: undefined,

			  // The duration of the animation for animate:'end'
			  animationDuration: undefined,

			  // A function that determines whether the node should be animated
			  // All nodes animated by default on animate enabled
			  // Non-animated nodes are positioned immediately when the layout starts
			  animateFilter: function ( node, i ){ return true; },


			  // The layout animates only after this many milliseconds for animate:true
			  // (prevents flashing on fast runs)
			  animationThreshold: 250,

			  // Number of iterations between consecutive screen positions update
			  // (0 -> only updated on the end)
			  refresh: 20,

			  // Whether to fit the network view after when done
			  fit: true,

			  // Padding on fit
			  padding: 30,

			  // Constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
			  boundingBox: undefined,

			  // Excludes the label when calculating node bounding boxes for the layout algorithm
			  nodeDimensionsIncludeLabels: false,

			  // Randomize the initial positions of the nodes (true) or use existing positions (false)
			  randomize: false,

			  // Extra spacing between components in non-compound graphs
			  componentSpacing: 40,

			  // Node repulsion (non overlapping) multiplier
			  nodeRepulsion: function( node ){ return 2048; },

			  // Node repulsion (overlapping) multiplier
			  nodeOverlap: 4,

			  // Ideal edge (non nested) length
			  idealEdgeLength: function( edge ){ return 32; },

			  // Divisor to compute edge forces
			  edgeElasticity: function( edge ){ return 32; },

			  // Nesting factor (multiplier) to compute ideal edge length for nested edges
			  nestingFactor: 1.2,

			  // Gravity force (constant)
			  gravity: 1,

			  // Maximum number of iterations to perform
			  numIter: 1000,

			  // Initial temperature (maximum node displacement)
			  initialTemp: 1000,

			  // Cooling factor (how the temperature is reduced between consecutive iterations
			  coolingFactor: 0.99,

			  // Lower temperature threshold (below this point the layout will end)
			  minTemp: 1.0,

			  // Pass a reference to weaver to use threads for calculations
			  weaver: false
			};

			//cy.add(data)
            cy.center();
		    //cy.layout(options);


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
			      ts = this.data("topDistribution");
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