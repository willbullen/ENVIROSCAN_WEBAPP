    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	///////////////////////////////////////////////////////////////// CREATE POWER WIDGET ////////////////////////////////////////////////////////////////////
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	/////////////////////////////////////////////////////////////////////////////////////
	// CREATE POWER CONTROLS
	function create_power_controls(id, node) {
		// CREATE POLAR CHART
		var polar = $('#power_polar_chart_' + id).dxPolarChart({
			palette: 'red',
			commonSeriesSettings: {
				point: {
					visible: false,
				},
			},
			loadingIndicator: {
				enabled: true
			},
			size: {
				height: 300,
			},
			series: [
			{
				type: 'line',
				name: 'L1',
				valueField: 'L1',
				argumentField: "Data_DateTime",
				argumentType: "datetime",
			},{
				type: 'line',
				name: 'L2',
				valueField: 'L2',
				argumentField: "Data_DateTime",
				argumentType: "datetime",
			},{
				type: 'line',
				name: 'L3',
				valueField: 'L3',
				argumentField: "Data_DateTime",
				argumentType: "datetime",
			}
		],
			argumentAxis: {
				inverted: false,
				startAngle: 0,
				tickInterval: 'hour',
				period: 'day',
			},
			tooltip: {
				enabled: true,
				shared: true,
				argumentFormat: "shortDateShortTime",
				contentTemplate: function (pointInfo, element) {
					var print = function (label, value) {
						var span = $("<span>", {
							"class": "tooltip-label",
							text: label
						});
						element.append($("<div>", {
							text: value
						}).prepend(span));
					};

					var powerData = {};
					powerData.Data = pointInfo.points[0].point.data;

					print("", powerData.Data.Data_DateTime);
					print("L1: ", powerData.Data.AppaPower_L1.toFixed(3));
					print("L2: ", powerData.Data.AppaPower_L2.toFixed(3));
					print("L3: ", powerData.Data.AppaPower_L3.toFixed(3));
					//print("Baseline: ", powerData.Data.Baseline.toFixed(3));
				},
			},
			legend: {
				verticalAlignment: 'top',
				horizontalAlignment: 'right',
				hoverMode: 'excludePoints',
			}
		});
		// CREATE BAR CHART
		var chart = $('#power_line_chart_' + id).dxChart({
			palette: 'red',
			commonSeriesSettings: {
				point: {
					visible: false,
				},
			},
			size: {
				height: 360,
			},
			loadingIndicator: {
				enabled: true
			},
			argumentAxis: {
				argumentType: "datetime",
				label: {
					format: "shortDateShortTime"
				},
				valueMarginsEnabled: false,
				discreteAxisDivisionMode: 'crossLabels',
				grid: {
					visible: true,
				},
			},
			series: [
				{
					type: 'spline',
					name: 'L1',
					valueField: 'L1',
					argumentField: "Data_DateTime",
					argumentType: "datetime",
				},{
					type: 'spline',
					name: 'L2',
					valueField: 'L2',
					argumentField: "Data_DateTime",
					argumentType: "datetime",
				},{
					type: 'spline',
					name: 'L3',
					valueField: 'L3',
					argumentField: "Data_DateTime",
					argumentType: "datetime",
				}
			],
			tooltip: {
				enabled: true,
			},
			legend: {
				visible: false,
			},
			crosshair: {
				enabled: true,
				color: '#949494',
				width: 1,
				dashStyle: 'dot',
				label: {
					visible: true,
					backgroundColor: '#949494',
					font: {
					color: '#fff',
					size: 12,
					},
				},
			},
			export: {
				enabled: false,
			},
			onPointClick: function (e) {
				var point = e.target;
				if (point.isSelected()) {
					point.clearSelection();
				} else {
					point.select();					
				}
			}
		});	
		// REFRESH CHART
		$('#refresh_' + id).click({}, function() {
			$("#power_line_chart_" + id).dxChart('instance').refresh();
			$("#power_polar_chart_" + id).dxPolarChart('instance').refresh();
		});
		// REFRESH CHART ON SLIDER CLICK
		$('#slider_' + id).click({}, function() {
			$("#power_line_chart_" + id).dxChart('instance').refresh();
			$("#power_polar_chart_" + id).dxPolarChart('instance').refresh();
		});
		// SET CHART SELECTION
		$('#select_chart_type_' + id).change({}, function() {
			//console.log(this.value);
			if (this.value === 'Bar') {
				$("#power_line_chart_" + id).show();
				$("#power_polar_chart_" + id).hide();
			} else if (this.value === 'Polar') {
				$("#power_line_chart_" + id).hide();
				$("#power_polar_chart_" + id).show();
			}
			$("#power_line_chart_" + id).dxChart('instance').refresh();
			$("#power_polar_chart_" + id).dxPolarChart('instance').refresh();
		});
		// SETUP DATEPICKER
		$('#daterange_' + id + ' span').html(moment().subtract(24, 'hours').format('DD-MM-YYYY HH:00') + ' - ' + moment().format('DD-MM-YYYY HH:00'));
		$('#daterange_' + id).daterangepicker({
			format: 'MM/DD/YYYY',
			startDate: moment().subtract(24, 'hours'),
			endDate: moment(),
			minDate: moment().subtract(6, 'months'),
			maxDate: moment(),
			dateLimit: { days: 60 },
			showDropdowns: true,
			showWeekNumbers: true,
			timePicker: true,
			timePickerIncrement: 1,
			timePicker12Hour: true,
			ranges: {
				'Today': [moment().startOf('day'), moment()],
				'Last 24 Hours': [moment().subtract(24, 'hours'), moment()],
				'Yesterday': [moment().subtract(1, 'days').startOf('day'), moment().subtract(1, 'days').endOf('day')],
				'Last 7 Days': [moment().subtract(6, 'days').startOf('day'), moment()],
				'This Month So Far': [moment().startOf('month'), moment().endOf('month')],
				'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
				'This Year So Far': [moment().startOf('year'), moment().endOf('year')],
				'Last Year': [moment().subtract(1, 'year').startOf('year'), moment().subtract(1, 'year').endOf('year')]
			},
			opens: 'right',
			drops: 'down',
			buttonClasses: ['btn', 'btn-sm'],
			applyClass: 'btn-primary',
			cancelClass: 'btn-default',
			separator: ' to ',
			locale: {
				applyLabel: 'Submit',
				cancelLabel: 'Cancel',
				fromLabel: 'From',
				toLabel: 'To',
				customRangeLabel: 'Custom',
				daysOfWeek: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr','Sa'],
				monthNames: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
				firstDay: 1
			}
		}, function(start, end, label) {
			$('#daterange_' + id + ' span').html(start.format('DD-MM-YYYY HH:00') + ' - ' + end.format('DD-MM-YYYY HH:00'));
			change_power_data(id, node, new Date(start.format()), new Date(end.format()), '10Min');
		});
		// LOG		
		var dataGrid = $('#power_log_' + id).dxDataGrid({
			//dataSource: data,
			keyExpr: 'ID',
			showColumnLines: false,
			showRowLines: true,
			rowAlternationEnabled: false,
			showBorders: true,
			paging: {
				pageSize: 8,
			},
			pager: {
				visible: true,
				allowedPageSizes: [5, 10, 'all'],
				showPageSizeSelector: true,
				showInfo: true,
				showNavigationButtons: true,
			},
			columns: [
				{
					title: "DATE TIME",
					dataField: 'Data_DateTime',
				}, {
					title: "L1",
					dataField: 'AppaPower_L1',
					width: 100,
				}, {
					title: "L2",
					dataField: 'AppaPower_L2',
					width: 100,
				}, {
					title: "L3",
					dataField: 'AppaPower_L3',
					width: 100,
				},
			],
		});
		// SHOW AND HIDE
		$("#power_line_chart_" + id).show();
		$("#power_polar_chart_" + id).hide();
	}
	/////////////////////////////////////////////////////////////////////////////////////
	// CHANGE POWER DATA
	function change_power_data(id, data, start, end, resolution) {
		// AJAX
		$.ajax({
			type: 'GET',
			url: '../node_power/get_by_id_and_dates/?node_id=' + id + '&start_datetime=' + start.toISOString() + '&end_datetime=' + end.toISOString() + '&resolution=' + resolution,
			headers: {
				"Authorization": "Basic " + btoa("admin" + ":" + "will1977"),
				'Accept' : 'application/json'
			},
			success: function(data) {	
				var data_history = data;
				var data_current = data[data.length-1];
				if (data != '') {
					// SET CHART DATA
					$("#power_line_chart_" + id).dxChart("option", "dataSource", data_history.map(function(element) {return {'Data_DateTime': element.Data_DateTime, 'L1': Math.abs(element.Irms_L1*element.Vrms_L1/1000), 'L2': Math.abs(element.Irms_L2*element.Vrms_L1/1000), 'L3': Math.abs(element.Irms_L3*element.Vrms_L1/1000)};}));
					$("#power_line_chart_" + id).dxChart('instance').refresh();
					$("#power_polar_chart_" + id).dxPolarChart("option", "dataSource", data_history.map(function(element) {return {'Data_DateTime': element.Data_DateTime, 'L1': Math.abs(element.AppaPower_L1), 'L2': Math.abs(element.AppaPower_L2), 'L3': Math.abs(element.AppaPower_L3)};}));
					$("#power_polar_chart_" + id).dxPolarChart('instance').refresh();
					// SET LOG VALUES
					$("#power_log_" + id).dxDataGrid("option", "dataSource", data_history.map(function(element) {return {'ID': element.id, 'Data_DateTime': element.Data_DateTime, 'L1': Math.abs(element.AppaPower_L1), 'L2': Math.abs(element.AppaPower_L2), 'L3': Math.abs(element.AppaPower_L3)};}));
					$("#power_log_" + id).dxDataGrid('instance').refresh();
					// GET kW/h
					var rate_day = 0.36;
					var rate_night = 0.25;
					var delta_T = 600/3600;							// Polling interval is 10 min
					var day_start = moment('07:00:00', 'HH:mm:ss');
					var day_end = moment('23:00:00', 'HH:mm:ss');
					
					var P1_sum = 0;									
					var prev_P1 = 0;								
					var Wh1_day = 0;
					var Wh1_night = 0;

					var P2_sum = 0;									
					var prev_P2 = 0;								
					var Wh2_day = 0;
					var Wh2_night = 0;

					var P3_sum = 0;									
					var prev_P3 = 0;								
					var Wh3_day = 0;
					var Wh3_night = 0;

					//console.log(data);

					//var readings = data.history.filter((item) => item.Data_DateTime.getTime() >= start && item.Data_DateTime.getTime() <= end);
					var readings = data_history;
					
					$.each(data_history, function(i, reading) {

						// correction
						if (data_current.id == 4) {
							reading.Irms_L1 = reading.Irms_L1/1000
							reading.Irms_L2 = reading.Irms_L2/1000
							reading.Irms_L3 = reading.Irms_L3/1000
						};

						var time = moment(new Date(reading.Data_DateTime).toLocaleTimeString([], {hourCycle: 'h23', hour: '2-digit', minute: '2-digit', second: '2-digit'}),'HH:mm:ss');

						var P_CT1 = Math.abs(reading.Irms_L1) * Math.abs(reading.Vrms_L1);
						var P_CT2 = Math.abs(reading.Irms_L2) * Math.abs(reading.Vrms_L1);
						var P_CT3 = Math.abs(reading.Irms_L3) * Math.abs(reading.Vrms_L1);

						P1_sum = prev_P1 + P_CT1;								
						prev_P1 = P_CT1;		
									
						P2_sum = prev_P2 + P_CT2;								
						prev_P2 = P_CT2;
									
						P3_sum = prev_P3 + P_CT3;								
						prev_P3 = P_CT3;

						if (time.isBetween(day_start, day_end)) {
							Wh1_day += delta_T / 2 * P1_sum;
							Wh2_day += delta_T / 2 * P2_sum;
							Wh3_day += delta_T / 2 * P3_sum;
						} else {
							Wh1_night += delta_T / 2 * P1_sum;
							Wh2_night += delta_T / 2 * P2_sum;
							Wh3_night += delta_T / 2 * P3_sum;
						}
					});

					// correction
					if (data_current.id == 4) {
						data_current.Irms_L1 = data_current.Irms_L1/1000
						data_current.Irms_L2 = data_current.Irms_L2/1000
						data_current.Irms_L3 = data_current.Irms_L3/1000
					};

					// total
					var kwh_total_day = ((Wh1_day + Wh2_day + Wh3_day) / 1000)
					var kwh_total_night = ((Wh1_night + Wh2_night + Wh3_night) / 1000)
					var kwh_total = kwh_total_day + kwh_total_night;

					// cost
					var total_cost = (kwh_total_day*rate_day) + (kwh_total_night*rate_night)
					$("#cost_value_" + id).text(total_cost.toFixed(2));
					$("#cost_bar_" + id).attr('style', 'width: ' + (total_cost/250*100).toFixed(0) + '%');
					$("#cost_day_" + id).text('Day Cost: €' + (kwh_total_day*rate_day).toFixed(2));
					$("#cost_night_" + id).text('Night Cost: €' + (kwh_total_night*rate_night).toFixed(2));

					// kW/h
					$("#total_kwh_value_" + id).text(kwh_total.toFixed(2));
					$("#total_kwh_bar_" + id).attr('style', 'width: ' + (kwh_total/600*100).toFixed(0) + '%');
					$("#total_kwh_info_" + id).text('@ ' + (kwh_total/600*100).toFixed(0) + '% of 600 kW.');
					$("#total_kwh_day_" + id).text('Day: ' + (kwh_total_day).toFixed(2) + 'kVA');
					$("#total_kwh_night_" + id).text('Night: ' + (kwh_total_night).toFixed(2) + 'kVA');

					// voltage
					var vrms_total = (Math.abs(Number(data_current.Vrms_L1)) + Math.abs(Number(data_current.Vrms_L2)) + Math.abs(Number(data_current.Vrms_L3)))/3
					$("#vrms_total_" + id).text(Number(vrms_total).toFixed(2));
					$("#vrms_l1_" + id).text(Number(data_current.Vrms_L1).toFixed(2));
					$("#vrms_l2_" + id).text(Number(data_current.Vrms_L2).toFixed(2));
					$("#vrms_l3_" + id).text(Number(data_current.Vrms_L3).toFixed(2));

					// current
					var irms_total = (Math.abs(Number(data_current.Irms_L1).toFixed(2)) + Math.abs(Number(data_current.Irms_L2).toFixed(2)) + Math.abs(Number(data_current.Irms_L3).toFixed(2)))
					$("#irms_total_" + id).text(Number(irms_total).toFixed(2));
					$("#irms_l1_" + id).text(Number(data_current.Irms_L1).toFixed(2));
					$("#irms_l2_" + id).text(Number(data_current.Irms_L2).toFixed(2));
					$("#irms_l3_" + id).text(Number(data_current.Irms_L3).toFixed(2));

					// power
					var power_total = (Math.abs(Number(data_current.Irms_L1)*Number(data_current.Vrms_L1)) + Math.abs(Number(data_current.Irms_L2)*Number(data_current.Vrms_L2)) + Math.abs(Number(data_current.Irms_L3)*Number(data_current.Vrms_L3))) / 1000
					$("#power_total_" + id).text(Number(power_total).toFixed(2));
					$("#power_l1_" + id).text((Number(data_current.Irms_L1)*Number(data_current.Vrms_L1)/1000).toFixed(2));
					$("#power_l2_" + id).text((Number(data_current.Irms_L2)*Number(data_current.Vrms_L1)/1000).toFixed(2));
					$("#power_l3_" + id).text((Number(data_current.Irms_L3)*Number(data_current.Vrms_L1)/1000).toFixed(2));
					
					$("#value_main_" + id).text(Number(power_total).toFixed(3) + ' kVA');
					$("#real_power_value_" + id).text(Number(power_total).toFixed(2));

					// SET STATUS
					if (parseInt(Math.abs(new Date()-new Date(data_current.Last_Updated)) / (1000 * 60)) > 2) {
						$('#Node_Status_' + id).addClass('bg-danger');
						$('#Node_Status_' + id).attr('title', 'Last time data updated was too long.');
						$("#hidden_Node_Status_" + id).val('1');
					} else {
						$('#Node_Status_' + id).removeClass('bg-danger');
						$("#hidden_Node_Status_" + id).val('0');
					}
				}	
			}
		});
	}
	//////////////////////////////////////////////////////////////////////
	// POWER WEBSOCKET
	var Power_WebSocket = function () {
		var autosondeSocket;
		//var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
		//var ws_path = ws_scheme + '://' + window.location.host + ':8001/power/';
		var ws_path = 'wss://www.enviroscan.io:8001/power/';
		console.log(ws_path);
		autosondeSocket = new WebSocket(ws_path);

		autosondeSocket.onmessage = function (e) {
			json_data = JSON.parse(e.data).message;
			console.log(json_data);
		};

		autosondeSocket.onclose = function (e) {
			console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
		};

		autosondeSocket.onerror = function (err) {
			console.error(err);
		};
	};
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	///////////////////////////////////////////////////////////////// CREATE POWER WIDGET ////////////////////////////////////////////////////////////////////
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
