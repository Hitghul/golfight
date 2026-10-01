const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const ws = new WebSocket(location.origin.replace("http", "ws") + "/ws");

let level = null;
let ball = null;
let aimStart = null;
let mouse = null;

// First message is the level, then the ball position every frame
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (level === null) level = data;
  else ball = data;
};

function mousePos(event) {
  const rect = canvas.getBoundingClientRect();
  return [event.clientX - rect.left, event.clientY - rect.top];
}

canvas.onmousedown = (event) => {
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
    drawCircle(ball[0], ball[1], 10, "white");
    if (aimStart) {
      drawLine(ball[0], ball[1], ball[0] + aimStart[0] - mouse[0], ball[1] + aimStart[1] - mouse[1], 4, "yellow");
    }
  }
  requestAnimationFrame(draw);
}

draw();
