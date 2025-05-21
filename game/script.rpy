## Arquivo principal Ren'Py: script.rpy

label start:
    call tela_inicial


label tela_inicial:
    # scene bg tela_inicial

    # call logic_screen_galeria_quadros
    # return

    # call screen galeria_quadros
    # $ quadro_escolhido = _return
    # call screen tela_quadro_detalhe(quadro_index=quadro_escolhido)
    # return

    menu:
        "Novo Jogo":
            call tela_casos
            return
            #call tela_perguntas_personagem("julien", "tela_inicial")

label logic_screen_galeria_quadros:
    call screen galeria_quadros
    $ quadro_escolhido = _return
    call screen tela_quadro_detalhe(quadro_index=quadro_escolhido)
    return

screen galeria_quadros():

    tag menu
    add "Cenarios/fundo_galeria.png"

    # Texto de instrução
    text "Escolha uma pintura para revisar.":
        xpos 0.5
        ypos 0.1
        xanchor 0.5
        yanchor 0.0
        size 40
        color "#FFFFFF"
        outlines [(2, "#000000")]

    imagebutton:
        idle "Ui/btn_ver_suspeitos_idle.png" 
        hover "Ui/btn_ver_suspeitos_hover.png" 
        xpos 1000 ypos 1000
        action [Hide("galeria_quadros"), Show("tela_todos_suspeitos")]

    vbox:
        align (0.5, 0.5)
        spacing 30

        for linha in range(2):
            hbox:
                spacing 20
                for coluna in range(4):
                    $ index = (linha * 4 + coluna)
                    imagebutton:
                        idle pinturas[index]["imagem_idle"] #"Quadros/Idle/quadro_{}_thumb.png".format(index)
                        hover pinturas[index]["imagem_hover"] #"Quadros/Hover/quadro_{}_thumb_hover.png".format(index)
                        action Return(index)

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
    #window show

    "Você é um detetive. Analise as pinturas e depoimentos para encontrar o culpado."
    "Pontuação: Após 5 perguntas feitas no total, -2 ponto a cada nova pergunta."

    #window hide
    #pause
    call tela_apresentacao_caso

label tela_apresentacao_caso:
    scene bg apresentacao_caso

    "A vítima foi encontrada em seu ateliê. Não há sinais de arrombamento."
    "Julien Armand, pintor vizinho, deixou 8 pinturas com possíveis pistas."

    call tela_suspeitos(0)

label tela_suspeitos(index):
    $ renpy.hide_screen("botao_voltar_suspeito")
    if index >= 5:
        $ chave = "s{}".format(index)
        $ s = personagens[chave]
        
        hide expression s['imagem_idle']
        call screen tela_quadro_detalhe(0, 1)
    else:    
        $ chave = "s{}".format(index+1)
        $ s = personagens[chave]

        scene bg apresentacao_suspeito

        show expression s['imagem_idle']

        show screen botao_voltar_suspeito(index)
        "Nome: [s['nome']]"
        "Histórico: [s['descricao']]"

        call tela_suspeitos(index + 1)
        # menu:
        #     "Avançar":
        #         call tela_suspeitos(index + 1)
        #     "Voltar":
        #         if index > 0:
        #             call tela_suspeitos(index - 1)
        #         else:
        #             call tela_apresentacao_caso

screen botao_voltar_suspeito(index):
    if index > 0:
        imagebutton:
            idle "Ui/voltar_idle.png"
            hover "Ui/voltar_hover.png"
            xpos 30
            ypos 30
            action [Hide("botao_voltar_suspeito"), Call("tela_suspeitos", index - 1)]
    else:
        imagebutton:
            idle "Ui/voltar_idle.png"
            hover "Ui/voltar_hover.png"
            xpos 30
            ypos 30
            action [Hide("botao_voltar_suspeito"), Call("tela_apresentacao_caso")]

screen tela_quadro_detalhe(quadro_index=0, b_ApresentacaoInicial=0):

    tag quadro_detalhe  # útil para poder substituir ou esconder depois

    # scene bg pintura
    # Mostra o quadro ampliado
    add pinturas[quadro_index]["imagem_idle"] xpos 200 ypos 100 #"Quadros/Idle/quadro_{}_thumb.png".format(quadro_index) xpos 200 ypos 100
    $ p = pinturas[quadro_index]

# Texto de instrução
    text "Pintor: Julien Armand - [p['descricao']]":
        xpos 0.5
        ypos 0.1
        xanchor 0.5
        yanchor 0.0
        size 40
        color "#FFFFFF"
        outlines [(2, "#000000")]

    if b_ApresentacaoInicial:
        imagebutton:
            idle personagens["julien"]['imagem_idle'] #"Personagens/Pintor/pintor_idle.png"
            hover personagens["julien"]['imagem_hover'] #"Personagens/Pintor/pintor_hover.png"
            xpos 1000 ypos 200
            action [Hide("tela_quadro_detalhe"), Call("tela_perguntas_personagem", "julien", "quadro", quadro_index, b_ApresentacaoInicial)]

        $ total_pinturas = len(pinturas)

        # Botão de avançar
        if (quadro_index + 1) >= total_pinturas:
            imagebutton:
                idle "Ui/avancar_idle.png"
                hover "Ui/avancar_hover.png"
                xpos 1000 ypos 50
                action [Hide("tela_quadro_detalhe"), Call("logic_screen_galeria_quadros")]
                
        else:
            imagebutton:
                idle "Ui/avancar_idle.png"
                hover "Ui/avancar_hover.png"
                xpos 1000 ypos 50
                action [Hide("tela_quadro_detalhe"), Show("tela_quadro_detalhe", quadro_index=quadro_index + 1, b_ApresentacaoInicial=b_ApresentacaoInicial)]
            
        imagebutton:
            idle "Ui/voltar_idle.png"
            hover "Ui/voltar_hover.png"
            xpos 50 ypos 50
            if quadro_index > 0:
                action [Hide("tela_quadro_detalhe"), Show("tela_quadro_detalhe", quadro_index=quadro_index - 1, b_ApresentacaoInicial=b_ApresentacaoInicial)]
            else:
                action [Hide("tela_quadro_detalhe"), Call("tela_suspeitos", 4)]
    else:
        # Botão com imagem do pintor
        imagebutton:
            idle personagens["julien"]['imagem_idle'] #"Personagens/Pintor/pintor_idle.png"
            hover personagens["julien"]['imagem_hover'] #"Personagens/Pintor/pintor_hover.png"
            xpos 1000 ypos 200
            action [Hide("tela_quadro_detalhe"), Call("tela_perguntas_personagem", "julien", "logic_screen_galeria_quadros", quadro_index)]

        imagebutton:
            idle "Ui/voltar.png"
            hover "Ui/voltar.png"
            xpos 50 ypos 50
            action [Hide("tela_quadro_detalhe"), Call("logic_screen_galeria_quadros")]
        
screen tela_todos_suspeitos():

    tag menu
    add "Cenarios/fundo_suspeitos.png"

    # Botão para voltar para a galeria de quadros
    imagebutton:
        idle "Ui/btn_GaleriaDeQuadros.png"
        hover "Ui/btn_GaleriaDeQuadros.png"
        xpos 50 ypos 50
        action [Hide("tela_todos_suspeitos"), Call("logic_screen_galeria_quadros")]

    # Botões dos 5 suspeitos
    hbox:
        align (0.5, 0.5)
        spacing 40

        for i in range(5):
            $ index_suspeito = i + 1
            $ s = personagens["s{}".format(index_suspeito)]
            imagebutton:
                idle s["imagem_idle"]
                hover s["imagem_hover"]
                action [Hide("tela_todos_suspeitos"), Show("tela_interrogar_suspeito", id="s{}".format(index_suspeito))]

screen tela_interrogar_suspeito(id):

    tag suspeito
    add "Cenarios/fundo_interrogatorio.png"

    $ suspeito = personagens[id]

    # Mostrar o suspeito no centro da tela
    add suspeito["imagem_idle"] xpos 0.5 ypos 0.3 xanchor 0.5 yanchor 0.5

    # Botão: Voltar para todos os suspeitos
    imagebutton:
        idle "Ui/voltar_idle.png"
        hover "Ui/voltar_idle.png"
        xpos 50 ypos 550
        action [Hide("tela_interrogar_suspeito"), Show("tela_todos_suspeitos")]

    # Botão: Interrogar (vai para tela_perguntas_personagem)
    imagebutton:
        idle "Ui/btn_interrogar_idle.png"
        hover "Ui/btn_interrogar_idle.png"
        xpos 500 ypos 550
        action [Hide("tela_interrogar_suspeito"), Call("tela_perguntas_personagem", id, "voltar_para_tela_todos_suspeitos")]

    # Botão: Prender (vai para tela_prender)
    imagebutton:
        idle "Ui/btn_prender_idle.png"
        hover "Ui/btn_prender_idle.png"
        xpos 950 ypos 550
        action [Hide("tela_interrogar_suspeito"), Call("tela_prender", id)]

label voltar_para_tela_todos_suspeitos:
    call screen tela_todos_suspeitos
    return

# label tela_perguntas_personagem(id, voltar_para, index_tela_anterior=0, b_ApresentacaoInicial=0):
#     $ personagem = personagens[id]
#     scene bg perguntas
#     "Perguntas para [personagem['nome']]"

#     if perguntas_feitas >= 5:
#         "Atenção: essa pergunta custará pontos."

#     $ total_perguntas = len(personagem['perguntas'])

#     python:
#         menu_opcoes = []

#         for i in range(total_perguntas):
#             pergunta_texto = personagem['perguntas'][i]
#             menu_opcoes.append((pergunta_texto, i))

#         menu_opcoes.append(("Voltar", "voltar"))

#         escolha = renpy.display_menu(menu_opcoes)

#     if escolha == "voltar":
#         # jump expression voltar_para
#         # $ label_name, arg = voltar_para
#         if voltar_para == "quadro":
#             call screen tela_quadro_detalhe(index_tela_anterior, b_ApresentacaoInicial)
#             return
#         else:
#             jump expression voltar_para
#     else:
#         $ perguntas_feitas += 1
#         call tela_resposta(id, escolha)
#         call tela_perguntas_personagem(id, voltar_para, index_tela_anterior, b_ApresentacaoInicial)  # Retorna ao menu após responder
#     return

screen screen_perguntas_personagem(id, voltar_para, index_tela_anterior=0, b_ApresentacaoInicial=0):
    default personagem = personagens[id]

    # Se for Julien, usamos as perguntas da pintura correspondente
    if id == "julien":
        default pintura_key = f"pintura{index_tela_anterior + 1}" 
    else:
        default pintura_key = ""
    default perguntas = personagem.get(f"perguntas_{pintura_key}", personagem.get("perguntas", []))
    default total_perguntas = len(perguntas)

    # default total_perguntas = len(personagem["perguntas"])

    tag menu
    add "bg perguntas"

    vbox:
        align (0.5, 0.1)
        spacing 20

        text "Perguntas para [personagem['nome']]" size 40 color "#FFFFFF" xalign 0.5

        if perguntas_feitas >= 5:
            text "Atenção: essa pergunta custará pontos." color "#FF4444" xalign 0.5 size 25

        for i in range(total_perguntas):
            $ pergunta = perguntas[i]
            if id == "julien":
                $ key = f"{id}_{pintura_key}_{i}"
            else:
                $ key = f"{id}_{i}"
            $ ja_feita = perguntas_respondidas.get(key, False)

            textbutton pergunta:
                xalign 0.5
                if ja_feita :
                    background Solid("#FFA500") 
                else:
                    background Solid("#FFFFFF")

                hover_background Solid("#CCCCCC")
                text_color "#000000"
                action Function(responder_pergunta, id, i, voltar_para, index_tela_anterior, b_ApresentacaoInicial)

        textbutton "Voltar":
            xalign 0.5
            background "#888888"
            text_color "#FFFFFF"
            action Return("voltar")

label tela_perguntas_personagem(id, voltar_para, index_tela_anterior=0, b_ApresentacaoInicial=0):
    $ personagem = personagens[id]
    call screen screen_perguntas_personagem(id, voltar_para, index_tela_anterior, b_ApresentacaoInicial)

    if _return == "voltar":
        if voltar_para == "quadro":
            call screen tela_quadro_detalhe(index_tela_anterior, b_ApresentacaoInicial)
        else:
            jump expression voltar_para
    return


label tela_resposta(id, q):
    if id == "julien":
        $ pintura_key = f"pintura{index_tela_anterior + 1}"
        $ resposta = personagens[id].get(f"respostas_{pintura_key}", [""])[q]
    else:
        $ resposta = personagens[id]['respostas'][q]

    "[resposta]"
    return

label tela_prender(id):
    $ suspeito = personagens[id]
    scene bg prender
    "Você está prestes a prender [suspeito['nome']]. Deseja confirmar?"
    menu:
        "Confirmar Prisão":
            call verificar_prisao(id)
        "Voltar":
            call screen tela_todos_suspeitos

label verificar_prisao(id):
    if id == culpado:
        call tela_vitoria
    else:
        call tela_derrota

label tela_vitoria:
    scene bg vitoria
    $ pontuacao -= calcular_penalidade()

    "Parabéns! Você solucionou o caso. Pontuação final: [pontuacao]"

    menu:
        "Voltar a menu de casos":
            call tela_casos
        "Ver solução":
            call tela_solucao
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

    menu:
        "Voltar a menu de casos":
            call tela_casos
        "Rever explicação":
            call tela_solucao
    return

label tela_resposta_com_fluxo:
    call tela_resposta(temp_id, temp_q)
    call tela_perguntas_personagem(temp_id, temp_voltar_para, temp_index_tela_anterior, temp_b_ApresentacaoInicial)
    return


init python:
    # tempo_jogo = 0
    perguntas_respondidas = {}

     # Variáveis temporárias para controle de fluxo
    temp_id = None
    temp_q = None
    temp_voltar_para = None
    temp_index_tela_anterior = 0
    temp_b_ApresentacaoInicial = 0

    def responder_pergunta(id, i, voltar_para, index_tela_anterior=0, b_ApresentacaoInicial=0):
        global perguntas_feitas, perguntas_respondidas
        global temp_id, temp_q, temp_voltar_para, temp_index_tela_anterior, temp_b_ApresentacaoInicial

        if id == "julien":
            pintura_key = f"pintura{index_tela_anterior + 1}"
            key = f"{id}_{pintura_key}_{i}"
        else:
            key = f"{id}_{i}"

        if key not in perguntas_respondidas:
            perguntas_respondidas[key] = True
            perguntas_feitas += 1

        temp_id = id
        temp_q = i
        temp_voltar_para = voltar_para
        temp_index_tela_anterior = index_tela_anterior
        temp_b_ApresentacaoInicial = b_ApresentacaoInicial

        renpy.jump("tela_resposta_com_fluxo")

    perguntas_feitas = 0
    pontuacao = 100
    culpado = "s3"  # exemplo

    def calcular_penalidade():
        # penalidade_tempo = max(0, (tempo_jogo - 10) // 2)
        penalidade_perguntas = 2 * max(0, perguntas_feitas - 5)
        return penalidade_perguntas

    # suspeitos = [
    #     {"nome": "Suspeito 1", "descricao": "Histórico 1", "foto": "suspeito1.png"},
    #     {"nome": "Suspeito 2", "descricao": "Histórico 2", "foto": "suspeito2.png"},
    #     {"nome": "Suspeito 3", "descricao": "Histórico 3", "foto": "suspeito3.png"},
    #     {"nome": "Suspeito 4", "descricao": "Histórico 4", "foto": "suspeito4.png"},
    #     {"nome": "Suspeito 5", "descricao": "Histórico 5", "foto": "suspeito5.png"},
    # ]

    pinturas = [
        {"imagem_idle": "Quadros/Idle/pintura1_idle.png", "imagem_hover": "Quadros/Hover/pintura1_hover.png", "descricao": "Descrição 1"},
        {"imagem_idle": "Quadros/Idle/pintura2_idle.png", "imagem_hover": "Quadros/Hover/pintura2_hover.png", "descricao": "Descrição 2"},
        {"imagem_idle": "Quadros/Idle/pintura3_idle.png", "imagem_hover": "Quadros/Hover/pintura3_hover.png", "descricao": "Descrição 3"},
        {"imagem_idle": "Quadros/Idle/pintura4_idle.png", "imagem_hover": "Quadros/Hover/pintura4_hover.png", "descricao": "Descrição 4"},
        {"imagem_idle": "Quadros/Idle/pintura5_idle.png", "imagem_hover": "Quadros/Hover/pintura5_hover.png", "descricao": "Descrição 5"},
        {"imagem_idle": "Quadros/Idle/pintura6_idle.png", "imagem_hover": "Quadros/Hover/pintura6_hover.png", "descricao": "Descrição 6"},
        {"imagem_idle": "Quadros/Idle/pintura7_idle.png", "imagem_hover": "Quadros/Hover/pintura7_hover.png", "descricao": "Descrição 7"},
        {"imagem_idle": "Quadros/Idle/pintura8_idle.png", "imagem_hover": "Quadros/Hover/pintura8_hover.png", "descricao": "Descrição 8"},
    ]

    personagens = {
    "julien": {
        "nome": "Julien Armand",
        "imagem_idle": "Personagens/Pintor/pintor_idle.png",
        "imagem_hover": "Personagens/Pintor/pintor_hover.png",
        "perguntas_pintura1": [
            "Pergunta 1", "Pergunta 2", "Pergunta 3", "Pergunta 4", "Pergunta 5"
        ],
        "respostas_pintura1": [
            "Resposta 1", "Resposta 2", "Resposta 3", "Resposta 4", "Resposta 5"
        ],
        "perguntas_pintura2": [
            "Pergunta 1", "Pergunta 2", "Pergunta 3", "Pergunta 4", "Pergunta 5"
        ],
        "respostas_pintura2": [
            "Resposta 1", "Resposta 2", "Resposta 3", "Resposta 4", "Resposta 5"
        ],
        "perguntas_pintura3": [
            "Pergunta 1", "Pergunta 2", "Pergunta 3", "Pergunta 4", "Pergunta 5"
        ],
        "respostas_pintura3": [
            "Resposta 1", "Resposta 2", "Resposta 3", "Resposta 4", "Resposta 5"
        ],
        "perguntas_pintura4": [
            "Pergunta 1", "Pergunta 2", "Pergunta 3", "Pergunta 4", "Pergunta 5"
        ],
        "respostas_pintura4": [
            "Resposta 1", "Resposta 2", "Resposta 3", "Resposta 4", "Resposta 5"
        ],
        "perguntas_pintura5": [
            "Pergunta 1", "Pergunta 2", "Pergunta 3", "Pergunta 4", "Pergunta 5"
        ],
        "respostas_pintura5": [
            "Resposta 1", "Resposta 2", "Resposta 3", "Resposta 4", "Resposta 5"
        ],
        "perguntas_pintura6": [
            "Pergunta 1", "Pergunta 2", "Pergunta 3", "Pergunta 4", "Pergunta 5"
        ],
        "respostas_pintura6": [
            "Resposta 1", "Resposta 2", "Resposta 3", "Resposta 4", "Resposta 5"
        ],
        "perguntas_pintura7": [
            "Pergunta 1", "Pergunta 2", "Pergunta 3", "Pergunta 4", "Pergunta 5"
        ],
        "respostas_pintura7": [
            "Resposta 1", "Resposta 2", "Resposta 3", "Resposta 4", "Resposta 5"
        ],
        "perguntas_pintura8": [
            "Pergunta 1", "Pergunta 2", "Pergunta 3", "Pergunta 4", "Pergunta 5"
        ],
        "respostas_pintura8": [
            "Resposta 1", "Resposta 2", "Resposta 3", "Resposta 4", "Resposta 5"
        ]

    },
    "s1": {
        "nome": "Suspeito 1",
        "descricao": "Histórico 1",
        "imagem_idle": "Personagens/Suspeito1/suspeito1_idle.png",
        "imagem_hover": "Personagens/Suspeito1/suspeito1_hover.png",
        "perguntas": [
            "Pergunta 1", "Pergunta 2", "Pergunta 3", "Pergunta 4", "Pergunta 5"
        ],
        "respostas": ["Resp 1", "Resp 2", "Resp 3", "Resp 4", "Resp 5"]
    },
    "s2": {
        "nome": "Suspeito 2",
        "descricao": "Histórico 2",
        "imagem_idle": "Personagens/Suspeito2/suspeito2_idle.png",
        "imagem_hover": "Personagens/Suspeito2/suspeito2_hover.png",
        "perguntas": [
            "Pergunta 1", "Pergunta 2", "Pergunta 3", "Pergunta 4", "Pergunta 5"
        ],
        "respostas": ["Resp 1", "Resp 2", "Resp 3", "Resp 4", "Resp 5"]
    },
    "s3": {
        "nome": "Suspeito 3",
        "descricao": "Histórico 3",
        "imagem_idle": "Personagens/Suspeito3/suspeito3_idle.png",
        "imagem_hover": "Personagens/Suspeito3/suspeito3_hover.png",
        "perguntas": [
            "Pergunta 1", "Pergunta 2", "Pergunta 3", "Pergunta 4", "Pergunta 5"
        ],
        "respostas": ["Resp 1", "Resp 2", "Resp 3", "Resp 4", "Resp 5"]
    },
    "s4": {
        "nome": "Suspeito 4",
        "descricao": "Histórico 4",
        "imagem_idle": "Personagens/Suspeito4/suspeito4_idle.png",
        "imagem_hover": "Personagens/Suspeito4/suspeito4_hover.png",
        "perguntas": [
            "Pergunta 1", "Pergunta 2", "Pergunta 3", "Pergunta 4", "Pergunta 5"
        ],
        "respostas": ["Resp 1", "Resp 2", "Resp 3", "Resp 4", "Resp 5"]
    },
    "s5": {
        "nome": "Suspeito 5",
        "descricao": "Histórico 5",
        "imagem_idle": "Personagens/Suspeito5/suspeito5_idle.png",
        "imagem_hover": "Personagens/Suspeito5/suspeito5_hover.png",
        "perguntas": [
            "Pergunta 1", "Pergunta 2", "Pergunta 3", "Pergunta 4", "Pergunta 5"
        ],
        "respostas": ["Resp 1", "Resp 2", "Resp 3", "Resp 4", "Resp 5"]
    }
}

