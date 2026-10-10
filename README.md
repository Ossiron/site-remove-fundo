# Remove Fundo

Site local de demonstração feito com HTML/CSS/JavaScript e Python (Flask).

## 1. Requisitos
- Python 3.10 ou versão compatível com a versão do `rembg` instalada.
- Internet na primeira instalação, para baixar as dependências e possivelmente o modelo do `rembg`.

## 2. Instalação

Abra o terminal dentro desta pasta e execute:

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Depois instale as dependências:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Executar

```bash
python app.py
```

Abra no navegador: http://127.0.0.1:5000

Na primeira execução, o `rembg` pode precisar baixar um modelo de IA, então o primeiro processamento pode demorar.

## Notas
- As imagens enviadas ficam em `static/resultados/`.
- Para uma publicação pública, desative `debug=True`, configure um servidor de produção e implemente uma política de limpeza dos arquivos enviados.
- O limite de upload desta demonstração é 15 MB.
