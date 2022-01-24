
// SET UNIVERSAL VARIABLES
var allStatusDataset = [];
var thisStatusDataset = [];
var thisNodeID = 0;

var startWebSocket = function () {
    var picarroSocket;
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + '/picarro/';
    picarroSocket = new WebSocket(ws_path);    

    picarroSocket.onmessage = function (e) {
        ws_Data = JSON.parse(e.data).message;
        console.log(ws_Data);
        // SET STATUS VALUES
        if (ws_Data.Data_Type == 'StatusData') {
            var StatusData = ws_Data.Data.data.map(function(h){ return {id: h.id, asset: h.Node_Name, location: h.Location, status: h.Status.toString(), asset_status: h.Asset_Status, asset_status_description: h.Asset_Status_Description, node_status: h.Node_Status, node_status_description: h.Node_Status_Description, server_status: h.Server_Status, server_status_description: h.Server_Status_Description, coords: [h.Node_Lat, h.Node_Lng]};});
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
            thisNodeID = ws_Data.Node_ID;
            // SET ALL STATUS DATASET
            allStatusDataset = ws_Data.Data.data;
            // SET THIS STATUS DATASET
            thisStatusDataset = allStatusDataset[allStatusDataset.findIndex(obj => obj.id==thisNodeID)];
        }
        // SET SETUP VALUES
        if (ws_Data.Data_Type == 'SetupData') {
            // SET THIS NODE
            thisNodeID = ws_Data.Node_ID;
            // SET THIS STATUS DATASET
            thisStatusDataset = ws_Data.Data.data[0];
            // SET STATUS HEADING
            $("#headingNetworkStatus").text(thisStatusDataset.Node_Name);
            //-- SET ASSET STATUS
            if (thisStatusDataset.Asset_Status == 1) {
                $("#assetNetworkStatus").addClass('text-danger').text('ERROR');
                $('#Asset_Status').addClass('bg-danger');
            } else {
                $("#assetNetworkStatus").removeClass('text-danger').text('OK');
                $('#Asset_Status').removeClass('bg-danger');
            }
            //-- SET NODE STATUS
            if (thisStatusDataset.Node_Status == 1) {
                $("#nodeNetworkStatus").addClass('text-danger').text('ERROR');
                $('#Node_Status').addClass('bg-danger');
                $('#Node_Status').attr('data-original-title', 'Not OK!!!!');
            } else {
                $("#nodeNetworkStatus").removeClass('text-danger').text('OK');
                $('#Node_Status').removeClass('bg-danger');
                $('#Node_Status').attr('data-original-title', 'OK');
            }
            //-- SET SERVER STATUS
            if (thisStatusDataset.Server_Status == 1) {
                $("#serverNetworkStatus").addClass('text-danger').text('ERROR');
            } else {
                $("#serverNetworkStatus").removeClass('text-danger').text('OK');
            }
        }
        // SET CHART VALUES
        if (ws_Data.Data_Type == 'HistoryData') {
            $("#metRadarChart").dxPolarChart("option", "dataSource", ws_Data.Data.data);
            $("#weatherChart").dxChart("option", "dataSource", ws_Data.Data.data);
            $("#picarroChart").dxChart("option", "dataSource", ws_Data.Data.data);

            $("#SSC_Voltage").dxChart("option", "dataSource", ws_Data.Data.data);
            var maxMinAvg_Voltage = maxMinAvg(ws_Data.Data.data, "Instrument_Supply_Voltage");
            $("#Voltage_Max").text(maxMinAvg_Voltage[0].toFixed(2));
            $("#Voltage_Min").text(maxMinAvg_Voltage[1].toFixed(2));
            $("#Voltage_Ave").text(maxMinAvg_Voltage[2].toFixed(2));

            $("#SSC_CavityTemp").dxChart("option", "dataSource", ws_Data.Data.data);
            var maxMinAvg_CavityTemp = maxMinAvg(ws_Data.Data.data, "Data_Cavity_Temp");
            $("#CavityTemp_Max").text(maxMinAvg_CavityTemp[0].toFixed(2));
            $("#CavityTemp_Min").text(maxMinAvg_CavityTemp[1].toFixed(2));
            $("#CavityTemp_Ave").text(maxMinAvg_CavityTemp[2].toFixed(2));

            $("#SSC_WarmBoxTemp").dxChart("option", "dataSource", ws_Data.Data.data);
            var maxMinAvg_WarmBoxTemp = maxMinAvg(ws_Data.Data.data, "Data_WarmBoxTemp");
            $("#WarmBoxTemp_Max").text(maxMinAvg_WarmBoxTemp[0].toFixed(2));
            $("#WarmBoxTemp_Min").text(maxMinAvg_WarmBoxTemp[1].toFixed(2));
            $("#WarmBoxTemp_Ave").text(maxMinAvg_WarmBoxTemp[2].toFixed(2));

            $("#SSC_CavityPres").dxChart("option", "dataSource", ws_Data.Data.data);
            var maxMinAvg_CavityPres = maxMinAvg(ws_Data.Data.data, "Data_CavityPressure");
            $("#CavityPres_Max").text(maxMinAvg_CavityPres[0].toFixed(2));
            $("#CavityPres_Min").text(maxMinAvg_CavityPres[1].toFixed(2));
            $("#CavityPres_Ave").text(maxMinAvg_CavityPres[2].toFixed(2));
        }
        // SET STATIC VALUES
        if (ws_Data.Data_Type == 'CurrentData') {
            var thisDateTime = new Date(ws_Data.Data.Data_DateTime);
            var thisTime = new Date(ws_Data.Data.Data_DateTime).toLocaleTimeString();
            var thisDate = new Date(ws_Data.Data.Data_DateTime).toLocaleDateString();
            thisDateTime = thisDateTime.toLocaleString();

            var endDate = new Date();
            var startDate = new Date(ws_Data.HeartBeat);
            var timeDiff = (endDate.getTime() - startDate.getTime()) / 1000;
            if (timeDiff > 70) {

            }            

            $("#Time").text(thisTime);
            $("#Date").text(thisDate);

            $("#CO2_Value").text(ws_Data.Data.Data_CO2.toFixed(1));
            $("#CO2_Time").text(thisTime);
            $("#CO2_Date").text(thisDate);
            $("#CO2_Bar").attr('style', 'width: ' + getPercentage(ws_Data.Data.Data_CO2, 420) + '%');

            $("#CO_Value").text(ws_Data.Data.Data_CO.toFixed(1));
            $("#CO_Time").text(thisTime);
            $("#CO_Date").text(thisDate);
            $("#CO_Bar").attr('style', 'width: ' + getPercentage(ws_Data.Data.Data_CO, 2) + '%');

            $("#H2O_Value").text(ws_Data.Data.Data_H2O.toFixed(1));
            $("#H2O_Time").text(thisTime);
            $("#H2O_Date").text(thisDate);
            $("#H2O_Bar").attr('style', 'width: ' + getPercentage(ws_Data.Data.Data_H2O, 4) + '%');

            $("#CH4_Value").text(ws_Data.Data.Data_CH4.toFixed(1));
            $("#CH4_Time").text(thisTime);
            $("#CH4_Date").text(thisDate);
            $("#CH4_Bar").attr('style', 'width: ' + getPercentage(ws_Data.Data.Data_CH4, 3) + '%');

            $("#Voltage_Value").text(ws_Data.Data.Instrument_Supply_Voltage.toFixed(1));
            $("#Voltage_Time").text(thisTime);
            $("#Voltage_Date").text(thisDate);
            $("#Voltage_Bar").attr('style', 'width: ' + getPercentage(ws_Data.Data.Instrument_Supply_Voltage, 26) + '%');

            $("#CavityTemp_Value").text(ws_Data.Data.Data_Cavity_Temp.toFixed(1));
            $("#CavityTemp_Time").text(thisTime);
            $("#CavityTemp_Date").text(thisDate);
            $("#CavityTemp_Bar").attr('style', 'width: ' + getPercentage(ws_Data.Data.Data_Cavity_Temp, 45) + '%');

            $("#CavityPres_Value").text(ws_Data.Data.Data_CavityPressure.toFixed(1));
            $("#CavityPres_Time").text(thisTime);
            $("#CavityPres_Date").text(thisDate);
            $("#CavityPres_Bar").attr('style', 'width: ' + getPercentage(ws_Data.Data.Data_CavityPressure, 1) + '%');

            $("#WarmBoxTemp_Value").text(ws_Data.Data.Data_WarmBoxTemp.toFixed(1));
            $("#WarmBoxTemp_Time").text(thisTime);
            $("#WarmBoxTemp_Date").text(thisDate);
            $("#WarmBoxTemp_Bar").attr('style', 'width: ' + getPercentage(ws_Data.Data.Data_WarmBoxTemp, 45) + '%');

            $("#Misc_1_Heading").text("CO2 DRY");
            $("#Misc_1_Value").text(ws_Data.Data.Data_CO2_Dry.toFixed(1));
            $("#Misc_1_Time").text(thisTime);
            $("#Misc_1_Date").text(thisDate);

            $("#Wind_Value").text(ws_Data.Data.Data_WindSpeed.toFixed(1));
            $("#Gust_Value").text(ws_Data.Data.Data_MaxGust.toFixed(1));
            $("#Dir_Value").text(ws_Data.Data.Data_WindDir.toFixed(1));
            $("#Temp_Value").text(ws_Data.Data.Data_GrassA.toFixed(1));
            $("#Hum_Value").text(ws_Data.Data.Data_HumA.toFixed(1));
            $("#Pres_Value").text(ws_Data.Data.Data_Pressure.toFixed(1));

            // MISC VALUES
            var jsonDataVis = [{
                data: ws_Data.Data.Data_CO2_Dry.toFixed(1),
                heading: "CO2 DRY",
                data_type: "PPM",
                time: thisTime,
                date: thisDate,
                type: "MISC",
            }, {
                data: ws_Data.Data.Data_CH4_Dry.toFixed(1),
                heading: "CH4 DRY",
                data_type: "PPM",
                time: thisTime,
                date: thisDate,
                type: "MISC",
            }, {
                data: ws_Data.Data.Data_Amb_P.toFixed(1),
                heading: "AMBIENT PRESSURE",
                data_type: "Pa",
                time: thisTime,
                date: thisDate,
                type: "MISC",
            }, {
                data: ws_Data.Data.Data_DasTemp.toFixed(1),
                heading: "DAS TEMPERATURE",
                data_type: "C",
                time: thisTime,
                date: thisDate,
                type: "MISC",
            }, {
                data: ws_Data.Data.Data_EtalonTemp.toFixed(1),
                heading: "ETALON TEMPERATURE",
                data_type: "C",
                time: thisTime,
                date: thisDate,
                type: "MISC",
            }, {
                data: ws_Data.Data.Data_Solenoid_Valves.toFixed(1),
                heading: "SOLENOID VALVE",
                data_type: "",
                time: thisTime,
                date: thisDate,
                type: "MISC",
            }, {
                data: ws_Data.Data.Data_MPVPosition.toFixed(1),
                heading: "MPV POSITION",
                data_type: "",
                time: thisTime,
                date: thisDate,
                type: "MISC",
            }, {
                data: ws_Data.Data.Data_OutletValve.toFixed(1),
                heading: "OUTLET VALVE",
                data_type: "",
                time: thisTime,
                date: thisDate,
                type: "MISC",
            }, {
                data: ws_Data.Data.Data_Species.toFixed(1),
                heading: "SPECIES",
                data_type: "",
                time: thisTime,
                date: thisDate,
                type: "MISC",
            }, {
                data: ws_Data.Data.Data_h2o_reported.toFixed(1),
                heading: "H2O REPORTED",
                data_type: "",
                time: thisTime,
                date: thisDate,
                type: "MISC",
            }, ];
            generateDataVis(jsonDataVis);
        }
    };

    picarroSocket.onclose = function (e) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
    };

    picarroSocket.onerror = function (err) {
        console.error(err);
    };
};

function generateDataVis(jsonData) {
    for (var i = 0, len = jsonData.length; i < len; ++i) {
        if (jsonData[i]["type"] == "MISC") {
            $("#Misc_" + i + "_Heading").text(jsonData[i]["heading"]);
            $("#Misc_" + i + "_Value").text(jsonData[i]["data"]);
            $("#Misc_" + i + "_Time").text(jsonData[i]["time"]);
            $("#Misc_" + i + "_Date").text(jsonData[i]["date"]);
            $("#Misc_" + i + "_Date_Type").text(jsonData[i]["date_type"]);
        }
    }
}

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

/* Controller
------------------------------------------------ */
$(document).ready(function () {
    startWebSocket();
    renderCharts();
    renderMaps();
    renderTableData();

    $(document).on('theme-reload', function () {
        $('[data-render="apexchart"], #chart-server, #world-map').empty();
        renderCharts();
        renderMaps();
    });
});