$(document).ready(function () {

    var Picarro_Chart_1Hour_Data = {};
    var Picarro_Chart_12Hours_Data = {};
    var Picarro_Chart_1Day_Data = {};
    var Picarro_Chart_1Week_Data = {};
    var Picarro_Data = {};
    var Picarro_Chart_Timespan = '1h';

    $('#side_dropdown a').click(function (e) {
        console.log("TAB SELECTED: " + $(this).attr('href'));
        e.preventDefault();
        $("#sidebar_text").text($(this).attr('href'));
        $(this).removeClass('active');
        $(this).tab('show');
    });


    //############################################################################### 
    // 
    //                                 CONTROLS START
    // 
    //############################################################################### 

    //################################# INSTRUMENT CHART  ###################################

    //################################# INSTRUMENT CHART  ###################################



    //################################# RADAR  ################################### 
    var radar = $("#radarChart").dxPolarChart({
        commonSeriesSettings: {
            type: "scatter"
        },
        series: [
            {
                valueField: "Data_MaxGust", 
                name: "Gusts (m/s)", 
                color: "#FF0000",
                argumentField: 'Data_MaxGustDir'
            },
            {
                valueField: "Data_WindSpeed", 
                name: "Wind Speed (m/s)", 
                color: "#5f8b95",
                argumentField: 'Data_WindDir'
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

                setTextValues(picarroData);

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

    //################################# LOCATION  ###################################    
    
    var map = $("#mapPicarro").dxMap({
        provider: "bing",
        zoom: 14,
        height: 500,
        width: "100%",
        controls: true,
        markers: [{
                location: "40.7825, -73.966111"
            }, {
                location: [40.755833, -73.986389]
            }, {
                location: { lat: 40.753889, lng: -73.981389}
            }, {
                location: "Brooklyn Bridge,New York,NY"
            }
        ],
        routes: [
            {
                weight: 6,
                color: "blue",
                opacity: 0.5,
                mode: "",
                locations: [
                    [40.782500, -73.966111],
                    [40.755833, -73.986389],
                    [40.753889, -73.981389],
                    "Brooklyn Bridge,New York,NY"
                ]
    
            }
        ]
    }).dxMap("instance");
    //################################# LOCATION  ################################### 

    //################################# LOADING PANEL  ###################################
    var picarroLoadPanel = $(".picarroLoadPanel").dxLoadPanel({
        shadingColor: "black",
        position: {
            of: "#collapsePicarro"
        },
        visible: true,
        showIndicator: true,
        showPane: true,
        shading: true,
        closeOnOutsideClick: false,
    }).dxLoadPanel("instance");
    //################################# LOADING PANEL  ###################################

    //################################# PROPERTIES  ###################################
    var propertyType = [{
        "ID": 1,
        "Type": "Switch"
    }, {
        "ID": 2,
        "Type": "Location"
    }, {
        "ID": 3,
        "Type": "Button"
    }, {
        "ID": 4,
        "Type": "Slider"
    }, {
        "ID": 5,
        "Type": "Value"
    }, {
        "ID": 6,
        "Type": "DropDown"
    }, {
        "ID": 7,
        "Type": "Text Area"
    }, {
        "ID": 8,
        "Type": "Date"
    }, {
        "ID": 9,
        "Type": "Select Box"
    }, {
        "ID": 10,
        "Type": "Calendar"
    }, {
        "ID": 11,
        "Type": "Number Box"
    }];
    $("#gridPicarroProperties").dxDataGrid({
        //Properties_DateCreated
        //Properties_Type
        //Properties_Title
        //Properties_Value

        showColumnLines: false,
        showRowLines: true,
        rowAlternationEnabled: true,
        showBorders: false,
        keyExpr: "id",
        editing: {
            mode: "cell",
            allowUpdating: true
        },
        columns: [{
                dataField: "Properties_DateCreated",
                caption: "Date Created",
                dataType: "date",
                visible: false
            },
            {
                dataField: "Properties_Title",
                caption: "Title"
            },
            {
                dataField: "Properties_Type",
                caption: "Type",
                lookup: {
                    dataSource: propertyType,
                    displayExpr: "Type",
                    valueExpr: "ID"
                },
                visible: false
            },
            {
                dataField: "Properties_Value",
                caption: "Value"
            },
            {
                dataField: "id",
                visible: false
            }
        ],
        onRowUpdated: function (e) {
            console.log("Properties Row Updated");
            var data = e.data;
            data.Node = 'Picarro';
            data.Module = 'Properties';
            data.Action = 'Update';
            console.log(data);
            picarroSocket.send(JSON.stringify(data));
        },
        onRowInserted: function (e) {
            console.log("Properties Row Inserted");
            var data = e.data;
            data.Node = 'Picarro';
            data.Module = 'Properties';
            data.Action = 'Add';
            console.log(data);
            picarroSocket.send(JSON.stringify(data));
        },
        scrolling: {
            rowRenderingMode: 'virtual'
        },
        paging: {
            pageSize: 5
        }
    });
    //################################# PROPERTIES  ###################################    

    //################################# LOGS  ###################################
    $("#gridPicarroLogs").dxDataGrid({
        showColumnLines: false,
        showRowLines: true,
        rowAlternationEnabled: true,
        showBorders: false,
        keyExpr: "id",
        scrolling: {
            rowRenderingMode: 'virtual'
        },
        paging: {
            pageSize: 5
        }
    });
    //################################# LOGS  ###################################

    //################################# ALARMS  ###################################
    $("#gridPicarroAlarms").dxDataGrid({
        showColumnLines: false,
        showRowLines: true,
        rowAlternationEnabled: true,
        showBorders: false,
        keyExpr: "id",
        scrolling: {
            rowRenderingMode: 'virtual'
        },
        paging: {
            pageSize: 5
        }
    });
    //################################# ALARMS  ###################################

    //################################# PLANNED MAINTENANCE  ###################################
    var pmType = [{
        "ID": 1,
        "Type": "Hours"
    }, {
        "ID": 2,
        "Type": "Days"
    }, {
        "ID": 3,
        "Type": "Months"
    }, {
        "ID": 4,
        "Type": "Years"
    }, {
        "ID": 5,
        "Type": "One-Time"
    }];
    var pmEnabled = [{
        "ID": 0,
        "State": "No"
    }, {
        "ID": 1,
        "State": "Yes"
    }];
    $("#gridPicarroPM").dxDataGrid({
        showColumnLines: false,
        showRowLines: true,
        rowAlternationEnabled: true,
        showBorders: false,
        keyExpr: "id",
        editing: {
            mode: "popup",
            allowUpdating: true,
            allowAdding: true,
            allowViewing: true,
            popup: {
                title: "Planned Maintenance",
                showTitle: true,
                width: 700,
                height: 525
            },
            form: {
                items: [{
                    itemType: "group",
                    colCount: 1,
                    colSpan: 2,
                    items: [
                        "PM_Title", 
                        "PM_Type", 
                        "PM_Time_Interval",
                        "PM_Task",
                        {
                            dataField: "PM_Enabled",
                            caption: "Enabled",
                            editorType: "dxSwitch",
                            colSpan: 2,
                        },
                        {
                            dataField: "PM_Details",
                            caption: "Details",
                            editorType: "dxTextArea",
                            colSpan: 2,
                            editorOptions: {
                                height: 100
                            },
                        },
                        {
                            dataField: "PM_Kwargs",
                            caption: "Kwargs",
                            editorType: "dxTextArea",
                            colSpan: 2,
                            editorOptions: {
                                height: 30
                            },
                        },
                        {
                            dataField: "PM_Args",
                            caption: "Args",
                            editorType: "dxTextArea",
                            colSpan: 2,
                            editorOptions: {
                                height: 30
                            },
                        }
                    ]
                }]
            }
        },
        columns: [{
                dataField: "PM_DateCreated",
                caption: "Date Created",
                dataType: "date",
                visible: false
            },
            {
                dataField: "PM_Title",
                caption: "Title"
            },
            {
                dataField: "PM_Type",
                caption: "Type",
                lookup: {
                    dataSource: pmType,
                    displayExpr: "Type",
                    valueExpr: "ID"
                }
            },
            {
                dataField: "PM_Time_Interval",
                caption: "Interval"
            },
            {
                dataField: "PM_Enabled",
                caption: "Enabled",
                lookup: {
                    dataSource: pmEnabled,
                    displayExpr: "State",
                    valueExpr: "ID"
                }
            },
            {
                dataField: "PM_Details",
                visible: false
            },
            {
                dataField: "id",
                visible: false
            }
        ],
        onRowUpdated: function (e) {
            console.log("PM Row Updated");
            var data = e.data;
            data.Node = 'Picarro';
            data.Module = 'PM';
            data.Action = 'Update';
            console.log(data);
            picarroSocket.send(JSON.stringify(data));
        },
        onRowInserted: function (e) {
            console.log("PM Row Inserted");
            var data = e.data;
            data.Node = 'Picarro';
            data.Module = 'PM';
            data.Action = 'Add';
            console.log(data);
            picarroSocket.send(JSON.stringify(data));
        },
        scrolling: {
            rowRenderingMode: 'virtual'
        },
        paging: {
            pageSize: 5
        }
    });

    //################################# JOBS  ###################################
    var jobsType = [{
        "ID": 0,
        "Type": "PM"
    }, {
        "ID": 1,
        "Type": "Once Off"
    }];
    var jobsStatus = [{
        "ID": 0,
        "Status": "Incomplete"
    }, {
        "ID": 1,
        "Status": "Completed"
    }, {
        "ID": 2,
        "Status": "Archived"
    }];
    $("#gridPicarroJobs").dxDataGrid({
        showColumnLines: false,
        showRowLines: true,
        rowAlternationEnabled: true,
        showBorders: false,
        keyExpr: "id",
        editing: {
            mode: "popup",
            allowUpdating: true,
            allowAdding: false,
            popup: {
                title: "Jobs",
                showTitle: true,
                width: 700,
                height: 525
            },
            form: {
                items: [{
                    itemType: "group",
                    colCount: 1,
                    colSpan: 2,
                    items: [
                        "Jobs_Title", 
                        "Jobs_Type",
                        "Jobs_Status", 
                        {
                            dataField: "Jobs_Description",
                            editorType: "dxTextArea",
                            colSpan: 2,
                            editorOptions: {
                                height: 100
                            }
                        }, 
                        {
                            dataField: "Jobs_Notes",
                            editorType: "dxTextArea",
                            colSpan: 2,
                            editorOptions: {
                                height: 100
                            }
                        }
                    ]
                }]
            }
        },
        columns: [{
                dataField: "Jobs_DateCreated",
                caption: "Date Created",
                dataType: "date",
                visible: false
            },
            {
                dataField: "Jobs_Title",
                caption: "Title"
            },
            {
                dataField: "Jobs_DateToBeCompleted",
                caption: "Date Due"
            },            
            {
                dataField: "Jobs_Type",
                caption: "Type",
                lookup: {
                    dataSource: jobsType,
                    displayExpr: "Type",
                    valueExpr: "ID"
                }
            },
            {
                dataField: "Jobs_Status",
                caption: "Status",
                lookup: {
                    dataSource: jobsStatus,
                    displayExpr: "Status",
                    valueExpr: "ID"
                }
            },
            {
                type: "buttons",
                buttons: [{
                    name: "save",
                    cssClass: "my-class"
                }, "edit", "delete"]
            },
            {
                dataField: "Jobs_Details",
                visible: false
            },
            {
                dataField: "Jobs_Notes",
                visible: false
            },
            {
                dataField: "id",
                visible: false
            }
        ],
        onEditorPrepared: function (e) {
            if (e.dataField == 'Jobs_Type') {
                console.log(e);
                console.log(e.row.isNewRow);
                e.editorOptions.disabled = e.row.isNewRow;
            }
        },
        onInitNewRow: function(e) {  
            e.component.__itemVisible = true;  
        },  
        onEditingStart: function(e) {  
            e.component.__itemVisible = false;  
        },
        onRowUpdated: function (e) {
            console.log("Jobs Row Updated");
            var data = e.data;
            data.Node = 'Picarro';
            data.Module = 'Jobs';
            data.Action = 'Update';
            console.log(data);
            picarroSocket.send(JSON.stringify(data));
        },
        onRowInserted: function (e) {
            console.log("Jobs Row Inserted");
            var data = e.data;
            data.Node = 'Picarro';
            data.Module = 'Jobs';
            data.Action = 'Add';
            console.log(data);
            picarroSocket.send(JSON.stringify(data));
        },
        scrolling: {
            rowRenderingMode: 'virtual'
        },
        paging: {
            pageSize: 5
        }
    });
    //################################# JOBS  ###################################

    //################################# WEATHER CHART  ###################################
    var weatherChart = $("#chartWeather").dxChart({
        dataSource: Picarro_Chart_1Hour_Data,
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
        panes: [{
            name: "windPane"
        }],
        series: [{
            pane: "windPane",
            type: "bar",
            valueField: "Data_MaxGust",
            name: "GUSTS (m/s)",
        },{
            pane: "windPane",
            type: "line",
            valueField: "Data_WindSpeed",
            name: "WIND (m/s)",
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

                setTextValues(picarroData);

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

    $("#chartWeather").mouseleave(function () {
        setValues(Picarro_Data);
    });
    //################################# WEATHER CHART  ###################################
    
    //################################# PICARRO INSTRUMENT  ###################################
    var picarroChart = $("#chartPicarro").dxChart({        
        dataSource: Picarro_Chart_1Hour_Data,
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
        }, {
            pane: "coPane",
            type: "line",
            valueField: "Data_CO",
            name: "CO (ppm)",
        }, {
            pane: "h2oPane",
            type: "line",
            valueField: "Data_H2O",
            name: "H2O (%)",
        }, {
            pane: "ch4Pane",
            type: "bar",
            valueField: "Data_CH4",
            name: "CH4 (ppm)",
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

                setTextValues(picarroData);

                print("", pointInfo.argumentText);
                print("CO2: ", picarroData.Data.Data_CO2.toFixed(3));
                print("CO: ", picarroData.Data.Data_CO.toFixed(3));
                print("H2O: ", picarroData.Data.Data_H2O.toFixed(3));
                print("CH4: ", picarroData.Data.Data_CH4.toFixed(3));

                //var weatherChart = $("#chartWeather").dxChart("instance");
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

    $("#chartPicarro").mouseleave(function () {
        setValues(Picarro_Data);
    });
    //################################# PICARRO INSTRUMENT  ###################################







    //############################################################################### 
    // 
    //                                 LOGIC START
    // 
    //###############################################################################

    var picarroSocket;

    function picarroConnect() {
        var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
        var ws_path = ws_scheme + '://' + window.location.host + '/valentia_picarro/';
        picarroSocket = new WebSocket(ws_path);
        picarroSocket.onmessage = function (e) {
            //console.log(e.data.message);
            Picarro_Data = JSON.parse(e.data).message;
            console.log(Picarro_Data);

            if (Picarro_Data.Data_Type == 'update_pm') {
                $("#gridPicarroPM").dxDataGrid("option", "dataSource", Picarro_Data.Data_PM.data);
                //$("#gridPicarroJobs").dxDataGrid("option", "dataSource", Picarro_Data.Data_Jobs.data);
                //DevExpress.ui.notify("Planned Maintenance Updated succesfully", "success", 600);
            } else if (Picarro_Data.Data_Type == 'update_jobs') {
                $("#gridPicarroJobs").dxDataGrid("option", "dataSource", Picarro_Data.Data_Jobs.data);
                //DevExpress.ui.notify("Jobs Updated succesfully", "success", 600);
            } else if (Picarro_Data.Data_Type == 'update_properties') {
                $("#gridPicarroProperties").dxDataGrid("option", "dataSource", Picarro_Data.Data_Properties.data);
                //DevExpress.ui.notify("Properties Updated succesfully", "success", 600);
            } else if (Picarro_Data.Data_Type == 'update_alarms') {
                $("#gridPicarroAlarms").dxDataGrid("option", "dataSource", Picarro_Data.Data_Alarms.data);
            } else if (Picarro_Data.Data_Type == 'update_logs') {
                $("#gridPicarroLogs").dxDataGrid("option", "dataSource", Picarro_Data.Data_Logs.data);
            } else if (Picarro_Data.Data_Type == 'update_chart_1week') {
                Picarro_Chart_1Week_Data = Picarro_Data.Data_Charts_1Week.data;
                if (Picarro_Chart_Timespan == '1w') {                   
                    $("#chartPicarro").dxChart("option", "dataSource", Picarro_Data.Data_Charts_1Week.data);
                    $("#radarChart").dxPolarChart("option", "dataSource", Picarro_Data.Data_Charts_1Week.data);
                    $("#chartWeather").dxChart("option", "dataSource", Picarro_Data.Data_Charts_1Week.data);
                }                
            } else if (Picarro_Data.Data_Type == 'update_chart_12hour') {
                Picarro_Chart_12Hours_Data = Picarro_Data.Data_Charts_12Hours.data;
                if (Picarro_Chart_Timespan == '12h') {
                    $("#chartPicarro").dxChart("option", "dataSource", Picarro_Data.Data_Charts_12Hours.data);
                    $("#radarChart").dxPolarChart("option", "dataSource", Picarro_Data.Data_Charts_12Hours.data);
                    $("#chartWeather").dxChart("option", "dataSource", Picarro_Data.Data_Charts_12Hours.data);
                }                
            } else if (Picarro_Data.Data_Type == 'update_chart_1hour') {
                Picarro_Chart_1Hour_Data = Picarro_Data.Data_Charts_1Hour.data;
                if (Picarro_Chart_Timespan == '1h') {
                    $("#chartPicarro").dxChart("option", "dataSource", Picarro_Data.Data_Charts_1Hour.data);
                    $("#radarChart").dxPolarChart("option", "dataSource", Picarro_Data.Data_Charts_1Hour.data);
                    $("#chartWeather").dxChart("option", "dataSource", Picarro_Data.Data_Charts_1Hour.data);
                }                
            } else if (Picarro_Data.Data_Type == 'update_chart_1day') {
                Picarro_Chart_1Day_Data = Picarro_Data.Data_Charts_1Day.data;
                if (Picarro_Chart_Timespan == '1d') {                    
                    $("#chartPicarro").dxChart("option", "dataSource", Picarro_Data.Data_Charts_1Day.data);
                    $("#radarChart").dxPolarChart("option", "dataSource", Picarro_Data.Data_Charts_1Day.data);
                    $("#chartWeather").dxChart("option", "dataSource", Picarro_Data.Data_Charts_1Day.data);
                }                
            } else {
                setValues(Picarro_Data);
            }

            picarroLoadPanel.hide();

        };
        picarroSocket.onclose = function (e) {
            console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
            picarroLoadPanel.show();
            setTimeout(function () {
                picarroConnect();
            }, 1000);
        };
        picarroSocket.onerror = function (err) {
            console.error(err);
            picarroLoadPanel.show();
        };
    }
    picarroConnect();

    setInterval(function () {
        if (picarroSocket.readyState === WebSocket.CLOSED) {
            console.log('Picarro WebSocket Closed !!!!!!');
            $('#picarro_websocket_status').removeClass('badge-outline-success');
            $('#picarro_websocket_status').removeClass('badge-outline-danger');
            $('#picarro_websocket_status').addClass('badge-outline-danger');
        } else {
            $('#picarro_websocket_status').removeClass('badge-outline-success');
            $('#picarro_websocket_status').removeClass('badge-outline-danger');
            $('#picarro_websocket_status').addClass('badge-outline-success');
            console.log('Picarro WebSocket OK');
        }
        var endDate = new Date();
        var startDate   = new Date(Picarro_Data.HeartBeat);
        var timeDiff = (endDate.getTime() - startDate.getTime()) / 1000;
        if (timeDiff > 70) {
            $('#picarro_node_status').removeClass('badge-outline-success');
            $('#picarro_data_status').removeClass('badge-outline-success');
            $('#picarro_instrument_status').removeClass('badge-outline-success');
            $('#dashboard_bgtask_status').removeClass('badge-outline-success');

            $('#picarro_node_status').removeClass('badge-outline-danger');
            $('#picarro_data_status').removeClass('badge-outline-danger');
            $('#picarro_instrument_status').removeClass('badge-outline-danger');
            $('#dashboard_bgtask_status').removeClass('badge-outline-danger');

            $('#picarro_node_status').addClass('badge-outline-danger');
            $('#picarro_data_status').addClass('badge-outline-danger');
            $('#picarro_instrument_status').addClass('badge-outline-danger');
            $('#dashboard_bgtask_status').addClass('badge-outline-danger'); 
        } else {
            $('#dashboard_bgtask_status').removeClass('badge-outline-danger');
            $('#dashboard_bgtask_status').removeClass('badge-outline-success');
            $('#dashboard_bgtask_status').addClass('badge-outline-success');            
        }
        console.log(timeDiff);
    }, 10000);

    $("#picarro_chart_switch_1H").click(function () {
        Picarro_Chart_Timespan = '1h';
        $("#chartPicarro").dxChart("option", "dataSource", Picarro_Chart_1Hour_Data);
        $("#radarChart").dxPolarChart("option", "dataSource", Picarro_Chart_1Hour_Data);
        $("#chartWeather").dxChart("option", "dataSource", Picarro_Chart_1Hour_Data);
    });

    $("#picarro_chart_switch_12H").click(function () {
        Picarro_Chart_Timespan = '12h';
        $("#chartPicarro").dxChart("option", "dataSource", Picarro_Chart_12Hours_Data);
        $("#radarChart").dxPolarChart("option", "dataSource", Picarro_Chart_12Hours_Data);
        $("#chartWeather").dxChart("option", "dataSource", Picarro_Chart_12Hours_Data);
    });

    $("#picarro_chart_switch_1D").click(function () {
        Picarro_Chart_Timespan = '1d';
        $("#chartPicarro").dxChart("option", "dataSource", Picarro_Chart_1Day_Data);
        $("#radarChart").dxPolarChart("option", "dataSource", Picarro_Chart_1Day_Data);
        $("#chartWeather").dxChart("option", "dataSource", Picarro_Chart_1Day_Data);
    });

    $("#picarro_chart_switch_1W").click(function () {
        Picarro_Chart_Timespan = '1w';
        $("#chartPicarro").dxChart("option", "dataSource", Picarro_Chart_1Week_Data);
        $("#radarChart").dxPolarChart("option", "dataSource", Picarro_Chart_1Week_Data);
        $("#chartWeather").dxChart("option", "dataSource", Picarro_Chart_1Week_Data);
    });

    function setValues(dataArray) {
        var thisDateTime = new Date(dataArray.Data.Data_DateTime);
        thisDateTime = thisDateTime.toLocaleString();

        $('#picarro_node_status').removeClass('badge-outline-success');
        $('#picarro_node_status').removeClass('badge-outline-danger');
        if (dataArray.Data.Data_NodeStatus == 1) {
            $('#picarro_node_status').addClass('badge-outline-danger');
        } else if (dataArray.Data.Data_NodeStatus == 0) {
            $('#picarro_node_status').addClass('badge-outline-success');
        }

        $('#picarro_data_status').removeClass('badge-outline-success');
        $('#picarro_data_status').removeClass('badge-outline-danger');
        if (dataArray.Data.Data_DataStatus == 1) {
            $('#picarro_data_status').addClass('badge-outline-danger');
        } else if (dataArray.Data.Data_DataStatus == 0) {
            $('#picarro_data_status').addClass('badge-outline-success');
        }

        $('#picarro_instrument_status').removeClass('badge-outline-success');
        $('#picarro_instrument_status').removeClass('badge-outline-danger');
        if (dataArray.Data.Data_InstrumentStatus == 1) {
            $('#picarro_instrument_status').addClass('badge-outline-danger');
        } else if (dataArray.Data.Data_InstrumentStatus == 0) {
            $('#picarro_instrument_status').addClass('badge-outline-success');
        }

        setTextValues(dataArray);
    }

    function setTextValues(dataArray) {
        var thisDateTime = new Date(dataArray.Data.Data_DateTime);
        var thisTime = new Date(dataArray.Data.Data_DateTime).toLocaleTimeString();
        var thisDate = new Date(dataArray.Data.Data_DateTime).toLocaleDateString();
        thisDateTime = thisDateTime.toLocaleString();

        $("#Time").text(thisTime);
        $("#Date").text(thisDate);

        $("#CO2_Value").text(dataArray.Data.Data_CO2.toFixed(3));
        $("#CO2_Time").text(thisTime);
        $("#CO2_Date").text(thisDate);

        $("#CO_Value").text(dataArray.Data.Data_CO.toFixed(3));
        $("#CO_Time").text(thisTime);
        $("#CO_Date").text(thisDate);

        $("#H2O_Value").text(dataArray.Data.Data_H2O.toFixed(3));
        $("#H2O_Time").text(thisTime);
        $("#H2O_Date").text(thisDate);

        $("#CH4_Value").text(dataArray.Data.Data_CH4.toFixed(3));
        $("#CH4_Time").text(thisTime);
        $("#CH4_Date").text(thisDate);

        $("#Wind_Value").text(dataArray.Data.Data_WindSpeed.toFixed(3));
        $("#Gust_Value").text(dataArray.Data.Data_MaxGust.toFixed(3));
        $("#Dir_Value").text(dataArray.Data.Data_WindDir.toFixed(3));
        $("#Temp_Value").text(dataArray.Data.Data_GrassA.toFixed(3));
        $("#Hum_Value").text(dataArray.Data.Data_HumA.toFixed(3));
        $("#Pres_Value").text(dataArray.Data.Data_Pressure.toFixed(3));

        $("#CH4_Dry_List_Value").text(dataArray.Data.Data_CH4_Dry.toFixed(3));
        $("#CO2_Dry_List_Value").text(dataArray.Data.Data_CO2_Dry.toFixed(3));
        $("#DateTime_List_Value").text(thisDateTime);        
        $("#OutletValve_List_Value").text(dataArray.Data.Data_OutletValve.toFixed(3));
        $("#Instrument_Humidity_List_Value").text(dataArray.Data.Instrument_Humidity.toFixed(3));
        $("#Instrument_Pressure_List_Value").text(dataArray.Data.Instrument_Pressure.toFixed(3));
        $("#Instrument_Status_List_Value").text(dataArray.Data.Instrument_Status);
        $("#Instrument_Supply_Current_List_Value").text(dataArray.Data.Instrument_Supply_Current.toFixed(3));
        $("#Instrument_Supply_Voltage_List_Value").text(dataArray.Data.Instrument_Supply_Voltage.toFixed(3));
        $("#Instrument_Temp_List_Value").text(dataArray.Data.Instrument_Temp.toFixed(3));
        $("#id_List_Value").text(dataArray.Data.id);

        if (dataArray.Data.Data_MPVPosition > 1) {
            document.getElementById("MPVPosition_List_Value").checked = true;
        } else {
            document.getElementById("MPVPosition_List_Value").checked = false;
        }
        if (dataArray.Data.Data_Solenoid_Valves > 1) {
            document.getElementById("Solenoid_Valves_List_Value").checked = true;
        } else {
            document.getElementById("Solenoid_Valves_List_Value").checked = false;
        }
    }

});