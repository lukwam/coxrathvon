"""CoxRathvon"""
import datetime
import json
import os

from flask import Flask
from flask import redirect
from flask import render_template
from flask import send_file

from google.oauth2 import service_account
from google.cloud import firestore
from google.cloud import secretmanager
from google.cloud import storage

app = Flask(__name__)


def generate_signed_url(bucket_name, object_name, credentials):
    """Generate a signed url for an object."""
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=15),
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
    with open("data.json") as f:
        data = json.load(f)
    return data


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
def puzzle(id):
    """Display an indidivual puzzle."""
    puzzle = get_puzzle_by_id(id)
    if not puzzle:
        return redirect("/")

    # get service account key and create credentials
    service_account_info = json.loads(get_secret("appengine-sa-key"))
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    pub = puzzle["publication"]
    image_name = f"{pub}/{id}_puzzle.png"
    image_url = generate_signed_url(
        bucket_name="lukwam-hex-archive-images",
        object_name=image_name,
        credentials=credentials,
    )
    puzzle["date"] = datetime.datetime.strptime(puzzle["date"], "%Y-%m-%d")
    body = render_template(
        "puzzle.html",
        puzzle=puzzle,
        image_url=image_url,
    )
    return render_theme(body, title=puzzle["title"])


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


@app.route("/data.json")
def data():
    """Return the data.json file."""
    return send_file("./data.json")


@app.route("/script.js")
def script():
    """Return the script.js file."""
    return send_file("./script.js")


@app.route("/update")
def update():
    """Update the data."""
    atlantic = 0
    wsj = 0
    puzzles = []
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
            "year": int(year),
            "month": int(month),
            "day": int(day),
        }
        puzzles.append(puzzle)

    print(f"Atlantic: {atlantic}")
    print(f"Wall Street Journal: {wsj}")

    puzzles = sorted(puzzles, key=lambda x: x["date"])
    output = json.dumps(puzzles, indent=2, sort_keys=True)
    f = open("data.json", "w")
    f.write(output)
    f.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
