import React, {useEffect} from "react";

export default function ListenBtn({name}){
    useEffect(function onFirstMount() {
        var gumStream; // stream from getUserMedia
        var rec; // Recorder.js object
        var AudioContext = window.AudioContext || window.webkitAudioContext;
        var audioContext;
        var recording = 0;
        var input;

        URL = window.URL;

        const record = () => {
            recording = 1;
    
            var constraints = {
                audio : true, 
                video : false
            }
    
            navigator.mediaDevices.getUserMedia(constraints).then(function(stream){
                gumStream = stream;

                audioContext = new AudioContext();
                input = audioContext.createMediaStreamSource(stream);
                
                rec = new Recorder(input, {
                    numChannels : 1
                })
    
                rec.record();
                console.log("Recording started");
            }).catch(function(err){
                console.log(err)
            });
        }
    
        const stopRecord = () => {
            recording = 0;
            console.log("stopping recording");
            rec.stop(); 

            // stop microphone access
            gumStream.getAudioTracks()[0].stop(); 
            
            
            // create the wav blob and pass it on to callback function
            rec.exportWAV(generateAudioControl);
        }

        const recorder = (e) => {
            if (!recording) {
                record()
            } else {
                stopRecord()
            }
        }
    
        function generateAudioControl(blob) {
            var url = URL.createObjectURL(blob);
            var au = document.createElement("audio");
            var playback_div = document.getElementById("playback");
            console.log(blob);
    
            au.controls = true;
            au.src = url;
    
            playback_div.appendChild(au);
        }

        document.getElementById("listen_btn").addEventListener("click", recorder);
    }, []);
    
    return (
        <div>
            <a id="listen_btn" href="#">{name}</a>
            <div id="playback"></div>
        </div>
    )
}

