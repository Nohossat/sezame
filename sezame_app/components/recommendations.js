import styles from './recommendations.module.css'
import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSearch } from '@fortawesome/free-solid-svg-icons'

export default function Recommendations({children}) {
    const reco = []

    for (const song of children) {
        reco.push(
            <div>
                <p>{song[0]}</p>
                <p>{song[1]}</p>
                <p>{song[2]}</p>
            </div>
        )
    }
    
    return (
        <div className={styles.recommendations_container}>
            <h3>Our Recommendations</h3>

            <div>
                {reco}
            </div>
            {children}
        </div>
    )
}