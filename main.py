import locale  # esse modulo e importante, pois como o Python trabalha com sistema americano de ponto ou virgula
import bs4
import requests
from tabulate import tabulate

import modelos

# Papel
# Segmento
# Cotação
# FFO Yield
# Dividend Yield
# P/VP
# Valor de Mercado
# Liquidez
# Qtd de Imoveis
# Preço do m2
# aluguel por m2
# Cap Rate
# Vacância Média

resultado = []
#ultilizo a classe 'Estrategia' para definir parametros para uma estratégia de fundos
estrategia = modelos.Estrategia(cotacao_atual_minima=0.0,
                                dividiend_yeld_minimo=1,
                                p_vp_minimo=0.70,
                                valor_mercado_minimo=2000000,
                                liquidez_minima=500,
                                qt_minima_imoveis=1,
                                maxima_vacancia_media=0)

# dados com pontos que no Brasil seriam considerados milhar, para o Python seria decimal oque acabaria acarretando erros

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # faço a conversão de tudo que vier do sistema brasileiro para


#o sistema americano

#agora faço uma função para tratar as % porcentagem que pro Python seria conhecido como resto


def trata_porcentagem(porcentagem_str):
    # '7,04%'#o dado vem dessa maneira, então pesso para o python quebralo em 2 usando '.split' assim ele quebrara
    # '7,04' #em 2 quando chegar no '%', com os dados separados em 2 indices eu seleciono que quero que apenas o indice
    # none # [0] volte, ou seja, sem o indice [1] a '%'
    return locale.atof(porcentagem_str.split('%')[0])


def trata_decimal(decimal_str):
    #'R$ 5.000,84' o dado vem dessa maneira ultilizo o '.split' para quebrar em dois e defino quero o indice [1]
    # a locale passara e me entraga o dado tratado
    return locale.atof(decimal_str)


#tipos de erro request
# 403 preciso trocar a maneira como faço o requerimento ultilizando headers e simulando um navegador
# 200 todos codigos com 200 são retornos de sucesso da requisição

headers = {'User-agent': 'Mozilla/5.0'}  # crio um dicionário para ser ultilizado como 'headers' simulando como
#se fosse um navegador 'Mozilla' e não um codigo Python fazendo buscas

#para ultilizar o requests eu preciso saber qual o tipo devo usar o GET, POST, PUT
# Paramettro 'headers' ultilizo para modificar a forma como o 'requests' vai enviar uma requisição
resposta = requests.get('https://www.fundamentus.com.br/fii_resultado.php', headers=headers)

# tranformo o arquivo do 'request', de uma maneira que facilite o python interpretalo ultilizando o BeautifulSoup,
#usando o Debug eu olho em qual variavel está o arquivo html nesse caso estava no '.text' da variavel 'resposta'.

soup = bs4.BeautifulSoup(resposta.text, 'html.parser')  # e uso a string 'html.parser'

#print(soup.prettify())  # posso ulilizar para ver se o codigo está ok


# soup.find(id="") posso passar um id especifico, dessa maneira eu posso olhar o 'id' que desejo trabalhar analisando o
# codigo HTML da página. tabela = soup.find(id='tabelaResultado') usando debug consigo ver tudo oque tem nessa 'id' a
# sua classe, os seus atributos os tipos do mesmo e etc linhastabela = soup.find(id='tabelaResultado').findAll('tr')
# atraves vez da BeautifulSoup eu consigo encadear a busca, ou seja, fiz a busca 'id = tabelaResultado' agora faço a
# busca 'tr' dentro do codigo da 'tabelaResultado', assim ela vai-me retornar essar linha que contem 'tr'


linhastabela_tbody = (soup.find(id='tabelaResultado')
                      .find('tbody').find_all('tr'))
#na parte do codigo html percebo que a dois 'tr' os do thead e outra na tbody, percebendo que os tr que quero são as
#do tbody eu especifico-os na '.find' e realizo novamente a busca 'tr' agora so as do tbody aparecerão


#eu preciso usar o 'find_all' mais uma vez porem e proibido então eu itero sobre a variavel'linhastabela_tbody'
#cada parte dela e analizada e enviada para 'linha' e nesse varial eu chamo mais um find 'linha.find_all('td')'
#agora pesquisando o 'td' de cada 'tr' e armazeno tudo na variavel 'dados' para poder consultar no debug

for linha in linhastabela_tbody:  # crio um iterção pegando cada linha de 'linhastabela_tbody' e passando para 'linha'
    dados_fundo = linha.find_all('td')  # depois aplico o 'find_all'tr' e pego os dados e passo para 'dados_fundo'
    codigo = dados_fundo[0].text  # o indice [0] de dados_fundo e o papel dos fundos imoniliarios
    segmento = dados_fundo[1].text  # passso cada indice para uma das variaveis da classe 'FundoImobiliario'
    cotacao_atual = trata_decimal(dados_fundo[2].text)  # assim cada variavel recebera um atributo especifico
    ffo_yeild = trata_porcentagem(dados_fundo[3].text)
    dividiend_yeld = trata_porcentagem(dados_fundo[4].text)
    p_vp = trata_decimal(dados_fundo[5].text)
    valor_mercado = trata_decimal(dados_fundo[6].text)
    liquidez = trata_decimal(dados_fundo[7].text)
    qt_imoveis = int(dados_fundo[8].text)
    preco_m2 = trata_decimal(dados_fundo[9].text)
    aluguel_m2 = trata_decimal(dados_fundo[10].text)
    cap_rate = trata_porcentagem(dados_fundo[11].text)
    vacancia_media = trata_porcentagem(dados_fundo[12].text)

    #trago as intancias da minha classe 'fundoImobiliario' importando o meu proprio modulo e trazendo a classe que criei

    fundo_imobiliario = modelos.FundoImobiliario(
        codigo, segmento, cotacao_atual, ffo_yeild, dividiend_yeld, p_vp, valor_mercado, liquidez,
        qt_imoveis, preco_m2, aluguel_m2, cap_rate, vacancia_media
    )

    if estrategia.aplica_estrategia(fundo_imobiliario):
        resultado.append(fundo_imobiliario)  #digo que caso o FIIS seja True o mesmo seja movido para a lista
        #"fundo_imobiliario'
    # seleciono o objeto da classe 'Estrategia' que contem a estratégia especifica que criei depois chamo o metodo
    # 'aplica_estrategia' qua aplica a estratégia que criei, ela sera aplicada dentro do meu sistema for sobre cada uma
    # dos indices iterados

#para facilitar a visualização dos dados eu posso ultilizar o modulo 'tabulate' crio o cabecalho da minha tabela
#os colocos como lista, pois assim posso trabalhar indice por indice defino o nome de cada indice
cabecalho = ['CÓDIGO', 'SEGMENTO', 'COTAÇÃO ATUAL', 'DIVIDEND YIELD']
#crio a tabela que ira receber o resultado da minha iteração abaixo
tabela = []

#itero sobre os dados oferecidos pela lista 'resultado' a iterando separo cada um dos seus indices na variavel
#'elemento' apos isso apenas adiciono os elementos a tabela, e inidco quais elementos da lista eu quero
# e os coloca na mesma ordem do cabeçalho acima.
for elemento in resultado:
    tabela.append([elemento.codigo, elemento.segmento, elemento.cotacao_atual, elemento.dividiend_yeld])

print(tabulate(tabela, headers=cabecalho, tablefmt='fancy_grid'))  # uso a 'tabulate' adciono a 'tabela'
# e defino o seu cabeçalho no 'headers', em seguida posso definir maneiras de como a tabela sera mostrada

pass