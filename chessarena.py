<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Advanced Chess</title>

<style>
body {
    font-family: Arial, sans-serif;
    background: #1e1e2f;
    color: white;
    text-align: center;
}

h1 { margin-bottom: 5px; }

.container {
    display: flex;
    justify-content: center;
    gap: 30px;
    margin-top: 20px;
}

#board {
    display: grid;
    grid-template-columns: repeat(8, 70px);
    border: 4px solid #333;
}

.square {
    width: 70px;
    height: 70px;
    font-size: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}

.white { background: #f0d9b5; }
.black { background: #b58863; }

.selected { outline: 3px solid yellow; }
.move { background: #6fcf97 !important; }
.capture { background: #eb5757 !important; }

.panel {
    width: 200px;
    text-align: left;
}

button {
    padding: 10px;
    margin-top: 10px;
    width: 100%;
    cursor: pointer;
}
</style>
</head>

<body>

<h1>♟️ Advanced Chess</h1>
<p id="status">Turn: White</p>

<div class="container">
    <div id="board"></div>

    <div class="panel">
        <h3>Game Info</h3>
        <p id="info">Select a piece</p>
        <button onclick="resetGame()">Restart</button>
    </div>
</div>

<script>
const board = document.getElementById("board");
const statusText = document.getElementById("status");
const info = document.getElementById("info");

let turn = "white";
let selected = null;
let validMoves = [];

const initialBoard = [
["bR","bN","bB","bQ","bK","bB","bN","bR"],
["bP","bP","bP","bP","bP","bP","bP","bP"],
["","","","","","","",""],
["","","","","","","",""],
["","","","","","","",""],
["","","","","","","",""],
["wP","wP","wP","wP","wP","wP","wP","wP"],
["wR","wN","wB","wQ","wK","wB","wN","wR"]
];

let game = JSON.parse(JSON.stringify(initialBoard));

function pieceSymbol(p) {
    const map = {
        wP:"♙", wR:"♖", wN:"♘", wB:"♗", wQ:"♕", wK:"♔",
        bP:"♟", bR:"♜", bN:"♞", bB:"♝", bQ:"♛", bK:"♚"
    };
    return map[p] || "";
}

function draw() {
    board.innerHTML = "";
    for (let r=0;r<8;r++) {
        for (let c=0;c<8;c++) {
            const sq = document.createElement("div");
            sq.className = "square " + ((r+c)%2===0?"white":"black");
            sq.dataset.r=r; sq.dataset.c=c;

            const piece = game[r][c];
            sq.textContent = pieceSymbol(piece);

            if (selected && selected.r==r && selected.c==c)
                sq.classList.add("selected");

            if (validMoves.some(m=>m.r==r && m.c==c)) {
                if (game[r][c]) sq.classList.add("capture");
                else sq.classList.add("move");
            }

            sq.onclick = () => clickSquare(r,c);
            board.appendChild(sq);
        }
    }
}

function clickSquare(r,c) {
    const piece = game[r][c];

    if (selected && validMoves.some(m=>m.r==r && m.c==c)) {
        game[r][c] = game[selected.r][selected.c];
        game[selected.r][selected.c] = "";

        selected = null;
        validMoves = [];
        turn = turn==="white"?"black":"white";
        updateStatus();
        draw();
        return;
    }

    if (piece && piece[0]===turn[0]) {
        selected = {r,c};
        validMoves = getMoves(r,c);
        draw();
    }
}

function getMoves(r,c) {
    const piece = game[r][c];
    if (!piece) return [];

    const type = piece[1];
    const color = piece[0];
    let moves = [];

    const dirs = {
        N:[[ -2,-1],[-2,1],[-1,-2],[-1,2],[1,-2],[1,2],[2,-1],[2,1]],
        B:[[1,1],[1,-1],[-1,1],[-1,-1]],
        R:[[1,0],[-1,0],[0,1],[0,-1]],
        Q:[[1,1],[1,-1],[-1,1],[-1,-1],[1,0],[-1,0],[0,1],[0,-1]],
        K:[[1,1],[1,-1],[-1,1],[-1,-1],[1,0],[-1,0],[0,1],[0,-1]]
    };

    function inside(r,c){ return r>=0&&r<8&&c>=0&&c<8; }

    if (type==="P") {
        let dir = color==="w"?-1:1;
        if (inside(r+dir,c) && !game[r+dir][c])
            moves.push({r:r+dir,c});
        if ((r===6&&color==="w")||(r===1&&color==="b")) {
            if (!game[r+dir][c] && !game[r+2*dir][c])
                moves.push({r:r+2*dir,c});
        }
        for (let dc of [-1,1]) {
            if (inside(r+dir,c+dc) && game[r+dir][c+dc] && game[r+dir][c+dc][0]!==color)
                moves.push({r:r+dir,c:c+dc});
        }
    }

    if (type==="N") {
        dirs.N.forEach(d=>{
            let nr=r+d[0], nc=c+d[1];
            if (inside(nr,nc) && (!game[nr][nc] || game[nr][nc][0]!==color))
                moves.push({r:nr,c:nc});
        });
    }

    if (["B","R","Q"].includes(type)) {
        dirs[type].forEach(d=>{
            let nr=r, nc=c;
            while(true){
                nr+=d[0]; nc+=d[1];
                if (!inside(nr,nc)) break;
                if (!game[nr][nc]) moves.push({r:nr,c:nc});
                else {
                    if (game[nr][nc][0]!==color)
                        moves.push({r:nr,c:nc});
                    break;
                }
            }
        });
    }

    if (type==="K") {
        dirs.K.forEach(d=>{
            let nr=r+d[0], nc=c+d[1];
            if (inside(nr,nc) && (!game[nr][nc] || game[nr][nc][0]!==color))
                moves.push({r:nr,c:nc});
        });
    }

    return moves;
}

function updateStatus() {
    statusText.textContent = "Turn: " + (turn==="white"?"White":"Black");
}

function resetGame() {
    game = JSON.parse(JSON.stringify(initialBoard));
    selected = null;
    validMoves = [];
    turn = "white";
    updateStatus();
    draw();
}

draw();
</script>

</body>
</html>