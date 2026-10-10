from pathlib import Path
from uuid import uuid4

from flask import Flask, render_template, request
from PIL import Image, UnidentifiedImageError
from rembg import new_session, remove

app = Flask(__name__)

# Mantém o modelo isnet-general-use que você prefere
print("Carregando modelo de IA (isnet-general-use)...")
MODELO_SESSAO = new_session("isnet-general-use")
print("Modelo carregado com sucesso!")

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "static" / "resultados"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Limite de upload: 15 MB
app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    erro = None

    if request.method == "POST":
        arquivo = request.files.get("imagem")

        if not arquivo or not arquivo.filename:
            erro = "Escolha uma imagem antes de continuar."
        elif Path(arquivo.filename).suffix.lower() not in ALLOWED_EXTENSIONS:
            erro = "Formato não suportado. Envie PNG, JPG, JPEG ou WEBP."
        else:
            try:
                # Abre a imagem enviada
                imagem = Image.open(arquivo.stream).convert("RGBA")

                # ECONOMIA DE RAM: Redimensiona imagens gigantes antes da IA processar
                MAX_TAMANHO = (1280, 1280)
                imagem.thumbnail(MAX_TAMANHO, Image.Resampling.LANCZOS)

                # Remove o fundo usando o modelo isnet-general-use
                imagem_sem_fundo = remove(imagem, session=MODELO_SESSAO)

                nome_saida = f"{uuid4().hex}.png"
                caminho_saida = UPLOAD_DIR / nome_saida
                imagem_sem_fundo.save(caminho_saida, format="PNG")

                resultado = f"/static/resultados/{nome_saida}"
            except (UnidentifiedImageError, OSError):
                erro = "Não foi possível ler essa imagem. Tente outro arquivo."
            except Exception as e:
                app.logger.exception("Erro ao remover o fundo")
                erro = f"Erro ao processar imagem: {type(e).__name__}: {e}"

    return render_template("index.html", resultado=resultado, erro=erro)


@app.errorhandler(413)
def arquivo_muito_grande(_error):
    return render_template(
        "index.html",
        resultado=None,
        erro="A imagem ultrapassa o limite de 15 MB."
    ), 413


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)