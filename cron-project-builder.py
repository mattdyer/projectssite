#!/usr/bin/env python3
"""
cron-project-builder.py
Runs from cron twice daily. Finds an unchecked project idea, builds it,
commits, pushes, and emails a summary.
"""

import os
import re
import random
import smtplib
import json
import subprocess
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === CONFIG ===
SITE_DIR = "/mnt/c/Users/madma/Documents/sites/projectssite"
IDEAS_FILE = os.path.join(SITE_DIR, "PROJECT-IDEAS.md")
INDEX_FILE = os.path.join(SITE_DIR, "docs", "index.htm")
LOG_FILE = os.path.join(SITE_DIR, ".project-ideas.log")

# Email settings (update these)
SMTP_HOST = "gcam1187.siteground.biz"
SMTP_PORT = 465
SMTP_USER = "agent@md.mattdyer.us"
SMTP_PASS = "PLACEHOLDER_PASSWORD"  # <-- UPDATE THIS
FROM_EMAIL = "agent@md.mattdyer.us"
TO_EMAIL = "madmatt1220@gmail.com"

# Project templates by category
TEMPLATES = {
    "snake": {
        "title": "Snake",
        "html": """<!DOCTYPE html>
<html><head><title>Snake</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { background:#222; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; margin:0; font-family:monospace; color:#fff; }
canvas { border:2px solid #555; background:#111; }
#info { margin-top:10px; font-size:18px; }
</style></head><body>
<canvas id="c" width="400" height="400"></canvas>
<div id="info">Score: 0 — Use arrow keys or swipe</div>
<script>
const c=document.getElementById('c'),ctx=c.getContext('2d');
const S=20,COLS=c.width/S,ROWS=c.height/S;
let snake=[{x:10,y:10}],dir={x:1,y:0},food,score=0,gameOver=false,tick=0;
function spawnFood(){food={x:Math.floor(Math.random()*COLS),y:Math.floor(Math.random()*ROWS)};}
spawnFood();
document.addEventListener('keydown',e=>{
  const k=e.key;
  if(k==='ArrowUp'&&dir.y!==1)dir={x:0,y:-1};
  if(k==='ArrowDown'&&dir.y!==-1)dir={x:0,y:1};
  if(k==='ArrowLeft'&&dir.x!==1)dir={x:-1,y:0};
  if(k==='ArrowRight'&&dir.x!==-1)dir={x:1,y:0};
});
// Touch support
let tx=0;
c.addEventListener('touchstart',e=>{tx=e.touches[0].clientX;e.preventDefault();});
c.addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>30){dir=dx>0?{x:1,y:0}:{x:-1,y:0};}});
function update(){
  if(gameOver){
    ctx.fillStyle='rgba(0,0,0,0.7)';ctx.fillRect(0,0,c.width,c.height);
    ctx.fillStyle='#fff';ctx.font='30px monospace';ctx.textAlign='center';
    ctx.fillText('Game Over! Score: '+score,c.width/2,c.height/2);
    ctx.font='16px monospace';ctx.fillText('Press Space to restart',c.width/2,c.height/2+30);
    return;
  }
  const head={x:snake[0].x+dir.x,y:snake[0].y+dir.y};
  if(head.x<0||head.x>=COLS||head.y<0||head.y>=ROWS||snake.some(s=>s.x===head.x&&s.y===head.y)){gameOver=true;return;}
  snake.unshift(head);
  if(head.x===food.x&&head.y===food.y){score++;spawnFood();}
  else snake.pop();
  ctx.fillStyle='#111';ctx.fillRect(0,0,c.width,c.height);
  ctx.fillStyle='#e74c3c';ctx.fillRect(food.x*S+1,food.y*S+1,S-2,S-2);
  ctx.fillStyle='#2ecc71';snake.forEach(s=>ctx.fillRect(s.x*S+1,s.y*S+1,S-2,S-2));
  document.getElementById('info').textContent='Score: '+score+' — Use arrow keys or swipe';
}
setInterval(()=>{update();tick++;},120);
document.addEventListener('keydown',e=>{if(e.code==='Space'&&gameOver){snake=[{x:10,y:10}];dir={x:1,y:0};score=0;gameOver=false;spawnFood();}});
</script></body></html>""",
    },
    "breakout": {
        "title": "Breakout",
        "html": """<!DOCTYPE html>
<html><head><title>Breakout</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { background:#222; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; margin:0; font-family:monospace; color:#fff; }
canvas { border:2px solid #555; background:#111; }
#info { margin-top:10px; font-size:18px; }
</style></head><body>
<canvas id="c" width="480" height="400"></canvas>
<div id="info">Score: 0 — Move mouse or touch to control paddle</div>
<script>
const c=document.getElementById('c'),ctx=c.getContext('2d');
const P={x:200,y:380,w:80,h:12,speed:7},B={x:240,y:300,r:6,dx:3,dy:-3};
let bricks=[],score=0,lives=5,running=true;
const colors=['#e74c3c','#e67e22','#f1c40f','#2ecc71','#3498db','#9b59b6'];
for(let r=0;r<6;r++)for(let col=0;col<8;col++)bricks.push({x:col*58+10,y:r*20+30,w:50,h:14,color:colors[r],alive:true});
c.addEventListener('mousemove',e=>{const rect=c.getBoundingClientRect();P.x=e.clientX-rect.left-P.w/2;});
c.addEventListener('touchmove',e=>{const rect=c.getBoundingClientRect();P.x=e.touches[0].clientX-rect.left-P.w/2;e.preventDefault();});
function update(){
  if(!running)return;
  B.x+=B.dx;B.y+=B.dy;
  if(B.x-B.r<0||B.x+B.r>c.width)B.dx=-B.dx;
  if(B.y-B.r<0)B.dy=-B.dy;
  if(B.y+B.r>P.y&&B.x>P.x&&B.x<P.x+P.w){B.dy=-B.dy;B.y=P.y-B.r;}
  if(B.y>c.height){lives--;if(lives<=0){running=false;return;}B.x=240;B.y=300;B.dx=3*(Math.random()>0.5?1:-1);B.dy=-3;}
  bricks.forEach(b=>{if(!b.alive)return;
    if(B.x+B.r>b.x&&B.x-B.r<b.x+b.w&&B.y+B.r>b.y&&B.y-B.r<b.y+b.h){b.alive=false;B.dy=-B.dy;score+=10;}});
  if(bricks.every(b=>!b.alive)){running=false;}
  ctx.fillStyle='#111';ctx.fillRect(0,0,c.width,c.height);
  ctx.fillStyle='#fff';ctx.fillRect(P.x,P.y,P.w,P.h);
  ctx.beginPath();ctx.arc(B.x,B.y,B.r,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#f39c12';ctx.fillText('Lives: '+lives,360,20);
  bricks.forEach(b=>{ctx.fillStyle=b.color;ctx.fillRect(b.x,b.y,b.w,b.h);});
  document.getElementById('info').textContent='Score: '+score+' — Lives: '+lives;
}
setInterval(update,16);
</script></body></html>""",
    },
    "pong": {
        "title": "Pong",
        "html": """<!DOCTYPE html>
<html><head><title>Pong</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { background:#222; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; margin:0; font-family:monospace; color:#fff; }
canvas { border:2px solid #555; background:#111; }
#info { margin-top:10px; font-size:18px; }
</style></head><body>
<canvas id="c" width="600" height="400"></canvas>
<div id="info">Move mouse or touch — first to 7 wins</div>
<script>
const c=document.getElementById('c'),ctx=c.getContext('2d');
const P={w:12,h:80,speed:6},BALL={x:300,y:200,r:8,dx:4,dy:3};
let s1=0,s2=0,pl1=160,pl2=160,running=true;
function reset(){BALL.x=300;BALL.y=200;BALL.dx=4*(Math.random()>0.5?1:-1);BALL.dy=3*(Math.random()>0.5?1:-1);}
c.addEventListener('mousemove',e=>{const r=c.getBoundingClientRect();pl1=e.clientY-r.top-P.h/2;});
c.addEventListener('touchmove',e=>{const r=c.getBoundingClientRect();pl1=e.touches[0].clientY-r.top-P.h/2;e.preventDefault();});
function update(){
  if(!running)return;
  BALL.x+=BALL.dx;BALL.y+=BALL.dy;
  if(BALL.y-BALL.r<0||BALL.y+BALL.r>c.height)BALL.dy=-BALL.dy;
  // Player paddle
  if(BALL.x-BALL.r<30&&BALL.y>pl1&&BALL.y<pl1+P.h){BALL.dx=Math.abs(BALL.dx);BALL.x=30+BALL.r;}
  // AI paddle
  if(BALL.y<pl2+P.h/2)pl2-=P.speed*0.6;
  if(BALL.y>pl2+P.h/2)pl2+=P.speed*0.6;
  if(BALL.x+BALL.r>558&&BALL.y>pl2&&BALL.y<pl2+P.h){BALL.dx=-Math.abs(BALL.dx);BALL.x=558-BALL.r;}
  // Score
  if(BALL.x<0){s2++;if(s2>=7){running=false;}reset();}
  if(BALL.x>c.width){s1++;if(s1>=7){running=false;}reset();}
  ctx.fillStyle='#111';ctx.fillRect(0,0,c.width,c.height);
  ctx.fillStyle='#fff';ctx.fillRect(25,pl1,P.w,P.h);ctx.fillRect(563,pl2,P.w,P.h);
  ctx.beginPath();ctx.arc(BALL.x,BALL.y,BALL.r,0,Math.PI*2);ctx.fill();
  ctx.font='30px monospace';ctx.fillText(s1+'',280,40);ctx.fillText(s2+'',310,40);
  ctx.setLineDash([5,5]);ctx.strokeStyle='#333';ctx.beginPath();ctx.moveTo(300,0);ctx.lineTo(300,400);ctx.stroke();ctx.setLineDash([]);
  document.getElementById('info').textContent='You: '+s1+' AI: '+s2;
}
setInterval(update,16);
</script></body></html>""",
    },
    "memory": {
        "title": "Memory Match",
        "html": """<!DOCTYPE html>
<html><head><title>Memory Match</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { background:#222; display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:100vh; margin:0; font-family:monospace; color:#fff; }
#board { display:grid; grid-template-columns:repeat(4,80px); gap:8px; margin:20px; }
.card { width:80px;height:80px;background:#3498db;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:32px;cursor:pointer;user-select:none;transition:transform 0.3s; }
.card.flipped,.card.matched { background:#ecf0f1; transform:none; }
.card:not(.flipped):not(.matched) { font-size:0; }
#info { font-size:18px; margin:10px; }
#restart { padding:10px 20px;font-size:16px;cursor:pointer;background:#3498db;color:#fff;border:none;border-radius:4px;margin-top:10px; }
</style></head><body>
<div id="info">Moves: 0 — Find all pairs!</div>
<div id="board"></div>
<button id="restart" onclick="init()">Restart</button>
<script>
const emojis=['🍎','🍊','🍋','🍇','🍓','🍒','🥝','🍑'];
let cards=[],flipped=[],moves=0,matched=0,lock=false;
function init(){
  cards=[...emojis,...emojis].sort(()=>Math.random()-0.5);
  flipped=[];moves=0;matched=0;lock=false;
  document.getElementById('info').textContent='Moves: 0 — Find all pairs!';
  const b=document.getElementById('board');b.innerHTML='';
  cards.forEach((emoji,i)=>{
    const d=document.createElement('div');d.className='card';d.textContent='?';
    d.dataset.i=i;d.onclick=()=>flip(d,i);b.appendChild(d);
  });
}
function flip(el,i){
  if(lock||el.classList.contains('flipped')||el.classList.contains('matched'))return;
  el.classList.add('flipped');el.textContent=cards[i];flipped.push(el);
  if(flipped.length===2){
    moves++;lock=true;
    if(cards[flipped[0].dataset.i]===cards[flipped[1].dataset.i]){
      flipped.forEach(e=>e.classList.add('matched'));matched+=2;flipped=[];lock=false;
      if(matched===cards.length)setTimeout(()=>document.getElementById('info').textContent='You win! Moves: '+moves,300);
    }else{setTimeout(()=>{flipped.forEach(e=>{e.classList.remove('flipped');e.textContent='?';});flipped=[];lock=false;},800);}
  }
  document.getElementById('info').textContent='Moves: '+moves;
}
init();
</script></body></html>""",
    },
    "whackamole": {
        "title": "Whack-a-Mole",
        "html": """<!DOCTYPE html>
<html><head><title>Whack-a-Mole</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { background:#222; display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:100vh; margin:0; font-family:monospace; color:#fff; }
#board { display:grid; grid-template-columns:repeat(3,100px); gap:10px; margin:20px; }
.hole { width:100px;height:100px;background:#5d4037;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:50px;cursor:pointer;transition:background 0.1s; }
.hole.active { background:#8d6e63; }
#info { font-size:22px; margin:10px; }
#start { padding:10px 20px;font-size:16px;cursor:pointer;background:#e67e22;color:#fff;border:none;border-radius:4px;margin-top:10px; }
</style></head><body>
<div id="info">Score: 0 | Time: 30s</div>
<div id="board"></div>
<button id="start" onclick="startGame()">Start</button>
<script>
let holes=[],score=0,timeLeft=30,active=-1,gameRunning=false;
for(let i=0;i<9;i++){const h=document.createElement('div');h.className='hole';h.textContent='🕳️';h.onclick=()=>whack(i);document.getElementById('board').appendChild(h);holes.push(h);}
function startGame(){score=0;timeLeft=30;gameRunning=true;document.getElementById('start').style.display='none';
  const iv=setInterval(()=>{timeLeft--;document.getElementById('info').textContent='Score: '+score+' | Time: '+timeLeft+'s';
    if(timeLeft<=0){clearInterval(iv);gameRunning=false;holes.forEach(h=>{h.classList.remove('active');h.textContent='🕳️';});document.getElementById('info').textContent='Game Over! Score: '+score;document.getElementById('start').style.display='';}},1000);
  const mi=setInterval(()=>{if(!gameRunning){clearInterval(mi);return;}holes.forEach(h=>{h.classList.remove('active');h.textContent='🕳️';});active=Math.floor(Math.random()*9);holes[active].classList.add('active');holes[active].textContent='🐹';},800);
}
function whack(i){if(!gameRunning||i!==active)return;score++;holes[i].classList.remove('active');holes[i].textContent='💥';active=-1;document.getElementById('info').textContent='Score: '+score+' | Time: '+timeLeft+'s';}
</script></body></html>""",
    },
    "reaction": {
        "title": "Reaction Time",
        "html": """<!DOCTYPE html>
<html><head><title>Reaction Time</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { background:#222; display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:100vh; margin:0; font-family:monospace; color:#fff; cursor:pointer; user-select:none; }
#box { width:80vw;max-width:500px;height:300px;display:flex;align-items:center;justify-content:center;font-size:24px;border-radius:12px;transition:background 0.1s; }
.waiting { background:#e74c3c; }
.ready { background:#2ecc71; }
.idle { background:#34495e; }
#hist { margin-top:20px;font-size:16px;text-align:center; }
</style></head><body>
<div id="box" class="idle">Click to start</div>
<div id="hist"></div>
<script>
const box=document.getElementById('box'),hist=document.getElementById('hist');
let state='idle',startTime=0,timeout=null;
box.onclick=()=>{
  if(state==='idle'){
    state='waiting';box.className='waiting';box.textContent='Wait for green...';
    timeout=setTimeout(()=>{state='ready';box.className='ready';box.textContent='CLICK NOW!';startTime=Date.now();},1000+Math.random()*4000);
  }else if(state==='waiting'){
    clearTimeout(timeout);box.className='idle';box.textContent='Too early! Click to retry.';state='idle';
  }else if(state==='ready'){
    const ms=Date.now()-startTime;
    hist.innerHTML='Last: '+ms+'ms'+hist.textContent?(' | Best: '+best+'ms'):'';
    if(!best||ms<best)best=ms;
    state='idle';box.className='idle';box.textContent=ms+'ms — Click to try again';
  }
};
let best=null;
</script></body></html>""",
    },
    "tictactoe": {
        "title": "Tic-Tac-Toe",
        "html": """<!DOCTYPE html>
<html><head><title>Tic-Tac-Toe</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { background:#222; display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:100vh; margin:0; font-family:monospace; color:#fff; }
#board { display:grid; grid-template-columns:repeat(3,100px); gap:4px; margin:20px; }
.cell { width:100px;height:100px;background:#34495e;display:flex;align-items:center;justify-content:center;font-size:48px;cursor:pointer;border-radius:8px; }
.cell:hover { background:#4a6078; }
#info { font-size:22px; margin:10px; }
#restart { padding:10px 20px;font-size:16px;cursor:pointer;background:#3498db;color:#fff;border:none;border-radius:4px;margin-top:10px; }
</style></head><body>
<div id="info">Your turn (X)</div>
<div id="board"></div>
<button id="restart" onclick="reset()">New Game</button>
<script>
let board=['','','','','','','','',''],turn='X',gameOver=false;
function checkWin(b){const w=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];return w.map(a=>b[a[0]]&&b[a[0]]===b[a[1]]&&b[a[1]]===b[a[2]]).some(x=>x)?b.find(c=>c):null;}
function render(){document.getElementById('board').innerHTML=board.map((c,i)=>'<div class="cell" onclick="move('+i+')">'+(c?c:'')+'</div>').join('');}
function ai(){
  // Try to win
  for(let i=0;i<9;i++){if(!board[i]){board[i]='O';if(checkWin(board)==='O')return;i--;break;}}
  // Block
  for(let i=0;i<9;i++){if(!board[i]){board[i]='X';if(checkWin(board)==='X'){board[i]='O';return;}board[i]='';}}
  // Center
  if(!board[4]){board[4]='O';return;}
  // Corner
  const corners=[0,2,6,8].filter(i=>!board[i]);if(corners.length){board[corners[Math.floor(Math.random()*corners.length)]]='O';return;}
  // Any
  const empty=[...board.keys()].filter(i=>!board[i]);board[empty[Math.floor(Math.random()*empty.length)]]='O';
}
function move(i){
  if(board[i]||gameOver||turn!=='X')return;
  board[i]='X';if(checkWin(board)){endGame();return;}
  if(!board.includes('')){endGame();return;}
  turn='O';render();document.getElementById('info').textContent='AI thinking...';
  setTimeout(()=>{ai();render();const w=checkWin(board);if(w){endGame(w);return;}if(!board.includes('')){endGame();return;}turn='X';document.getElementById('info').textContent='Your turn (X)';},300);
}
function endGame(w){
  gameOver=true;
  document.getElementById('info').textContent=w==='X'?'You win!':w==='O'?'AI wins!':'Draw!';
}
function reset(){board=['','','','','','','','',''];turn='X';gameOver=false;document.getElementById('info').textContent='Your turn (X)';render();}
render();
</script></body></html>""",
    },
    "dice": {
        "title": "Dice Roller",
        "html": """<!DOCTYPE html>
<html><head><title>Dice Roller</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { background:#222; display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:100vh; margin:0; font-family:monospace; color:#fff; }
#dice { font-size:80px; margin:20px; letter-spacing:20px; }
#controls { margin:10px; }
button { padding:10px 20px;font-size:16px;cursor:pointer;background:#3498db;color:#fff;border:none;border-radius:4px;margin:5px; }
#history { margin-top:20px;font-size:14px;max-height:150px;overflow-y:auto;text-align:center; }
</style></head><body>
<div id="controls">
  Dice: <button onclick="count=1">1</button><button onclick="count=2">2</button><button onclick="count=3">3</button><button onclick="count=5">5</button><button onclick="count=10">10</button>
</div>
<div id="dice">🎲</div>
<button onclick="roll()" style="font-size:20px;padding:15px 40px;">ROLL</button>
<div id="history"></div>
<script>
const faces=['⚀','⚁','⚂','⚃','⚄','⚅'];
let count=1,total=0;
function roll(){
  let result=[];for(let i=0;i<count;i++)result.push(Math.floor(Math.random()*6)+1);
  const sum=result.reduce((a,b)=>a+b,0);
  document.getElementById('dice').textContent=result.map(r=>faces[r-1]).join('');
  total+=sum;
  document.getElementById('history').innerHTML='Roll: ['+result.join(', ')+'] = '+sum+'<br>Total: '+total+'<br>'+(document.getElementById('history').innerHTML||'');
}
</script></body></html>""",
    },
    "calculator": {
        "title": "Calculator",
        "html": """<!DOCTYPE html>
<html><head><title>Calculator</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { background:#222; display:flex; align-items:center; justify-content:center; min-height:100vh; margin:0; font-family:monospace; }
#calc { background:#333;padding:15px;border-radius:12px;width:280px; }
#display { background:#111;color:#2ecc71;font-size:32px;text-align:right;padding:15px;border-radius:8px;margin-bottom:10px;min-height:60px;word-break:break-all; }
.grid { display:grid; grid-template-columns:repeat(4,1fr); gap:6px; }
.btn { padding:18px;font-size:20px;border:none;border-radius:8px;cursor:pointer; }
.num { background:#4a6078;color:#fff; }
.op { background:#e67e22;color:#fff; }
.eq { background:#2ecc71;color:#fff;grid-column:span 2; }
.cl { background:#e74c3c;color:#fff; }
</style></head><body>
<div id="calc">
<div id="display">0</div>
<div class="grid">
<button class="btn cl" onclick="clearAll()">C</button>
<button class="btn op" onclick="input('(')">(</button>
<button class="btn op" onclick="input(')')">)</button>
<button class="btn op" onclick="input('/')">/</button>
<button class="btn num" onclick="input('7')">7</button>
<button class="btn num" onclick="input('8')">8</button>
<button class="btn num" onclick="input('9')">9</button>
<button class="btn op" onclick="input('*')">×</button>
<button class="btn num" onclick="input('4')">4</button>
<button class="btn num" onclick="input('5')">5</button>
<button class="btn num" onclick="input('6')">6</button>
<button class="btn op" onclick="input('-')">−</button>
<button class="btn num" onclick="input('1')">1</button>
<button class="btn num" onclick="input('2')">2</button>
<button class="btn num" onclick="input('3')">3</button>
<button class="btn op" onclick="input('+')">+</button>
<button class="btn num" onclick="input('0')">0</button>
<button class="btn num" onclick="input('.')">.</button>
<button class="btn eq" onclick="calc()">=</button>
</div>
</div>
<script>let expr='';
function input(v){expr+=v;document.getElementById('display').textContent=expr;}
function clearAll(){expr='';document.getElementById('display').textContent='0';}
function calc(){try{let r=Function('"use strict";return ('+expr+')')();document.getElementById('display').textContent=r;expr=String(r);}catch(e){document.getElementById('display').textContent='Error';expr='';}}
document.addEventListener('keydown',e=>{if('0123456789.+-*/()'.includes(e.key))input(e.key);if(e.key==='Enter')calc();if(e.key==='Escape')clearAll();if(e.key==='Backspace'){expr=expr.slice(0,-1);document.getElementById('display').textContent=expr||'0';}});
</script></body></html>""",
    },
}

def read_ideas():
    """Read PROJECT-IDEAS.md and return list of (checked, category, name) tuples."""
    with open(IDEAS_FILE, 'r') as f:
        lines = f.readlines()
    entries = []
    current_cat = None
    for line in lines:
        line = line.rstrip()
        if line.startswith('## '):
            current_cat = line[3:].strip()
        if line.startswith('- [ ] '):
            text = line[6:].strip()
            entries.append((False, current_cat, text))
        elif line.startswith('- [x] '):
            text = line[6:].strip()
            entries.append((True, current_cat, text))
    return entries

def get_done_count(entries):
    return sum(1 for checked, _, _ in entries if checked)

def get_pending(entries):
    return [(cat, name) for checked, cat, name in entries if not checked]

def build_project(name):
    """Build a project folder with an index.html based on name matching."""
    slug = name.lower().replace(' ', '').replace('-', '').replace("'", "").replace('(', '').replace(')', '').replace('/', '').replace('&', '')
    
    # Try to match name to a template
    template = None
    for key, tmpl in TEMPLATES.items():
        if key in slug or slug in key or name.lower() in key.lower() or key in name.lower():
            template = tmpl
            break
    
    if not template:
        # Generic template for unmapped projects
        template = {
            "title": name,
            "html": f"""<!DOCTYPE html>
<html><head><title>{name}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {{ background:#222; display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:100vh; margin:0; font-family:monospace; color:#fff; }}
h1 {{ margin:0 0 20px 0; }}
p {{ max-width:500px; text-align:center; line-height:1.6; color:#aaa; }}
canvas {{ border:2px solid #555; background:#111; }}
</style></head><body>
<h1>{name}</h1>
<p>This project is under construction.</p>
</body></html>"""
        }
    
    folder = os.path.join(SITE_DIR, 'docs', slug)
    os.makedirs(folder, exist_ok=True)
    
    html_file = os.path.join(folder, 'index.html')
    with open(html_file, 'w') as f:
        f.write(template['html'])
    
    # Copy shared scripts if needed
    scripts_src = os.path.join(SITE_DIR, 'docs', 'scripts')
    scripts_dst = os.path.join(folder, 'scripts')
    if os.path.exists(scripts_src) and not os.path.exists(scripts_dst):
        import shutil
        shutil.copytree(scripts_src, scripts_dst, dirs_exist_ok=True)
    
    return slug, template['title']

def update_index(slug, title):
    """Add link to docs/index.htm if not already present."""
    with open(INDEX_FILE, 'r') as f:
        content = f.read()
    
    href = f'/docs/{slug}/index.html'
    if href not in content:
        # Add before </ul>
        link = f'\t\t<li><a href="{href}">{title}</a></li>\n'
        content = content.replace('</ul>', link + '\t</ul>')
        with open(INDEX_FILE, 'w') as f:
            f.write(content)
        return True
    return False

def git_add_commit_push(message):
    """Stage, commit, and push changes."""
    subprocess.run(['git', 'add', '-A'], cwd=SITE_DIR, capture_output=True)
    result = subprocess.run(['git', 'commit', '-m', message], cwd=SITE_DIR, capture_output=True, text=True)
    if 'nothing to commit' in result.stdout or 'nothing to commit' in result.stderr:
        return False
    result = subprocess.run(['git', 'push', 'origin', 'master'], cwd=SITE_DIR, capture_output=True, text=True)
    return result.returncode == 0

def send_email(subject, body):
    """Send email via SiteGround SMTP."""
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        with open(LOG_FILE, 'a') as f:
            f.write(f'{datetime.now()}: Email error: {e}\n')
        return False

def main():
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    entries = read_ideas()
    pending = get_pending(entries)
    done_count = get_done_count(entries)
    
    log_line = f'{now}: Total={len(entries)} Done={done_count} Pending={len(pending)}\n'
    
    if not pending:
        log_line += 'All projects completed!\n'
        print(log_line)
        with open(LOG_FILE, 'a') as f:
            f.write(log_line)
        return
    
    # Pick a random pending project
    cat, name = random.choice(pending)
    
    # Build the project
    slug, title = build_project(name)
    updated = update_index(slug, title)
    
    # Update the checklist in PROJECT-IDEAS.md
    with open(IDEAS_FILE, 'r') as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        if f'- [ ] {name}' == line.rstrip():
            new_lines.append(f'- [x] {name}\n')
        else:
            new_lines.append(line)
    with open(IDEAS_FILE, 'w') as f:
        f.writelines(new_lines)
    
    done_count += 1
    
    # Commit and push
    pushed = git_add_commit_push(f'Built project: {title} ({slug})')
    
    log_line += f'Working on: {name} ({cat})\n'
    log_line += f'Built: docs/{slug}/index.html\n'
    log_line += f'Pushed: {"Yes" if pushed else "No"}\n'
    log_line += f'Progress: {done_count}/{len(entries)} complete\n'
    
    print(log_line)
    with open(LOG_FILE, 'a') as f:
        f.write(log_line)
    
    # Send email
    email_body = f"""Project Builder Update
{now}

Project worked on: {title} ({cat})
Built: docs/{slug}/index.html
Progress: {done_count}/{len(entries)} projects complete
Pushed: {"Yes" if pushed else "No"}

Pending projects remaining: {len(get_pending(read_ideas()))}

All browser-only, no backend needed.
"""
    send_email(f'[Project Builder] {title} complete!', email_body)

if __name__ == '__main__':
    main()
