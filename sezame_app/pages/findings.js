import Head from "next/head";
import Layout from "../components/layout";
import RecommendItem from '../components/recommendItem';
import { ResultContext } from '../contexts/resultContext';
import React, {useContext} from "react";
import { motion } from "framer-motion";

export default function Findings(){
    const { result, storeResult } = useContext(ResultContext);
    console.log(result);
    const items = result.previous_findings.map((value, index) =>
        <RecommendItem theme="white" sezame_find="true" key={index}>
            {value}
        </RecommendItem>
    )

    const layoutVariants = {
        initial: { 
          backgroundColor: "#fff"
        },
        enter: { background: "#efefef", transition: { duration: 1, ease: [0.42, 0.15, 0.25, 0.2] } },
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
        <motion.div className="findings_container" initial="initial" animate="enter" exit="exit" variants={layoutVariants}>
            <Head>
                <title>Sezame - Previous Sezames</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>
                <Layout>
                    <h1 className="findings_title"> Your Previous Sezames </h1>
                    <motion.div initial="initial" animate="enter" exit="exit" variants={resultVariants}>
                        <div className="findings_list">
                            {items}
                        </div>
                    </motion.div>
                </Layout>
        </motion.div>
    )
}