from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, session
import uuid
import os
from blocchi import get_lista_blocchi

app = Flask(__name__)
app.secret_key = "1ae416544d6589449473aaf6r5237583"

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
    
    lista_temporanea = session.get("lista_blocchi", [])
    nuova_lista = []
    
    for blocco in lista_temporanea:
        nuovo_blocco = blocco.copy()
        if nuovo_blocco["id"] == id_da_modificare:
            # Se c'è un file caricato (per blocchi immagine)
            if file_immagine and file_immagine.filename:
                cartella_destinazione = os.path.join('static', 'uploads')
                if not os.path.exists(cartella_destinazione):
                    os.makedirs(cartella_destinazione)
                percorso_salvataggio = os.path.join(cartella_destinazione, file_immagine.filename)
                file_immagine.save(percorso_salvataggio)
                nuovo_blocco["contenuto"] = f"/static/uploads/{file_immagine.filename}"
            elif testo_aggiornato is not None:
                # Per blocchi testo e titolo
                nuovo_blocco["contenuto"] = testo_aggiornato

            if nuovo_blocco["tipo"] == "immagine":
                nuovo_blocco["standalone"] = True if request.form.get("standalone") == "on" else False
                
            if nuovo_blocco["tipo"] == "testo" and request.form.get("colore_testo"):
                nuovo_blocco["colore_testo"] = request.form.get("colore_testo")
            if nuovo_blocco["tipo"] == "titolo" and request.form.get("colore_titolo"):
                nuovo_blocco["colore_titolo"] = request.form.get("colore_titolo")
        nuova_lista.append(nuovo_blocco)
            
    session["lista_blocchi"] = nuova_lista
    
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
    session["lista_blocchi"] = []
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


if __name__ == "__main__":
    app.run(debug=True)