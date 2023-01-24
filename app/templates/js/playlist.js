function downloadBlob(blob, filename) {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.style.display = "none";
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
}

function singleItemPlaylist(file, name, basicAuth) {
  name = decodeURI(name)
  let hostUrl = `http://${basicAuth}${window.location.host}`;
  let pd = "";
  pd += "#EXTM3U\n";
  pd += `#EXTINF: ${name}\n`;
  pd += `${hostUrl}/${file}\n`;
  let blob = new Blob([pd], { endings: "native" });
  downloadBlob(blob, `${name}.m3u`);
}
