import styles from './recommendations.module.css';
import React from 'react';
import RecommendItem from './recommendItem';

export default function Recommendations({children}) {

    const items = children.map((value, index) =>
        <RecommendItem key={index}>
            {value}
        </RecommendItem>
    )

    return (
        <div className={styles.recommendations_container}>
            <h3 className={styles.reco_title}>Our Recommendations</h3>

            <div className={styles.recommendations}>
            {items}
            </div>
        </div>
    )
}