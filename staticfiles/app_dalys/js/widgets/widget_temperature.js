    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	///////////////////////////////////////////////////////////////// CREATE TEMPERATURE WIDGET ////////////////////////////////////////////////////////////////////
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////
	// CREATE TEMPERATURE CONTROLS
	function create_temperature_controls(id, node) {
		// CREATE POLAR CHART
		var polar = $('#temperature_polar_chart_' + id).dxPolarChart({
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
				name: 'Temperature',
				valueField: 'Temperature',
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

					var temperatureData = {};
					temperatureData.Data = pointInfo.points[0].point.data;

					print("", temperatureData.Data.Data_DateTime);
					print("Temperature: ", temperatureData.Data.Temperature.toFixed(3));
				},
			},
			legend: {
				verticalAlignment: 'top',
				horizontalAlignment: 'right',
				hoverMode: 'excludePoints',
			}
		});
		// CREATE BAR CHART
		var chart = $('#temperature_line_chart_' + id).dxChart({
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
					name: 'Temperature',
					valueField: 'Temperature',
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
			$("#temperature_line_chart_" + id).dxChart('instance').refresh();
			$("#temperature_polar_chart_" + id).dxPolarChart('instance').refresh();
		});
		// REFRESH CHART ON SLIDER CLICK
		$('#slider_' + id).click({}, function() {
			$("#temperature_line_chart_" + id).dxChart('instance').refresh();
			$("#temperature_polar_chart_" + id).dxPolarChart('instance').refresh();
		});
		// SET CHART SELECTION
		$('#select_chart_type_' + id).change({}, function() {
			//console.log(this.value);
			if (this.value === 'Bar') {
				$("#temperature_line_chart_" + id).show();
				$("#temperature_polar_chart_" + id).hide();
			} else if (this.value === 'Polar') {
				$("#temperature_line_chart_" + id).hide();
				$("#temperature_polar_chart_" + id).show();
			}
			$("#temperature_line_chart_" + id).dxChart('instance').refresh();
			$("#temperature_polar_chart_" + id).dxPolarChart('instance').refresh();
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
			change_temperature_data(id, node, new Date(start.format()), new Date(end.format()), '10Min');
		});
		// LOG		
		var dataGrid = $('#temperature_log_' + id).dxDataGrid({
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
					title: "Temperature",
					dataField: 'Temperature',
					width: 100,
				}, {
					title: "Batt mV",
					dataField: 'Battery_MV',
					width: 100,
				}, {
					title: "Batt Percent",
					dataField: 'Battery_Percent',
					width: 100,
				},
			],
		});
		// SHOW AND HIDE
		$("#temperature_line_chart_" + id).show();
		$("#temperature_polar_chart_" + id).hide();
	}
	//////////////////////////////////////////////////////////////////////////////
	// CHANGE TEMPERATURE DATA
	function change_temperature_data(id, data, start, end, resolution) {
		// AJAX
		$.ajax({
			type: 'GET',
			url: '../node_temperature/get_by_id_and_dates/?node_id=' + id + '&start_datetime=' + start.toISOString() + '&end_datetime=' + end.toISOString() + '&resolution=' + resolution,
			headers: {
				"Authorization": "Basic " + btoa("admin" + ":" + "will1977"),
				'Accept' : 'application/json'
			},
			success: function(data) {
				var data_history = data;
				var data_current = data[data.length-1];
				if (data != '') {
					
					// SET CHART DATA
					$("#temperature_line_chart_" + id).dxChart("option", "dataSource", data_history.map(function(element) {return {'Data_DateTime': element.Data_DateTime, 'Temperature': element.Temperature};}));
					$("#temperature_line_chart_" + id).dxChart('instance').refresh();
					$("#temperature_polar_chart_" + id).dxPolarChart("option", "dataSource", data_history.map(function(element) {return {'Data_DateTime': element.Data_DateTime, 'Temperature': element.Temperature};}));
					$("#temperature_polar_chart_" + id).dxPolarChart('instance').refresh();

					// SET LOG VALUES
					$("#temperature_log_" + id).dxDataGrid("option", "dataSource", data_history.map(function(element) {return {'ID': element.id, 'Data_DateTime': element.Data_DateTime, 'Temperature': element.Temperature, 'Battery_MV': element.Battery_MV, 'Battery_Percent': element.Battery_Percent};}));
					$("#temperature_log_" + id).dxDataGrid('instance').refresh();

					// TEMPERATURE
					$("#temperature_value_" + id).text(data_current.Temperature.toFixed(2));
					$("#temperature_bar_" + id).attr('style', 'width: ' + ((data_current.Temperature/250)*100).toFixed(0) + '%');
					$("#temperature_max_" + id).text('MAX: ' + data_current.Temperature.toFixed(2));
					$("#temperature_min_" + id).text('MIN: ' + data_current.Temperature.toFixed(2));

					// BATTERY VOLTAGE
					$("#battery_voltage_value_" + id).text(data_current.Battery_MV.toFixed(2));
					$("#battery_voltage_bar_" + id).attr('style', 'width: ' + ((data_current.Battery_MV/250)*100).toFixed(0) + '%');
					$("#battery_voltage_max_" + id).text('MAX: ' + data_current.Battery_MV.toFixed(2));
					$("#battery_voltage_min_" + id).text('MIN: ' + data_current.Battery_MV.toFixed(2));

					// BATTERY PERCENT
					$("#battery_percent_value_" + id).text(data_current.Battery_Percent.toFixed(2));
					$("#battery_percent_bar_" + id).attr('style', 'width: ' + ((data_current.Battery_Percent/250)*100).toFixed(0) + '%');
					$("#battery_percent_max_" + id).text('MAX: ' + data_current.Battery_Percent.toFixed(2));
					$("#battery_percent_min_" + id).text('MIN: ' + data_current.Battery_Percent.toFixed(2));
					
					// SET TEXT VALUES
					$("#value_main_" + id).text(Number(data_current.Temperature).toFixed(2) + ' °C');
					$("#node_status_value_" + id).text('OK');
					$("#signal_status_value_" + id).text('99.8 dB');
					$("#battery_status_value_" + id).text(Number(data_current.Battery_Percent).toFixed(2) + ' %');
					$('#battery_status_' + data_current.Meter_Id).removeClass('text-success');
					$('#battery_status_' + data_current.Meter_Id).removeClass('text-warning');
					$('#battery_status_' + data_current.Meter_Id).removeClass('text-danger');
					if (Number(data_current.Battery_Percent) > 80) {
						$('#battery_status_' + id).addClass('text-success');
						$('#battery_status_' + id).attr('title', 'Battery good.');
					} else if (Number(data_current.Battery_Percent) < 80 && Number(data_current.Battery_Percent) > 40) {
						$('#battery_status_' + id).addClass('text-warning');
						$('#battery_status_' + id).attr('title', 'Under charged.');
					} else {
						$('#battery_status_' + id).addClass('text-danger');
						$('#battery_status_' + id).attr('title', 'Battery needs to be replaced.');
					}

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
    /////////////////////////////////////////////////////////////////////////////////////////
    // TEMPERATURE WEBSOCKET
	var Temperature_WebSocket = function () {
		var autosondeSocket;
		//var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
		//var ws_path = ws_scheme + '://' + window.location.host + ':8001/temperature/';
		var ws_path = 'wss://www.enviroscan.io:8001/temperature/';
		console.log(ws_path);
		autosondeSocket = new WebSocket(ws_path);

		autosondeSocket.onmessage = function (e) {
			json_data = JSON.parse(e.data).message;
			console.log(json_data);
			$("#value_main_" + json_data.Meter_Id).text(Number(json_data.Temperature).toFixed(2) + ' °C');
			$("#node_status_value_" + json_data.Meter_Id).text('OK');
			$("#signal_status_value_" + json_data.Meter_Id).text('99.8 dB');
			$("#battery_status_value_" + json_data.Meter_Id).text(Number(json_data.Battery_Percent).toFixed(2) + ' %');
			$('#battery_status_' + json_data.Meter_Id).removeClass('text-success');
			$('#battery_status_' + json_data.Meter_Id).removeClass('text-warning');
			$('#battery_status_' + json_data.Meter_Id).removeClass('text-danger');
			if (Number(json_data.Battery_Percent) > 80) {				
				$('#battery_status_' + json_data.Meter_Id).addClass('text-success');
				$('#battery_status_' + json_data.Meter_Id).attr('title', 'Battery good.');
			} else if (Number(json_data.Battery_Percent) < 80 && Number(json_data.Battery_Percent) > 40) {
				$('#battery_status_' + json_data.Meter_Id).addClass('text-warning');
				$('#battery_status_' + json_data.Meter_Id).attr('title', 'Under charged.');
			} else {
				$('#battery_status_' + json_data.Meter_Id).addClass('text-danger');
				$('#battery_status_' + json_data.Meter_Id).attr('title', 'Battery needs to be replaced.');
			}
		};

		autosondeSocket.onclose = function (e) {
			console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
		};

		autosondeSocket.onerror = function (err) {
			console.error(err);
		};
	};
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	///////////////////////////////////////////////////////////////// CREATE TEMPERATURE WIDGET ////////////////////////////////////////////////////////////////////
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
