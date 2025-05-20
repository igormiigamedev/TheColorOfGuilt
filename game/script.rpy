## Arquivo principal Ren'Py: script.rpy

label start:
    call tela_inicial

label tela_inicial:
    scene bg tela_inicial
    menu:
        "Novo Jogo":
            call tela_casos
            # call tela_perguntas_personagem("julien", "tela_inicial")

label tela_casos:
    scene bg tela_casos
    "Escolha um caso para começar."
    menu:
        "Caso 1 - O Vulto na Névoa":
            call tela_introducao
        "Caso 2 (Bloqueado)":
            "Novos casos em breve."
            jump tela_casos
        "Caso 3 (Bloqueado)":
            "Novos casos em breve."
            jump tela_casos

label tela_introducao:
    scene bg tela_introducao
    $ tempo_jogo = 0
    $ perguntas_feitas = 0
    $ pontuacao = 100
    "Você é um detetive. Analise as pinturas e depoimentos para encontrar o culpado."
    "Pontuação: "
    "   . Tempo: Após 10 minutos passados, -1 ponto a cada 2 minutos; "
    "   . Perguntas: Após 5 perguntas feitas no total, -1 ponto a cada pergunta."
    menu:
        "Avançar":
            call tela_apresentacao_caso

label tela_apresentacao_caso:
    scene bg apresentacao_caso
    "A vítima foi encontrada em seu ateliê. Não há sinais de arrombamento."
    "Julien Armand, pintor vizinho, deixou 8 pinturas com possíveis pistas."
    menu:
        "Avançar":
            call tela_suspeitos(0)

label tela_suspeitos(index):
    if index >= 5:
        call tela_pinturas(0)
    else:
        $ s = suspeitos[index]
        scene bg apresentacao_suspeito
        show s['foto']
        "Nome: [s['nome']]
        Histórico: [s['descricao']]"
        menu:
            "Avançar":
                call tela_suspeitos(index + 1)
            "Voltar":
                if index > 0:
                    call tela_suspeitos(index - 1)
                else:
                    call tela_apresentacao_caso

label tela_pinturas(index):
    $ total_pinturas = len(pinturas)
    if index >= total_pinturas:
        call tela_galeria
    else:
        $ p = pinturas[index]
        scene bg pintura
        show p['imagem']
        "[p['descricao']]"
        "Pintor: Julien Armand"
        menu:
            "Avançar":
                call tela_pinturas(index + 1)
            "Voltar":
                if index > 0:
                    call tela_pinturas(index - 1)
                else:
                    call tela_suspeitos(4)
            "Falar com Julien":
                call tela_perguntas_personagem("julien", "NULL")
                call tela_pinturas(index)

label tela_galeria:
    scene bg galeria
    "Escolha uma pintura para revisar."
    # Mostrar miniaturas e permitir navegação
    menu:
        "Ver Suspeitos":
            call tela_todos_suspeitos

label tela_todos_suspeitos:
    scene bg suspeitos
    "Escolha um suspeito para interrogar ou prender."
    menu:
        "Ver Pinturas":
            call tela_galeria
        # Loop para cada suspeito
        # Exemplo:
        "Interrogar Suspeito 1":
            call tela_perguntas_personagem("s1", "tela_todos_suspeitos")
        "Prender Suspeito 1":
            call tela_prender("s1")
        # Repetir para s2, s3...

label tela_perguntas_personagem(id, voltar_para):
    $ personagem = personagens[id]
    scene bg perguntas
    "Perguntas para [personagem['nome']]"

    if perguntas_feitas >= 5:
        "Atenção: essa pergunta custará pontos."

    $ total_perguntas = len(personagem['perguntas'])

    python:
        menu_opcoes = []

        for i in range(total_perguntas):
            pergunta_texto = personagem['perguntas'][i]
            menu_opcoes.append((pergunta_texto, i))

        menu_opcoes.append(("Voltar", "voltar"))

        escolha = renpy.display_menu(menu_opcoes)

    if escolha == "voltar":
        # jump expression voltar_para
        # $ label_name, arg = voltar_para
        if voltar_para == "NULL":
            return
        else:
            jump expression voltar_para
    else:
        $ perguntas_feitas += 1
        call tela_resposta(id, escolha)
        call tela_perguntas_personagem(id, voltar_para)  # Retorna ao menu após responder
    return


label tela_resposta(id, q):
    $ resposta = personagens[id]['respostas'][q]
    "[resposta]"
    # menu:
    #     "Voltar para perguntas":
    #         call tela_perguntas_personagem(id, voltar_para)
    return

label tela_prender(id):
    $ suspeito = personagens[id]
    scene bg prender
    "Você está prestes a prender [suspeito['nome']]. Deseja confirmar?"
    menu:
        "Confirmar Prisão":
            call verificar_prisao(id)
        "Voltar":
            call tela_todos_suspeitos

label verificar_prisao(id):
    if id == culpado:
        call tela_vitoria
    else:
        call tela_derrota

label tela_vitoria:
    scene bg vitoria
    $ pontuacao -= calcular_penalidade()
    "Parabéns! Você solucionou o caso. Pontuação final: [pontuacao]"
    return

label tela_derrota:
    scene bg derrota
    "Você prendeu a pessoa errada."
    menu:
        "Reiniciar caso":
            call tela_casos
        "Ver solução":
            call tela_solucao

label tela_solucao:
    scene bg solucao
    "Explicação passo a passo do caso."
    return

init python:
    tempo_jogo = 0
    perguntas_feitas = 0
    pontuacao = 10
    culpado = "s3"  # exemplo

    def calcular_penalidade():
        penalidade_tempo = max(0, (tempo_jogo - 10) // 2)
        penalidade_perguntas = max(0, perguntas_feitas - 5)
        return penalidade_tempo + penalidade_perguntas

    suspeitos = [
        {"nome": "Suspeito 1", "descricao": "Histórico 1", "foto": "suspeito1.png"},
        {"nome": "Suspeito 2", "descricao": "Histórico 2", "foto": "suspeito2.png"},
        {"nome": "Suspeito 3", "descricao": "Histórico 3", "foto": "suspeito3.png"},
        {"nome": "Suspeito 4", "descricao": "Histórico 4", "foto": "suspeito4.png"},
        {"nome": "Suspeito 5", "descricao": "Histórico 5", "foto": "suspeito5.png"},
    ]

    pinturas = [
        {"imagem": "pintura1.jpg", "descricao": "Descrição 1"},
        {"imagem": "pintura2.jpg", "descricao": "Descrição 2"},
        {"imagem": "pintura3.jpg", "descricao": "Descrição 3"},
        {"imagem": "pintura4.jpg", "descricao": "Descrição 4"},
        {"imagem": "pintura5.jpg", "descricao": "Descrição 5"},
        {"imagem": "pintura6.jpg", "descricao": "Descrição 6"},
        {"imagem": "pintura7.jpg", "descricao": "Descrição 7"},
        {"imagem": "pintura8.jpg", "descricao": "Descrição 7"},
        # até pintura8
    ]

    personagens = {
        "julien": {
            "nome": "Julien Armand",
            "perguntas": [
                "Pergunta 1", "Pergunta 2", "Pergunta 3", "Pergunta 4", "Pergunta 5"
            ],
            "respostas": [
                "Resposta 1", "Resposta 2", "Resposta 3", "Resposta 4", "Resposta 5"
            ]
        },
        "s1": {
            "nome": "Suspeito 1",
            "perguntas": [
                "Pergunta 1", "Pergunta 2", "Pergunta 3", "Pergunta 4", "Pergunta 5"
            ],
            "respostas": ["Resp 1", "Resp 2", "Resp 3", "Resp 4", "Resp 5"]
        },
        # etc para s2, s3, s4, s5
    }
