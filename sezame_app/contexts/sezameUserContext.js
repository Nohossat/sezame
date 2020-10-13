import React, { createContext, useState } from 'react';

export const sezameUserContext = createContext();

const sezameUserProvider = (props) => {
  const [ sezameUser, setSezameUser ] = useState([{
      song_name : "Timeless",
      artists : ["James Blake", "Kendrik Lamar"],
      sezame_nb : 3,
      album_cover : "https://i.scdn.co/image/ab67616d0000b27387d15f78ec75621d40028baf",
      spotify_preview : "https://p.scdn.co/mp3-preview/45cb08fdb67744ab7f1f172bb750e9c10415c37a?cid=774b29d4f13844c495f206cafdad9c86"
  }]);

  const storeResult = result => {
    setSezameUser({
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
    <sezameUserContext.Provider value={{ sezameUser,  storeResult }}>
      {props.children}
    </sezameUserContext.Provider>
  )
}

export default ResultContextProvider;