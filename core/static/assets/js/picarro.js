
// SET UNIVERSAL VARIABLES
var allStatusDataset = [];
var thisStatusDataset = [];
var thisNodeID = 0;

function setHistory(db_Data) {
    // MET DATA
    $("#metRadarChart").dxPolarChart("option", "dataSource", db_Data.Data.data);
    $("#weatherChart").dxChart("option", "dataSource", db_Data.Data.data);
    // CORE DATA
    $("#picarroChart").dxChart("option", "dataSource", db_Data.Data.data);
    // SUPPLY VOLTAGE
    $("#SSC_Voltage").dxChart("option", "dataSource", db_Data.Data.data);
    var maxMinAvg_Voltage = maxMinAvg(db_Data.Data.data, "Instrument_Supply_Voltage");
    $("#Voltage_Max").text(maxMinAvg_Voltage[0].toFixed(2));
    $("#Voltage_Min").text(maxMinAvg_Voltage[1].toFixed(2));
    $("#Voltage_Ave").text(maxMinAvg_Voltage[2].toFixed(2));
    // CAVITY TEMPERATURE
    $("#SSC_CavityTemp").dxChart("option", "dataSource", db_Data.Data.data);
    var maxMinAvg_CavityTemp = maxMinAvg(db_Data.Data.data, "Data_Cavity_Temp");
    $("#CavityTemp_Max").text(maxMinAvg_CavityTemp[0].toFixed(2));
    $("#CavityTemp_Min").text(maxMinAvg_CavityTemp[1].toFixed(2));
    $("#CavityTemp_Ave").text(maxMinAvg_CavityTemp[2].toFixed(2));
    // WARM BOX TEMPERATURE
    $("#SSC_WarmBoxTemp").dxChart("option", "dataSource", db_Data.Data.data);
    var maxMinAvg_WarmBoxTemp = maxMinAvg(db_Data.Data.data, "Data_WarmBoxTemp");
    $("#WarmBoxTemp_Max").text(maxMinAvg_WarmBoxTemp[0].toFixed(2));
    $("#WarmBoxTemp_Min").text(maxMinAvg_WarmBoxTemp[1].toFixed(2));
    $("#WarmBoxTemp_Ave").text(maxMinAvg_WarmBoxTemp[2].toFixed(2));
    // CAVITY PRESSURE
    $("#SSC_CavityPres").dxChart("option", "dataSource", db_Data.Data.data);
    var maxMinAvg_CavityPres = maxMinAvg(db_Data.Data.data, "Data_CavityPressure");
    $("#CavityPres_Max").text(maxMinAvg_CavityPres[0].toFixed(2));
    $("#CavityPres_Min").text(maxMinAvg_CavityPres[1].toFixed(2));
    $("#CavityPres_Ave").text(maxMinAvg_CavityPres[2].toFixed(2));
}
function setCurrent(db_Data) {
    var thisDateTime = new Date(db_Data.Data.Data_DateTime);
    var thisTime = new Date(db_Data.Data.Data_DateTime).toLocaleTimeString();
    var thisDate = new Date(db_Data.Data.Data_DateTime).toLocaleDateString();
    thisDateTime = thisDateTime.toLocaleString();

    var endDate = new Date();
    var startDate = new Date(db_Data.HeartBeat);
    var timeDiff = (endDate.getTime() - startDate.getTime()) / 1000;
    if (timeDiff > 70) {

    }
    
    // SET DATE TIME EVERYWHERE
    for (var i = 0, len = 20; i < len; ++i) {
        $("#Time_" + i).text(thisTime);
    }
    $("#Time").text(thisTime);
    $("#Date").text(thisDate);
    // CORE DATA
    $("#CO2_Value").text(db_Data.Data.Data_CO2.toFixed(1));
    $("#CO2_Bar").attr('style', 'width: ' + getPercentage(db_Data.Data.Data_CO2, 420) + '%');
    $("#CO_Value").text(db_Data.Data.Data_CO.toFixed(1));
    $("#CO_Bar").attr('style', 'width: ' + getPercentage(db_Data.Data.Data_CO, 2) + '%');
    $("#H2O_Value").text(db_Data.Data.Data_H2O.toFixed(1));
    $("#H2O_Bar").attr('style', 'width: ' + getPercentage(db_Data.Data.Data_H2O, 4) + '%');
    $("#CH4_Value").text(db_Data.Data.Data_CH4.toFixed(1));
    $("#CH4_Bar").attr('style', 'width: ' + getPercentage(db_Data.Data.Data_CH4, 3) + '%');
    // SUPPLY VOLTAGE
    $("#Voltage_Value").text(db_Data.Data.Instrument_Supply_Voltage.toFixed(1));
    $("#Voltage_Bar").attr('style', 'width: ' + getPercentage(db_Data.Data.Instrument_Supply_Voltage, 26) + '%');
    // CAVITY TEMPERATURE
    $("#CavityTemp_Value").text(db_Data.Data.Data_Cavity_Temp.toFixed(1));
    $("#CavityTemp_Bar").attr('style', 'width: ' + getPercentage(db_Data.Data.Data_Cavity_Temp, 45) + '%');
    // WARM BOX TEMPERATURE
    $("#CavityPres_Value").text(db_Data.Data.Data_CavityPressure.toFixed(1));
    $("#CavityPres_Bar").attr('style', 'width: ' + getPercentage(db_Data.Data.Data_CavityPressure, 1) + '%');
    // CAVITY PRESSURE
    $("#WarmBoxTemp_Value").text(db_Data.Data.Data_WarmBoxTemp.toFixed(1));
    $("#WarmBoxTemp_Bar").attr('style', 'width: ' + getPercentage(db_Data.Data.Data_WarmBoxTemp, 45) + '%');
    // MISC DATA
    $("#CO2_Dry_Value").text(db_Data.Data.Data_CO2_Dry.toFixed(1));
    $("#CH4_Dry_Value").text(db_Data.Data.Data_CH4_Dry.toFixed(1));
    $("#Amb_P_Value").text(db_Data.Data.Data_Amb_P.toFixed(1));
    $("#DasTemp_Value").text(db_Data.Data.Data_DasTemp.toFixed(1));
    $("#EtalonTemp_Value").text(db_Data.Data.Data_EtalonTemp.toFixed(1));
    $("#Solenoid_Valves_Value").text(db_Data.Data.Data_Solenoid_Valves.toFixed(1));
    $("#MPVPosition_Value").text(db_Data.Data.Data_MPVPosition.toFixed(1));
    $("#OutletValve_Value").text(db_Data.Data.Data_OutletValve.toFixed(1));
    $("#Species_Value").text(db_Data.Data.Data_Species.toFixed(1));
    $("#H2O_Reported_Value").text(db_Data.Data.Data_h2o_reported.toFixed(1));
    // MET DATA
    $("#Wind_Value").text(db_Data.Data.Data_WindSpeed.toFixed(1));
    $("#Gust_Value").text(db_Data.Data.Data_MaxGust.toFixed(1));
    $("#Dir_Value").text(db_Data.Data.Data_WindDir.toFixed(1));
    $("#Temp_Value").text(db_Data.Data.Data_GrassA.toFixed(1));
    $("#Hum_Value").text(db_Data.Data.Data_HumA.toFixed(1));
    $("#Pres_Value").text(db_Data.Data.Data_Pressure.toFixed(1));
}
function setStatus(db_Data) {
    var StatusData = db_Data.Data.data.map(function(h){ return {id: h.id, asset: h.Node_Name, location: h.Location, status: h.Status.toString(), asset_status: h.Asset_Status, asset_status_description: h.Asset_Status_Description, node_status: h.Node_Status, node_status_description: h.Node_Status_Description, server_status: h.Server_Status, server_status_description: h.Server_Status_Description, coords: [h.Node_Lat, h.Node_Lng]};});
    // SET MAP VALUES
    //var mapObject = $('#networkStatusMap').vectorMap('get', 'mapObject'); 
    //mapObject.addMarkers(StatusData.map(function(h){ return {name: h.asset, latLng: h.coords, id: h.id};}), []);
    //mapObject.series.markers[0].setValues(StatusData.reduce(function(p, c, i){ p[i] = c.status; return p;},{}));
    // SET MAP VALUES
    var tableObject = $('#networkStatusTable').DataTable();
    tableObject.clear();
    tableObject.rows.add(StatusData.map(function(h){ return [h.asset, h.status, h.location, h.asset_status, h.data_status, h.node_status, h.server_status, h.id];}));
    tableObject.draw();
    // SET THIS NODE
    thisNodeID = db_Data.Node_ID;
    // SET ALL STATUS DATASET
    allStatusDataset = db_Data.Data.data;
    // SET THIS STATUS DATASET
    thisStatusDataset = allStatusDataset[allStatusDataset.findIndex(obj => obj.id==thisNodeID)];
}
function setSetup(db_Data) {
    // SET THIS NODE
    thisNodeID = db_Data.Node_ID;
    // SET THIS STATUS DATASET
    thisStatusDataset = db_Data.Data.data[0];
    // SET STATUS HEADING
    $("#headingNetworkStatus").text(thisStatusDataset.Node_Name);
    //-- SET ASSET STATUS
    if (thisStatusDataset.Asset_Status == 1) {
        $("#assetNetworkStatus").addClass('text-danger').text('ERROR');
        $('#Asset_Status').addClass('bg-danger');
        $("#Asset_Status").attr('title', thisStatusDataset.Asset_Status_Description);
        $("#Asset_Status").attr('data-original-title', thisStatusDataset.Asset_Status_Description);
        $("#Asset_Status").tooltip('update');
        $("#Asset_Status").tooltip('show');
    } else {
        $("#assetNetworkStatus").removeClass('text-danger').text('OK');
        $('#Asset_Status').removeClass('bg-danger');
        $("#Asset_Status").tooltip({ title : "OK" });
    }
    //-- SET NODE STATUS
    if (thisStatusDataset.Node_Status == 1) {
        $("#nodeNetworkStatus").addClass('text-danger').text('ERROR');
        $('#Node_Status').addClass('bg-danger');
        $("#Node_Status").tooltip({ title : "ERROR" });
    } else {
        $("#nodeNetworkStatus").removeClass('text-danger').text('OK');
        $('#Node_Status').removeClass('bg-danger');
        $("#Node_Status").tooltip({ title : "OK" });
    }
    //-- SET SERVER STATUS
    if (thisStatusDataset.Server_Status == 1) {
        $("#serverNetworkStatus").addClass('text-danger').text('ERROR');
    } else {
        $("#serverNetworkStatus").removeClass('text-danger').text('OK');
    }
}

var startWebSocket = function () {
    var picarroSocket;
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + ':8001/picarro/';
    picarroSocket = new WebSocket(ws_path);    

    picarroSocket.onmessage = function (e) {
        ws_Data = JSON.parse(e.data).message;
        console.log(ws_Data);
        // SET STATUS VALUES
        if (ws_Data.Data_Type == 'Status_Data') {
            setStatus(ws_Data);
        }
        // SET SETUP VALUES
        if (ws_Data.Data_Type == 'Setup_Data') {
            setSetup(ws_Data);
        }
        // SET CHART VALUES
        if (ws_Data.Data_Type == 'History_Data') {
            setHistory(ws_Data);
        }
        // SET STATIC VALUES
        if (ws_Data.Data_Type == 'Current_Data') {
            setCurrent(ws_Data);
        }
    };

    picarroSocket.onclose = function (e) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
    };

    picarroSocket.onerror = function (err) {
        console.error(err);
    };
};

function getPercentage(act, max) {
    return (act / max) * 100;
}

function maxMinAvg(arr, column) {
    var max = arr[0][column];
    var min = arr[0][column];
    var sum = arr[0][column];
    for (var i = 1; i < arr.length; i++) {
        if (arr[i][column] > max) {
            max = arr[i][column];
        }
        if (arr[i][column] < min) {
            min = arr[i][column];
        }
        sum = sum + arr[i][column];
    }
    var avg = sum / arr.length;
    return [max, min, avg];
}

// ARRAY SMALL SINGLE CHART
var charts_SSC = [];
var json_SSC = [{
        id: "Voltage",
        pane_name: "voltagePane",
        series_pane: "voltagePane",
        series_type: "line",
        series_valueField: "Instrument_Supply_Voltage",
        series_name: "Voltage (V)",
        series_color: app.color.theme,
        valueAxis_pane: "voltagePane",
        size_height: 120,
    },
    {
        id: "CavityTemp",
        pane_name: "cavitytempPane",
        series_pane: "cavitytempPane",
        series_type: "line",
        series_valueField: "Data_Cavity_Temp",
        series_name: "Cavity Temp (C)",
        series_color: app.color.theme,
        valueAxis_pane: "cavitytempPane",
        size_height: 120,
    },
    {
        id: "WarmBoxTemp",
        pane_name: "warmboxtempPane",
        series_pane: "warmboxtempPane",
        series_type: "line",
        series_valueField: "Data_WarmBoxTemp",
        series_name: "Warm Box Temp (C)",
        series_color: app.color.theme,
        valueAxis_pane: "warmboxtempPane",
        size_height: 120,
    },
    {
        id: "CavityPres",
        pane_name: "cavitypressurePane",
        series_pane: "cavitypressurePane",
        series_type: "line",
        series_valueField: "Data_Cavity_Temp",
        series_name: "Cavity Pressure (Pa)",
        series_color: app.color.theme,
        valueAxis_pane: "cavitypressurePane",
        size_height: 120,
    }
];

// BUILD SMALL SINGLE CHART
function createSSC(params) {
    var element_SSC = document.getElementById('SSC_' + params.id);
    charts_SSC[params.id] = new DevExpress.viz.dxChart(element_SSC, {
        commonSeriesSettings: {
            argumentField: "Data_DateTime",
            argumentType: "datetime",
            label: {
                format: "shortTime"
            },
            point: {
                visible: false,
            }
        },
        loadingIndicator: {
            enabled: true,
        },
        size: {
            height: params.size_height,
        },
        panes: [{
            name: params.pane_name,
        }],
        series: [{
            pane: params.series_pane,
            type: params.series_type,
            valueField: params.series_valueField,
            name: params.series_name,
            color: params.series_color,
        }],
        valueAxis: [{
            pane: params.valueAxis_pane,
            grid: {
                visible: true
            },
            constantLines: [{
                value: 220,
                color: "#fc3535",
                dashStyle: "dash",
                width: 1,
                label: {
                    visible: false
                }
            }],
        }],
        argumentAxis: {
            argumentType: "datetime",
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

                var picarroData = {};
                picarroData.Data = pointInfo.points[0].point.data;
                //setTextValues(picarroData);
                print("", pointInfo.argumentText);
                print("Voltave: ", picarroData.Data.Data_CO2.toFixed(3));
            }
        },
        crosshair: {
            enabled: true,
            horizontalLine: {
                visible: false
            }
        },
        "export": {
            enabled: false
        },
        legend: {
            visible: false,
            horizontalAlignment: "center",
            verticalAlignment: "top"
        }
    });
}

var renderTableData = function () {     
    //-- GENERATE TABLES
    var pageScrollPos = 0;
    var networkStatusTable = $('#networkStatusTable').DataTable({
        searching: false,
        ordering: true,
        info: false,
        lengthChange: false,
        paging: false,
        scrollY: "85px",
        scrollX: false,
        scrollCollapse: false,
        autoWidth: false,
        data: [],
        columns: [{
                title: "ASSETS",
                width: "95%"
            },
            {
                title: "STAT",
                width: "5%"
            },
        ],
        preDrawCallback: function (settings) {
            pageScrollPos = $('body').scrollTop();
        },
        drawCallback: function (settings) {
            $('body').scrollTop(pageScrollPos);
        },
        createdRow: function (row, data, dataIndex) {
            if (data[1] == 1) {
                $(row).addClass('text-danger');
                $(row).find('td:eq(1)').html('ERR');
            } else {
                $(row).addClass('text-theme');
                $(row).find('td:eq(1)').html('OK');
            }
        }
    });
    $('#networkStatusTable tbody').on('click', 'tr', function () {
        var data = networkStatusTable.row(this).data();
        setAssetNetValues(data[7]);
    });
    $('#networkStatusTable tbody').on('mouseenter', 'td', function () {
        var rowIdx = networkStatusTable.cell(this).index().row;
        $(networkStatusTable.rows().nodes()).removeClass('fw-bold');
        $(networkStatusTable.row(rowIdx).nodes()).addClass('fw-bold');
    });
    function setAssetNetValues(id) {      
        var thisNode = allStatusDataset[allStatusDataset.findIndex(obj => obj.id==thisNodeID)];
        var selectedNode = allStatusDataset[allStatusDataset.findIndex(obj => obj.id==id)];
        $("#headingNetworkStatus").text(selectedNode.Node_Name);
        //-- SET ASSET STATUS
        if (selectedNode.Asset_Status == 1) {
            $("#assetNetworkStatus").addClass('text-danger').text('ERROR');
        } else {
            $("#assetNetworkStatus").removeClass('text-danger').text('OK');
        }
        //-- SET NODE STATUS
        if (selectedNode.Node_Status == 1) {
            $("#nodeNetworkStatus").addClass('text-danger').text('ERROR');
        } else {
            $("#nodeNetworkStatus").removeClass('text-danger').text('OK');
        }
        //-- SET SERVER STATUS
        if (selectedNode.Server_Status == 1) {
            $("#serverNetworkStatus").addClass('text-danger').text('ERROR');
        } else {
            $("#serverNetworkStatus").removeClass('text-danger').text('OK');
        }        
    }
};


var renderCharts = function () {

    //################################# RADAR  ################################### 
    var radar = $("#metRadarChart").dxPolarChart({
        commonSeriesSettings: {
            type: "scatter"
        },
        loadingIndicator: {
            enabled: true
        },
        size: {
            height: 200,
        },
        series: [{
                valueField: "Data_MaxGust",
                name: "Gusts (m/s)",
                color: app.color.white,
                argumentField: 'Data_MaxGustDir',
                size: 0.5
            },
            {
                valueField: "Data_WindSpeed",
                name: "Wind Speed (m/s)",
                color: app.color.theme,
                argumentField: 'Data_WindDir',
                size: 0.5
            }
        ],
        argumentAxis: {
            inverted: false,
            startAngle: 0,
            tickInterval: 30,
            period: 360,
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

                var picarroData = {};
                picarroData.Data = pointInfo.points[0].point.data;
                //console.log(picarroData);

                //setTextValues(picarroData);

                print("", picarroData.Data.Data_DateTime);
                print("WIND SPEED: ", picarroData.Data.Data_WindSpeed.toFixed(3));
                print("GUST: ", picarroData.Data.Data_MaxGust.toFixed(3));
            },
        },
        legend: {
            visible: false,
        }
    }).dxPolarChart("instance");
    //################################# RADAR  ###################################
    //################################# WEATHER CHART  ###################################
    var weatherChart = $("#weatherChart").dxChart({
        commonSeriesSettings: {
            argumentField: "Data_DateTime",
            argumentType: "datetime",
            label: {
                format: "shortTime"
            },
            point: {
                visible: false
            },
        },
        loadingIndicator: {
            enabled: true
        },
        size: {
            height: 150,
        },
        panes: [{
            name: "windPane"
        }],
        series: [{
            pane: "windPane",
            type: "line",
            valueField: "Data_MaxGust",
            name: "GUSTS (m/s)",
            color: app.color.theme
        }, {
            pane: "windPane",
            type: "line",
            valueField: "Data_WindSpeed",
            name: "WIND (m/s)",
            color: app.color.white
        }],
        valueAxis: [{
            pane: "windPane",
            grid: {
                visible: true
            },
            constantLines: [{
                value: 15,
                color: "#fc3535",
                dashStyle: "dash",
                width: 1,
                label: {
                    visible: false
                }
            }],
        }],
        argumentAxis: {
            argumentType: "datetime",
            //minVisualRangeLength: { minutes: 1 },
            //visualRange: { length: "hour"}
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

                var picarroData = {};
                picarroData.Data = pointInfo.points[0].point.data;
                //console.log(picarroData);

                //setTextValues(picarroData);

                print("", pointInfo.argumentText);
                print("WIND SPEED: ", picarroData.Data.Data_WindSpeed.toFixed(3));
                print("GUST: ", picarroData.Data.Data_MaxGust.toFixed(3));
            }
        },
        crosshair: {
            enabled: true,
            horizontalLine: {
                visible: false
            }
        },
        "export": {
            enabled: false
        },
        legend: {
            visible: true,
            horizontalAlignment: "center",
            verticalAlignment: "top"
        }
    });

    $("#weatherChart").mouseleave(function () {
        if (ws_Data != {}) {
            //setValues(ws_Data);
        }
    });
    //################################# WEATHER CHART  ###################################
    //################################# PICARRO INSTRUMENT  ###################################
    var picarroChart = $("#picarroChart").dxChart({
        commonSeriesSettings: {
            argumentField: "Data_DateTime",
            argumentType: "datetime",
            label: {
                format: "shortTime"
            },
            point: {
                visible: false
            }
        },
        loadingIndicator: {
            enabled: true
        },
        size: {
            height: 370,
        },
        panes: [{
            name: "co2Pane"
        }, {
            name: "coPane"
        }, {
            name: "h2oPane"
        }, {
            name: "ch4Pane"
        }],
        series: [{
            pane: "co2Pane",
            type: "line",
            valueField: "Data_CO2",
            name: "CO2 (ppm)",
            color: app.color.theme
        }, {
            pane: "coPane",
            type: "line",
            valueField: "Data_CO",
            name: "CO (ppm)",
            color: app.color.theme
        }, {
            pane: "ch4Pane",
            type: "line",
            valueField: "Data_CH4",
            name: "CH4 (ppm)",
            color: app.color.theme
        }, {
            pane: "h2oPane",
            type: "line",
            valueField: "Data_H2O",
            name: "H2O (%)",
            color: app.color.theme
        }],
        valueAxis: [{
            pane: "co2Pane",
            grid: {
                visible: true
            },
            constantLines: [{
                value: 410,
                color: "#fc3535",
                dashStyle: "dash",
                width: 1,
                label: {
                    visible: false
                }
            }],
        }, {
            pane: "coPane",
            grid: {
                visible: true
            },
            constantLines: [{
                value: 1,
                color: "#fc3535",
                dashStyle: "dash",
                width: 1,
                label: {
                    visible: false
                }
            }],
        }, {
            pane: "ch4Pane",
            grid: {
                visible: true
            },
            constantLines: [{
                value: 1.94,
                color: "#fc3535",
                dashStyle: "dash",
                width: 1,
                label: {
                    visible: false
                }
            }],
        }, {
            pane: "h2oPane",
            grid: {
                visible: true
            },
            constantLines: [{
                value: 1.4,
                color: "#fc3535",
                dashStyle: "dash",
                width: 1,
                label: {
                    visible: false
                }
            }],
        }],
        argumentAxis: {
            argumentType: "datetime",
            //minVisualRangeLength: { minutes: 1 },
            //visualRange: { length: "hour"}
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

                var picarroData = {};
                picarroData.Data = pointInfo.points[0].point.data;
                //console.log(picarroData);

                //setTextValues(picarroData);

                print("", pointInfo.argumentText);
                print("CO2: ", picarroData.Data.Data_CO2.toFixed(3));
                print("CO: ", picarroData.Data.Data_CO.toFixed(3));
                print("H2O: ", picarroData.Data.Data_H2O.toFixed(3));
                print("CH4: ", picarroData.Data.Data_CH4.toFixed(3));

                //var weatherChart = $("#weatherChart").dxChart("instance");
                //weatherChart.crosshair.show();
            }
        },
        crosshair: {
            enabled: true,
            horizontalLine: {
                visible: false
            }
        },
        "export": {
            enabled: false
        },
        legend: {
            visible: false,
            horizontalAlignment: "center",
            verticalAlignment: "top"
        }
    });

    $("#picarroChart").mouseleave(function () {
        if (ws_Data != {}) {
            //setValues(ws_Data);
        }
    });
    //################################# PICARRO INSTRUMENT  ###################################
    //################################# SSC CHART  ###################################
    // SETUP SMALL SINGLE CHART
    for (var i = 0, len = json_SSC.length; i < len; ++i) {
        var jdata = json_SSC[i];

        if (document.getElementById('SSC_' + jdata.id) != null) {
            createSSC(jdata);
        }

    }
    //################################# SSC CHART  ###################################
};

// -- MAP
var renderMaps = function () {
    var siteMap = $('#networkStatusMap').dxMap({
        center: [51.94011137604235, -10.244128704071045],
        zoom: 14,
        height: 380,
        width: '100%',
        provider: 'bing',
        controls: true,
        type: 'hybrid',
        markers: markersData,
    }).dxMap('instance');
};
// -- GET OVERALL STATUS 
var markersData = [];
var newMarker = {};
var icon = '';
var ajax_call = function() {
    $.ajax({
        type: 'GET',
        url: '../nodes/node/',
        headers: {
            "Authorization": "Basic " + btoa("admin" + ":" + "will1977"),
            'Accept' : 'application/json'
        },
        success: function(data) {
            $.each(data.results, function(i, asset) {
                
                if (asset.Asset_Status == 1) {icon = '/static/assets/img/map/error_marker.png';} else {icon = '/static/assets/img/map/ok_marker.png';}
                newMarker = {
                    location: {
                        lat: asset.Node_Lat, 
                        lng: asset.Node_Lng
                    },
                    tooltip: {
                        text: asset.Node_Name,
                    },
                    iconSrc: icon,
                };
                markersData.push(newMarker);
            });
            $("#networkStatusMap").dxMap({
                markers: markersData
            });
        }
    });
};
var interval_status = 60000; // 60 secs
setInterval(ajax_call, interval_status);


function initialSetup() {
    setStatus(Status_Data);
    setSetup(Setup_Data);
    setHistory(History_Data);
    setCurrent(Current_Data);
}

/* Controller
------------------------------------------------ */
$(document).ready(function () {
    startWebSocket();
    renderCharts();
    renderMaps();
    renderTableData();
    initialSetup();
    ajax_call();

    $(document).on('theme-reload', function () {
        $('[data-render="apexchart"], #chart-server, #world-map').empty();
        renderCharts();
        renderMaps();
        renderTableData();
        ajax_call();
    });
});