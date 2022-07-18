// SET UNIVERSAL VARIABLES

function setHistory(db_Data) {    
    $("#Main_Chart").dxChart("option", "dataSource", db_Data);
    $("#Main_Chart_Range_Selector").dxRangeSelector("option", "dataSource", db_Data);
}

function reviver(key, value) {
    if (key === 'Data_DateTime') {
        return new Date(value);
    }
    return value;
}

var startWebSocket = function () {
    var autosondeSocket;
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + '/daqc/';
    autosondeSocket = new WebSocket(ws_path);

    autosondeSocket.onmessage = function (e) {
        ws_Data = JSON.parse(e.data).message.Data.data;
        console.log(ws_Data);
        //setHistory(ws_Data);
    };

    autosondeSocket.onclose = function (e) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
    };

    autosondeSocket.onerror = function (err) {
        console.error(err);
    };
};

function renderForms() {
    $('#range-selector').dxRangeSelector({
        scale: {
            startValue: new Date(2021, 1, 1),
            endValue: new Date(),
            minorTickInterval: 'day',
            tickInterval: 'week',
            minRange: 'day',
            maxRange: 'year',
            minorTick: {
                visible: false,
            },
        },
        sliderMarker: {
            format: 'monthAndDay',
        },
        //value: [new Date(2022, 1, 2), new Date(2022, 2, 2)],
    });
}

function renderDataGrids() {
    var changeLogData = [{
        id: 1,
        asset: 'PICARRiO',
        field: 'CO2',
        date_altered: new Date().getDate(),
        origional_value: 470.87,
        altered_value: 410.98,
    }, {
        id: 2,
        asset: 'PICARRO',
        field: 'CO',
        date_altered: new Date().getDate(),
        origional_value: 9.9,
        altered_value: 1.2,
    }];

    var changeLogsTable = $('#changeLogsTable').DataTable({
        searching: true,
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
                title: "ASSET",
                //width: "95%"
            },
            {
                title: "FIELD",
                //width: "95%"
            },
            {
                title: "DATE ALTERED",
                //width: "5%"
            },
            {
                title: "ORIGIONAL VALUE",
                //width: "5%"
            },
            {
                title: "ALTERED VALUE",
                //width: "5%"
            },
            {
                title: "VIEW",
                //width: "5%"
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
            } else {
                $(row).addClass('text-theme');
            }
        }
    });

    var tableObject = $('#changeLogsTable').DataTable();
    tableObject.clear();
    tableObject.rows.add(changeLogData.map(function (h) {
        return [h.asset, h.field, h.date_altered, h.origional_value, h.altered_value, h.id];
    }));
    tableObject.draw();
}

function initialSetup() {
    setHistory(History_Data);
}

/* Controller
------------------------------------------------ */
$(document).ready(function () {
    startWebSocket();
    renderCharts();
    renderForms();
    renderDataGrids();
    initialSetup();
});