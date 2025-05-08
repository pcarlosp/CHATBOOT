import json
from datetime import datetime

ARQUIVO = "conversas.json"

def carregar_conversas():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def salvar_mensagem(usuario, mensagem, resposta):
    historico = carregar_conversas()
    historico.append({
        "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "usuario": usuario,
        "mensagem": mensagem,
        "resposta": resposta
    })
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=4, ensure_ascii=False)