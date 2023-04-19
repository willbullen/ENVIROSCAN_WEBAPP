/* ---------------------------------------------------------------------

 Matterport SDK v3.0.6 Kitchen Sink
 Copyright 2017 Chris Hickman

 Demonstration of all Matterport SDK v3.0 functions.
 
 Parameters:
 
	?m=MODELID - Launch immediately with MODELID

 All functions are scoped under loadedShowcaseHandler()
 Uses jQuery for click events

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License, version 3, as
 published by the Free Software Foundation.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 https://www.gnu.org/licenses/gpl-3.0.en.html

------------------------------------------------------------------------ */

/* global $ */
/*
SCAN TEMPLATE
project = {
     "project_name": "",
     "project_description": "",
     "project_status": "",
     "project_name": "",
     "models":[
        {
            "model_name":"Replace Name",
            "model_mportid":"xxxxxxxxxxxxx",
            "model_datetime":"xxxxxxxxxxxxx",
            "model_imagepath":"/images/temp/Plan/ga.png",
            "default_level":"0",
            "levels":[
                {
                    "level_name":"New Level",
                    "level_id":"0",
                    "start_value":"0",
                    "level_imagepath":"../../images/template/Levels/level.png",
                    "xoffset":"0",
                    "xconst":"0",
                    "zoffset":"0",
                    "zconst":"0",
                    "mexoffset":"0",
                    "mexconst":"0",
                    "mezoffset":"0",
                    "mezconst":"0",
                    "rotate":"0",
                    "flip_me":"0",
                    "scans":[
                        {
                            "pid":"0",
                            "value":"0",
                            "title":"0",
                            "xpos":"0",
                            "zpos":"0",
                            "show":"0",
                            "color":"pano z-depth-3",
                            "number":"0"
                        }
                    ]
                }
            ]
        }
    ]
}
*/

console.log('Welcome to the Matterport SDK Kitchen Sink!');

var map = document.getElementById('imageMap');

var scanSettings = [];
var me = [];
var levelId;
var btn = [];
var btnVariables = [];

function panoMove(event) {
	//console.log(event.target.value);
	return showcase.Sweep.moveTo(event.target.value)
		.then(handleMessage)
		.catch(handleError);
}

// Allow URL parameters

$.urlParam = function(name){
	var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
	if (results==null)
       return false;
    else
       return results[1] || 0;
}

var model = decodeURIComponent($.urlParam('m'));
if (model!='false') {
	$('#showcase_iframe').attr('src', 'https://my.matterport.com/show/?m=' + model + '&play=1&tourcta=0');
	$('#showcase_iframe').on('load',showcaseLoader);
}
else {
	$('#showcase_loader').fadeIn();
}

$('body').on('click','dd a', function(e) {
	e.stopPropagation();
})
$('body').on('click', 'dd', function (e){
	if ($(this).hasClass('pre')) {
		$(this).removeClass('pre');
	}
	else {
		$(this).addClass('pre');
	}
});


// Helper Functions --------------------------------------------------------------------------------------

// Simple time to formatted date function
function dateFormat(d){
	if (d != 0) {
		var s = new Date(d);
		var month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
		var date = s.getDate() + " " + month[s.getMonth()] + ", " +  s.getFullYear();
		var time = s.toLocaleTimeString().toLowerCase();
		return (d + " (" + date + " " + time + ")"); 
	}
	else 
		return '0';
}


// Output formatted content to the in-browser console as well as the native console.
function c(input,output,subscription = false) {
	var dt = new Date().toJSON();
    if (subscription == true) {
		$('#listeners').prepend('<dt>' + input + '</dt><dd>' + output + '</dd>');
	}
	else {
		console.log(input + ' - ' + output);
		$('#commands').prepend('<dt>' + input + '</dt><dd>' + output + '</dd>');
	}	
}

/////////////////////////////////////////////////////////////////////
$('#load_project_setup').click(function() {
	$('#project_setup_iframe').attr('src', 'https://my.matterport.com/show/?m=' + $('#project_setup_matp_id').val() + '&utm_source=sdkdebug&play=1&tourcta=0');
	$('#project_setup_iframe').on('load',project_setup_matterport_loader);
});

function project_setup_matterport_loader() {
	try {
		var showcase = window.MP_SDK.connect(
			document.getElementById('project_setup_iframe'),
            '7rbk6ztzfti5rwifim395bqec',
			''
		)
		.then(function(mpSdk) {
			c('window.SHOWCASE_SDK.connect($("#commands")), [apikey], "")', 'SDK Loaded!');
			project_setup_matterport_loader_handler(mpSdk);
		})
		.catch(function(error) {
			c('window.SHOWCASE_SDK.connect($("#commands")), [apikey], "")','Error: ' + error);
		});
	}
	catch (e) {
		console.error(e);
	}
}

function project_setup_matterport_loader_handler(mpSdk) {
	
	// Store modelData at the main function level. (used later with Mattertags)
	var modelData;	
	mpSdk.Model.getData()
		.then(function(model) {
			modelData = model;

			
			var models = {};
			var levels = {};
			var scans = {};
			var model_level = "";

			for (var i = 0, len = modelData.sweeps.length; i < len; ++i) {
				var jdata = modelData.sweeps[i];
				if (model_level != jdata.floor) {
					console.log(model_level);
				}
				model_level = jdata.floor;
			}
			project = {
				"project_name": "",
				"project_description": "",
				"project_status": "",
				"models":[
				   {
					   "model_name":"Replace Name",
					   "model_mportid":"xxxxxxxxxxxxx",
					   "model_datetime":"xxxxxxxxxxxxx",
					   "model_imagepath":"/images/temp/Plan/ga.png",
					   "default_level":"0",
					   "levels":[
						   {
							   "level_name":"New Level",
							   "level_id":"0",
							   "start_value":"0",
							   "level_imagepath":"../../images/template/Levels/level.png",
							   "xoffset":"0",
							   "xconst":"0",
							   "zoffset":"0",
							   "zconst":"0",
							   "mexoffset":"0",
							   "mexconst":"0",
							   "mezoffset":"0",
							   "mezconst":"0",
							   "rotate":"0",
							   "flip_me":"0",
							   "scans":[
								   {
									   "pid":"0",
									   "value":"0",
									   "title":"0",
									   "xpos":"0",
									   "zpos":"0",
									   "show":"0",
									   "color":"pano z-depth-3",
									   "number":"0"
								   }
							   ]
						   }
					   ]
				   }
			   ]
		   };
		   console.log('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');


			c('mpSdk.Model.getData()',JSON.stringify(model,null,2));
		}).catch(function(error) {
			c('mpSdk.Model.getData()', 'Failed: ' + error);
		}
	);
	
}
////////////////////////////////////////////////////////////////////

// Defer starting Showcase SDK until user input on URL box
$('#loadTour').click(function() {
	$('#showcase_iframe').attr('src', $('#tourURL').val() + '&play=1&tourcta=0');
	$('#console').fadeIn();
	$('#showcase_loader').fadeOut();
	$('#showcase_iframe').on('load',showcaseLoader);
});


function showcaseLoader() {
	try {
		var showcase = window.MP_SDK.connect(
			document.getElementById('showcase_iframe'),
            '7rbk6ztzfti5rwifim395bqec', // SDK Key -- swap for your own. 
			'' // Unused but needs to be a valid string (was previously SDK version)

		)
		.then(function(mpSdk) {
			// Model.Event.MODEL_LOADED
			c('window.SHOWCASE_SDK.connect($("#commands")), [apikey], "")', 'SDK Loaded!');
			loadedShowcaseHandler(mpSdk);
		})
		.catch(function(error) {
			c('window.SHOWCASE_SDK.connect($("#commands")), [apikey], "")','Error: ' + error);
		});
	}
	catch (e) {
		console.error(e);
	}
}

// Execute on Showcase IFRAME Load
function loadedShowcaseHandler(mpSdk) {

	// Initialize scrollbars on functions / subscriptions 
	
	var cScroll = new PerfectScrollbar('#commands');
	cScroll.update();

	var lScroll = new PerfectScrollbar('#listeners');
	lScroll.update();
	
	// Output all SDK functions to content box.
	console.log(mpSdk);
	c('mpSdk',JSON.stringify(mpSdk,null,2));

	// Store modelData at the main function level. (used later with Mattertags)
	var modelData;	
	mpSdk.Model.getData()
		.then(function(model) {
			modelData = model;

			console.log('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');

			var project = {
				"project_name": "",
				"project_description": "",
				"project_status": "",
				"models":[],
			};
			var models = {};
			var levels = {};
			var scans = {};

			for (var i = 0, len = modelData.sweeps.length; i < len; ++i) {
				var jdata = modelData.sweeps[i];
				var model_level = jdata.floor;
			}
			project = {
				"project_name": "",
				"project_description": "",
				"project_status": "",
				"models":[
				   {
					   "model_name":"Replace Name",
					   "model_mportid":"xxxxxxxxxxxxx",
					   "model_datetime":"xxxxxxxxxxxxx",
					   "model_imagepath":"/images/temp/Plan/ga.png",
					   "default_level":"0",
					   "levels":[
						   {
							   "level_name":"New Level",
							   "level_id":"0",
							   "start_value":"0",
							   "level_imagepath":"../../images/template/Levels/level.png",
							   "xoffset":"0",
							   "xconst":"0",
							   "zoffset":"0",
							   "zconst":"0",
							   "mexoffset":"0",
							   "mexconst":"0",
							   "mezoffset":"0",
							   "mezconst":"0",
							   "rotate":"0",
							   "flip_me":"0",
							   "scans":[
								   {
									   "pid":"0",
									   "value":"0",
									   "title":"0",
									   "xpos":"0",
									   "zpos":"0",
									   "show":"0",
									   "color":"pano z-depth-3",
									   "number":"0"
								   }
							   ]
						   }
					   ]
				   }
			   ]
		   };
		   console.log('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');




















			//////////////////////////////////////////////
			
			var dotArray = [];
			var dotPid, dotValue, dotTitle, dotXpos, dotZpos, dotShow, dotClass, dotNumber;
			for (var i = 0, len = modelData.sweeps.length; i < len; ++i) {
				var jdata = modelData.sweeps[i];
				
				dotPid = 'p' + jdata.uuid;
				dotValue = jdata.uuid;
				dotClass = 'pano z-depth-3';
				dotNumber = i;

				dotTitle = i;
				dotXpos = jdata.position.x;
				dotZpos = jdata.position.z;
				dotShow = 1; 
				
				btn[i] = document.createElement('BUTTON');
				btn[i].setAttribute('title', dotTitle);
				btn[i].setAttribute('id', dotPid);
				btn[i].setAttribute('value', dotValue);
				btn[i].style.zIndex = '400';
				btnVariables[i] = {zPos: jdata.position.z, xPos: jdata.position.x};

				btn[i].style.left = dotXpos + '%';
				btn[i].style.top = dotZpos + '%';

				if (dotShow) {
					btn[i].style.visibility = 'visible';
				} else {
					btn[i].style.visibility = 'hidden';
				}
				btn[i].setAttribute('class', 'pano z-depth-3');
				btn[i].addEventListener('click', panoMove);
				map.appendChild(btn[i]);

				dotArray.push({
					pid: dotPid, 
					value: dotValue,
					title: dotTitle, 
					xpos: dotXpos, 
					zpos: dotZpos,
					show: dotShow,
					color: dotClass,
					number: dotNumber,
					level: jdata.floor
				});
			}

			me[0] = document.createElement('IMG');
			me[0].setAttribute('id', 'meIcon');
			me[0].style.width = '22px';
			me[0].style.height = '45px';
			me[0].style.left = '50%';
			me[0].style.top = '50%';
			me[0].style.position = 'absolute';
			me[0].src = '/staticfiles/app_dalys/img/dot.png';
			me[0].style.zIndex = '500';
			me[0].setAttribute('class', 'meIcon');
			map.appendChild(me[0]);

			//map.setAttribute('style', 'transform:rotate(' + scanSettings.Levels[levelId].qlRotOffset + 'deg)');
			/////////////////////////////////////////////


			c('mpSdk.Model.getData()',JSON.stringify(model,null,2));
		}).catch(function(error) {
			c('mpSdk.Model.getData()', 'Failed: ' + error);
		}
	);

	// Store modelDetails at the main function level.  Not used currently.
	var modelDetails;
	mpSdk.Model.getDetails()
		.then(function(details) {
			modelDetails = details;
			c('mpSdk.Model.getDetails()', JSON.stringify(details,null,2));
		}).catch(function(error) {
			c('mpSdk.Model.getDetails()', 'Failed: ' + error);
		}
	);

	// Store floorDetails at the main function level.  Not used currently.
	var floorDetails;
	mpSdk.Floor.getData()
		.then(function(floors) {
			// Floor data retreival complete.
			c('mdSdk.Floor.getData()', JSON.stringify(floors,null,2));
			
			// Create floor navigation buttons
			var i = 0;
			for (i = floors.totalFloors; i > 0; i--) {
				$('#floors').prepend('<button class="b_Floor_moveTo" data-val="' + (i-1) + '" ><i class="floor-number">' + i + '</i><i class="icon icon-floor-controls"></i></button>');
			}
		})
		.catch(function(error) {
			c('mdSdk.Floor.getData()', 'Failed: ' + error);
		}
	);

	var settings = [
		'presented_by','highlight_reel','floor_plan','tour_buttons','labels','dollhouse','fast_transitions','contact_email','address','contact_name','model_summary','contact_phone','model_name','external_url'
	];
	$.each(settings, function(k,e) {
		mpSdk.Settings.get(e).then(function(data) {
	    // Setting retreival complete.
	    	c('<span class="settings" data-name="' + e + '" data-value="' + data + '">mpSdk.Settings.get("' + e + '")</span>', data);
		})
		.catch(function(error) {
	  		c('mpSdk.Settings.get("' + e + '")', error);
		});
	});
	$('#console').delegate('.settings', 'click', settingsToggle);
	function settingsToggle() {
		var setting = this.getAttribute("data-name");
		var settingValue = this.getAttribute("data-value");
		$(this).setAttribute("data-value",!settingValue);
		mpSdk.Settings.update(setting,(!settingValue))
			.then(function(results) {
				c('mpSdk.Settings.update("'+setting+'","'+(!settingValue)+'")', results);
				return true;
				
			}).catch(function(error) {
				c('mpSdk.Settings.update("'+setting+'","'+(!settingValue)+'")', 'Failed: ' + error);
				return false;
			})
	}

//	$('.settings').delegate

// Button Click Events
// Each button gets its own function so that I can change to onclick== HTML params.

	// Map Marker Icon -- Camera.getPose()
	$('.b_getPose').click(getPose);
	function getPose() {
		mpSdk.Camera.getPose()
			.then(function(pose){
				c('mpSdk.Camera.getPose()', JSON.stringify(pose,null,2));
				return pose;
			}).catch(function(error) {
				c('mpSdk.Camera.getPose()', 'Failed: ' + error);
				return false;
			}
		);	
	}
	
	// Left, Right, Forward, Backward, Up and Down Arrows
	$('.b_moveInDirection').click(MoveInDirection);
	function MoveInDirection() {
		// Use data-var attribute to determine direction
		var dir = $(this).data("val");
		
		mpSdk.Camera.moveInDirection(dir)
			.then(function(){
				c('mpSdk.Camera.moveInDirection(' + dir + ')', 'Success');
				return true;
			})
			.catch(function(error){
				c('mpSdk.Camera.moveInDirection(' + dir + ')', 'Failed: ' + error);
				return false;
			}
		);
	}

	// Home Button -- Dual function

	$('.b_home').click(home);	
	function home() {
		mpSdk.Camera.getPose()
			.then(function(pose){
				
				// In Dollhouse and Floorplan Mode
				// Use mpSdk.Camera.pan({ x: 0, z: 0 }); to return to directly above the very first pano scanned.

				if (pose.mode == 'mode.dollhouse' || pose.mode == 'mode.floorplan') {
					mpSdk.Camera.pan({ x: 0, z: 0 })
						.then(function() {
							c('mpSdk.Camera.pan({ x: 0, z: 0})', 'Success - Returned directly above the first pano scanned (absolute coordinates).');
							return true;
						})
						.catch(function(error) {
							c('mpSdk.Camera.pan({ x: 0, z: 0})', 'Failed: ' + error);
							return false;
						}
					);
				}
				
				// In Inside and Outside Mode, return to first scan -- should probably make this return to the start position
				else if (pose.mode == 'mode.inside' || pose.mode == 'mode.outside') {
					mpSdk.Sweep.moveTo(modelData.sweeps[0].uuid) /*,
						{ // According to the SDK docs, I should be able to pass these parameters -- however it fails when I do.
							rotation: [0,0,0],
							transition: 'transition.fade'
						}
					)*/
					.then(function(sweepId){
						c('mpSdk.Sweep.moveTo("'+modelData.sweeps[0].uuid+')', 'Arrived at sweep #1 (Home)');
						return true;
					})
					.catch(function(error){
						c('mpSdk.Sweep.moveTo("'+modelData.sweeps[0].uuid+')', 'Failed: ' + error);
						return false;
					});
				}
			});
	}
	
	// Takes a Screenshot	
	$('.b_takeScreenshot').click(takeScreenshot);
	function takeScreenshot() {
		
		// Take Screenshot cannot handle a full screen area and the width/height must be proportional
		// to the Showcase frame to generate a proportional image.  Kind of a pain, but we'll find
		// the width/height of the iframe and scale it proportionally for 640 x X
		
		var width = $('#showcase_iframe').width();
		var height = $('#showcase_iframe').height();
		var propHeight = parseInt(height * 640 / width);
		
		// width / height = 640 / X
		var dimensions = { width: 640, height: propHeight };
		var options = { mattertags: false, sweeps: true};
		mpSdk.Camera.takeScreenShot( dimensions, options)
			.then(function (screenShotUrl) {
				var d = new Date();
				var id = d.getTime();
				c('mpSdk.Camera.takeScreenShot( {width: 640, height: ' + propHeight + '},{mattertags: false, sweeps: true})', '<img id="i' + id + '" />');
				$('#i'+id).attr('src',screenShotUrl);
				return screenShotUrl;
			})
			.catch(function(error) { // Undocumented -- is error logging avialable?
				c('mpSdk.Camera.takeScreenShot( {width: 640, height: ' + propHeight + '},{mattertags: false, sweeps: true})', 'Error: ' + error);
				return false;
			});
	}
	
	$('.b_takePano').click(takePano);
	function takePano() {
		
		// width / height = 640 / X
		var dimensions = { width: 8192, height: 4096 };
		var options = { mattertags: false, sweeps: true};
		mpSdk.Renderer.takeEquirectangular(dimensions,options)
			.then(function (screenShotUrl) {
				var d = new Date();
				var id = d.getTime();
				c('mpSdk.Renderer.takeEquirectangular( {width: 4096, height: 2048},{mattertags: false, sweeps: true})', '<img id="i' + id + '" />');
				$('#i'+id).attr('src',screenShotUrl);
				return screenShotUrl;
			})
			.catch(function(error) { // Undocumented -- is error logging avialable?
				c('mpSdk.Renderer.takeEquirectangular( {width: 4096, height: 2048},{mattertags: false, sweeps: true})', 'Error: ' + error);
				return false;
			});
	}

	// Labels
	$('.b_LabelgetData').click(getLabelData);
	function getLabelData() {
		mpSdk.Label.getData()
			.then(function(labels) {
				// Label data retreival complete.
				if (labels.length > 0 ) {
					c('mpSdk.Label.getData()', 'Total labels: ' + labels.length + ' - ' + JSON.stringify(labels,null,2));
					return labels;
				}
				else {
					c('mpSdk.Label.getData()', 'Total labels: 0');
					return false;
				}
			})
			.catch(function(error) {
				c('mpSdk.Label.getData()', 'Failed: ' + error);
				return false;
			});
	}

	// Mattertags
	$('.b_Mattertag').click(getMattertagData);
	function getMattertagData() {
		mpSdk.Mattertag.getData()
			.then(function(mattertags) {
				// Mattertag data retreival complete.
				if(mattertags.length > 0) {
					c('mpSdk.Mattertag.getData()', 'Total Mattertags: ' + mattertags.length + ' - ' + JSON.stringify(mattertags, null, 2));
					// Generate clicakble list in console.
					var clicktags = 'Mattertags: ';
					$.each(mattertags, function(key,mattertag) {
						 clicktags += "<span class='mattertag' data-val='"+ mattertag.sid + "'>Tag #" + key + "</span> ";
					});
					c('mpSdk.Mattertag.navigateToTag(sid)', clicktags);
					return mattertags;
				}
				else {
					c('mpSdk.Mattertag.getData()', 'Total Mattertags: 0');
					return false;
				}
			})
			.catch(function(error) {
				c('mpSdk.Mattertag.getData()', 'Failed: ' + error);
				return false;
			});			
	}
	
	// Allow clickable Mattertags from generated list in console.
	$('#console').delegate('.mattertag', 'click', mattertagToggle);
	function mattertagToggle() {
		var tag = this.getAttribute("data-val");

		// SDK v3.0.6 - https://static.matterport.com/showcase/3.0.6.0-119-g2e3a1524c/*
		if (typeof mpSdk.Mattertag.Transition != 'undefined') {
			mpSdk.Mattertag.navigateToTag(tag, mpSdk.Mattertag.Transition.FADEOUT).
				then(function(results) {
					c('mpSdk.Mattertag.navigateToTag("'+tag+'")', 'Success: ' + results);
					return true;
				})
				.catch (function(error) {
					c('mpSdk.Mattertag.navigateToTag("'+tag+'")', 'Error : ' + error);
					return false;
				});
		}
		else {
			mpSdk.Mattertag.navigateToTag(tag).
				then(function(results) {
					c('mpSdk.Mattertag.navigateToTag("'+tag+'")', 'Success: ' + results);
					return true;
				})
				.catch (function(error) {
					c('mpSdk.Mattertag.navigateToTag("'+tag+'")', 'Error : ' + error);
					return false;
				});
		}
	
	}
	
	// Rotation
	$('.b_rotateInDirection').click(rotateInDirection);
	function rotateInDirection() {
		var directions = {
			'LEFT'  : [-40, 0],
			'RIGHT' : [ 40, 0],
			'UP'    : [0,20],
			'DOWN'  : [0,-20]
		};
		var dir = this.getAttribute("data-val");
		
		mpSdk.Camera.rotate(directions[dir][0], directions[dir][1])
		  .then(function(){
			c('mpSdk.Camera.rotate(' + directions[dir][0] + ',' + directions[dir][1] + ')', 'Success' );
			})
		  .catch(function(error){
			c('mpSdk.Camera.rotate(' + directions[dir][0] + ',' + directions[dir][1] + ')', 'Failed: ' + error );
		  });
	}

	// Change Mode
	$('.b_moveTo').click(moveTo);
	function moveTo() {
		var mode = this.getAttribute("data-val");
		mpSdk.Camera.getPose()
			.then(function(pose){
				// If dollhouse is requested while already in Dollhouse, show all floors.
				if (pose.mode == 'mode.dollhouse' && mode == 'mode.dollhouse') {
					mpSdk.Floor.showAll()
					  .then(function(){
						c('mpSdk.Floor.showAll()', 'Now displaying all floors.');
					  })
					  .catch(function(error) {
						c('mpSdk.Floor.showAll()', 'Failed: ' + error);
					  });					
				} else {
					mpSdk.Mode.moveTo(mode)
					  .then(function(nextMode){
						c('mpSdk.Mode.moveTo("' + mode + '")', 'Success');
					  })
					  .catch(function(error){
						c('mpSdk.Mode.moveTo("' + mode + '")', 'Failed: ' + error);
					  });					
				}
			}
		);
	}
	
	// Guided Tour

	// Set data val for button toggle.
	$('#tourToggle').data('val','START');

	// We will store the step so that when we restart the tour, it will not restart.
	$('#tourToggle').data('step',-1);

	$('.b_tour').click(tourToggle);
	function tourToggle() {
		var buttonMode = $('#tourToggle').data('val');
		c(buttonMode,buttonMode);
		if (buttonMode != 'START') {
			mpSdk.Tour.stop()
				.then(function() {
					// Tour start complete.
					c('mpSdk.Tour.stop()', 'Success');
				})
				.catch(function(error) {
					// Tour start error.
					c('mpSdk.Tour.stop(1)', 'Failed: ' + error);
				}
			);
		}
		else {
			var step = new Number($('#tourToggle').data('step'))+1;
			mpSdk.Tour.start(step)
				.then(function() {
					mpSdk.Tour.getData().then(function(tour) {
						c('mpSdk.Tour.getData()', JSON.stringify(tour, null, 2));
					}).
					catch(function(error) {
						c('mpSdk.Tour.getData()','Failed: ' + error);
					});
					// Tour start complete.
					c('mpSdk.Tour.start(' + step + ')', 'Success');
				})
				.catch(function(error) {
					// Tour start error.
					c('mpSdk.Tour.start(' + step + ')', 'Failed: ' + error);
				}
			);		
		}
	}

	// Tour Step - Prev
	$('.b_tour_prev').click(tourPrev);
	function tourPrev() {

		// Detect if tour is playing based on stored value
		if ($('#tourToggle').data('val') == 'PAUSE') {
			// Simulate a mouseclick to stop the tour (jQuery is fun!)
			$('#tourToggle').click();
		}

		mpSdk.Tour.prev()
			.then(function() {
				// Tour next complete.
				c('mpSdk.Tour.prev()','Success');
			})
			.catch(function(error) {
				// Tour next error.
				c('mpSdk.Tour.prev()','Failed: ' + error);
			}
		);
	}

	// Tour Step - Next
	$('.b_tour_next').click(tourNext);
	function tourNext() {

		// Detect if tour is playing based on stored value
		if ($('#tourToggle').data('val') == 'PAUSE') {
			// Simulate a mouseclick to stop the tour (jQuery is fun!)
			$('#tourToggle').click();
		}
	
		mpSdk.Tour.next()
			.then(function() {
				// Tour next complete.
				c('mpSdk.Tour.next()','Success');
			})
			.catch(function(error) {
				// Tour next error.
				c('mpSdk.Tour.next()','Failed: ' + error);
			}
		);
	}

	// Tour Step - Next
	$('.b_Floors').click(function() {
		mpSdk.Floor.getData()
		  .then(function(floors) {
		    // Floor data retreival complete.
		    c('mpSdk.Floor.getData()', JSON.stringify(floors, null, 2));
		  })
		  .catch(function(error) {
		    // Floors data retrieval error.
		    c('mpSdk.Floor.getData()', 'Failed: ' + error)
		  });
	});
			
	// Move Floors
	$('#floors').delegate('button.b_Floor_moveTo', 'click', moveFloors);
	function moveFloors() {
		var floor = Number($(this).data("val"));
		mpSdk.Floor.moveTo(floor)
		  .then(function(floorIndex) {
			c('mpSdk.Floor.moveTo('+floor+')', 'Success');
			// Move to floor complete.
		  })
		  .catch(function(error) {
			// Error moving to floor.
			c('mpSdk.Floor.moveTo('+floor+')', 'Failed: ' + error);
		  });
	}


// Subscriptions


	// https://matterport.github.io/showcase-sdk/docs/sdk/reference/current/modules/app.html#state-1
	
	c('mpSdk.App.state.subscribe(function (appState) {...})', '');
	mpSdk.App.state.subscribe(function (appState) {
		c('App state has changed (mpSdk.App.state.subscribe)', '', true);
		c('The current application (appState.application): ', appState.application, true);
		c('The current phase (appState.phase): ', appState.phase, true); 
		c('Loaded at time (appState.phaseTimes[mpSdk.App.Phase.LOADING])', dateFormat(appState.phaseTimes[mpSdk.App.Phase.LOADING]), true);
		c('Started at time (appState.phaseTimes[mpSdk.App.Phase.STARTING])', dateFormat(appState.phaseTimes[mpSdk.App.Phase.STARTING]), true);
	});	


// Event Actions

	// Create variable to store the initial pose at the function level.
	// We'll fire this from mpSdk.on(mpSdk.App.Event.PLAYING) when appphase.playing
	var initialPose = getPose();

	// This event fires when the camera is starting to transition to a mode.
	mpSdk.on(mpSdk.Mode.Event.CHANGE_START, function(from,to){
		  
		$('.xtour').css('display','inline-block');
		// Hide Current Mode's Icon
		switch (to) {
			case 'mode.dollhouse':
				$('.b_dollhouse').css('display','none');
				break;
			case 'mode.inside':	
				$('.b_inside').css('display','none');
				break;
			case 'mode.floorplan':
				$('.b_floorplan').css('display','none');
				break;
		}
	
		c('mpSdk.on(mpSdk.Mode.Event.CHANGE_START)', 'From: ' + from + ' To: ' + to, true);
		
	  }
	);

	// This event fires when the camera's pose has changed via a position or orientation change.
	mpSdk.on(mpSdk.Camera.Event.MOVE, function(pose){
		c('mpSdk.on(mpSdk.Camera.Event.MOVE)', JSON.stringify(pose,null,2), true);
	  }
	);
	
	
	// This event fires when the camera has completed a transition to a mode.
	mpSdk.on(mpSdk.Mode.Event.CHANGE_END,
	  function(from, to){
		c('mpSdk.on(mpSdk.Mode.Event.CHANGE_END)', 'From: ' + from + ' To: ' + to, true);
	  }
	);
	
	// This event fires when a floor change is starting.
	mpSdk.on(mpSdk.Floor.Event.CHANGE_START,
	  function(to, from) {
		c('mpSdk.on(mpSdk.Floor.Event.CHANGE_START)', 'To: ' + to + ' From: ' + from, true);
	  }
	);
	
	// This event fires when a floor change is ending.
	mpSdk.on(mpSdk.Floor.Event.CHANGE_END,
	  function(floor) {
		c('mpSdk.on(mpSdk.Floor.Event.CHANGE_END)', 'Moved to: ' + JSON.stringify(floor), true);
	  }
	);		

	// This event fires when the input pointer selects a mattertag.
	//  --
	// There's a bug with the SDK where selecting will trigger moving the viewer to the closest sweep -- and then select AGAIN
	// This fires the bottom function twice... which really shouldn't happen.
	mpSdk.on(mpSdk.Mattertag.Event.CLICK,
	  function(selectionSID){
	  		c('mpSdk.on(Sdk.Mattertag.Event.CLICK)', 'Selected: ' + selectionSID, true);
			mpSdk.Mattertag.getData()
			  .then(function(mattertags) {
				$.each(mattertags, function(key,mattertag) {
					if (mattertag.sid == selectionSID) {
						c('mpSdk.Mattertag.getData() (filtered by ' + selectionSID + ')', JSON.stringify(mattertag,null,2));
					}
				});
			  })
			  .catch(function(error) {
				c('mpSdk.on(Sdk.Mattertag.Event.CLICK)', 'Failed: ' + error, true);
			  });			
		}
	);		

	// This event fires when first entering a sweep.
	mpSdk.on(mpSdk.Sweep.Event.ENTER,
		function(oldSweep,newSweep){
			c('mpSdk.on(mpSdk.Sweep.Event.ENTER)', 'Entered: ' + newSweep + ' from: ' + oldSweep, true);
		}
	);		

	// This event fires when exiting a sweep (added 1/7/22)
	mpSdk.on(mpSdk.Sweep.Event.EXIT,
		function(to,from){
			c('mpSdk.on(mpSdk.Sweep.Event.EXIT)', 'Leaving: ' + from + ' Entering: ' + to, true);
		}
	);		


	// This event fires when the tour has started.
	mpSdk.on(mpSdk.Tour.Event.STARTED,
		function() {
			c('mpSdk.on(mpSdk.Tour.Event.STARTED)', 'Tour started!',true);

			// Change intent of Play button to Pause
			$('#tourToggle').data('val','PAUSE');
			$('#tourToggle').html('<i class="icon icon-tour-pause" aria-hidden="true"></i>');

			// Hide Dollhouse, Floorplan and inside view tools
			$('.xtour').css('display', 'none'); 	
		}
	);		

	// This event fires when the tour has stopped.
	mpSdk.on(mpSdk.Tour.Event.STOPPED,
		function() {
			c('mpSdk.on(mpSdk.Tour.Event.STOPPED)', 'Tour stopped!',true);

			// Change intent of Pause button to Play
			$('#tourToggle').data('val','START');
			$('#tourToggle').html('<i class="icon icon-tour-play" aria-hidden="true"></i>');

			// Show Dollhouse and Floorplan Icons (not inside view)
			$('.b_dollhouse').css('display', 'inline-block');
			$('.b_floorplan').css('display', 'inline-block');			
		}
	);

	// This event fires when the tour has ended.
	mpSdk.on(mpSdk.Tour.Event.ENDED,
		function() {
			c('mpSdk.Tour.Event.ENDED', 'TRUE',true);

			// Change intent of Pause button to Play
			$('#tourToggle').data('val','START');
			$('#tourToggle').html('<i class="icon icon-tour-play" aria-hidden="true"></i>');
			
			// Reset starting point of Play Button
			$('#tourToggle').data('step', i);
					
			// Show Dollhouse and Floorplan Icons (not inside view)
			$('.b_dollhouse').css('display', 'inline-block');
			$('.b_floorplan').css('display', 'inline-block');			
		}
	);

	// This event fires when the tour has stepped.
	mpSdk.on(mpSdk.Tour.Event.STEPPED,
		function(activeIndex) {
			// Log the current tour step in 'data-step' attribute of button
			$('#tourToggle').data('step',activeIndex);
			c('mpSdk.on(mpSdk.Tour.Event.STEPPED)', 'Tour Step: ' + activeIndex, true);
		}
	);

	
	// This event fires when a camera performance statistic is created. To enable this event, set the url parameter &perf=1
	// This is disabled because it constantly creates feedback.
	mpSdk.on(mpSdk.Camera.Event.PERF_STAT,
	  function(state){
		c('mpSdk.on(mpSdk.Camera.Event.PERF_STAT)', JSON.stringify(state),true);
	  }
	);

	// This event fires when the input pointer hovers over a mattertag.
	// This is disabled because it constantly creates feedback when hovering a Mattertag.
	// The same status can be retrieved on click
	
	mpSdk.on(mpSdk.Mattertag.Event.HOVER,
	  function(sid, hovering) {
	  	c('mpSdk.Mattertag.Event.HOVER', sid + ': ' + JSON.stringify(hovering,null,2),true);
	  }
	);

	// This event fires when any mattertag changes its screen position.
	// This is disabled because it constantly creates feedback when a mattertag is visible while panning a pano
	mpSdk.on(mpSdk.Mattertag.Event.UPDATED,
	  function(tags){
		c('mpSdk.on(mpSdk.Mattertag.Event.UPDATED)', JSON.stringify(tags),true);
	  }
	);		
	
}







/////////////////////////////////////////////
// LOAD PAGE
window.onload = function () {
	getSiteSettings();
	projectName = window.location.pathname;
	projectName = projectName.split('/')[3];
};
// GET SITE SETTINGS
function getSiteSettings() {
	$.get('/scans/getSiteSettings', { contentType: 'application/json' }).then((response) => {
		//siteSettings = JSON.parse(response);
		//loadNavigation();
	});
}