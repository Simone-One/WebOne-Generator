import uuid

def get_lista_blocchi(layout):
    if layout == "layout1":
        lista_blocchi = [
            { 
                "id": str(uuid.uuid4()),
                "tipo": "titolo",
                "contenuto": "Scrivi qui il tuo titolo..."
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "testo",
                "contenuto": "Scrivi qui il tuo testo..."
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "immagine",
                "contenuto": "/static/uploads/placeholder.png"
            },
        ]
        return lista_blocchi
    if layout == "layout2":
        lista_blocchi = [
            { 
                "id": str(uuid.uuid4()),
                "tipo": "titolo",
                "contenuto": "Scrivi qui il tuo titolo..."
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "testo",
                "contenuto": "Scrivi qui il tuo testo..."
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "immagine",
                "contenuto": "/static/uploads/placeholder.png"
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "testo",
                "contenuto": "Scrivi qui il tuo testo..."
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "immagine",
                "contenuto": "/static/uploads/placeholder.png"
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "testo",
                "contenuto": "Scrivi qui il tuo testo..."
            }
        ]
        return lista_blocchi