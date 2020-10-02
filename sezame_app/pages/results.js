import Head from "next/head";
import Layout from "../components/layout";
import ResultInfo from "../components/resultInfo";

export default function Results() {
    return (
        <div class="cover">
            <Head>
                <title>Sezame - Results</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <Layout>
                <ResultInfo artist="James Blake" song="Timeless" sezame_nb="3" spotify_link="#">
                </ResultInfo>
            </Layout>
        </div>
    )
}