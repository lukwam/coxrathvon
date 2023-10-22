"""CoxRathvon app."""
import datetime
import json
import os
import shutil

from flask import Flask
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import send_file

from google.oauth2 import service_account
from google.cloud import firestore
from google.cloud import secretmanager
from google.cloud import storage

from puzzle import Puzzle

app = Flask(__name__)


def generate_signed_url(bucket_name, object_name, credentials):
    """Generate a signed url for an object."""
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    if not blob.exists():
        return None
    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=60),
        method="GET",
    )
    return url


def get_collection(collection, project=None):
    """Return a collection from firestore."""
    client = firestore.Client(project=project)
    items = []
    for doc in client.collection(collection).stream():
        item = doc.to_dict()
        item["id"] = doc.id
        items.append(item)
    return items


def get_data():
    """Return the data from the data.json file."""
    filename = "/tmp/data.json"
    if not os.path.isfile(filename):
        shutil.copy("data.json", filename)
    with open(filename) as f:
        data = json.load(f)
    return data


def get_object(bucket_name, object_name):
    """Return the given object from the given bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    if not blob.exists():
        return None
    return blob.download_as_bytes()


def get_puzzle_by_id(id):
    """Return the puzzle by id."""
    puzzles = get_puzzles_dict()
    return puzzles.get(id)


def get_puzzles_dict(key="id"):
    """Return the puzzles dictionary."""
    data = get_data()
    puzzles = {}
    for item in data:
        k = item[key]
        puzzles[k] = item
    return puzzles


def get_secret(secret_name):
    """Get secret from the secret manager."""
    secret_manager = secretmanager.SecretManagerServiceClient()
    name = f"projects/{os.environ['GOOGLE_CLOUD_PROJECT']}/secrets/{secret_name}/versions/latest"
    response = secret_manager.access_secret_version(
        request={"name": name}
    )
    return response.payload.data.decode("UTF-8")


def prepare_puzzle(id):
    """Prepare a single puzzle."""
    puzzle = get_puzzle_by_id(id)
    if not puzzle:
        return None

    hexgrid = puzzle.get("hexgrid", {})
    if not hexgrid:
        return None

    # prepare puzzle data
    hexgrid["clues"] = hexgrid["clue_groups"]
    hexgrid["date"] = datetime.datetime.strptime(hexgrid["date"], "%Y-%m-%d")
    del hexgrid["clue_groups"]
    del hexgrid["id"]

    try:
        hex = Puzzle(hexgrid)
    except Exception as error:
        print(f"ERROR: Failed to load puzzle: {error}")
        return redirect(f"/puzzles/{id}")

    return hex


def render_theme(body, **kwargs):
    """Render the theme."""
    return render_template(
        "theme.html",
        body=body,
        **kwargs,
    )


@app.route("/")
def index():
    """Display the main index."""
    puzzles = get_data()
    puzzles = sorted(puzzles, key=lambda x: x["date"], reverse=True)
    body = render_template(
        "index.html",
        puzzles=puzzles,
    )
    return render_theme(body)


@app.route("/admin")
def admin():
    """Display the admin index."""
    body = render_template("admin.html")
    return render_theme(body)


@app.route("/puzzles/<id>")
def puzzle_page(id):
    """Display an indidivual puzzle."""
    puzzle = get_puzzle_by_id(id)
    if not puzzle:
        return redirect("/")

    # get service account key and create credentials
    service_account_info = json.loads(get_secret("appengine-sa-key"))
    credentials = service_account.Credentials.from_service_account_info(service_account_info)

    pub = puzzle["publication"]

    # generate signed url for the puzzle image
    image_name = f"{pub}/{id}_puzzle.png"
    image_url = generate_signed_url(
        bucket_name="lukwam-hex-archive-images",
        object_name=image_name,
        credentials=credentials,
    )

    # generate signed url for the solution image
    solution_name = f"{pub}/{id}_solution.png"
    solution_url = generate_signed_url(
        bucket_name="lukwam-hex-archive-images",
        object_name=solution_name,
        credentials=credentials,
    )

    # generate signed url for the solution image
    # pdf_name = f"{pub}/{id}_puzzle.pdf"
    # pdf_url = generate_signed_url(
    #     bucket_name="lukwam-hex-archive",
    #     object_name=pdf_name,
    #     credentials=credentials,
    # )

    # fix the date string to be an actual date
    puzzle["date"] = datetime.datetime.strptime(puzzle["date"], "%Y-%m-%d")

    # generate the body
    body = render_template(
        "puzzle.html",
        puzzle=puzzle,
        image_url=image_url,
        # pdf_url=pdf_url,
        solution_url=solution_url,
    )
    return render_theme(body, title=puzzle["title"])


@app.route("/puzzles/<id>/pdf")
def puzzle_pdf(id):
    """Return the pdf for the given puzzle."""
    puzzle = get_puzzle_by_id(id)
    if not puzzle:
        return redirect("/")
    date = puzzle["date"]
    pub = puzzle["publication"]
    title = puzzle["title"]

    object_name = f"{pub}/{id}_puzzle.pdf"

    if request.args.get("download"):
        image_binary = get_object("lukwam-hex-archive", object_name)
        response = make_response(image_binary)
        response.headers["Content-Type"] = "image/jpeg"
        response.headers.set(
            "Content-Disposition",
            "attachment",
            filename=f"{date} {title}.pdf",
        )
        return response

    # get service account key and create credentials
    service_account_info = json.loads(get_secret("appengine-sa-key"))
    credentials = service_account.Credentials.from_service_account_info(service_account_info)

    object_url = generate_signed_url(
        bucket_name="lukwam-hex-archive",
        object_name=object_name,
        credentials=credentials,
    )
    return redirect(object_url)


@app.route("/puzzles/<id>/svg")
@app.route("/solutions/<id>/svg")
def puzzle_svg(id):
    """Display an individual puzzle svg."""
    puzzle = prepare_puzzle(id)
    show_solution = False
    if "/solutions/" in request.path:
        show_solution = True
    body = render_template(
        "svg.html",
        id=id,
        puzzle=puzzle,
        show_solution=show_solution,
    )
    headers = {"content-type": "image/svg+xml"}
    return make_response(body, 200, headers)


@app.route("/puzzles/<id>/view")
def puzzle_view(id):
    """Display an individual web puzzle."""
    puzzle = prepare_puzzle(id)
    body = render_template(
        "web.html",
        id=id,
        puzzle=puzzle,
    )
    title = f"{puzzle.title} - Emily Cox & Henry Rathvon"
    return render_theme(body, title=title)


@app.route("/solutions/<id>")
def solution(id):
    """Display an indidivual puzzle solution."""
    puzzle = get_puzzle_by_id(id)
    if not puzzle:
        return redirect("/")

    # get service account key and create credentials
    service_account_info = json.loads(get_secret("appengine-sa-key"))
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    pub = puzzle["publication"]
    image_name = f"{pub}/{id}_solution.png"
    image_url = generate_signed_url(
        bucket_name="lukwam-hex-archive-images",
        object_name=image_name,
        credentials=credentials,
    )
    puzzle["date"] = datetime.datetime.strptime(puzzle["date"], "%Y-%m-%d")
    body = render_template(
        "solution.html",
        puzzle=puzzle,
        image_url=image_url,
    )
    return render_theme(body, title=puzzle["title"])

@app.route("/solutions/<id>/view")
def solution_view(id):
    """Display an individual web solution."""
    puzzle = prepare_puzzle(id)
    body = render_template(
        "web_solution.html",
        id=id,
        puzzle=puzzle,
    )
    title = f"{puzzle.title} - Emily Cox & Henry Rathvon"
    return render_theme(body, title=title)


@app.route("/years")
def years_view():
    """Display the puzzles by year."""
    puzzles = get_data()
    years = {}
    for puzzle in sorted(puzzles, key=lambda x: x["date"]):
        date = puzzle["date"]
        year = date.split("-")[0]
        if year not in years:
            years[year] = []
        years[year].append(puzzle)
    decades = {}
    for year in years:
        decade = year[:3] + "0s"
        if decade not in decades:
            decades[decade] = []
        decades[decade].append(year)
    body = render_template(
        "years.html",
        decades=decades,
        years=years,
    )
    return render_theme(body)


@app.route("/data.json")
def data():
    """Return the data.json file."""
    if os.path.isfile("/tmp/data.json"):
        return send_file("/tmp/data.json")
    return send_file("./data.json")


@app.route("/script.js")
def script():
    """Return the script.js file."""
    return send_file("./script.js")


@app.route("/style.css")
def style():
    """Return the style.css file."""
    return send_file("./style.css")


@app.route("/update")
def update():
    """Update the data."""
    atlantic = 0
    wsj = 0
    puzzles = []

    hexgrids = {}
    for hex in get_collection("hexgrids", project="lukwam-hex"):
        id = hex["id"]
        hexgrids[id] = hex

    for item in get_collection("puzzles", project="lukwam-hex"):
        pub = item.get("pub")
        if pub not in [
            "atlantic",
            "wsj"
        ]:
            continue
        if pub == "atlantic":
            atlantic += 1
        elif pub == "wsj":
            wsj += 1
        date = str(item["date"])[:10]
        year, month, day = date.split("-")
        puzzle = {
            "id": item["id"],
            "title": item["title"],
            "date": date,
            "publication": item["pub"],
            "issue": item.get("issue"),
            "number": item.get("num"),
            "year": int(year),
            "month": int(month),
            "day": int(day),
            "hexgrid": hexgrids.get(item["id"])
        }
        puzzles.append(puzzle)

    print(f"Atlantic: {atlantic}")
    print(f"Wall Street Journal: {wsj}")

    puzzles = sorted(puzzles, key=lambda x: x["date"])
    output = json.dumps(puzzles, indent=2, sort_keys=True)
    f = open("/tmp/data.json", "w")
    f.write(output)
    f.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
