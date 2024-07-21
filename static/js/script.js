document.addEventListener('DOMContentLoaded', () => {
  fetch('/start')
      .then(response => response.json())
      .then(data => {
          document.getElementById('enemy-name').innerText = data.enemy.name;
          document.getElementById('enemy-hp').innerText = data.enemy.hp;
          document.getElementById('player-hp').innerText = data.player.hp;
          document.getElementById('enemy-image').src = `/static/images/${data.enemy.image}`;
      });
});


function sendAction(action) {
  fetch('/action', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ action: action }),
  })
  .then(response => response.json())
  .then(data => {
      document.getElementById('result').innerText = data.message;
      if (data.enemy && data.player) {
          document.getElementById('enemy-hp').innerText = data.enemy.hp;
          document.getElementById('player-hp').innerText = data.player.hp;
      }
      if (data.winner) {
          document.getElementById('result').innerText += ` Winner: ${data.winner}`;
      }
  });
}
