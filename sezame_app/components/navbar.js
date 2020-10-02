import styles from './navbar.module.css'
import Link from 'next/link'

export default function Navbar({children}) {
    return (
        <div className={styles.nav}>
            <Link href="/findings"><a>Your findings</a></Link>
            <p>Search</p>
        </div>
    )
}