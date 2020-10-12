import React, { createContext, useState } from 'react';

export const ResultContext = createContext();

const ResultContextProvider = (props) => {
  const [ result, setResult ] = useState({
      confidence : 0,
      song_name : "Timeless",
      artists : ["James Blake", "Kendrik Lamar"],
      sezame_nb : 3,
      album_cover : "https://i.scdn.co/image/ab67616d0000b27387d15f78ec75621d40028baf",
      spotify_preview : "https://p.scdn.co/mp3-preview/45cb08fdb67744ab7f1f172bb750e9c10415c37a?cid=774b29d4f13844c495f206cafdad9c86",
      recommendations : [{ 
                            'name' : 'In My Mind', 
                            'artists' : ["James Blake", "Disclosure"], 
                            'genre' : 'house', 
                            'image' : 'https://i.scdn.co/image/ab67616d0000b27364e59ba8129ddf22cc254111', 
                            'preview' : "https://p.scdn.co/mp3-preview/53eb07b952513e35c7314e4328eb37964bbe4dc6?cid=0005b39baaa34e71839a304b3cef086f"
                          },
                          { 
                            'name' : 'Disco Bango - Radio Edit', 
                            'artists' : ["Bonobo"], 
                            'genre' : 'rnb', 
                            'image' : 'https://i.scdn.co/image/ab67616d0000b273d7658a5bf66a2f3f11878bdf', 
                            'preview' : "https://p.scdn.co/mp3-preview/45cb08fdb67744ab7f1f172bb750e9c10415c37a?cid=774b29d4f13844c495f206cafdad9c86"
                          },
                          { 
                            'name' : 'Lost on You', 
                            'artists' : ["Kendrick Lamar"], 
                            'genre' : 'rock', 
                            'image' : 'https://i.scdn.co/image/ab67616d0000b273a6d8b25a848296895e3717c2', 
                            'preview' : "https://p.scdn.co/mp3-preview/212b25730adafc2b4b68af3b8141a70c414a6daf?cid=0005b39baaa34e71839a304b3cef086f"
                          },
                          { 
                            'name' : 'Whatever', 
                            'artists' : ["Jill Scott"], 
                            'genre' : 'metal', 
                            'image' : 'https://i.scdn.co/image/ab67616d0000b273b1a199f973b9e127111711c0', 
                            'preview' : "https://p.scdn.co/mp3-preview/1e734a762cf8b4e07ba2adbfcad9f6be97fd0e11?cid=0005b39baaa34e71839a304b3cef086f"
                          }]
  });

  const storeResult = result => {
    setResult({
      confidence : result.confidence,
      song_name : result.song_name,
      artists : result.artists,
      sezame_nb : result.sezame_nb,
      album_cover : result.album_cover,
      spotify_preview : result.spotify_preview,
      recommendations : result.recommendations
      })
  }

  return (
    <ResultContext.Provider value={{ result,  storeResult }}>
      {props.children}
    </ResultContext.Provider>
  )
}

export default ResultContextProvider;