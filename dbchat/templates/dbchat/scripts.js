let ws =  new WebSocket("ws://localhost:8000/public_chat/");

ws.onmessage = (event) => {
    console.log(event);
    console.log(event.data);
}