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
    console.log(stream.getVideoTracks()[0].getSettings().frameRate);
    console.log(stream.getVideoTracks()[0].getSettings());
}

// openStream().then(stream=>playStream("localStream", stream));

const peer = new Peer({host:'peerjs-server.herokuapp.com', secure:true, port:443}); 
peer.on("open", id=>$("#my-peer").append(id))

//caller
$("#call-button").click(() =>{
    const id=$("#remote-id").val();
    openStream()
    .then(stream =>{
        playStream("localStream",stream);
        const call= peer.call(id, stream);
        console.log("my video fps:");
        call.on('stream', remoStream =>playStream('remoteStream', remoStream));

    })
});

peer.on("call", call=>{
    openStream().then(stream =>{
        call.answer(stream);
        playStream("localStream",stream);
        call.on('stream', remoStream =>playStream('remoteStream', remoStream));
    })
})
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
$('#btn').bind('click', function() {
    console.log ( "daaaaaaaa" ) ; 
    var  video  =  VideoFrame ( { 
        id : 'remoteStream' , 
        frameRate: FrameRates.film , 
        callback: function ( response )  { 
            console.log ( 'callback response:'  +  response ); 
        } 
    } ) ;
    sleep(2000);
    var a =video.get();
    setTimeout(function(){ console.log("Hello"); 
        var b =video.get();
        framera = (b- a)/2
        console.log(a )
        console.log(b)
        console.log(b-a)
        console.log("fps = " + framera )
    }, 2000);

   
    
});