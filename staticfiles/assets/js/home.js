
// SET UNIVERSAL VARIABLES


function setHistory(db_Data) {
    console.log(db_Data);
}
function setCurrent(db_Data) {
    console.log(db_Data);
}
function setStatus(db_Data) {
    console.log(db_Data);
}
function setSetup(db_Data) {
    console.log(db_Data);
}

var startWebSocket = function () {
    var autosondeSocket;
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + '/home/';
    autosondeSocket = new WebSocket(ws_path);    

    autosondeSocket.onmessage = function (e) {
        ws_Data = JSON.parse(e.data).message;
        console.log(ws_Data);
    };

    autosondeSocket.onclose = function (e) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
    };

    autosondeSocket.onerror = function (err) {
        console.error(err);
    };
};

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
    initialSetup();
});