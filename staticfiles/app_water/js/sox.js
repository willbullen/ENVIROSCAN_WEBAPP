
// SET UNIVERSAL VARIABLES
var allStatusDataset = [];
var thisStatusDataset = [];
var thisNodeID = 0;

function setStatus(db_Data) {
    var StatusData = db_Data.Data.data.map(function(h){ return {id: h.id, asset: h.Node_Name, location: h.Location, status: h.Status.toString(), asset_status: h.Asset_Status, asset_status_description: h.Asset_Status_Description, node_status: h.Node_Status, node_status_description: h.Node_Status_Description, server_status: h.Server_Status, server_status_description: h.Server_Status_Description, coords: [h.Node_Lat, h.Node_Lng]};});
    // SET MAP VALUES
    var mapObject = $('#networkStatusMap').vectorMap('get', 'mapObject'); 
    mapObject.addMarkers(StatusData.map(function(h){ return {name: h.asset, latLng: h.coords, id: h.id};}), []);
    mapObject.series.markers[0].setValues(StatusData.reduce(function(p, c, i){ p[i] = c.status; return p;},{}));
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

function setHistory(db_Data) {
    // MET DATA
    $("#metRadarChart").dxPolarChart("option", "dataSource", db_Data.Data.data);
    $("#weatherChart").dxChart("option", "dataSource", db_Data.Data.data);
    // CORE DATA
    $("#soxChart").dxChart("option", "dataSource", db_Data.Data.data);
    // SUPPLY VOLTAGE
    $("#miniChart_1").dxChart("option", "dataSource", db_Data.Data.data);
    var maxMinAvg_Voltage = maxMinAvg(db_Data.Data.data, "Instrument_Supply_Voltage");
    $("#Voltage_Max").text(maxMinAvg_Voltage[0].toFixed(2));
    $("#Voltage_Min").text(maxMinAvg_Voltage[1].toFixed(2));
    $("#Voltage_Ave").text(maxMinAvg_Voltage[2].toFixed(2));
    // Sample_Flow
    $("#miniChart_2").dxChart("option", "dataSource", db_Data.Data.data);
    var maxMinAvg_Sample_Flow = maxMinAvg(db_Data.Data.data, "Data_Sample_Flow");
    $("#Sample_Flow_Max").text(maxMinAvg_Sample_Flow[0].toFixed(2));
    $("#Sample_Flow_Min").text(maxMinAvg_Sample_Flow[1].toFixed(2));
    $("#Sample_Flow_Ave").text(maxMinAvg_Sample_Flow[2].toFixed(2));
    // UV_Lamp
    $("#miniChart_3").dxChart("option", "dataSource", db_Data.Data.data);
    var maxMinAvg_UV_Lamp = maxMinAvg(db_Data.Data.data, "Data_UV_Lamp");
    $("#UV_Lamp_Max").text(maxMinAvg_UV_Lamp[0].toFixed(2));
    $("#UV_Lamp_Min").text(maxMinAvg_UV_Lamp[1].toFixed(2));
    $("#UV_Lamp_Ave").text(maxMinAvg_UV_Lamp[2].toFixed(2));
    // Stability
    $("#miniChart_4").dxChart("option", "dataSource", db_Data.Data.data);
    var maxMinAvg_Stability = maxMinAvg(db_Data.Data.data, "Data_Stability");
    $("#Stability_Max").text(maxMinAvg_Stability[0].toFixed(2));
    $("#Stability_Min").text(maxMinAvg_Stability[1].toFixed(2));
    $("#Stability_Ave").text(maxMinAvg_Stability[2].toFixed(2));
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
    // CORE DATA 1
    $("#SO2_Concentration_Value").text(db_Data.Data.Data_SO2_Concentration.toFixed(1));
    $("#SO2_Concentration_Bar").attr('style', 'width: ' + getPercentage(db_Data.Data.Data_SO2_Concentration, 420) + '%');
    // CORE DATA 2
    $("#Sox_Pressure_Value").text(db_Data.Data.Data_Sox_Pressure.toFixed(1));
    $("#Sox_Pressure_Bar").attr('style', 'width: ' + getPercentage(db_Data.Data.Data_Sox_Pressure, 2) + '%');
    // CORE DATA 3
    $("#HVPS_Value").text(db_Data.Data.Data_HVPS.toFixed(1));
    $("#HVPS_Bar").attr('style', 'width: ' + getPercentage(db_Data.Data.Data_HVPS, 4) + '%');
    // CORE DATA 4
    $("#Pressure_Value").text(db_Data.Data.Data_Pressure.toFixed(1));
    $("#Pressure_Bar").attr('style', 'width: ' + getPercentage(db_Data.Data.Data_Pressure, 3) + '%');
    // SUPPLY VOLTAGE
    $("#Voltage_Value").text(db_Data.Data.Instrument_Supply_Voltage.toFixed(1));
    $("#Voltage_Bar").attr('style', 'width: ' + getPercentage(db_Data.Data.Instrument_Supply_Voltage, 26) + '%');
    // Sample_Flow
    $("#Sample_Flow_Value").text(db_Data.Data.Data_Sample_Flow.toFixed(1));
    $("#Sample_Flow_Bar").attr('style', 'width: ' + getPercentage(db_Data.Data.Data_Sample_Flow, 45) + '%');
    // UV_Lamp
    $("#UV_Lamp_Value").text(db_Data.Data.Data_UV_Lamp.toFixed(1));
    $("#UV_Lamp_Bar").attr('style', 'width: ' + getPercentage(db_Data.Data.Data_UV_Lamp, 1) + '%');
    // Stability
    $("#Stability_Value").text(db_Data.Data.Data_Stability.toFixed(1));
    $("#Stability_Bar").attr('style', 'width: ' + getPercentage(db_Data.Data.Data_Stability, 45) + '%');
    // MISC DATA
    $("#Lamp_Dark_Value").text(db_Data.Data.Data_Lamp_Dark.toFixed(1));
    $("#Lamp_Ratio_Value").text(db_Data.Data.Data_Lamp_Ratio.toFixed(1));
    $("#Norm_PMT_Value").text(db_Data.Data.Data_Norm_PMT.toFixed(1));
    $("#PMT_Value").text(db_Data.Data.Data_PMT.toFixed(1));
    $("#PMT_Dark_Value").text(db_Data.Data.Data_PMT_Dark.toFixed(1));
    $("#PMT_Signal_Value").text(db_Data.Data.Data_PMT_Signal.toFixed(1));
    $("#PMT_Temp_Value").text(db_Data.Data.Data_PMT_Temp.toFixed(1));
    $("#Photo_Absolute_Value").text(db_Data.Data.Data_Photo_Absolute.toFixed(1));
    $("#REF_V_4096_Dark_Value").text(db_Data.Data.Data_REF_V_4096_Dark.toFixed(1));
    $("#REF_V_4096_Light_Value").text(db_Data.Data.Data_REF_V_4096_Light.toFixed(1));
    // MET DATA
    $("#Wind_Value").text(db_Data.Data.Data_WindSpeed.toFixed(1));
    $("#Gust_Value").text(db_Data.Data.Data_MaxGust.toFixed(1));
    $("#Dir_Value").text(db_Data.Data.Data_WindDir.toFixed(1));
    $("#Temp_Value").text(db_Data.Data.Data_GrassA.toFixed(1));
    $("#Hum_Value").text(db_Data.Data.Data_HumA.toFixed(1));
    $("#Pres_Value").text(db_Data.Data.Data_Pressure.toFixed(1));
}

function initialSetup() {
    setStatus(Status_Data);
    setSetup(Setup_Data);
    setHistory(History_Data);
    setCurrent(Current_Data);
}

var startWebSocket = function () {
    var soxSocket;
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + '/sox/';
    soxSocket = new WebSocket(ws_path);    

    soxSocket.onmessage = function (e) {
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

    soxSocket.onclose = function (e) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
    };

    soxSocket.onerror = function (err) {
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

var renderTableData = function () {    
    //-- GENERATE MAP
    var networkStatusMap = $('#networkStatusMap').vectorMap({
        map: '26counties',
        normalizeFunction: 'polynomial',
        hoverOpacity: 0.5,
        hoverColor: false,
        zoomOnScroll: false,
        series: {
            regions: [{
                normalizeFunction: 'polynomial'
            }],
            markers: [{
                attribute: 'fill',
                scale: {
                    '1': '#FF0000',
                    '0': app.color.theme,
                },
                values: [],
            }]
        },
        focusOn: {
            x: 0.5,
            y: 0.5,
            scale: 1
        },
        regionStyle: {
            initial: {
                fill: app.color.white,
                "fill-opacity": 0.35,
                stroke: 'none',
                "stroke-width": 0.4,
                "stroke-opacity": 1
            },
            hover: {
                "fill-opacity": 0.5
            }
        },
        backgroundColor: 'transparent',
        markers: [],
        onRegionClick: function (event, code, isSelected,  selectedRegions) {            
            $('#networkStatusMap').vectorMap('get','mapObject').setFocus({region: code});
        },
        onMarkerClick: function (event, index) {
            setAssetNetValues(allStatusDataset[index].id);
            //$('#networkStatusMap').vectorMap('get','mapObject').setFocus({marker: index});
        },
    });
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

var renderMaps = function () {


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

                var soxData = {};
                soxData.Data = pointInfo.points[0].point.data;
                //console.log(soxData);

                //setTextValues(soxData);

                print("", soxData.Data.Data_DateTime);
                print("WIND SPEED: ", soxData.Data.Data_WindSpeed.toFixed(3));
                print("GUST: ", soxData.Data.Data_MaxGust.toFixed(3));
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

                var soxData = {};
                soxData.Data = pointInfo.points[0].point.data;
                //console.log(soxData);

                //setTextValues(soxData);

                print("", pointInfo.argumentText);
                print("WIND SPEED: ", soxData.Data.Data_WindSpeed.toFixed(3));
                print("GUST: ", soxData.Data.Data_MaxGust.toFixed(3));
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
    //################################# SOX INSTRUMENT  ###################################
    var soxChart = $("#soxChart").dxChart({
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
            name: "SO2_Concentration_Pane"
        }, {
            name: "Sox_Pressure_Pane"
        }, {
            name: "HVPS_Pane"
        }, {
            name: "Pressure_Pane"
        }],
        series: [{
            pane: "SO2_Concentration_Pane",
            type: "line",
            valueField: "Data_SO2_Concentration",
            name: "SO2_Concentration (ppm)",
            color: app.color.theme
        }, {
            pane: "Sox_Pressure_Pane",
            type: "line",
            valueField: "Data_Sox_Pressure",
            name: "Sox_Pressure (ppm)",
            color: app.color.theme
        }, {
            pane: "Pressure_Pane",
            type: "line",
            valueField: "Data_Pressure",
            name: "Pressure (ppm)",
            color: app.color.theme
        }, {
            pane: "HVPS_Pane",
            type: "line",
            valueField: "Data_HVPS",
            name: "HVPS (%)",
            color: app.color.theme
        }],
        valueAxis: [{
            pane: "SO2_Concentration_Pane",
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
            pane: "Sox_Pressure_Pane",
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
            pane: "Pressure_Pane",
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
            pane: "HVPS_Pane",
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

                var soxData = {};
                soxData.Data = pointInfo.points[0].point.data;
                //console.log(soxData);

                //setTextValues(soxData);

                print("", pointInfo.argumentText);
                print("SO2_Concentration: ", soxData.Data.Data_SO2_Concentration.toFixed(3));
                print("Sox_Pressure: ", soxData.Data.Data_Sox_Pressure.toFixed(3));
                print("HVPS: ", soxData.Data.Data_HVPS.toFixed(3));
                print("Pressure: ", soxData.Data.Data_Pressure.toFixed(3));

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

    $("#soxChart").mouseleave(function () {
        if (ws_Data != {}) {
            //setValues(ws_Data);
        }
    });
    //################################# PICARRO INSTRUMENT  ###################################

    //################################# MINI CHART 1  ###################################
    var miniChart_1 = $("#miniChart_1").dxChart({
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
            height: 120,
        },
        panes: [{
            name: "Pane1",
        }],
        series: [{
            pane: "Pane1",
            type: "line",
            valueField: "Instrument_Supply_Voltage",
            name: "Voltage (V)",
            color: app.color.theme,
        }],
        valueAxis: [{
            pane: "Pane1",
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

                var soxData = {};
                soxData.Data = pointInfo.points[0].point.data;
                //setTextValues(soxData);
                //print("", pointInfo.argumentText);
                //print("Voltave: ", soxData.Data.Data_CO2.toFixed(3));
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
    //################################# MINI CHART 2  ###################################
    var miniChart_2 = $("#miniChart_2").dxChart({
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
            height: 120,
        },
        panes: [{
            name: "Pane1",
        }],
        series: [{
            pane: "Pane1",
            type: "line",
            valueField: "Data_Sample_Flow",
            name: "Flow (lpm)",
            color: app.color.theme,
        }],
        valueAxis: [{
            pane: "Pane1",
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

                var soxData = {};
                soxData.Data = pointInfo.points[0].point.data;
                //setTextValues(soxData);
                //print("", pointInfo.argumentText);
                //print("Voltave: ", soxData.Data.Data_CO2.toFixed(3));
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
    //################################# MINI CHART 3  ###################################
    var miniChart_3 = $("#miniChart_3").dxChart({
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
            height: 120,
        },
        panes: [{
            name: "Pane1",
        }],
        series: [{
            pane: "Pane1",
            type: "line",
            valueField: "Data_UV_Lamp",
            name: "Lumens (L)",
            color: app.color.theme,
        }],
        valueAxis: [{
            pane: "Pane1",
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

                var soxData = {};
                soxData.Data = pointInfo.points[0].point.data;
                //setTextValues(soxData);
                //print("", pointInfo.argumentText);
                //print("Voltave: ", soxData.Data.Data_CO2.toFixed(3));
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
    //################################# MINI CHART 4  ###################################
    var miniChart_4 = $("#miniChart_4").dxChart({
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
            height: 120,
        },
        panes: [{
            name: "Pane1",
        }],
        series: [{
            pane: "Pane1",
            type: "line",
            valueField: "Data_Stability",
            name: "Stability",
            color: app.color.theme,
        }],
        valueAxis: [{
            pane: "Pane1",
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

                var soxData = {};
                soxData.Data = pointInfo.points[0].point.data;
                //setTextValues(soxData);
                //print("", pointInfo.argumentText);
                //print("Voltave: ", soxData.Data.Data_CO2.toFixed(3));
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
};

/* Controller
------------------------------------------------ */
$(document).ready(function () {
    startWebSocket();
    renderCharts();
    renderMaps();
    renderTableData();
    initialSetup();

    $(document).on('theme-reload', function () {
        $('[data-render="apexchart"], #chart-server, #world-map').empty();
        renderCharts();
        renderMaps();
        renderTableData();
        //initialSetup();
    });
});