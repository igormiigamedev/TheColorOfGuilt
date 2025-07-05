## Arquivo principal Ren'Py: script.rpy

init:
    image bg bg_tela_introducao = "images/bg/bg_tela_inicial.png"
    image bg tela_suspeitos = "images/bg/bg_tela_suspeitos.png"
    image bg artista = "images/bg/bg_tela_artista.png"


label start:

    play music "audio/bg_ost.mp3" loop
    call tela_inicial from _call_tela_inicial


label tela_inicial:
    scene bg bg_tela_introducao

    # call logic_screen_galeria_quadros
    # return

    # call screen galeria_quadros
    # $ quadro_escolhido = _return
    # call screen tela_quadro_detalhe(quadro_index=quadro_escolhido)
    # return

    menu:
        "Novo Jogo":
            call tela_casos from _call_tela_casos
            return
            #call tela_perguntas_personagem("julien", "tela_inicial")

label logic_screen_galeria_quadros:
    call screen galeria_quadros
    $ quadro_escolhido = _return
    call screen tela_quadro_detalhe(quadro_index=quadro_escolhido)
    return

screen galeria_quadros():

    tag menu
    add "images/bg/bg_tela_artista.png"

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
        xpos 1600 ypos 800
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
    scene bg bg_tela_introducao
    "Escolha um caso para começar."
    menu:
        "Caso 1 - O Vulto na Névoa":
            call tela_introducao from _call_tela_introducao
        "Caso 2 (Bloqueado)":
            "Novos casos em breve."
            jump tela_casos
        "Caso 3 (Bloqueado)":
            "Novos casos em breve."
            jump tela_casos

label tela_introducao:
    scene bg bg_tela_introducao
    $ tempo_jogo = 0
    $ perguntas_feitas = 0
    $ pontuacao = 100
    # window show

    "Você é um detetive. Analise as pinturas e depoimentos para encontrar o culpado."
    "Para resolver o mistério, você poderá fazer perguntas aos suspeitos e ao pintor"
    "- Ao todo você pode fazer 10 perguntas gratuitamente."
    "- Após essas 10 perguntas, cada pergunta adicional custa 2 pontos da sua pontuação final."
    "- Investigue com sabedoria: encontrar as contradições e os pequenos detalhes pode ser mais valioso do que acumular falas."
    "- Sua pontuação final será baseada em eficiência, precisão nas acusações e uso estratégico de perguntas."
    # window hide
    # pause
    call tela_apresentacao_caso from _call_tela_apresentacao_caso

label tela_apresentacao_caso:
    scene bg bg_tela_introducao

    "Na manhã de terça-feira, o renomado botânico Dr. William Hargrove foi encontrado sem vida dentro de sua estufa. "
    "A causa da morte: Envenenamento por uma substância rara. Não havia sinais de luta ou arrombamento. "
    "Você, detetive Valentin Mireau, foi chamado para investigar o caso. Durante a investigação inicial, um vizinho excêntrico, o pintor Julien Armand, entrega oito quadros que fez da janela de sua varanda. "
    "As pinturas retratam cenas do jardim e da estufa nos dias e noites que antecederam a morte do botânico."
    "Com base em interrogatórios, observações e nas pistas visuais das obras, você deverá revelar a verdade por trás deste assassinato silencioso — e artístico."

    call tela_suspeitos(0) from _call_tela_suspeitos

label tela_suspeitos(index):
    scene bg tela_suspeitos
    $ renpy.hide_screen("botao_voltar_suspeito")
    if index >= 5:
        $ chave = "s{}".format(index)
        $ s = personagens[chave]
        
        hide expression s['imagem_idle']
        call screen tela_quadro_detalhe(0, 1)
    else:    
        $ chave = "s{}".format(index+1)
        $ s = personagens[chave]


        show expression s['imagem_idle'] at Position(xalign=0.5, yalign=-0.5)
        show screen botao_voltar_suspeito(index)
        "Nome: [s['nome']]"
        "Histórico: [s['descricao']]"

        call tela_suspeitos(index + 1) from _call_tela_suspeitos_1
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

    add "images/bg/bg_tela_artista.png"

    tag quadro_detalhe

    $ p = pinturas[quadro_index]

    # Mostra o quadro ampliado, centralizado
    add Transform(p["imagem_idle"], zoom=1.5):  # Ajuste o zoom conforme necessário
        xalign 0.5
        yalign 0.4

# Texto de instrução
    text "Julien - [p['descricao']]":
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
                xpos 1700 ypos 200
                action [Hide("tela_quadro_detalhe"), Call("logic_screen_galeria_quadros")]
                
        else:
            imagebutton:
                idle "Ui/avancar_idle.png"
                hover "Ui/avancar_hover.png"
                xpos 1700 ypos 200
                action [Hide("tela_quadro_detalhe"), Show("tela_quadro_detalhe", quadro_index=quadro_index + 1, b_ApresentacaoInicial=b_ApresentacaoInicial)]
            
        imagebutton:
            idle "Ui/voltar_idle.png"
            hover "Ui/voltar_hover.png"
            xpos 30 ypos 30
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
            idle "Ui/voltar_idle.png"
            hover "Ui/voltar_hover.png"
            xpos 30 ypos 30
            action [Hide("tela_quadro_detalhe"), Call("logic_screen_galeria_quadros")]
        
screen tela_todos_suspeitos():

    add "images/bg/bg_tela_suspeitos.png" 

    # Botão para voltar para a galeria de quadros
    imagebutton:
        idle "Ui/btn_GaleriaDeQuadros_idle.png"
        hover "Ui/btn_GaleriaDeQuadros_hover.png"
        xpos 50 ypos 50
        action [Hide("tela_todos_suspeitos"), Call("logic_screen_galeria_quadros")]

    # Container para centralizar tudo na tela
    frame:
        align (0.5, 1.4)
        background None

        hbox:
            spacing 5
            for i in range(5):
                $ index_suspeito = i + 1
                $ s = personagens["s{}".format(index_suspeito)]
                imagebutton:
                    idle Transform(s["imagem_idle"], xsize=410, ysize=750)
                    hover Transform(s["imagem_hover"], xsize=410, ysize=750)
                    action [Hide("tela_todos_suspeitos"), Show("tela_interrogar_suspeito", id="s{}".format(index_suspeito))]


screen tela_interrogar_suspeito(id):
    tag suspeito
    add "images/bg/bg_tela_suspeitos.png"

    $ suspeito = personagens[id]

    # Mostrar o suspeito no centro da tela
    add suspeito["imagem_idle"] xpos 0.5 ypos -0.5 xanchor 0.5 yanchor -0.5


    # Botão: Voltar para todos os suspeitos
    imagebutton:
        idle "Ui/btn_voltar_suspeito_idle.png"
        hover "Ui/btn_voltar_suspeito_hover.png"
        xpos 275 ypos 800
        action [Hide("tela_interrogar_suspeito"), Show("tela_todos_suspeitos")]

    # Botão: Interrogar (vai para tela_perguntas_personagem)
    imagebutton:
        idle "Ui/btn_interrogar_hover.png"
        hover "Ui/btn_interrogar_idle.png"
        xpos 875 ypos 800
        action [Hide("tela_interrogar_suspeito"), Call("tela_perguntas_personagem", id, "voltar_para_tela_todos_suspeitos")]

    # Botão: Prender (vai para tela_prender)
    imagebutton:
        idle "Ui/btn_prender_hover.png"
        hover "Ui/btn_prender_idle.png"
        xpos 1475 ypos 800
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
        add "images/bg/bg_tela_artista.png"
        default pintura_key = f"pintura{index_tela_anterior + 1}" 
    else:
        add "images/bg/bg_tela_suspeitos.png"
        default pintura_key = ""
    default perguntas = personagem.get(f"perguntas_{pintura_key}", personagem.get("perguntas", []))
    default total_perguntas = len(perguntas)

    # default total_perguntas = len(personagem["perguntas"])

    tag menu

    vbox:
        align (0.5, 0.1)
        spacing 20

        text "Perguntas para [personagem['nome']]" size 40 color "#FFFFFF" xalign 0.5

        if perguntas_feitas >= 10:
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

    show expression personagens[id]['imagem_idle'] at Position(xalign=0.5, yalign=-0.5)

    "[resposta]"
    return


label tela_prender(id):
    $ suspeito = personagens[id]
    scene bg tela_suspeitos
    show expression personagens[id]['imagem_idle'] at Position(xalign=0.5, yalign=-0.5)
    "Você está prestes a prender [suspeito['nome']]. Deseja confirmar?"
    menu:
        "Confirmar Prisão":
            call verificar_prisao(id) from _call_verificar_prisao
        "Voltar":
            call screen tela_todos_suspeitos

label verificar_prisao(id):
    if id == culpado:
        call tela_vitoria from _call_tela_vitoria
    else:
        call tela_derrota from _call_tela_derrota

label tela_vitoria:
    scene bg bg_tela_introducao
    $ pontuacao -= calcular_penalidade()

    "Parabéns! Você solucionou o caso. Pontuação final: [pontuacao]"

    menu:
        "Voltar a menu de casos":
            call tela_casos from _call_tela_casos_1
        "Ver solução":
            call tela_solucao from _call_tela_solucao
    return

label tela_derrota:
    scene bg bg_tela_introducao
    "Você prendeu a pessoa errada."
    menu:
        "Reiniciar caso":
            call tela_casos from _call_tela_casos_2
        "Ver solução":
            call tela_solucao from _call_tela_solucao_1

label tela_solucao:
    scene bg bg_tela_introducao
    "Explicação passo a passo do caso:"
    "Assassina: Beatrice Hargrove, a sobrinha"
    "Motivação: Beatrice estava endividada e frustrada com a postura do tio, que mantinha uma valiosa coleção de plantas raras apenas como hobby, recusando-se a patenteá-las ou vendê-las. Como herdeira parcial, ela via uma fortuna inexplorada diante de si."
    "Ao eliminá-lo, ela teria acesso ao acervo completo e, com as suspeitas recaindo sobre os demais envolvidos — cada um com um motivo visível — seu plano parecia perfeito. "
    "A assassina criou um cenário onde todos os outros pareciam culpados. Porém, em meio às intenções cruzadas, a verdadeira culpada era a única que silenciosamente movia cada peça do tabuleiro."
    "Método: Obteve a planta venenosa azul em duplicidade. Uma foi vendida ao antigo assistente (como distração), outra foi guardada em segredo."
    "Manipulou a narrativa dos demais suspeitos:"
    "   - Pediu ao jardineiro que entregasse a planta ao ex-assistente, o que gerou sua demissão. Além de colocar nas mãos do assistente a arma do futuro crime"
    "   - Chamou a Dra. Clarissa, rival do tio, à estufa dias antes, sabendo que ela encontraria sinais de plágio."
    "   - Ganhou a simpatia da vizinha, tornando-se uma aliada indireta."
    "Na noite do crime, colocou discretamente uma pequena dose do extrato da planta azul na xícara de chá habitual de William, que costumava tomar sozinho na estufa ao final do dia."

    menu:
        "Voltar a menu de casos":
            call tela_casos from _call_tela_casos_3
        "Rever explicação":
            call tela_solucao from _call_tela_solucao_2
    return

label tela_resposta_com_fluxo:
    scene bg bg_tela_introducao
    if(temp_id == "julien"):
        scene bg artista
    else:
        scene bg tela_suspeitos
    call tela_resposta(temp_id, temp_q) from _call_tela_resposta
    call tela_perguntas_personagem(temp_id, temp_voltar_para, temp_index_tela_anterior, temp_b_ApresentacaoInicial) from _call_tela_perguntas_personagem
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
    culpado = "s1"  # exemplo

    def calcular_penalidade():
        # penalidade_tempo = max(0, (tempo_jogo - 10) // 2)
        penalidade_perguntas = 2 * max(0, perguntas_feitas - 10)
        return penalidade_perguntas

    # suspeitos = [
    #     {"nome": "Suspeito 1", "descricao": "Histórico 1", "foto": "suspeito1.png"},
    #     {"nome": "Suspeito 2", "descricao": "Histórico 2", "foto": "suspeito2.png"},
    #     {"nome": "Suspeito 3", "descricao": "Histórico 3", "foto": "suspeito3.png"},
    #     {"nome": "Suspeito 4", "descricao": "Histórico 4", "foto": "suspeito4.png"},
    #     {"nome": "Suspeito 5", "descricao": "Histórico 5", "foto": "suspeito5.png"},
    # ]

    pinturas = [
        {"imagem_idle": "Quadros/Idle/pintura1_idle.png", "imagem_hover": "Quadros/Hover/pintura1_hover.png", "descricao": "Um confronto silencioso sob galhos nus."},
        {"imagem_idle": "Quadros/Idle/pintura2_idle.png", "imagem_hover": "Quadros/Hover/pintura2_hover.png", "descricao": "Aquecidos por uma urgência muda."},
        {"imagem_idle": "Quadros/Idle/pintura3_idle.png", "imagem_hover": "Quadros/Hover/pintura3_hover.png", "descricao": "Luz entre folhas e sombra entre olhares."},
        {"imagem_idle": "Quadros/Idle/pintura4_idle.png", "imagem_hover": "Quadros/Hover/pintura4_hover.png", "descricao": "A raiva veste tons lilases."},
        {"imagem_idle": "Quadros/Idle/pintura5_idle.png", "imagem_hover": "Quadros/Hover/pintura5_hover.png", "descricao": "Palavras suaves mascaram raízes duras."},
        {"imagem_idle": "Quadros/Idle/pintura6_idle.png", "imagem_hover": "Quadros/Hover/pintura6_hover.png", "descricao": "Florescendo entre vidros"},
        {"imagem_idle": "Quadros/Idle/pintura7_idle.png", "imagem_hover": "Quadros/Hover/pintura7_hover.png", "descricao": "A Troca Azul"},
        {"imagem_idle": "Quadros/Idle/pintura8_idle.png", "imagem_hover": "Quadros/Hover/pintura8_hover.png", "descricao": "A sombra da frustração se arrasta pelo solo."},
    ]

    personagens = {
    "julien": {
        "nome": "Julien Armand",
        "imagem_idle": "Personagens/Pintor/pintor_idle.png",
        "imagem_hover": "Personagens/Pintor/pintor_hover.png",
        "perguntas_pintura1": [
        "O que o motivou a pintar essa cena?",
        "O senhor ouviu algo durante essa cena?",
        "Por que o assistente aparece com um guarda-chuva?",
        "A planta azul no fundo é bastante visível. Foi intencional?",
        "Qual era o clima geral naquele momento?"
    ],
    "respostas_pintura1": [
        "Havia uma tensão no ar, como o estalar de galhos secos no inverno. A mancha azul da planta era a única chama em meio ao cinza. A rejeição saltava dos gestos — pintá-la foi inevitável.",
        "Um grito abafado. Não palavras, mas um som de frustração… seguido pelo estrondo da porta da estufa.",
        "Ele o leva sempre. Hábito, talvez superstição. Não chovia naquela tarde.",
        "Era como um segredo mal enterrado, querendo florescer mesmo no frio. A cor exigia presença.",
        "O inverno parecia mais frio ao redor deles. Dois homens, e um adeus seco como geada na pele."
    ],

    "perguntas_pintura2": [
        "Por que pintou esse momento em especial?",
        "Consegue identificar o conteúdo do envelope?",
        "O que te chamou mais atenção nessa cena?",
        "Eles pareciam nervosos ou calmos?",
        "Havia mais alguém por perto?"
    ],
    "respostas_pintura2": [
        "Porque foi um gesto raro: calor no inverno. Um segredo selado em papel pálido.",
        "Não. Só vi que ele o tirou do bolso do casaco, cuidadosamente. Ela o escondeu rápido.",
        "A cor — o vermelho do vestido dela cortava a paisagem morta. Era como se ela carregasse o fogo do outono em pleno gelo.",
        "Cúmplices. Trocaram poucas palavras, mas muitos olhares.",
        "Só o silêncio. E o peso de algo prestes a germinar — como uma semente guardada."
    ],

    "perguntas_pintura3": [
        "Por que decidiu pintar uma cena noturna?",
        "Era comum o Dr. Hargrove trabalhar à noite?",
        "Como descreve o semblante das duas mulheres?",
        "Por que há tanto contraste de luz na pintura?",
        "Algo mais chamou sua atenção nessa noite?"
    ],
    "respostas_pintura3": [
        "Porque a noite sussurra verdades que o dia encobre. A luz da estufa parecia pulsar como um coração em febre, e os olhos nas janelas... dois faróis de julgamento.",
        "Sim, especialmente na primavera. Dizia que as plantas “sussurravam melhor sob a lua”.",
        "A vizinha, como uma coruja inquieta. A sobrinha, uma vela acesa pela dúvida — ou pela lembrança.",
        "Porque a cena era feita de extremos: luz artificial contra escuridão natural. Revelações à força.",
        "Um som agudo vindo da estufa, como metal forçado. Parecia mecânico."
    ],

    "perguntas_pintura4": [
        "O que motivou essa pintura?",
        "O que pareciam discutir?",
        "A sobrinha parecia preocupada?",
        "Por que as cores estão tão desbotadas nessa pintura?",
        "O que havia no jardim nesse momento?"
    ],
    "respostas_pintura4": [
        "Foi uma manhã de vozes elevadas e gestos pontiagudos. A lavanda da roupa dela parecia engolida pelo cinza da irritação.",
        "Luz. Ela apontava para a estufa, fazia gestos com as mãos nos olhos.",
        "Não. Observava de longe, sem intervir. Como quem espera o fim de uma peça.",
        "Porque a raiva apaga a beleza. E ali, a manhã parecia vestida de bruma, como se até a primavera recuasse.",
        "As flores recém-abertas não se intrometiam. Mas o vento levava fragmentos do que foi dito."
    ],

    "perguntas_pintura5": [
        "Por que pintar esse momento aparentemente banal?",
        "Pareciam estar em conflito ou harmonia?",
        "Algum objeto trocado entre elas?",
        "Qual foi sua principal escolha de composição?",
        "Alguma coisa incomum no fundo da imagem?"
    ],
    "respostas_pintura5": [
        "Porque a calma é um véu. Sob ele, às vezes se escondem conspirações. E ali, o lilás do lenço parecia dialogar com o laranja do vestido — dissonantes, porém próximas.",
        "Conversa calma. Mas a sobrinha gesticulava. Parecia justificar algo.",
        "Não vi trocas. Só palavras, gestos e... talvez segundas intenções.",
        "Usei tons quentes cercados por sombra — o dia bonito tentando encobrir algo não dito.",
        "Um pássaro sobre o telhado da estufa. Observava. Como eu."
    ],

    "perguntas_pintura6": [
        "O que motivou essa pintura?",
        "O que pareciam estar fazendo?",
        "Você notou algo estranho nessa cena?",
        "Por que as cores são mais vibrantes nesta pintura?",
        "Qual sensação teve ao concluir essa obra?"
    ],
    "respostas_pintura6": [
        "Porque o vidro não separava o mundo — só o distorcia. Lá dentro, um azul gritando pelo futuro e sussurando o passado.",
        "A doutora gesticulava com força. A sobrinha tentava explicar. Algo havia sido descoberto.",
        "A cientista saiu sozinha pouco depois. O rosto... sombrio, de raiva. A sobrinha não a acompanhou.",
        "Porque a tensão elétrica pairava. Era o tipo de momento onde tudo poderia florescer... ou murchar de vez.",
        "Que algo estava prestes a quebrar. Como vidro sob pressão."
    ],

    "perguntas_pintura7": [
        "O que é representado nessa imagem?",
        "O Dr reagiu imediatamente?",
        "Como descreve o clima emocional da cena?",
        "Você sabia o que era a planta entregue?",
        "Alguém mais estava por perto?"
    ],
    "respostas_pintura7": [
        "Uma transição, tranquila, entre o jardineiro e o antigo assistente. Mas um detalhe que não pintei foi o Dr vendo tudo da janela, irritado.",
        "Não desceu. Mas sumiu da janela logo depois. Como se precisasse pensar.",
        "O calor da primavera não aquecia o gesto. Era uma troca amarga sob um sol que parecia zombar.",
        "Era azul, como a do inverno. Só podia ser a mesma flor.",
        "Não. Só o vento, como um sussurro de advertência."
    ],

    "perguntas_pintura8": [
        "O que expressava o corpo do jardineiro?",
        "Ele estava levando algo da estufa?",
        "O senhor ouviu ou viu o Dr. Hargrove nesse momento?",
        "Por que a luz e sombra são tão contrastantes nessa pintura?",
        "O que sentiu ao pintar essa imagem?"
    ],
    "respostas_pintura8": [
        "Era como um tronco arrancado do chão. Cada passo era raiva contida. A pá em sua mão brilhava como ferro sob a luz do meio-dia.",
        "Sim. Ferramentas — e raiva.",
        "Não. Apenas a Dra Wynn estava pela estufa nesse momento, com um rosto de raiva profunda.",
        "Porque era um fim de cena. E finais merecem claridade e escuridão dançando juntas.",
        "Que tudo estava prestes a terminar. Ou começar de novo, mas manchado."
    ]

    },
    "s1": {
        "nome": "Beatrice Hargrove",
        "descricao": "Sonha em viajar o mundo e tem dívidas crescentes. O falecido estava estava com pesquisas em andamento com potencial valor que ela poderia herdar.",
        "imagem_idle": "Personagens/Suspeito1/suspeito1_idle.png",
        "imagem_hover": "Personagens/Suspeito1/suspeito1_hover.png",
        "perguntas": [
            "Você estava prestes a viajar, não?", 
            "Como era sua relação com seu tio?", 
            "O que você recebeu do Assistente no Inverno?", 
            "O que você e a Dra. Wynn estavam fazendo na estufa naquele dia?", 
            "Foi você?"
        ],
        "respostas": [
            "Sim, sonhava em sair daqui. Uma nova vida em outro continente... Meu tio sempre foi uma pessoa que fez de tudo por mim. Mesmo com seu falecimento, conseguiu arrumar uma maneira de me ajudar deixando-me a herança",
            "Ele me tratava como filha, era uma pessoa com pouca visão de futuro, nunca enxergou o potencial que tinha nas mãos com suas plantas e acabou falecendo sem usufruir desse privilégio.",
            "Recebi um envelope com dinheiro em troca de uma muda de planta azul rara que cultivei com ajuda do jardineiro.",
            "Pedi a ajuda dela para entender porque meu tio precisava trabalhar na estufa durante a noite. Ela me explicou que era por causa do tipo da planta, mas saiu muito chateada ao ver algumas pesquisas dela que meu tio estava usando",
            "Por que eu mataria meu tio?! 😢"
        ]
    },
    "s2": {
        "nome": "Thomas Bexley",
        "descricao": "Jardineiro da casa. Diz ter sido demitido de maneira injusta.",
        "imagem_idle": "Personagens/Suspeito2/suspeito2_idle.png",
        "imagem_hover": "Personagens/Suspeito2/suspeito2_hover.png",
        "perguntas": [
            "É verdade que o Dr. Hargrove te demitiu pouco antes de morrer?",
            "O que era aquela planta que você entregou ao Assistente?",
            "A planta que entregou ao Assistente era a última do tipo azul na casa?",
            "Você cuidava das plantas que estavam dentro da estufa também?",
            "Foi você?"
        ],
        "respostas": [
            "Sim, ele achou que eu estava vendendo as plantas por conta própria, mas foi a pedido da Beatrice.",
            "Uma planta venenosa azul rara que a Beatrice começou a cultivar no inverno e eu cuidei até o Assistente buscá-la na primavera. Acho que era uma das preferidas de Dr. Hargrove e de Beatrice, cuidavam dela como um filho",
            "Era a última na estufa durante a primavera. Mas no período de primavera ela sobrevive fora da estufa também, acho difícil Dr. Hargrove e Beatrice permitirem que a última planta azul fosse vendida",
            "Muito raramente, na estufa tinham as plantas raras do Doutor. Essas ele cuidava sozinho.",
            "Plantaram isso contra mim, com certeza!"
        ]
    },
    "s3": {
        "nome": "Dr. Clarissa Wynn",
        "descricao": "Bióloga vegetal. Anos atrás, acusou Hargrove de plagiar suas pesquisas, ambos resolveram judicialmente o assunto.",
        "imagem_idle": "Personagens/Suspeito3/suspeito3_idle.png",
        "imagem_hover": "Personagens/Suspeito3/suspeito3_hover.png",
        "perguntas": [
            "Como você conheceu o Dr. Hargrove?",
            "É verdade que o Dr. e você tinham uma intriga?",
            "O que você foi fazer na Estufa com a Senhorita Beatrice naquele dia?",
            "Você foi visitar a estufa depois daquele dia?",
            "Foi você?"
        ],
        "respostas": [
            "Fomos colegas de doutorado, nada além disso.",
            "Sim, ele publicou um artigo baseado na minha apresentação anos atrás, mas se desculpou quando confrontei e disse que não faria uso delas de novo.",
            "Ela me pediu para explicar o motivo de o trabalho com algumas plantas precisar ser noturno. Algumas plantas raras exigem isso, algo que eu explorei em minhas pesquisas que aparentemente Dr. Hargrove ainda usava",
            "Não, queria me afastar ao máximo de Dr. Hargrove. Estar perto dele é um perigo para as minhas novas pesquisas.",
            "Você não é um detetive muito bom, não é?"
        ]
    },
    "s4": {
        "nome": "Miles Torrence",
        "descricao": "Pesquisador autônomo e ex-assistente do botânico. Ao ser demitido, ficou frustado por não conseguir seguir sua pesquisa sem a planta de Hargrove.",
        "imagem_idle": "Personagens/Suspeito4/suspeito4_idle.png",
        "imagem_hover": "Personagens/Suspeito4/suspeito4_hover.png",
        "perguntas": [
            "Você trabalhava como assistente para o Dr Hargrove, não?",
            "Era difícil trabalhar para o Dr?",
            "O que você entregou à Sobrinha no inverno?",
            "Afinal o que era essa planta azul?",
            "Foi você?"
        ],
        "respostas": [
            "Sim. Até ele me cortar o acesso à pesquisa. Aquilo arruinou meu projeto com as plantas raras.",
            "Ele era um chefe bem chato, e não deixava eu colocar as mãos nas pesquisas direito.",
            "Dinheiro, em troca de uma amostra igual à do tio dela que ela prometeu conseguir. Essa planta me perimitiu voltar as pesquisas do meu projeto, então sou muito grato a Beatrice",
            "Uma variedade desconhecida. Extremamente rara... e, descobri depois, venenosa.",
            "Se eu fosse o culpado, você acha que eu diria sim?"
        ]
    },
    "s5": {
        "nome": "Eleanor Finch",
        "descricao": "Vizinha da vítima, professora aposentada de música. Se queixava constantemente das luzes noturnas da estufa.",
        "imagem_idle": "Personagens/Suspeito5/suspeito5_idle.png",
        "imagem_hover": "Personagens/Suspeito5/suspeito5_hover.png",
        "perguntas": [
            "A luz da estufa durante a noite te estressava?",
            "Além dos barulhos, ele era um bom vizinho?",
            "A Sobrinha da vítima é confiável?",
            "Algum outro residente ou visitante poderia ter problemas com o Dr Hargrove?",
            "Foi você?"
        ],
        "respostas": [
            "Sim, me tirava o sono.",
            "Discreto, mas egocêntrico e já ouvi histórias de desentendimentos e plágio.",
            "Sim, sempre prestativa, mas um pouco mimada e sem rumo na vida.",
            "A Dra. Wynn. E o rapaz que vinha antes — o assistente. Todos pareciam carregados.",
            "Acusar assim sem prova? Espere eu chamar meus advogados!"
        ]
    }
}

