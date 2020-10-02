import styles from './layout.module.css'
import Navbar from '../components/navbar'

export default function Layout({children}) {
    return (
        <div className={styles.container}>
            <Navbar></Navbar>
            {children}
        </div>
    )
}