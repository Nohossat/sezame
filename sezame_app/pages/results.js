import Head from "next/head";
import Layout from "../components/layout";
import ResultInfo from "../components/resultInfo";
import { useRouter } from 'next/router';

export default function Results() {
    return (
        <div className="cover">
            <Head>
                <title>Sezame - Results</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <Layout>
                <ResultInfo artist="James Blake" song="Timeless" sezame_nb="3" album="Album : Black Sands - 2017" spotify_link="https://p.scdn.co/mp3-preview/45cb08fdb67744ab7f1f172bb750e9c10415c37a?cid=774b29d4f13844c495f206cafdad9c86">
                </ResultInfo>
            </Layout>
        </div>
    )
}
  