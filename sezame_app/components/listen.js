import { useRouter } from 'next/router';
import { ResultContext } from '../contexts/resultContext';
import React, {useContext, useEffect, useState} from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlayCircle } from '@fortawesome/free-solid-svg-icons';
import { motion } from "framer-motion";

export default function ListenBtn(){
    const { result, storeResult } = useContext(ResultContext);

    const router = useRouter();
    let limit = 5;
    let count = 0;
    let recording = false;
    let queue = new Array();
    let currentPathResult;

    useEffect(
        function onFirstMount() {
            URL = window.URL;

            const record = () => {
                let gumStream;
                let AudioContext = window.AudioContext || window.webkitAudioContext;
                let audioContext;
                let input;

                var constraints = {
                    audio : true, 
                    video : false
                }
        
                navigator.mediaDevices.getUserMedia(constraints).then(function(stream){
                    gumStream = stream;

                    audioContext = new AudioContext();
                    input = audioContext.createMediaStreamSource(stream);
                    
                    let rec = new Recorder(input, {
                        numChannels : 1
                    })
        
                    rec.record();
                    console.log("Recording started - timeout begin");

                    setTimeout(function(){ 
                        // stop recording + send data to Flask
                        stopRecord(rec, gumStream);
                    }, 10000);

                }).catch(function(err){
                    console.log(err)
                });
            }
        
            const stopRecord = (rec, gumStream) => {
                console.log("stopping recording");
                rec.stop(); 
                // stop microphone access
                gumStream.getAudioTracks()[0].stop(); 
                
                // create the wav blob and pass it on to callback function
                rec.exportWAV(sendBlob);
            }

            function sendBlob(blob) {
                // only send request if we still don't have any good news from Flask
                // or if we are still on the index page
                let nb_request = Math.random();
                queue.push(nb_request);

                let confidence_thres = 0.4;

                if (result.confidence >= confidence_thres || router.pathname == "/results" ) {
                    return true
                }
                
                var xhr = new XMLHttpRequest()
                let data = new FormData();
                
                data.append('audio', blob, 'sample.wav');
                data.append('confidence_thres', confidence_thres);

                xhr.open('POST', '/api/reco');

                // send the request with the song
                xhr.send(data);

                // get a callback when the server responds
                xhr.addEventListener('load', () => {
                    let result_api = JSON.parse(xhr.responseText)
                    result_api = result_api.data;

                    if (!currentPathResult && (result_api.confidence >= confidence_thres || queue.indexOf(nb_request) + 1 == limit)) {
                        console.log(result_api);
                        recording = false;

                        storeResult({
                            confidence : result_api.confidence,
                            song_name : result_api.matched_song["name"],
                            artists : result_api.matched_song["artists"],
                            sezame_nb : 10,
                            album_cover : result_api.matched_song["cover"],
                            spotify_preview : result_api.matched_song["preview"],
                            recommendations : result_api.similar_songs
                        })

                        router.push({
                            pathname: '/results'
                        })

                        currentPathResult = true;
                        console.log("we changed route");
                    }
                })
            }

            const recorder = (e) => {
                e.preventDefault();
                recording = true;
                currentPathResult = false;
                console.log(currentPathResult);

                // we will send 3 seconds each time to the Flask APi to analyze the song when 
                // it finds a match with a good confidence value, we display the result

                count = count + 1;
                console.log("new recording " + count);
                record();

                let recording = setInterval(function(){ 
                    count = count + 1;
                    console.log("new recording " + count);
                    record();

                    if (count == limit) {
                        clearInterval(recording);
                    }
                }, 3000);

            }

            document.getElementById("listen_btn").addEventListener("click", recorder);
        }, 
    []);

    const variants = {
        stopListening : {
            opacity : 1
        },
        listening : {
            color : ["#884467", "#C185A4"],
            scale : [1.1, 1.3, 1.5]
        }
    }

    const btnTransitionRecording = {
        color : {
            duration: 1,
            yoyo: Infinity,
            ease: "easeOut"
        },
        scale : {
            duration: 1,
            yoyo: Infinity,
        }
    }
    
    return (
        <motion.div id="listen_btn" className="listen_btn mt-3"
            initial = {{
                opacity: 0,
                color : "#884467"
            }}
            animate={recording ? "listening" : "stopListening"}
            transition ={ btnTransitionRecording }
            variants={variants}
            whileHover={{
                color: "#C185A4",
                scale : 1.1,
                transition: { duration: 0.5 },
            }}>
            <FontAwesomeIcon icon={faPlayCircle} className="play_icon"/>
        </motion.div>
    )
}

