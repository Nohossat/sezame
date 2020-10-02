import styles from "./resultInfo.module.css"

export default function ResultInfo({artist, song, sezame_nb, spotify_link}) {
    return (
        <div className={styles.bloc_result}>
            <div class={styles.bloc_result_container}>
                <div>
                    <h3>{artist}</h3>
                    <h2>{song}</h2>
                    <div className={styles.meta}>
                        <p>{sezame_nb} Sezames </p>
                        <a href={spotify_link}>Add to Spotify</a>
                    </div>
                </div>
                <div>
                    <button className={styles.btn_margin}>Play</button>
                </div>
            </div>
        </div>
    )
}