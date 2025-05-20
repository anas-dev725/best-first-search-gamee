const gridSize = 10;
const grid = document.getElementById("grid");
let cells = [];
let start = [0, 0];
let target = [9, 9];
let walls = new Set();

// Build grid
for (let row = 0; row < gridSize; row++) {
  for (let col = 0; col < gridSize; col++) {
    const cell = document.createElement("div");
    cell.classList.add("cell");
    grid.appendChild(cell);

    cell.addEventListener("click", () => toggleWall(row, col));
    cell.addEventListener("contextmenu", (e) => {
      e.preventDefault();
      setStartOrTarget(row, col);
    });

    cells.push(cell);
  }
}

function index(row, col) {
  return row * gridSize + col;
}

function cellKey(row, col) {
  return `${row},${col}`;
}

function toggleWall(row, col) {
  const key = cellKey(row, col);
  const i = index(row, col);
  const cell = cells[i];

  if (cell.classList.contains("start") || cell.classList.contains("target")) return;

  if (walls.has(key)) {
    walls.delete(key);
    cell.classList.remove("wall");
  } else {
    walls.add(key);
    cell.classList.add("wall");
  }
}

function setStartOrTarget(row, col) {
  const i = index(row, col);
  const key = cellKey(row, col);
  const cell = cells[i];

  if (walls.has(key)) return;

  if (!startSet) {
    start = [row, col];
    cell.classList.add("start");
    startSet = true;
  } else if (!targetSet) {
    target = [row, col];
    cell.classList.add("target");
    targetSet = true;
  }
}

let startSet = true;
let targetSet = true;

cells[index(...start)].classList.add("start");
cells[index(...target)].classList.add("target");

function runBFS() {
  const visited = Array.from({ length: gridSize }, () => Array(gridSize).fill(false));
  const prev = Array.from({ length: gridSize }, () => Array(gridSize).fill(null));
  const queue = [start];
  visited[start[0]][start[1]] = true;

  const directions = [
    [0, 1],
    [1, 0],
    [0, -1],
    [-1, 0],
  ];

  const interval = setInterval(() => {
    if (queue.length === 0) {
      clearInterval(interval);
      alert("No path found.");
      return;
    }

    const [r, c] = queue.shift();
    if (r === target[0] && c === target[1]) {
      clearInterval(interval);
      reconstructPath(prev, r, c);
      return;
    }

    for (let [dr, dc] of directions) {
      const nr = r + dr;
      const nc = c + dc;
      const key = cellKey(nr, nc);

      if (
        nr >= 0 && nc >= 0 && nr < gridSize && nc < gridSize &&
        !visited[nr][nc] && !walls.has(key)
      ) {
        visited[nr][nc] = true;
        prev[nr][nc] = [r, c];
        queue.push([nr, nc]);
        const cellIdx = index(nr, nc);
        if (!cells[cellIdx].classList.contains("target")) {
          cells[cellIdx].classList.add("visited");
        }
      }
    }
  }, 50);
}

function reconstructPath(prev, r, c) {
  let path = [];
  while (prev[r][c]) {
    path.push([r, c]);
    [r, c] = prev[r][c];
  }
  for (let [row, col] of path) {
    const i = index(row, col);
    if (!cells[i].classList.contains("start") && !cells[i].classList.contains("target")) {
      cells[i].classList.remove("visited");
      cells[i].classList.add("path");
    }
  }
}

function resetGrid() {
  cells.forEach(cell => {
    cell.className = "cell";
  });
  walls.clear();
  start = [0, 0];
  target = [9, 9];
  startSet = true;
  targetSet = true;
  cells[index(...start)].classList.add("start");
  cells[index(...target)].classList.add("target");
}
