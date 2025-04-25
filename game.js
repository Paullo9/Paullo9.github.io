// game.js
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const scoreEl = document.getElementById("score");

let score = 0;
const box = { x: 50, y: 50, size: 50, color: "#e74c3c" };

function drawBox() {
  ctx.clearRect(0, 0, 400, 400);
  ctx.fillStyle = box.color;
  ctx.fillRect(box.x, box.y, box.size, box.size);
}

function randomizeBox() {
  box.x = Math.random() * (canvas.width - box.size);
  box.y = Math.random() * (canvas.height - box.size);
}

canvas.addEventListener("click", (e) => {
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;
  if (
    mx >= box.x && mx <= box.x + box.size &&
    my >= box.y && my <= box.y + box.size
  ) {
    score++;
    scoreEl.textContent = score;
    randomizeBox();
    drawBox();
  }
});

// Initialize
drawBox();
