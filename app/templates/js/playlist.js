function singleItemPlaylist(file,name,basicAuth){
    let hostUrl = `http://${basicAuth}${window.location.host}`
    let pd = ""
    pd += '#EXTM3U\n'
    pd += `#EXTINF: ${name}\n`
    pd += `${hostUrl}/${file}\n`
    let blob = new Blob([pd], { endings: "native" });
    saveAs(blob, `${name}.m3u`);
}
