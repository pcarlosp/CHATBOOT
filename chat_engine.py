def responder(mensagem):
    if "oi" in mensagem.lower():
        return "Olá! Em que posso ajudar?"
    elif "ajuda" in mensagem.lower():
        return "Claro! Qual sua dúvida?"
    else:
        return "Mensagem recebida. Alguém da equipe responderá em breve."