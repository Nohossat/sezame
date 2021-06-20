import styles from "./resultInfo.module.css"
import React, {useEffect, useState} from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlayCircle, faPause } from '@fortawesome/free-solid-svg-icons'
import { motion } from "framer-motion";

export default function ResultInfo({artists, song, sezame_nb, album_cover, spotify_link}) {
    const [isPlaying, setIsPlaying] = useState(false);
    const [audio, setAudio] = useState(0);

    useEffect(() => {
        if (isPlaying) {
            audio.play();
        } else {
            console.log(typeof(audio))
            if (typeof(audio) == Object) {
                audio.pause();
            }
        }
    }, [audio, isPlaying]);

    function audioControl(url){
        if (!isPlaying) {
            setAudio(new Audio(url));
            setIsPlaying(!isPlaying);
        } else {
            setIsPlaying(!isPlaying);
            if (audio instanceof Audio) {
                audio.pause();
            }
        }
    }

    let artist = artists;

    if (Array.isArray(artists)) {
        const nbArtists = artists.length;
        artist = artists.map((name, i) => {
            if (nbArtists == i + 1) {
            return <span key={i}>{name}</span>
            } else {
            return <span key={i}>{name}, </span>
            }
        })
    }

    let button;

    if (!isPlaying) {
       button = <FontAwesomeIcon icon={faPlayCircle} className={styles.play_icon}/>;
    } else {
        button = <FontAwesomeIcon icon={faPause} className={styles.pause_icon}/>;
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
                        <p>{sezame_nb} {sezame_nb == 1 ? 'Sezame' : 'Sezames'}</p>
                        <a href={spotify_link}>Add to Spotify</a>
                    </div>
                </div>
                <div className={styles.bloc_album}>
                    <img className={styles.album_cover} src={album_cover} alt="album_cover"/>
                    {spotify_link != 0 &&
                        <motion.span 
                        className={styles.btn_play} 
                        whileHover={{
                            scale : 1.1,
                            transition : { duration : 0.5 }
                        }}
                        onClick={() => audioControl(spotify_link)}>
                            {button}
                        </motion.span>
                    }
                    <div className={styles.result_overlay}></div> 
                </div>
            </div>
        </div>
    )
}