(function() {
    var $msg = $('#msg');
    var $text = $('#text');

    var WebSocket = window.WebSocket || window.MozWebSocket;
    if (WebSocket) {
        try {
            url = 'ws://' + window.location.hostname + ':' + window.location.port + '/chat'
            /*'ws://localhost:8080/test/chat'*/
            var socket = new WebSocket(url);
        } catch (e) {}
    }

    if (socket) {
        socket.onmessage = function(event) {
            $msg.append('<p> server:   ' + event.data + '</p>');
        }

        $('form').submit(function() {
            socket.send($text.val());
            $text.val('').select();
            return false;
        });
    }
})();