import styles from './recommendItem.module.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlayCircle, faPause } from '@fortawesome/free-solid-svg-icons'
import React, {useState, useEffect} from "react";
import { motion } from "framer-motion";

export default function RecommendItem({children, theme="black", sezame_find=null}) {
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

    let button;

    if (!isPlaying) {
       button = <FontAwesomeIcon icon={faPlayCircle} className={styles.play_icon}/>;
    } else {
        button = <FontAwesomeIcon icon={faPause} className={styles.pause_icon}/>;
    }

    const nbArtists = children.artists.length;

    const artists = children.artists.map((name, i) => {
        if (nbArtists == i + 1) {
           return <span key={i}>{name}</span>
        } else {
           return <span key={i}>{name}, </span>
        }
    })

    let sezame_count;
    
    if (sezame_find) {
    sezame_count = <p>{children.sezame_nb} {children.sezame_nb == 1 ? 'Sezame' : 'Sezames'}</p>
    }

    return (
    <div className={styles.song_recommended}>
        <div className={styles.image_container}>
            <img className={styles.image} src={children.image} alt="cover"/>
            {children.preview != 0 &&
                <motion.span 
                className={styles.btn_play} 
                onClick={() => audioControl(children.preview)}
                whileHover={{
                    scale : 1.1,
                    transition : { duration : 0.5 }
                }}
                >
                    {button}
                </motion.span>
            }
        </div>
        <div className={theme == "black" ? styles.recommendInfo : styles.recommendInfo_white}>
            <h3 className={styles.title}>{children.name}</h3>
            <h4 className={styles.artist}>{artists}</h4>
            {children.genre && <h5 className={styles.genre}>{children.genre}</h5>}
                {sezame_count}
        </div>
    </div>
    )
}