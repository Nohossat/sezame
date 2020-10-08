import '../styles/global.css';
import ResultContextProvider from "../contexts/resultContext";
import App from 'next/app';
import Head from "next/head";

class MyApp extends App {
  render() {
    const { Component, pageProps } = this.props;
    return (
      <div>
        <Head>
            <title>Sezame - Home</title>
            <link rel="icon" href="/favicon.ico" />
        </Head>
        <ResultContextProvider>
          <Component {...pageProps} />
        </ResultContextProvider>
      </div>
    )
  }
}

export default MyApp;