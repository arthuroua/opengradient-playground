<!DOCTYPE html>
<html>

<head>

<title>OpenGradient Neon AI Terminal</title>

<script src="https://cdn.jsdelivr.net/npm/ethers@5.7.2/dist/ethers.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.158.0/build/three.min.js"></script>

<style>

body{
background:#03040a;
font-family:monospace;
color:#00f2ff;
margin:0;
}

.container{
max-width:1100px;
margin:auto;
padding:40px;
}

.title{
font-size:42px;
text-align:center;
margin-bottom:40px;
text-shadow:0 0 25px #00f2ff;
}

.panel{
background:#0b0f1a;
border:1px solid #00f2ff;
border-radius:10px;
padding:20px;
margin-bottom:25px;
}

button{
padding:10px 20px;
margin:5px;
background:#00f2ff;
border:none;
cursor:pointer;
box-shadow:0 0 10px #00f2ff;
}

button:hover{
box-shadow:0 0 25px #00f2ff;
}

textarea{
width:100%;
height:140px;
background:#0b0f1a;
color:white;
border:1px solid #00f2ff;
padding:15px;
}

.result{
margin-top:20px;
background:#0b0f1a;
padding:20px;
border:1px solid #00f2ff;
min-height:120px;
}

#graph{
height:400px;
border:1px solid #00f2ff;
}

</style>

</head>

<body>

<div class="container">

<div class="title">
OpenGradient Neon AI Terminal
</div>

<div class="panel">

<div id="wallet">Wallet: not connected</div>
<div id="balance">Balance: -</div>

<button onclick="connect()">Connect Wallet</button>
<button onclick="disconnect()">Disconnect</button>
<button onclick="loadBalance()">Refresh Balance</button>
<button onclick="approve()">Approve OPG</button>

</div>

<div class="panel">

<h3>💧 Faucet</h3>

<button onclick="getETH()">Get ETH</button>
<button onclick="getOPG()">Get OPG</button>

</div>

<div class="panel">

<h3>AI Playground</h3>

<textarea id="prompt">
Explain zero knowledge proofs simply
</textarea>

<br>

<button onclick="runModel()">Run Model</button>

<div class="result" id="result">
Model output...
</div>

</div>

<div class="panel">

<h3>🌐 AI Model Network</h3>

<div id="graph"></div>

</div>

</div>

<script>

let provider
let signer
let account

const OPG =
"0x240b09731D96979f50B2C649C9CE10FcF9C7987F"

const PERMIT2 =
"0x000000000022D473030F116dDEE9F6B43aC78BA3"

async function connect(){

if(!window.ethereum){
alert("Install MetaMask")
return
}

const accounts = await window.ethereum.request({
method:"eth_requestAccounts"
})

account = accounts[0]

provider = new ethers.providers.Web3Provider(window.ethereum)
signer = provider.getSigner()

document.getElementById("wallet").innerText =
"Wallet: "+account

await loadBalance()

}

function disconnect(){

account=null
provider=null
signer=null

document.getElementById("wallet").innerText="Wallet: disconnected"

}

async function loadBalance(){

if(!provider) return

const ethBalance =
await provider.getBalance(account)

const eth =
ethers.utils.formatEther(ethBalance)

const token =
new ethers.Contract(
OPG,
["function balanceOf(address owner) view returns(uint256)"],
provider
)

const raw =
await token.balanceOf(account)

const opg =
ethers.utils.formatUnits(raw,18)

document.getElementById("balance").innerText =
"ETH: "+eth+" | OPG: "+opg

}

async function approve(){

if(!signer){
alert("Connect wallet first")
return
}

const token =
new ethers.Contract(
OPG,
["function approve(address spender,uint256 amount) public returns(bool)"],
signer
)

const amount =
ethers.utils.parseUnits("1000",18)

const tx =
await token.approve(PERMIT2, amount)

await tx.wait()

alert("Approve confirmed")

}

async function runModel(){

const prompt =
document.getElementById("prompt").value

const res =
await fetch("/chat",{
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

function getETH(){
window.open("https://www.coinbase.com/faucets/base-sepolia-faucet")
}

function getOPG(){
window.open("https://hub.opengradient.ai/faucet")
}

</script>

<script>

const models = [
"gpt-4o",
"gemini-2.5-pro",
"claude-3.7-sonnet",
"grok-4-fast",
"o4-mini",
"gemini-2.5-flash"
]

const scene = new THREE.Scene()
const camera = new THREE.PerspectiveCamera(75,window.innerWidth/400,0.1,1000)
const renderer = new THREE.WebGLRenderer()

renderer.setSize(window.innerWidth,400)
document.getElementById("graph").appendChild(renderer.domElement)

camera.position.z = 5

const nodes=[]

models.forEach((m,i)=>{

const geometry = new THREE.SphereGeometry(0.2)
const material = new THREE.MeshBasicMaterial({color:0x00ffff})
const sphere = new THREE.Mesh(geometry,material)

sphere.position.x = Math.sin(i)*2
sphere.position.y = Math.cos(i)*2

scene.add(sphere)

nodes.push(sphere)

})

function animate(){

requestAnimationFrame(animate)

nodes.forEach((n,i)=>{
n.rotation.x +=0.01
n.rotation.y +=0.01
})

renderer.render(scene,camera)

}

animate()

</script>

</body>
</html>
