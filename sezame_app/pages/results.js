import Head from "next/head";
import Layout from "../components/layout";
import ResultInfo from "../components/resultInfo";
import { ResultContext } from '../contexts/resultContext';
import React, {useContext, useEffect} from "react";
import Recommendations from "../components/recommendations";
import { motion } from "framer-motion";

export default function Results() {
    const { result, storeResult } = useContext(ResultContext);

    const layoutVariants = {
        initial: { 
          backgroundColor: "#B46A90"
        },
        enter: { background: "#000", transition: { duration: 1, ease: [0.42, 0.15, 0.25, 0.2] } },
        exit: {
          backgroundColor: "#efefef",
          transition: { duration: 2 , ease: [0.42, 0.15, 0.25, 0.2]}
        }
    };

    const resultVariants = {
        initial : {
            opacity : 0
        },
        enter: { opacity: 1, transition: { delay: 1, duration: 1, ease: [0.48, 0.15, 0.25, 0.96] } },
        exit: {
          opacity: 0,
          transition: { delay: 0.1, duration: 0.5 }
        }
    };

    return (
        <motion.div initial="initial" animate="enter" exit="exit" variants={layoutVariants}>
            <Head>
                <title>Sezame - Results</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>
                <Layout>
                    <motion.div initial="initial" animate="enter" exit="exit" variants={resultVariants}>
                        <div className="cover">
                            <ResultInfo artist={result.artists} song={result.song_name} sezame_nb={result.sezame_nb} album_cover = {result.album_cover} spotify_link={result.spotify_preview}>
                            </ResultInfo>
                        </div>
                        <div>
                            <Recommendations>
                                {result.recommendations}
                            </Recommendations>
                        </div>
                        
                    </motion.div>
                </Layout>
        </motion.div>
    )
}
  