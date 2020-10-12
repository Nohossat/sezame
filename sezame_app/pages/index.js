import Head from 'next/head'
import Layout from '../components/layout'
import ListenBtn from '../components/listen'
import Link from 'next/link'
import { motion } from "framer-motion"

export default function Home() {
  const indexVariants = {
    initial: { 
      opacity : 0,
      backgroundColor: "#efefef"
    },
    enter: { opacity: 1, transition: { duration: 0.7 } },
    exit: {
      backgroundColor: "#B46A90",
      transition: { duration: 2 , ease: [0.48, 0.15, 0.25, 0.96]}
    }
  };

  return (
    <motion.div className="main-container" initial="initial" animate="enter" exit="exit" variants={indexVariants}>
      <Head>
        <title>Sezame - Home</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Layout>
        <div className="description">
          <h1>Sezame</h1>
          <p>Recognize your favourite songs with our app, press on the symbol below to start recording</p>
          <ListenBtn></ListenBtn>
        </div>
      </Layout>

      <footer>
        <script src="https://cdn.rawgit.com/mattdiamond/Recorderjs/08e7abd9/dist/recorder.js"></script>
      </footer>
    </motion.div>
  )
}
