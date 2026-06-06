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
                "contenuto": "Scrivi qui il tuo titolo..."
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "immagine",
                "contenuto": "/static/uploads/traffico.jpg"
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
                "contenuto": "Scrivi qui il tuo titolo..."
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "immagine",
                "contenuto": "/static/uploads/traffico.jpg"
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "testo",
                "contenuto": "Scrivi qui il tuo titolo..."
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "immagine",
                "contenuto": "/static/uploads/traffico.jpg"
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "testo",
                "contenuto": "Scrivi qui il tuo titolo..."
            }
        ]
        return lista_blocchi
    
def check_lista(lista_blocchi):
    lista_blocchi1 = [
            { 
                "id": str(uuid.uuid4()),
                "tipo": "titolo",
                "contenuto": "Scrivi qui il tuo titolo..."
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "testo",
                "contenuto": "Scrivi qui il tuo titolo..."
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "immagine",
                "contenuto": "/static/uploads/traffico.jpg"
            },
        ]
    lista_blocchi2 = [
            { 
                "id": str(uuid.uuid4()),
                "tipo": "titolo",
                "contenuto": "Scrivi qui il tuo titolo..."
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "testo",
                "contenuto": "Scrivi qui il tuo titolo..."
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "immagine",
                "contenuto": "/static/uploads/traffico.jpg"
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "testo",
                "contenuto": "Scrivi qui il tuo titolo..."
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "immagine",
                "contenuto": "/static/uploads/traffico.jpg"
            },
            { 
                "id": str(uuid.uuid4()),
                "tipo": "testo",
                "contenuto": "Scrivi qui il tuo titolo..."
            }
        ]
    if lista_blocchi == lista_blocchi1 or lista_blocchi == lista_blocchi2:
        lista_blocchi = []
        return lista_blocchi
    return lista_blocchi