
function getFormattedRevenue(revenue) {
  if (revenue < 1000) {
    return `${revenue} K`;
  }
  const formattedRevenue = (revenue / 1000).toFixed(1);
  return `${formattedRevenue} M`;
}

const names = document.querySelectorAll("[data-name]");
const value = document.querySelectorAll("[data-revenue]");
const namePodium = document.querySelectorAll("[data-name-podium]");
const valuePodium = document.querySelectorAll("[data-revenue-podium]");
const avatarPodium = document.querySelectorAll("[data-avatar-podium]");  
const avatar = document.querySelectorAll("[data-avatar]");  

const fetchData = () => {
  fetch('/api/get-ranking-data/')
    .then(response => response.json())
    .then(data => {
      console.log('Data received:', data);

      const iterations = data.length > names.length ? names.length : data.length;

      for (let i = 0; i < iterations; i++) {
        names[i].innerHTML = data[i].nome;
        value[i].innerHTML = getFormattedRevenue(data[i].total_pontuacao);
        avatar[i].src = data[i].avatar_url; 
        console.log('Updating:', names[i].innerHTML, value[i].innerHTML, avatar[i].src);

        if (i < namePodium.length && i < valuePodium.length && i < avatarPodium.length) {
          namePodium[i].innerHTML = data[i].nome;
          valuePodium[i].innerHTML = getFormattedRevenue(data[i].total_pontuacao);
          avatarPodium[i].src = data[i].avatar_url;  
          console.log('Podium updating:', namePodium[i].innerHTML, valuePodium[i].innerHTML, avatarPodium[i].src);
        }
      }
    })
    .catch(error => console.error('Error fetching data:', error));
}

window.addEventListener("load", () => {
  fetchData();
  setInterval(fetchData, 60 * 1000);
});



