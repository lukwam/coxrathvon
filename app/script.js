function get(url) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("GET", url, false);
  xmlHttp.send(null);
  return xmlHttp.responseText;
}

// get json response from an HTTP get request
function getJson(url) {
  var response = get(url);
  return JSON.parse(response);
}

function getPuzzles() {
  return getJson("data.json");
}

// get puzzles by id
function getPuzzlesByID() {
  var ids = {};
  var data = getPuzzles();
  for (var i = 0; i < data.length; i++) {
    var puzzle = data[i];
    ids[puzzle.id] = puzzle;
  }
  return ids;
}

// get puzzles by year
function getPuzzlesByYear() {
  var years = {};
  var data = getPuzzles();
  for (var i = 0; i < data.length; i++) {
    var puzzle = data[i];
    if (!(puzzle.year in years)) {
      years[puzzle.year] = [];
    }
    years[puzzle.year].push(puzzle);
  }
  return years;
}

function loadPuzzles() {
  var data = getJson("data.json");
  console.log("Puzzles: " + data.length);

  var puzzles = document.getElementById("puzzles");
  for (var i = 0; i < data.length; i++) {
    var li = document.createElement("li");
    var puzzle = data[i];

    // add the date div
    var dateDiv = document.createElement("div");
    dateDiv.innerHTML = puzzle.date;
    // dateDiv.classList.add("col-sm-4")
    dateDiv.classList.add("float-start")
    dateDiv.classList.add("me-2")
    dateDiv.classList.add("puzzle-list-date")
    dateDiv.classList.add("text-center")
    // dateDiv.style.whiteSpace = "nowrap";
    li.appendChild(dateDiv);

    // create title link
    var a = document.createElement("a");
    a.href = "/puzzles/" + puzzle.id;
    a.innerHTML = puzzle.title;

    // add the title div
    var titleDiv = document.createElement("div");
    titleDiv.appendChild(a);
    titleDiv.classList.add("puzzle-list-title")
    titleDiv.classList.add("float-start")
    // titleDiv.classList.add("col-sm-8")
    li.appendChild(titleDiv);

    li.id = "puzzle-" + puzzle.id;
    li.classList.add("list-group-item")
    puzzles.appendChild(li);
  }
}
