import styles from "./resultInfo.module.css"
import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlayCircle, faTimes } from '@fortawesome/free-solid-svg-icons'

export default function ResultInfo({artist, song, sezame_nb, album_cover, spotify_link}) {
    let audio = "";
    let playing = 0;

    function playPreview(url){
        audio = new Audio(url);
        playing = 1;
        audio.play();
    }

    function stopPreview(){
        playing = 0;
        audio.pause();
    }

    function audioControl(url){
        if (!playing) {
            playPreview(url);
        } else {
            stopPreview();
        }
    }

    return (
        <div className={styles.bloc_result}>
            <div className={styles.bloc_result_container}>
                <div className={styles.bloc_info_artist}>
                    <h3>
                        {artist}
                    </h3>
                    <h1>{song}</h1>
                    <div className={styles.meta}>
                        <p>{sezame_nb} Sezames </p>
                        <a href={spotify_link}>Add to Spotify</a>
                    </div>
                </div>
                <div className={styles.bloc_album}>
                    <img className={styles.album_cover} src={album_cover} alt="album_cover"/>
                    {spotify_link != 0 &&
                        <span className={styles.btn_play} onClick={() => audioControl(spotify_link)}>
                            <FontAwesomeIcon icon={faPlayCircle} className={styles.play_icon}/>
                        </span>
                    }
                    <div className={styles.result_overlay}></div> 
                </div>
            </div>
        </div>
    )
}