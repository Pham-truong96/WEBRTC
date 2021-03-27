
javascript:(
    function(){
        var script=document.createElement('script');
        script.onload=function(){
            var stats=new Stats();
            document.body.appendChild(stats.dom);
            requestAnimationFrame(
                function loop(){
                    stats.update();
                    requestAnimationFrame(loop)
                }
            );
        };
    
        script.src='//mrdoob.github.io/stats.js/build/stats.min.js';
        document.head.appendChild(script);
    }
)()
    
function openStream(){
    const config = {
        audio: true,
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
    var stats = new Stats();
    stats.showPanel( 1 ); // 0: fps, 1: ms, 2: mb, 3+: custom
    document.body.appendChild( stats.dom );

    function animate() {

        stats.begin();

        // monitored code goes here
        console.log(sta)
        stats.end();

        requestAnimationFrame(animate);

    }

    requestAnimationFrame(animate);
        
});