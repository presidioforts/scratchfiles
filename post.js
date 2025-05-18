const url = `${config.API_URL}?q=${encodeURIComponent(content)}`;
const response = await fetch(url, {
  method: 'POST'
});
