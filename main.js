var received = $('#received');


var socket = new WebSocket("ws://"+window.location.hostname+":8080/ws");

var m2;


socket.onopen = function(){
  console.log("connected"); 
}; 

socket.onmessage = function (message) {
  console.log("receiving: " + message.data);
  received.append(message.data);
  received.append($('<br/>'));
};

socket.onclose = function(){
  console.log("disconnected"); 
};

var sendMessage = function(message) {
  console.log("sending:" + message.data);
  socket.send(message.data);
};

//$(window).on("gamepadconnected", function() {
  //sendMessage({'data' : 'gamepad connected'})
//});
window.addEventListener("gamepadconnected", function(e) {
  socket.send("Gamepad connected at index "+e.gamepad.index+": "+e.gamepad.id+". "+e.gamepad.buttons.length+" buttons, "+e.gamepad.axes.length+" axes.",);
});

window.addEventListener("gamepaddisconnected", function(e) {
  socket.send("Gamepad disconnected from index %d: %s",
    e.gamepad.index, e.gamepad.id);
});

//var interval;

if (!('ongamepadconnected' in window)) {
  // No gamepad events available, poll instead.
  setInterval(pollGamepads, 100);
}

function buttonPressed(b) {
  if (typeof(b) == "object") {
    return b.pressed;
  }
  return b == 1.0;
}


function pollGamepads() {
  var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads : []);
  for (var i = 1; i < gamepads.length; i++) {
    var gp = gamepads[i];
    if (gp) {
		if(gp.buttons.length > 3)
		{
		  //message = "Gamepad connected at index " + gp.index + ": " + gp.id + ". It has " + gp.buttons.length + " buttons and " + gp.axes.length + " axes.";
		  //message = "Button 2 = " + buttonPressed(gp.buttons[7]);
		  message = "{\"Axis0\" : \""+gp.axes[0]+"\",\"Button6\" : \""+buttonPressed(gp.buttons[6])+"\",\"Button7\" : \""+buttonPressed(gp.buttons[7])+"\"}";
		  if(message != m2)
		  {
			socket.send(message);
			m2 = message;
		  }
		  //clearInterval(interval);
		}
    }
  }
}

// GUI Stuff


// send a command to the serial port
$("#cmd_send").click(function(ev){
  ev.preventDefault();
  var cmd = $('#cmd_value').val();
  sendMessage({ 'data' : cmd});
  $('#cmd_value').val("");
});

$('#clear').click(function(){
  received.empty();
});

