<!DOCTYPE html>
<html>

<head>

<title>OpenGradient Intelligence Terminal</title>

<script src="https://cdn.jsdelivr.net/npm/ethers@5.7.2/dist/ethers.min.js"></script>

<style>

body{
background:#04060c;
color:#00f2ff;
font-family:monospace;
margin:0;
}

.container{
max-width:1100px;
margin:auto;
padding:40px;
}

.title{
font-size:40px;
text-align:center;
margin-bottom:40px;
text-shadow:0 0 20px #00f2ff;
}

.grid{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
gap:20px;
margin-top:30px;
}

.card{
background:#0b0f1a;
padding:20px;
border:1px solid #00f2ff;
border-radius:10px;
}

.card:hover{
box-shadow:0 0 15px #00f2ff;
}

textarea{
width:100%;
height:140px;
background:#0b0f1a;
color:white;
border:1px solid #00f2ff;
padding:15px;
}

button{
margin-top:15px;
padding:10px 20px;
background:#00f2ff;
border:none;
cursor:pointer;
}

.result{
margin-top:30px;
padding:20px;
background:#0b0f1a;
border:1px solid #00f2ff;
min-height:120px;
}

</style>

</head>

<body>

<div class="container">

<div class="title">
OpenGradient Intelligence Terminal
</div>

<h2>AI Playground</h2>

<textarea id="prompt">
Explain zero knowledge proofs simply
</textarea>

<br>

<button onclick="runModel()">Run Model</button>

<div class="result" id="result">
Model output...
</div>

<h2>Model Hub Explorer</h2>

<button onclick="loadModels()">Load Models</button>

<div class="grid" id="models"></div>

</div>

<script>

async function runModel(){

const prompt = document.getElementById("prompt").value

const res = await fetch("/chat",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({prompt})
})

const data = await res.json()

document.getElementById("result").innerText =
data.response || data.error

}

async function loadModels(){

const res = await fetch("/models")

const models = await res.json()

const grid = document.getElementById("models")

grid.innerHTML=""

models.forEach(m=>{

const el = document.createElement("div")

el.className="card"

el.innerText=m

grid.appendChild(el)

})

}

</script>

</body>

</html>
