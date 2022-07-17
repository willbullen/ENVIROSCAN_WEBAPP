// SET UNIVERSAL VARIABLES


function setHistory(db_Data) {

}

function setCurrent(db_Data) {

}

function setSounding(db_Data) {
    // SET SOUNDING CHART DATA
    $("#chartSounding").dxChart("option", "dataSource", db_Data.Data.data);
    // REMAP TRACK DATA
    var SoundingData = db_Data.Data.data.map(function (h) {
        return {
            id: h.id,
            status: '0',
            datetime: h.Data_DateTime,
            air_temperature: h.Data_Air_Temperature,
            dewpoint_temperature: h.Data_Dewpoint_Temperature,
            direction: h.Data_Direction,
            evss: h.Data_EVSS,
            geopotential_height: h.Data_Geopotential_Height,
            pressure: h.Data_Pressure,
            speed: h.Data_Speed,
            coords: [h.Data_Lat, h.Data_Lng]
        };
    });
    //var mapObject = $('#networkStatusMap').vectorMap('get', 'mapObject');
    //mapObject.addMarkers(SoundingData.map(function (h) {
    //    return {
    //        name: h.datetime,
    //        latLng: h.coords,
    //        id: h.id
    //    };
    //}), []);
    //mapObject.series.markers[0].setValues(SoundingData.reduce(function (p, c, i) {
    //    p[i] = c.status;
    //    return p;
    //}, {}));
}

function setStatus(db_Data) {

}

function setSetup(db_Data) {

}

var startWebSocket = function () {

};
var renderTableData = function () {

};
var renderMaps = function () {

    $('#siteMap').dxVectorMap({
        // [minLongitude, maxLatitude, maxLongitude, minLatitude]
        bounds: [-12, 55, -5, 51],
        maxZoomFactor: 1000,
        background: {
            color: 'transparent',
            borderColor: 'transparent',
        },
        layers: [{
            dataSource: mapData
        }, {
            type: 'marker',
            elementType: 'image',
            dataField: 'url',
            size: 51,
            label: {
                dataField: 'text',
                font: {
                    size: 14,
                },
            },
            //dataSource: equipmentData,
        }, {
            name: 'water',
            dataSource: streamsData,
            //colorGroupingField: 'tag',
            //colorGroups: [0, 1, 2],
            //palette: ['#3c20c8', '#d82020'],
            //borderColor: 'none',
            hoverEnabled: false,
        }],
        legends: [{
            font: {
                size: 14,
            },
            horizontalAlignment: 'right',
            verticalAlignment: 'top',
            customizeText() {
                if (this.color === '#3c20c8') {
                    return 'Cold';
                }
                return 'Warm';
            },
            source: {
                layer: 'water',
                grouping: 'color'
            },
        }],
    });

};
var renderCharts = function () {
    //-- GENERATE CHART
    $('#chartSounding').dxChart({
        palette: 'Harmony Light',
        commonSeriesSettings: {
            argumentField: 'Data_DateTime',
        },
        argumentAxis: {
            argumentType: 'datetime',
        },
        series: [{
            valueField: 'Data_Geopotential_Height',
            axis: 'altitude',
            name: 'altitude',
            color: '#e91e63',
            type: 'line',
        }, {
            valueField: 'Data_Air_Temperature',
            axis: 'temperature',
            name: 'temperature',
            color: '#03a9f4',
            type: 'line',
        }, ],
        valueAxis: [{
            name: 'altitude',
            title: {
                text: 'Altitude, m',
                font: {
                    color: '#e91e63',
                },
            },
            label: {
                font: {
                    color: '#e91e63',
                },
            },
        }, {
            name: 'temperature',
            position: 'right',
            title: {
                text: 'Temperature, K',
                font: {
                    color: '#03a9f4',
                },
            },
            label: {
                font: {
                    color: '#03a9f4',
                },
            },
        }],
        legend: {
            verticalAlignment: 'bottom',
            horizontalAlignment: 'center',
        },
    });

    //  --RADAR
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
    //-- RADAR   

    //-- WEATHER CHART 
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
    //-- WEATHER CHART

};

function initialSetup() {
    setStatus(Status_Data);
    setSetup(Setup_Data);
    setHistory(Ground_Station_Data);
    //setSoundings(Soundings_Data);
    setSounding(Sounding_Data);
    //setLogs(Log_Data);
}

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







function getImageUrl(name) {
    return `images/VectorMap/${name}.png`;
}

var equipmentData = {
    type: 'FeatureCollection',
    features: [{
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-74.007118, 40.71455],
        },
        properties: {
            url: getImageUrl('Storm'),
            text: 'New York',
        },
    }, {
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-77.016251, 38.904758],
        },
        properties: {
            url: getImageUrl('Cloudy'),
            text: 'Washington',
        },
    }, {
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-81.674782, 30.332251],
        },
        properties: {
            url: getImageUrl('Storm'),
            text: 'Jacksonville',
        },
    }, {
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-84.423058, 33.763191],
        },
        properties: {
            url: getImageUrl('Rain'),
            text: 'Atlanta',
        },
    }, {
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-97.514839, 35.466179],
        },
        properties: {
            url: getImageUrl('PartlyCloudy'),
            text: 'Oklahoma City',
        },
    }, {
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-87.632408, 41.884151],
        },
        properties: {
            url: getImageUrl('Rain'),
            text: 'Chicago',
        },
    }, {
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-93.103882, 44.947769],
        },
        properties: {
            url: getImageUrl('PartlyCloudy'),
            text: 'St. Paul',
        },
    }, {
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-94.626823, 39.113522],
        },
        properties: {
            url: getImageUrl('Cloudy'),
            text: 'Kansas City',
        },
    }, {
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-95.381889, 29.775419],
        },
        properties: {
            url: getImageUrl('Sunny'),
            text: 'Houston',
        },
    }, {
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-104.991997, 39.740002],
        },
        properties: {
            url: getImageUrl('PartlyCloudy'),
            text: 'Denver',
        },
    }, {
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-116.193413, 43.606979],
        },
        properties: {
            url: getImageUrl('Sunny'),
            text: 'Boise',
        },
    }, {
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-118.245003, 34.053501],
        },
        properties: {
            url: getImageUrl('PartlyCloudy'),
            text: 'Los Angeles',
        },
    }, {
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-121.886002, 37.3386],
        },
        properties: {
            url: getImageUrl('PartlyCloudy'),
            text: 'San Jose',
        },
    }, {
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-123.0252, 44.923199],
        },
        properties: {
            url: getImageUrl('Sunny'),
            text: 'Salem',
        },
    }, {
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-122.329437, 47.603561],
        },
        properties: {
            url: getImageUrl('Sunny'),
            text: 'Seattle',
        },
    }],
};

var streamsData = {
    "type": "FeatureCollection",
    "features": [{
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10.24524450302124,
                            51.94160615230632
                        ],
                        [
                            -10.245587825775146,
                            51.94141434751819
                        ],
                        [
                            -10.245823860168455,
                            51.94027672984908
                        ],
                        [
                            -10.243957042694092,
                            51.93909278315192
                        ],
                        [
                            -10.243463516235352,
                            51.93931766928593
                        ],
                        [
                            -10.241800546646118,
                            51.93813369727791
                        ],
                        [
                            -10.241650342941284,
                            51.93821307068018
                        ],
                        [
                            -10.239826440811157,
                            51.93753177774059
                        ],
                        [
                            -10.239622592926025,
                            51.93782943126837
                        ],
                        [
                            -10.239665508270264,
                            51.937968335572215
                        ],
                        [
                            -10.23952603340149,
                            51.938021251384335
                        ],
                        [
                            -10.239408016204834,
                            51.938570249252535
                        ],
                        [
                            -10.23952603340149,
                            51.93876868056399
                        ],
                        [
                            -10.242862701416014,
                            51.94032302880576
                        ],
                        [
                            -10.243431329727173,
                            51.940554522872375
                        ],
                        [
                            -10.24524450302124,
                            51.94160615230632
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "stroke": "#555555",
                "stroke-width": 3,
                "stroke-opacity": 1,
                "fill": "#555555",
                "fill-opacity": 0.5
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10.244295671582222,
                            51.940319721739016
                        ],
                        [
                            -10.24427555501461,
                            51.94025523388867
                        ],
                        [
                            -10.244329199194908,
                            51.94024903312896
                        ],
                        [
                            -10.244311094284058,
                            51.940189919176525
                        ],
                        [
                            -10.244254097342491,
                            51.94019653332893
                        ],
                        [
                            -10.244193077087402,
                            51.940000588650854
                        ],
                        [
                            -10.244101211428642,
                            51.940010509920945
                        ],
                        [
                            -10.244092494249344,
                            51.93997950594462
                        ],
                        [
                            -10.243991911411285,
                            51.93999066737855
                        ],
                        [
                            -10.244003981351852,
                            51.94002415166373
                        ],
                        [
                            -10.243948996067047,
                            51.94003076584056
                        ],
                        [
                            -10.244048237800598,
                            51.94034865856479
                        ],
                        [
                            -10.244295671582222,
                            51.940319721739016
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10.239945128560066,
                            51.938479714675104
                        ],
                        [
                            -10.2403025329113,
                            51.93821555109674
                        ],
                        [
                            -10.240195915102959,
                            51.938160981900765
                        ],
                        [
                            -10.239977315068243,
                            51.93832220887899
                        ],
                        [
                            -10.23988679051399,
                            51.93827673466175
                        ],
                        [
                            -10.239749327301979,
                            51.93837967168756
                        ],
                        [
                            -10.239945128560066,
                            51.938479714675104
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10.241225212812424,
                            51.938799271979775
                        ],
                        [
                            -10.241302326321602,
                            51.93873643553561
                        ],
                        [
                            -10.241202414035797,
                            51.93869013494151
                        ],
                        [
                            -10.241125300526619,
                            51.938753798246076
                        ],
                        [
                            -10.241225212812424,
                            51.938799271979775
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10.242781564593315,
                            51.9392767434006
                        ],
                        [
                            -10.242853313684464,
                            51.93923251033103
                        ],
                        [
                            -10.242772176861761,
                            51.939185796855085
                        ],
                        [
                            -10.242698416113853,
                            51.93923251033103
                        ],
                        [
                            -10.242781564593315,
                            51.9392767434006
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10.242434889078138,
                            51.93967442567476
                        ],
                        [
                            -10.242375880479813,
                            51.93964590180366
                        ],
                        [
                            -10.242323577404022,
                            51.93967897295689
                        ],
                        [
                            -10.242379903793335,
                            51.93971204408578
                        ],
                        [
                            -10.242434889078138,
                            51.93967442567476
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10.242412090301512,
                            51.93955040871181
                        ],
                        [
                            -10.24234302341938,
                            51.93955040871181
                        ],
                        [
                            -10.24234302341938,
                            51.93963060638704
                        ],
                        [
                            -10.242412090301512,
                            51.93963060638704
                        ],
                        [
                            -10.242412090301512,
                            51.93955040871181
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10.241891741752625,
                            51.93968724074141
                        ],
                        [
                            -10.241958796977995,
                            51.939635980452934
                        ],
                        [
                            -10.24189978837967,
                            51.93960373604789
                        ],
                        [
                            -10.24183139204979,
                            51.93966326416216
                        ],
                        [
                            -10.241891741752625,
                            51.93968724074141
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10.241568535566328,
                            51.93944912793775
                        ],
                        [
                            -10.241537690162659,
                            51.93943631280311
                        ],
                        [
                            -10.241513550281525,
                            51.939453675242724
                        ],
                        [
                            -10.241544395685196,
                            51.93946897071965
                        ],
                        [
                            -10.241568535566328,
                            51.93944912793775
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10.241286903619766,
                            51.93936479601671
                        ],
                        [
                            -10.241429060697556,
                            51.93925979428564
                        ],
                        [
                            -10.241257399320602,
                            51.93917050128157
                        ],
                        [
                            -10.241115242242811,
                            51.939274676435694
                        ],
                        [
                            -10.241286903619766,
                            51.93936479601671
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10.243156403303146,
                            51.93961696452456
                        ],
                        [
                            -10.243109464645384,
                            51.93959464146793
                        ],
                        [
                            -10.243051797151564,
                            51.93962936621788
                        ],
                        [
                            -10.243102759122849,
                            51.93965747671005
                        ],
                        [
                            -10.243156403303146,
                            51.93961696452456
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10.244101211428642,
                            51.93933957908798
                        ],
                        [
                            -10.244072377681732,
                            51.93927550322167
                        ],
                        [
                            -10.243936255574226,
                            51.939297826437105
                        ],
                        [
                            -10.243964418768883,
                            51.93936479601671
                        ],
                        [
                            -10.244101211428642,
                            51.93933957908798
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10.245322957634924,
                            51.940108068959994
                        ],
                        [
                            -10.245276018977165,
                            51.94007747843669
                        ],
                        [
                            -10.245190188288689,
                            51.94012295082865
                        ],
                        [
                            -10.245245173573494,
                            51.94015767516966
                        ],
                        [
                            -10.245322957634924,
                            51.940108068959994
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10.244303047657011,
                            51.940865384454064
                        ],
                        [
                            -10.244274884462357,
                            51.940808338208164
                        ],
                        [
                            -10.244123339653015,
                            51.94082983390355
                        ],
                        [
                            -10.244154185056686,
                            51.94089101390323
                        ],
                        [
                            -10.244303047657011,
                            51.940865384454064
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10.241183638572693,
                            51.938403235551824
                        ],
                        [
                            -10.2411487698555,
                            51.93813865811968
                        ],
                        [
                            -10.240800082683563,
                            51.938163462320205
                        ],
                        [
                            -10.240851044654844,
                            51.938429693209216
                        ],
                        [
                            -10.241183638572693,
                            51.938403235551824
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10.242359787225723,
                            51.93915644588511
                        ],
                        [
                            -10.242327600717545,
                            51.93913412259935
                        ],
                        [
                            -10.242280662059784,
                            51.93916057982572
                        ],
                        [
                            -10.242312848567963,
                            51.93918455667364
                        ],
                        [
                            -10.242359787225723,
                            51.93915644588511
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10.242048650979996,
                            51.938762892996515
                        ],
                        [
                            -10.242008417844772,
                            51.93873891592323
                        ],
                        [
                            -10.241966843605042,
                            51.93875875901927
                        ],
                        [
                            -10.242012441158295,
                            51.93878935044181
                        ],
                        [
                            -10.242048650979996,
                            51.938762892996515
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -10.242414772510527,
                            51.93885880116146
                        ],
                        [
                            -10.24238795042038,
                            51.938836477727584
                        ],
                        [
                            -10.242350399494171,
                            51.93884887963667
                        ],
                        [
                            -10.242381244897842,
                            51.93887533703125
                        ],
                        [
                            -10.242414772510527,
                            51.93885880116146
                        ]
                    ]
                ]
            }
        }
    ]
};