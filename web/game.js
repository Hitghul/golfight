const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let ws = null;
let level = null;
let ball = null;
let canShoot = false;
let aimStart = null;
let hits = 0;
let mouse = null;
let scored = false;

function onMessage(event) {
  const data = JSON.parse(event.data);
  if (data.type === "level") {
    level = data;
    scored = false;
  } else if (data.type === "state") {
    ball = data.pos;
    canShoot = data.can_shoot;
    hits = data.hits;
  } else if (data.type === "scored") {
    scored = true;
  }
}

function showScreen(id) {
  for (const screen of document.querySelectorAll(".screen")) screen.hidden = true;
  document.getElementById(id).hidden = false;
}

function backToMenu() {
  ws.close();
  ball = null;
  showScreen("menu");
}

function startSolo() {
  showScreen("solo");
  ws = new WebSocket(location.origin.replace("http", "ws") + "/ws");
  ws.onmessage = onMessage;
}

function mousePos(event) {
  const rect = canvas.getBoundingClientRect();
  const ratio = canvas.width / rect.width;
  return [(event.clientX - rect.left) * ratio, (event.clientY - rect.top) * ratio];
}

canvas.onmousedown = (event) => {
  if (!ball || !canShoot || scored) return;
  aimStart = mouse = mousePos(event);
};

canvas.onmousemove = (event) => {
  mouse = mousePos(event);
};

canvas.onmouseup = (event) => {
  if (!aimStart) return;
  ws.send(JSON.stringify([aimStart, mousePos(event)]));
  aimStart = null;
};

function drawLine(x1, y1, x2, y2, width, color) {
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
}

function drawCircle(x, y, radius, color) {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, Math.PI * 2);
  ctx.fill();
}

function draw() {
  ctx.fillStyle = "#228b22";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  if (ball) {
    drawCircle(level.hole_pos[0], level.hole_pos[1], 15, "black");
    for (const [x1, y1, x2, y2] of level.walls) {
      drawLine(x1, y1, x2, y2, 10, "#8b4513");
    }
    if (!scored) drawCircle(ball[0], ball[1], 10, "white");
    ctx.fillStyle = "white";
    ctx.font = "bold 28px Arial";
    ctx.fillText(`Score : ${level.score}`, 20, 45);
    ctx.fillText(`Hits : ${hits}`, 20, 85);
    if (aimStart) {
      const dx = aimStart[0] - mouse[0];
      const dy = aimStart[1] - mouse[1];
      const scale = Math.min(1, level.max_power / Math.hypot(dx, dy));
      drawLine(ball[0], ball[1], ball[0] + dx * scale, ball[1] + dy * scale, 4, "yellow");
    }
    if (scored) {
      ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = "gold";
      ctx.textAlign = "center";
      ctx.font = "bold 50px Arial";
      ctx.fillText("Scored !", canvas.width / 2, canvas.height / 2);
      ctx.textAlign = "left";
    }
  }
  requestAnimationFrame(draw);
}

draw();
