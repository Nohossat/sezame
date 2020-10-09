import Head from 'next/head'
import Layout from '../components/layout'
import ListenBtn from '../components/listen'
import Link from 'next/link'

export default function Home() {
  return (
    <div className="main-container">
      <Head>
        <title>Sezame - Home</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Layout>
        <div className="description">
          <h1>Sezame</h1>
          <p>Recognize your favourite songs with our app, press on the symbol below to start recording</p>
          <ListenBtn></ListenBtn>
          <Link href="/results"><a className="test">test</a></Link>
        </div>
      </Layout>

      <footer>
        <script src="https://cdn.rawgit.com/mattdiamond/Recorderjs/08e7abd9/dist/recorder.js"></script>
      </footer>
    </div>
  )
}
