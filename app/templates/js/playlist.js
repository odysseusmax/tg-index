function singleItemPlaylist(file,name){
    let hostUrl = 'http://' + window.location.host
    let pd = ""
    pd += '#EXTM3U\n'
    pd += `#EXTINF: ${name}\n`
    pd += `${hostUrl}/${file}\n`
    let blob = new Blob([pd], { endings: "native" });
    saveAs(blob, `${name}.m3u`);
} 

// function createPlaylist(indexSite, id, playlistName = "Playlist", duration = 60) {
//     let pd = ""
//     name = playlistName
//     pd += '#EXTM3U\n'
//     pd += `#EXTINF: ${duration * 60} | ${name}\n`
//     pd += `${indexSite}/${id}/v.mp4\n`
//     return pd
// }

// function playlist(id, name) {
//     hostUrl = 'https://' + window.location.host
//     playlistData = createPlaylist(hostUrl, id, name);
//     let blob = new Blob([playlistData], { endings: "native" });
//     saveAs(blob, `${name}.m3u`);
// }

