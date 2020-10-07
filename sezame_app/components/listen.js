import React, {useEffect} from "react";
import { useRouter } from 'next/router';

export default function ListenBtn({name}){
    
    const router = useRouter()

    useEffect(
        function onFirstMount() {
            var gumStream; // stream from getUserMedia
            var rec;
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
                e.preventDefault();

                if (!recording) {
                    record()
                } else {
                    stopRecord()
                }
            }
        
            function generateAudioControl(blob) {
                
                /*
                keep it so you know how to play the song in the result page
                var url = URL.createObjectURL(blob);
                var au = document.createElement("audio");
                var playback_div = document.getElementById("playback");
                au.controls = true;
                au.src = url;
                playback_div.appendChild(au);
                */

                // we need to send this blob to flask service
                var xhr = new XMLHttpRequest()

                let data = new FormData();
                data.append('audio', blob, 'sample.wav');
                xhr.open('POST', '/api/reco');

                // send the request with the song
                xhr.send(data);

                // get a callback when the server responds
                xhr.addEventListener('load', () => {
                    var result = JSON.parse(xhr.responseText)
                    console.log(xhr.responseText)

                    router.push({
                        pathname: '/results',
                        query: { 
                                song: result.data.song.name,
                                artists: result.data.song.artists
                        }
                    })
                })
            }

            document.getElementById("listen_btn").addEventListener("click", recorder);
        }, 
    []);
    
    return (
        <div>
            <a id="listen_btn" href="#">{name}</a>
            <div id="playback"></div>
        </div>
    )
}

