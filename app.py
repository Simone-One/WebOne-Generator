from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import uuid
import os
from blocchi import get_lista_blocchi
from html_generator import generate_html
from pathlib import Path

app = Flask(__name__)
app.secret_key = "1ae416544d2584432473aef6r5237583"
BASE_DIR = Path(__file__).resolve().parent

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/selezione")
def selezione():
    return render_template("selezione.html")

@app.route("/start/<layout>")
def start(layout):
    session["layout"] = layout
    if "lista_blocchi" not in session:
        lista_blocchi_temporanea = get_lista_blocchi(layout)
        session["lista_blocchi"] = lista_blocchi_temporanea
    if "colore_sfondo" not in session:
        colore_sfondo_temporaneo = "#ffffff"
        session["colore_sfondo"] = colore_sfondo_temporaneo
    return render_template(f"{layout}.html", blocchi=session["lista_blocchi"], colore_sfondo=session["colore_sfondo"])

@app.route("/aggiungi", methods=["POST"])
def aggiungi():
    tipo = request.form.get("tipo_blocco")
    
    if tipo == "titolo":
        nuovo_blocco = {
            "id": str(uuid.uuid4()),
            "tipo": tipo,
            "contenuto": "Scrivi qui il tuo titolo..."
        }
    elif tipo == "testo":
        nuovo_blocco = {
            "id": str(uuid.uuid4()),
            "tipo": tipo,
            "contenuto": "Scrivi qui il tuo testo..."
        }
    elif tipo == "immagine":
        # 1. Python prende il file dall'input HTML chiamato "file_immagine"
        file = request.files.get("file_immagine")

        if file:
            # 2. Definiamo dove salvare il file sul tuo PC (dentro static/uploads/)
            cartella_destinazione = os.path.join('static', 'uploads')
            
            # Creiamo la cartella se non esiste ancora
            if not os.path.exists(cartella_destinazione):
                os.makedirs(cartella_destinazione)
                
            percorso_salvataggio = os.path.join(cartella_destinazione, file.filename)
            
            # 3. Salva fisicamente il file sul tuo computer
            file.save(percorso_salvataggio)
            
            # 4. Il contenuto del blocco diventa il percorso web dell'immagine
            contenuto_blocco = f"/static/uploads/{file.filename}"

            nuovo_blocco = {
                "id": str(uuid.uuid4()),
                "tipo": tipo,
                "contenuto": contenuto_blocco
            }
    else:
        print("Questo non doveva succedere")

    lista_temporanea = session["lista_blocchi"]
    lista_temporanea.append(nuovo_blocco)
    session["lista_blocchi"] = lista_temporanea
    
    return redirect(url_for("start", layout=session["layout"]))

@app.route("/salva", methods=["POST"])
def salva():
    id_da_modificare = request.form.get("id_blocco")
    testo_aggiornato = request.form.get("nuovo_testo")
    file_immagine = request.files.get("file_immagine")
    
    lista_temporanea = session["lista_blocchi"]
    
    for blocco in lista_temporanea:
        if blocco["id"] == id_da_modificare:
            # Se c'è un file caricato (per blocchi immagine)
            if file_immagine and file_immagine.filename:
                cartella_destinazione = os.path.join('static', 'uploads')
                if not os.path.exists(cartella_destinazione):
                    os.makedirs(cartella_destinazione)
                percorso_salvataggio = os.path.join(cartella_destinazione, file_immagine.filename)
                file_immagine.save(percorso_salvataggio)
                blocco["contenuto"] = f"/static/uploads/{file_immagine.filename}"
            else:
                # Per blocchi testo e titolo
                blocco["contenuto"] = testo_aggiornato
                
            if blocco["tipo"] == "testo" and request.form.get("colore_testo"):
                blocco["colore_testo"] = request.form.get("colore_testo")
            if blocco["tipo"] == "titolo" and request.form.get("colore_titolo"):
                blocco["colore_titolo"] = request.form.get("colore_titolo")
            break
            
    session["lista_blocchi"] = lista_temporanea
    
    return redirect(url_for("start", layout=session["layout"]))

@app.route("/muovi", methods=["POST"])
def muovi():
    id_blocco = request.form.get("id_blocco")
    direzione = request.form.get("direzione")
    
    lista_temporanea = session["lista_blocchi"]
    
    indice_attuale = None
    for i, blocco in enumerate(lista_temporanea):
        if blocco["id"] == id_blocco:
            indice_attuale = i
            break
            
    if indice_attuale is not None:
        if direzione == "su" and indice_attuale > 0:
            # Scambia il blocco attuale con quello precedente (indice - 1)
            lista_temporanea[indice_attuale], lista_temporanea[indice_attuale - 1] = \
                lista_temporanea[indice_attuale - 1], lista_temporanea[indice_attuale]
                
        elif direzione == "giu" and indice_attuale < len(lista_temporanea) - 1:
            # Scambia il blocco attuale con quello successivo (indice + 1)
            lista_temporanea[indice_attuale], lista_temporanea[indice_attuale + 1] = \
                lista_temporanea[indice_attuale + 1], lista_temporanea[indice_attuale]
                
    session["lista_blocchi"] = lista_temporanea
    return redirect(url_for("start", layout=session["layout"]))

@app.route("/elimina", methods=["POST"])
def elimina():
    id_da_cancellare = request.form.get("id_blocco")
    
    lista_temporanea = session["lista_blocchi"]
    
    for blocco in lista_temporanea:
        if blocco["id"] == id_da_cancellare:
            lista_temporanea.remove(blocco)
            break
            
    session["lista_blocchi"] = lista_temporanea
    
    return redirect(url_for("start", layout=session["layout"]))

@app.route("/svuota", methods=["POST"])
def svuota():
    del session["lista_blocchi"]
    return redirect(url_for("start", layout=session["layout"]))

@app.route("/pubblica")
def pubblica():
    if "lista_blocchi" not in session:
        session["lista_blocchi"] = []
    return render_template("pubblica.html", blocchi=session["lista_blocchi"], layout=session["layout"], colore_sfondo=session["colore_sfondo"])

@app.route("/imposta_sfondo", methods=["POST"])
def imposta_sfondo():
    session["colore_sfondo"] = request.form.get("colore")
    print(f"colore scelto: {session["colore_sfondo"]}")
    return redirect(url_for("start", layout=session["layout"]))

@app.route("/torna_home")
def torna_home():
    del session["lista_blocchi"]
    del session["layout"]
    return redirect(url_for("hello_world"))

@app.route("/download")
def download():
    lista_blocchi_temporanea = session["lista_blocchi"]
    generate_html(lista_blocchi_temporanea)
    return send_from_directory(
        BASE_DIR,
        "download.html",
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)