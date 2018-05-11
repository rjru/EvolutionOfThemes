$( document ).ready(function() {
    console.log( "document loaded" );

var graph = null;
var hoverDetail = null;

var cyInNode;

colors_pubmed = {'Malar_J':'Fuchsia', 'Nucleic_Acids_Res':'Teal'};

$("#result_from").change(function () {

      $("#tss").html('');
      if (hoverDetail != null){
          hoverDetail._removeListeners();
      }

	  var namefile = $("#result_from :selected").attr('value');
	  console.log(namefile)
	  $.ajax({dataType:"json", url: "../clustering_process/final_result/"+namefile, success: function(result){
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
			            //'label': 'data(yearTheme)',
			            'width': '2em',
			            'height': '2em',
			            'color': 'black',
			            'background-fit': 'contain',
			            'background-clip': 'none',
			            'border-style': 'solid',
			            'border-width': '0.1em',
			            'border-color': 'gray',
			            'font-size' : '2em',
			            //'background-color': 'data(class)',
			            'background-color': '#40FF00'
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

			var params = {
                name: 'cola',
                //maxSimulationTime: 20000,//800000, // max length in ms to run the layout
                edgeLength: function( edge ){var len = parseFloat(edge.data('length')); return Math.sqrt(len); },
                nodeSpacing: function( node ){ return 1; },
                nodeSpacing: 5,
                edgeLengthVal: 45,
                animate: true,
                randomize: false,
                //edgeLength
                //edgeSymDiffLength: undefined, // symmetric diff edge length in simulation
                //edgeJaccardLength: undefined
                //fit: false,
                infinite: true
            };

            $('#search_button').on('click', function() {
               var value = $("#input_search").val();
               cy.$('node[class!="grey"]').forEach(function( ele ){
                if (typeof ele.data('topWords')[value] == 'undefined'){
                    console.log(ele.data('id'))
                    cy.style().selector(ele).style({'width': '0.2'.concat('em'), 'height': '0.2'.concat('em')}).update()
                }else{
                    console.log(ele.data('id'), ele.data('topWords')[value])
                    cy.style().selector(ele).style({'width': (ele.data('topWords')[value]*10).toString().concat('em'), 'height': (ele.data('topWords')[value]*10).toString().concat('em')}).update()
                }
               });
               //console.log(value)
            });

            //cy.fit(); # holaaa
            var ly = cy.layout(params) //{name: 'cola'}
            //var ly2 = cyInNode.layout(params)
            //cy.center();

            $("#node_label").change(function () {
                var type_label = $("#node_label :selected").attr('value');
                if(type_label == "none_label"){cy.style().selector('node').style('label', '').update();}
                if(type_label == "name_theme"){cy.style().selector('node').style('label', 'data(label)').update();}
                if(type_label == "date_theme"){cy.style().selector('node').style('label', 'data(yearTheme)').update();}
                //var stringStylesheet = 'node { label: "data(label)" }';

            });


            $("#paint_node").change(function () {
                var type_label = $("#paint_node :selected").attr('value');
                if(type_label == "none_color"){
                    cy.$('node[class!="grey"]').forEach(function( ele ){
                          cy.style().selector(ele).style({
                          'pie-size': '0%',
                          'background-color':'#40FF00'
                          }).update()
                    });
                }
                if(type_label == "class_color"){
                    cy.$('node[class!="grey"]').forEach(function( ele ){
                          cy.style().selector(ele).style({
                          'pie-size': '0%',
                          'background-color':'data(class)'
                          }).update()
                    });
                }
                if(type_label == "pie_color"){

                    cy.$('node[class!="grey"]').forEach(function( ele ){
                      //console.log( ele.id() );
                      var topVenueSort = setFormatJs(ele.data("topVenue"), 'string');
                      topVenueSort.sort(function (a, b) {return  b.y - a.y;});
                      console.log(topVenueSort)
                      //style().ele.style({'width':'30em'}).update()
                      cy.style().selector(ele).style({
                      'pie-size': '100%',
                      'pie-1-background-color':colors_pubmed[topVenueSort[0]["x"]], 'pie-1-background-size':String(topVenueSort[0]["y"]*100)+'%',
                      'pie-2-background-color':colors_pubmed[topVenueSort[1]["x"]], 'pie-2-background-size':String(topVenueSort[1]["y"]*100)+'%',
                      //'pie-3-background-color':'#74E883', 'pie-3-background-size':String(topVenueSort[2]["y"]*100)+'%',
                      //'pie-4-background-color':'#E1E52B', 'pie-4-background-size':String(topVenueSort[3]["y"]*100)+'%'
                      }).update()
                    });
                }
                //var stringStylesheet = 'node { label: "data(label)" }';

            });

            //var $config = $('#config');
            //var $btnParam = $('<div class="param"></div>');
            //$config.append( $btnParam );

            /*
              var sliders = [
              {
                label: 'Node spacing',
                param: 'nodeSpacing',
                min: 1,
                max: 50
              }
            ];
            */
            //sliders.forEach( makeSlider );

            //function makeSlider( opts ){
              var $input = $('#in');
              //var $param = $('<div class="param"></div>');

              //$param.append('<span class="label label-default">'+ opts.label +'</span>');
              //$param.append( $input );

              //$config.append( $param );

              var p = $input.slider({
                min: 0.2,
                max: 10,
                //value: params[ opts.param ]
              }).on('slide', _.throttle( function(){

                console.log(p.getValue())
                //params[ opts.param ] = p.getValue();

                //ly.stop();  //'width': '0.5em',   cy.$('node').not('[class="grey"]').layout(defaults)
                cy.style().selector('node[class!="grey"]').style({'width': p.getValue().toString().concat('em'), 'height': p.getValue().toString().concat('em')}).update()
                //ly.run();
              }, 16 ) ).data('slider');
            //}


            var flag = true;
            //cy.layout({name: 'cola'})
            $('#playPause').on('click', function() {
                if(flag) {
                    $(this).html('<i class="fa fa-pause"></i>');
                      //console.log(cy.$('node')[0]._private.style.label.hide())   'label': 'data(yearTheme)'
                    ly.run();
                } else {
                    $(this).html('<i class="fa fa-play"></i>');
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
                //width: '100%',
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
                console.log("result Hereee!", x, y)
                //console.log(result.idToPmid[x])
                var title = '<span class="date">' + result.metaDoc[result.idToPmid[result.idDocOrdened[x]]]["title"] + '</span>'; //parseFloat(x)
                var swatch = '<span class="detail_swatch" style="background-color:"></span>'; // ' + series.color + '
                var year = result.metaDoc[result.idToPmid[result.idDocOrdened[x]]]["year"];
                var pmid = result.metaDoc[result.idToPmid[result.idDocOrdened[x]]]["pmid"];
                var venue = result.metaDoc[result.idToPmid[result.idDocOrdened[x]]]["venue"];
                var content = swatch + "Prob: " + parseFloat(y).toFixed(5) + " pmid: <span id='pmid' data-pmid="+pmid+">"+ pmid + "</span> venue:" + venue +" year:" + year + '<br>' + title; //
                return content;
            }
          });

            cy.on('tap', function(event){
              // target holds a reference to the originator
              // of the event (core or element)
              var evtTarget = event.target;

              if( evtTarget === cy ){
                  console.log('tap on background (cy)');
                  while(data.length > 0) {
                      var e = data.pop();
                      //$(String(e.name)).css("border-color", '#FE2E2E');
                      //data.pop();
                  }
                  graph.update();
                  $("#cy_in_node").html('');

              } else {
                console.log('tap on some element (cy)');
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
            //cy.$(':selected').remove();
            // ele.selected()
            //cy.on("cxttap", "node", function (evt) { });

            function make_njinnode(){
                //console.log("click derecho nueva version 4", this.id(), result.njInNode[this.id()])
                cyInNode = cytoscape({
                    container: document.getElementById('cy_in_node'),
                    elements: result.njInNode[this.id()],
                    // so we can see the ids
                  style:
                  [
                    {
                      selector: 'node',
                      style:{
                            //'label': 'data(yearTheme)',
                            'width': '2em',
                            'height': '2em',
                            'color': 'black',
                            'background-fit': 'contain',
                            'background-clip': 'none',
                            'border-style': 'solid',
                            'border-width': '0.1em',
                            'border-color': 'gray',
                            'font-size' : '2em',
                            //'background-color': 'data(class)',
                            'background-color':'data(class)'
                            }
                    },
                    {
                      selector: 'node:selected',
                      style: {
                        "border-width": '1em',
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
                          }
                          //
                      //layout:{defaults}
                }); // fin citoscape

                // https://stackoverflow.com/questions/46076684/cytoscape-js-detecting-if-any-nodes-have-been-selected-on-boxend


                cyInNode.on('click', 'node', function(evt){

                       //cyInNode.style().selector('node[class!="grey"]').style({"border-width": '0em', "border-color": '#FE2E2E', "border-opacity": '0.5',"text-outline-color": '#77828C'}).update();
                       //cyInNode.style().selector(this).style({"border-width": '1em', "border-color": '#FE2E2E', "border-opacity": '0.5',"text-outline-color": '#77828C'}).update();  //css("border-color", '#FE2E2E');

                       $("#timeline").html('');

                       var annotator = new Rickshaw.Graph.Annotate({
                          graph: graph,
                          element: document.getElementById('timeline')
                       });

                       $("#id_doc").text(this.id());
                       $("#title_doc").text(result.metaDoc[this.id()]["title"]);
                       $("#year_doc").text(result.metaDoc[this.id()]["year"]);
                       $("#link_doc").text('pubmed/'+this.id());
                       $("#link_doc").attr("href", 'https://www.ncbi.nlm.nih.gov/pubmed/'+this.id());
                       // aquiiii

                        // en las variables existe idtopmid pero se necesita pmidtoid esa es la mejor solución por el momento se hará solo una busqueda
                        mark_Key = null;
                        for(var key in result.idToPmid) {
                            //console.log(result.idToPmid[key]," ", Number(this.id()))
                            if(result.idToPmid[key] === Number(this.id())) {
                                mark_Key = key;
                                console.log("key: ",key, "pmid: ", this.id())
                                break;
                            }
                        }

                        // deberia optimizarse hace dos busquedas
                        for(var key in result.idDocOrdened) {
                            //console.log(result.idToPmid[key]," ", Number(this.id()))
                            if(result.idDocOrdened[key] === Number(mark_Key)) {
                                mark_Key = key;
                                console.log("key real: ", mark_Key)
                                break;
                            }
                        }

                        annotator.add(mark_Key, "");
                        console.log(annotator)
                        annotator.update();
                    });

                cyInNode.on('tap', function(event){
                      var evtTarget = event.target;
                      if( evtTarget === cyInNode ){
                          console.log('tap on background (cyInNode)');
                            $("#timeline").html('');

                      } else {
                        console.log('tap on some element (cyInNode)');
                      }
                    });

                //cy.$(':selected').remove();
                // ele.selected()
                cyInNode.$('node[class!="grey"]').on("box", function (evt) {

                        var annotator = new Rickshaw.Graph.Annotate({
                            graph: graph,
                            element: document.getElementById('timeline')
                        });

                        ran_color = getRandomColor();
                        evt.target.css("border-color", ran_color);
                        console.log(evt.target.id())//cy.$(':selected'));

                        mark_Key = null;
                        for(var key in result.idToPmid) {
                            //console.log(result.idToPmid[key]," ", Number(this.id()))
                            if(result.idToPmid[key] === Number(evt.target.id())) {
                                mark_Key = key;
                                console.log("key: ",key, "pmid: ", evt.target.id())
                                break;
                            }
                        }

                        // deberia optimizarse hace dos busquedas
                        for(var key in result.idDocOrdened) {
                            //console.log(result.idToPmid[key]," ", Number(this.id()))
                            if(result.idDocOrdened[key] === Number(mark_Key)) {
                                mark_Key = key;
                                console.log("key real: ", mark_Key)
                                break;
                            }
                        }

                        //annotator.css("border-color", ran_color);
                        annotator.add(mark_Key, "");
                        console.log(annotator)
                        annotator.update();

                        $(".annotation").last().attr( 'id', mark_Key)
                        $('#'+mark_Key).css("background-color", ran_color);
                    });

            };

			cy.on('click', 'node', function(evt){

              ran_color = getRandomColor();

              if(evt.originalEvent.ctrlKey) {
                console.log(this.id())
                if (this.selected()){
                    //console.log("unselect")
                    for (var i = 0; i < data.length; i ++) {
                        if (data[i].name == this.id()) {
                            data.splice(i, 1);
                            break;
                        }
                    }
                }
                else{
                    //console.log("select")
                    this.css("border-color", ran_color);
                    ts = this.data("topDistribution");
                    data.push({name: this.id(), data: setFormatJs(ts, 'number'), color: ran_color});
                    //console.log(data)
                }
                graph.update();
              }
              else{
                  $("#timeline").html('');
			      ts = this.data("topDistribution");
			      console.log(setFormatJs(ts, 'number'));
			      //console.log("click normal")
			      // add rows top venue
			      $("#top_venues").html('');
                  var topVenueSort = setFormatJs(this.data("topVenue"), 'string');
                  topVenueSort.sort(function (a, b) {return  b.y - a.y;});
                  //console.log(topVenueSort)

                  for (v in topVenueSort){
                  //console.log(v)
                    $('#top_venues').append('<tr class="item"><td><div class="swatch" style="background-color:'+ colors_pubmed[topVenueSort[v]['x']] +';"></div>'+ topVenueSort[v]['x'].replace(/_/g , " ") +'</td><td>'+ topVenueSort[v]['y'] +'</td></tr>');
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
                  // http://mistic100.github.io/jQCloud/demo.html
			      var words = [];
                  jQuery('#wordcloud_second').jQCloud(words, {width: 300,
                        height: 300});

                  for(e in this.data("topWords")){words.push({text:e, weight:this.data("topWords")[e]})}

			      //console.log(words)
                    //$('#wordcloud').html('')
                   //$('#tree_wordcloud').on('click', function() {
                      //console.log("click word cloud")
                      jQuery('#wordcloud_second').jQCloud('update', words, {
                        width: 300,
                        height: 300,
                      //shape: 'rectangular',
                      colors: ["rgb(31, 119, 180)", "rgb(174, 199, 232)", "rgb(255, 127, 14)", "rgb(255, 187, 120)", "rgb(44, 160, 44)", "rgb(152, 223, 138)", "rgb(214, 39, 40)", "rgb(255, 152, 150)", "rgb(148, 103, 189)", "rgb(197, 176, 213)", "rgb(140, 86, 75)", "rgb(227, 119, 194)", "rgb(247, 182, 210)", "rgb(127, 127, 127)", "rgb(199, 199, 199)", "rgb(188, 189, 34)", "rgb(23, 190, 207)", "rgb(158, 218, 229)", "rgb(196, 156, 148)", "rgb(219, 219, 141)"]
                     });
                   //});
                   $('#wordcloud_first').html($('#wordcloud_second').html())
                   // aqui
                   make_njinnode.apply(this);;
              }
			}); // fin click

            $('#tree_wordcloud').on('click', function() {
                //console.log($('#wc_1').html());
                $('#wordcloud_first').html($('#wordcloud_second').html())
            });


			$('#config-toggle').on('click', function(){
			  $('body').toggleClass('config-closed');
			  cy.resize();
			});

			$("#tss").on('click', function(evt){
               var pmid = document.getElementById("pmid").getAttribute("data-pmid");
               cyInNode.style().selector('node[class!="grey"]').style({"border-width": '0em', "border-color": '#FE2E2E', "border-opacity": '0.5',"text-outline-color": '#77828C'}).update();
               cyInNode.style().selector(cyInNode.getElementById(pmid)).style({"border-width": '5em', "border-color": '#FE2E2E', "border-opacity": '0.5',"text-outline-color": '#77828C'}).update();  //css("border-color", '#FE2E2E');
/*
               cyInNode.$('node[class!="grey"]').forEach(function( ele ){
                if (ele.data('id') == pmid){
                    console.log('CHI',ele.data('id'))
                    cyInNode.style().selector(ele).style({"border-width": '5em', "border-color": '#FE2E2E', "border-opacity": '0.5',"text-outline-color": '#77828C'}).update()
                }
               });
*/
                console.log(cyInNode.getElementById(pmid));
            });

            $("#tss").bind("contextmenu", function(){
              //console.log(document.getElementById("pmid").getAttribute("data-pmid"));
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