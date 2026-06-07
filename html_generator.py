def write_into_html(testo):
    with open("download.html", "a", encoding="utf-8") as f:
        f.write(f"\n{testo}")
        return

def generate_html(lista_blocchi):
    with open("download.html", "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>\n<html lang="it">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>WebSite by WebOne Generator</title>\n</head>\n<body>""")

    for blocco in lista_blocchi:
        if blocco["tipo"] == "titolo":
            testo = f"""    <h1 style="font-family: Arial, Helvetica, sans-serif; font-size: 1.4em; border-bottom: 2px solid #333; padding-bottom: 0.6rem; color: {blocco.get("colore_titolo", "#000000")}; margin: 0;">{blocco["contenuto"]}</h1>"""
            write_into_html(testo)
        elif blocco["tipo"] == "testo":
            testo = f"""    <p style="font-family: Arial, Helvetica, sans-serif; font-size: 0.9em; line-height: 1.5; color: {blocco.get("colore_testo", "#000000")}; margin: 0.6rem 0;">{blocco["contenuto"]}</p>"""
            write_into_html(testo)
        elif blocco["tipo"] == "immagine":
            testo = f"""    <img src="{blocco["contenuto"]}" alt="Immagine" style="width: 100%; height: auto; display: block; border-radius: 6px; margin: 0.6rem 0;">"""
            write_into_html(testo)
    write_into_html("</body>\n</html>")
    return