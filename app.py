import os, json
from flask import Flask, render_template, request, redirect, url_for, flash
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)
app.secret_key = "qsf-ski-cakung"  # bebas

# ====== Google Sheets auth (Service Account via ENV) ======
def make_gspread_client():
    creds_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
    return gspread.authorize(creds)

def get_worksheet():
    gc = make_gspread_client()
    sheet_id = os.environ["SHEET_ID"]
    sh = gc.open_by_key(sheet_id)
    try:
        ws = sh.worksheet("Sheet1")
    except gspread.WorksheetNotFound:
        ws = sh.sheet1
    return ws

@app.route("/", methods=["GET"])
def index():
    ws = get_worksheet()
    data = ws.get_all_values()
    return render_template("index.html", data=data)

@app.route("/submit", methods=["POST"])
def submit():
    ws = get_worksheet()
    no_po = request.form.get("no_po", "")
    tgl_tiba = request.form.get("tgl_tiba", "")
    tgl_bongkar = request.form.get("tgl_bongkar", "")
    item_po = request.form.get("item_po", "")
    item_bongkar = request.form.get("item_bongkar", "")
    jml_sampling = request.form.get("jml_sampling", "")
    berat_kotor = request.form.get("berat_kotor", "")
    berat_bersih = request.form.get("berat_bersih", "")

    fields = ["kotor","layu","keriput","white_spot","tertusuk","pecah","berjamur","black_spot","memar","busuk"]
    hasil_list = [request.form.get(f, "0") for f in fields]

    row = [no_po, tgl_tiba, tgl_bongkar, item_po, item_bongkar, jml_sampling, berat_kotor, berat_bersih] + hasil_list
    ws.append_row(row)
    flash("Data tersimpan!")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
