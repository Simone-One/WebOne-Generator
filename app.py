from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, session
import uuid
import os

app = Flask(__name__)
app.secret_key = "1ae416548d4589849773aaf6c6237583"

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/selezione")
def selezione():
    return render_template("selezione.html")

@app.route("/start")
def start():
    if "lista_blocchi" not in session:
        session["lista_blocchi"] = []
    return render_template("start.html", blocchi=session["lista_blocchi"])

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
    
    return redirect(url_for("start"))

@app.route("/salva", methods=["POST"])
def salva():
    id_da_modificare = request.form.get("id_blocco")
    testo_aggiornato = request.form.get("nuovo_testo")
    
    lista_temporanea = session["lista_blocchi"]
    
    for blocco in lista_temporanea:
        if blocco["id"] == id_da_modificare:
            blocco["contenuto"] = testo_aggiornato
            break
            
    session["lista_blocchi"] = lista_temporanea
    
    return redirect(url_for("start"))

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
    return redirect(url_for("start"))

@app.route("/elimina", methods=["POST"])
def elimina():
    id_da_cancellare = request.form.get("id_blocco")
    
    lista_temporanea = session["lista_blocchi"]
    
    for blocco in lista_temporanea:
        if blocco["id"] == id_da_cancellare:
            lista_temporanea.remove(blocco)
            break
            
    session["lista_blocchi"] = lista_temporanea
    
    return redirect(url_for("start"))

@app.route("/svuota", methods=["POST"])
def svuota():
    session["lista_blocchi"] = []
    
    return redirect(url_for("start"))

@app.route("/pubblica")
def pubblica():
    if "lista_blocchi" not in session:
        session["lista_blocchi"] = []
    return render_template("pubblica.html", blocchi=session["lista_blocchi"])

@app.route("layout_1")
def layout_1():
    if "lista_blocchi" not in session:
        session["lista_blocchi"] = []
    return render_template("start.html", blocchi=session["lista_blocchi"])

if __name__ == "__main__":
    app.run(debug=True)