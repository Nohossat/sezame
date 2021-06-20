import styles from './navbar.module.css'
import Link from 'next/link'
import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSearch } from '@fortawesome/free-solid-svg-icons'

export default function Navbar({children}) {
    return (
        <div className={styles.nav}>
            <Link href="/findings"><a>Your previous Sezames</a></Link>
            <div className={styles.search_icon}><FontAwesomeIcon icon={faSearch}/></div>
        </div>
    )
}