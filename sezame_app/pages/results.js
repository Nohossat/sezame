import Head from "next/head";
import Layout from "../components/layout";
import ResultInfo from "../components/resultInfo";
import { ResultContext } from '../contexts/resultContext';
import React, {useContext, useEffect} from "react";
import Recommendations from "../components/recommendations";

export default function Results() {

    const { result, storeResult } = useContext(ResultContext);

    return (
        <div>
            <Head>
                <title>Sezame - Results</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>
                <Layout>
                    <div className="cover">
                        <ResultInfo artist={result.artists} song={result.song_name} sezame_nb={result.sezame_nb} album_cover = {result.album_cover} spotify_link={result.spotify_preview}>
                        </ResultInfo>
                    </div>
                    <div>
                        <Recommendations>
                            {result.recommendations}
                        </Recommendations>
                    </div>
                </Layout>
        </div>
    )
}
  