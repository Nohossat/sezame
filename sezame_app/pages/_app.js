import '../styles/global.css';
import ResultContextProvider from "../contexts/resultContext";
import App from 'next/app';
import Head from "next/head";
import { AnimatePresence } from 'framer-motion';

class MyApp extends App {
  render() {
    const { Component, pageProps, router } = this.props;
    
    return (
      <AnimatePresence exitBeforeEnter>
      <div>
        <Head>
            <title>Sezame - Home</title>
            <link rel="icon" href="/favicon.ico" />
        </Head>
        <ResultContextProvider>
          <Component {...pageProps} key={router.route} />
        </ResultContextProvider>
      </div>
      </AnimatePresence>
    )
  }
}

export default MyApp;