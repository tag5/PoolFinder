import os
from flask import Flask, request, send_from_directory
from PIL import Image, ImageDraw

INPUT = '/images/'
OUTPUT = '/tagged_images/'

app = Flask(__name__)

PAGE = """<html><body>
<canvas id="c" style="cursor:crosshair" style="margin-bottom:10px;"></canvas>

<button onclick="valider()">Valider</button>

<script>
var canvas = document.getElementById("c");
var ctx = canvas.getContext("2d");
var img = new Image();
var sx=0, sy=0, ex=0, ey=0, drawing=false;
img.src = "/img/NAME";

img.onload = function() {
  canvas.width = img.width;
  canvas.height = img.height;
  ctx.drawImage(img, 0, 0);
};

function pos(e) {
  var r = canvas.getBoundingClientRect();
  return [e.clientX - r.left, e.clientY - r.top];
}

canvas.onmousedown = function(e) {
  var p = pos(e); sx = p[0]; sy = p[1]; drawing = true;
};

canvas.onmousemove = function(e) {
  if (!drawing) return;
  var p = pos(e); ex = p[0]; ey = p[1];
  ctx.drawImage(img, 0, 0);
  ctx.strokeStyle = "red";
  ctx.lineWidth = 3;
  ctx.strokeRect(sx, sy, ex - sx, ey - sy);
};

canvas.onmouseup = function(e) {
  drawing = false; 
};

function valider() {
  fetch("/save", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({name: "NAME", x1: sx, y1: sy, x2: ex, y2: ey})
  }).then(function() { location.reload(); });
}
</script>
</body>
</html>"""

def next_image():
    for f in sorted(os.listdir(INPUT)):
        if f.lower().endswith(".webp") and not os.path.exists(os.path.join(OUTPUT, f)):
            return f
    return None

@app.route("/")
def index():
    name = next_image()
    if name is None:
        return "Terminé"
    return PAGE.replace("NAME", name)

@app.route("/img/<name>")
def img(name):
    return send_from_directory(INPUT, name)

@app.route("/save", methods=["POST"])
def save():
    d = request.get_json()
    im = Image.open(os.path.join(INPUT, d["name"])).convert("RGB")
    draw = ImageDraw.Draw(im)
    x1, x2 = sorted([d["x1"], d["x2"]])
    y1, y2 = sorted([d["y1"], d["y2"]])
    draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
    im.save(os.path.join(OUTPUT, d["name"]), "WEBP")
    return "ok"

app.run(host="0.0.0.0", port=5000)
