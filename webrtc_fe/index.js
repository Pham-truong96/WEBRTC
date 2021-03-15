function openStream(){
    const config = {
        audio: false,
        video: true
    };
    return navigator.mediaDevices.getUserMedia(config);
}

function playStream(idVideoTag, stream){
    const video = document.getElementById(idVideoTag);
    video.srcObject = stream;
    video.play();
}

// openStream().then(stream=>playStream("localStream", stream));

const peer = new Peer({host:'peerjs-server.herokuapp.com', secure:true, port:443}); 
peer.on("open", id=>console.log(id))

