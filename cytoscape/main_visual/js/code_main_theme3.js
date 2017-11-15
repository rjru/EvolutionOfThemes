$( document ).ready(function() {
    console.log( "document loaded" );

var graph = null;
var hoverDetail = null;

$("#result_from").change(function () {

      $("#tss").html('');
      if (hoverDetail != null){
          hoverDetail._removeListeners();
      }

	  var namefile = $("#result_from :selected").attr('value');
	  console.log(namefile)
	  $.ajax({dataType:"json", url: "../../clustering_process/final_result/"+namefile, success: function(result){
	  console.log(result) //[0]["data"]["length"]
	  es = result.edges;

	  var max_edge = max_edge_fun(es);

	  function max_edge_fun(es){
                    max = 0;
                     for (len_edge in es){
                         if (parseFloat(es[len_edge]["data"]["length"]) > max){
                            //console.log(parseFloat(es[len_edge]["data"]["length"]))
                            max = parseFloat(es[len_edge]["data"]["length"])
                            }
                        }
                    return max;
                   }

	  //console.log(max_edge)

			  var cy = cytoscape({
			  container: document.getElementById('cy'),
               /*
			  layout: {
			            name: 'cola',
			            //maxSimulationTime: 20000,//800000, // max length in ms to run the layout
			            edgeLength: function( edge ){var len = parseFloat(edge.data('length')); return Math.sqrt(len); },
			            ready: function(){}, // on layoutready
			            //edgeLength
                        //edgeSymDiffLength: undefined, // symmetric diff edge length in simulation
                        //edgeJaccardLength: undefined
                        //fit: true,
			            infinite: true
			            }, */
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
			            'border-width': '0.1em',
			            'border-color': 'gray',
			            'font-size' : '2em',
			            'background-color': 'data(class)'
			      		}
			    },
			    {
			      selector: 'node:selected',
                  style: {
                    "border-width": '5em',
                    "border-color": '#FE2E2E',
                    "border-opacity": '0.5',
                    //"background-color": '#2efe2e',
                    "text-outline-color": '#77828C'
                  }
                 },
			    {
			      selector: 'node[class="grey"]',
			      style:{
			            //'label': 'data(label)',
			            //'width': '0.5px',
			            //'height': '0.5px',
			            'width': '0.5em',
			            'height': '0.5em',
			            'color': 'yellow',
			            'background-fit': 'contain',
			            'background-clip': 'none',
			            'border-style': 'solid',
			            'border-width': '0.02em',
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
			            'width': '0.2em',
			            'control-point-step-size': '0.3em',
			            'line-color': 'gray'
			             }
			    }
			  ],


			  layout: {
			          name: 'preset',
                      //fit:false,
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
			      	  //

			      //layout:{defaults}
			}); // fin citoscape

			//cy.add(data)
			//console.log(data.edges[0]["data"]["length"])

			var defaults = {
                name: 'cola',
                //maxSimulationTime: 20000,//800000, // max length in ms to run the layout
                edgeLength: function( edge ){var len = parseFloat(edge.data('length')); return Math.sqrt(len); },
                nodeSpacing: function( node ){ return 1; },
                //edgeLength
                //edgeSymDiffLength: undefined, // symmetric diff edge length in simulation
                //edgeJaccardLength: undefined
                //fit: false,
                infinite: true
            };

            //cy.fit(); # holaaa
            var ly = cy.layout(defaults) //{name: 'cola'}
            //cy.center();

            var flag = true;
            //cy.layout({name: 'cola'})
            $('#playPause').on('click', function() {
                if(flag) {
                    $(this).html('Pause');

                      //console.log(cy.$('node')[0]._private.style.label.hide())   'label': 'data(yearTheme)'
                      var stringStylesheet = 'node { label: "data(label)" }';
                      console.log(cy.style().selector('node').style('label', '').update() );
                    ly.run();
                } else {
                    $(this).html('Play');
                    ly.stop();
                }
                flag = !flag;
            });
		    //cy.layout(options);
            /*
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

            */
			function  timeSeriesView(objTS){
			  var cad ="";
			  for (prop in objTS) {
			    cad = String(objTS[prop])+cad;
			  }
			  return cad;
			}



            var data = []

            // inicio  Rickshaw.Graph
            var graph = new Rickshaw.Graph( {
                element: document.getElementById("tss"),
                //width: '1150',
                renderer: 'line',
                series: data,//[
                    //{
                    //    color: "#6060c0",
                    //    data: setFormatJs(ts, 'number'),
                    //    name: 'Prob'
                    //}
                //]
            } );

            //for(e in a){d[Number(e)] = a[e]}
            var format = function(n) {

            /*
                var map = {
                    0: 'zero',
                    1: 'first',
                    2: 'second',
                    3: 'third',
                    4: 'fourth'
                };
            */
                var docDates = result.docDates;
                var map = {}
                for(e in docDates){map[Number(e)] = docDates[e]}

                return map[n];
            }

            var x_ticks = new Rickshaw.Graph.Axis.X( {
                graph: graph,
                orientation: 'bottom',
                element: document.getElementById('x_axis'),
                pixelsPerTick: 70,
                tickFormat: format
            } );

            graph.render();


            hoverDetail = new Rickshaw.Graph.HoverDetail( {
            graph: graph,
            formatter: function(series, x, y) {
                console.log("result")
                //console.log(result.idToPmid[x])
                var title = '<span class="date">' + result.metaDoc[result.idToPmid[result.idDocOrdened[x]]]["title"] + '</span>'; //parseFloat(x)
                var swatch = '<span class="detail_swatch" style="background-color:"></span>'; // ' + series.color + '
                var year = result.metaDoc[result.idToPmid[result.idDocOrdened[x]]]["year"];
                var pmid = result.metaDoc[result.idToPmid[result.idDocOrdened[x]]]["pmid"];
                var venue = result.metaDoc[result.idToPmid[result.idDocOrdened[x]]]["venue"];
                var content = swatch + series.name + ": " + parseFloat(y).toFixed(5) + " pmid: <span id='pmid' data-pmid="+pmid+">"+ pmid + "</span> venue:" + venue +" year:" + year + '<br>' + title; //
                return content;
            }
          });


            cy.on('tap', function(event){
              // target holds a reference to the originator
              // of the event (core or element)
              var evtTarget = event.target;

              if( evtTarget === cy ){
                  console.log('tap on background');
                  while(data.length > 0) {
                      var e = data.pop();
                      //$(String(e.name)).css("border-color", '#FE2E2E');
                      //data.pop();
                  }
                  graph.update();

              } else {
                console.log('tap on some element');
              }
            });

            function getRandomColor() {
              var letters = '0123456789ABCDEF';
              var color = '#';
              for (var i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
              }
              return color;
            }

			cy.on('click', 'node', function(evt){

              ran_color = getRandomColor();

              if(evt.originalEvent.ctrlKey) {
                console.log(this.id())
                if (this.selected()){
                    console.log("unselect")
                    for (var i = 0; i < data.length; i ++) {
                        if (data[i].name == this.id()) {
                            data.splice(i, 1);
                            break;
                        }
                    }
                }
                else{
                    console.log("select")

                    this.css("border-color", ran_color);
                    ts = this.data("topDistribution");
                    data.push({name: this.id(), data: setFormatJs(ts, 'number'), color: ran_color});
                    console.log(data)
                }
                graph.update();
              }
              else{
			      ts = this.data("topDistribution");
			      console.log(ts);
			      // add rows top venue
			      $("#top_venues").html('');

                  var topVenueSort = setFormatJs(this.data("topVenue"), 'string');
                  topVenueSort.sort(function (a, b) {return  b.y - a.y;});
                  //console.log(topVenueSort)
                  for (v in topVenueSort){
                    $('#top_venues').append('<tr class="item"><td>'+ topVenueSort[v]['x'].replace(/_/g , " ") +'</td><td>'+ topVenueSort[v]['y'] +'</td></tr>');
                   }

                  $("#top_words").html('');
                  var topWordsSort = setFormatJs(this.data("topWords"), 'string');
                  topWordsSort.sort(function (a, b) {return  b.y - a.y;});
                  for (w in topWordsSort){
                    $('#top_words').append('<tr><td>'+ topWordsSort[w]['x'] +'</td><td>'+ topWordsSort[w]['y'] +'</td></tr>');
                   }

                  $("#titles_list").html('');
                  //var topWordsSort = setFormatJs(this.data("metaDoc"), 'string');
                  //topWordsSort.sort(function (a, b) {return  b.y - a.y;});  <li class="list-group-item">One</li>
                  for (md in this.data("topDistribution")){
                    if(this.data("topDistribution")[md] >= 0.05){
                        $('#titles_list').append('<li class="list-group-item">'+result.metaDoc[result.idToPmid[md]]["title"]+'</li>');
                    }
                   }


                  // INIT LIBRARY OF TIME SERIES
                  //if (hoverDetail != null){
                  //    hoverDetail._removeListeners();
                  //}

                  while(data.length > 0) {
                      data.pop();
                  }
                  this.css("border-color", '#FE2E2E');
                  data.push({name: this.id(), data: setFormatJs(ts, 'number'), color: '#FE2E2E'});
                  graph.update();

			  // END LIBRARY OF TIME SERIES
              }
			}); // fin click

			$('#config-toggle').on('click', function(){
			  $('body').toggleClass('config-closed');
			  cy.resize();
			});

			$("#tss").on('click', function(){
              console.log(document.getElementById("pmid").getAttribute("data-pmid"));
              var pmid = document.getElementById("pmid").getAttribute("data-pmid");
              window.open('https://www.ncbi.nlm.nih.gov/pubmed/'+pmid);

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
	}); // fin ajax json

});

	function setFormatJs(dataKeyVal, typeData){
	  arrayJs = [];
	  if (typeData == "number"){
	        for(e in dataKeyVal){arrayJs.push({x:Number(e),y:dataKeyVal[e]})}
	        }
	  if (typeData == "string"){
	        for(e in dataKeyVal){arrayJs.push({x:e,y:dataKeyVal[e]})}
	        }

	  return arrayJs;
	}
});