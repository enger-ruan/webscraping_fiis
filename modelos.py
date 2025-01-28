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

class FundoImobiliario:  # crio uma classe com cada atributo da tabela dos fundo imobiliarios
    #
    def __init__(self, codigo, segmento, cotacao_atual, ffo_yeild, dividiend_yeld, p_vp, valor_mercado, liquidez,
                 qt_imoveis, preco_m2, aluguel_m2, cap_rate, vacancia_media):
        self.codigo = codigo
        self.segmento = segmento
        self.cotacao_atual = cotacao_atual
        self.ffo_yeild = ffo_yeild
        self.dividiend_yeld = dividiend_yeld
        self.p_vp = p_vp
        self.valor_mercado = valor_mercado
        self.liquidez = liquidez
        self.qt_imoveis = qt_imoveis
        self.preco_m2 = preco_m2
        self.aluguel_m2 = aluguel_m2
        self.cap_rate = cap_rate
        self.vacancia_media = vacancia_media


#crio uma classe função para analisar fundo imobiliarios
class Estrategia:
    def __init__(self, segmento='', cotacao_atual_minima=0, ffo_yeild_minimo=0, dividiend_yeld_minimo=0, p_vp_minimo=0,
                valor_mercado_minimo=0, liquidez_minima=0, qt_minima_imoveis=0, valor_minimo_preco_m2=0,
                valor_minimo_aluguel_m2=0, valor_minimo_cap_rate=0, maxima_vacancia_media=0):
        self.segmento = segmento
        self.cotacao_atual_minima = cotacao_atual_minima
        self.ffo_yeild_minimo = ffo_yeild_minimo
        self.dividiend_yeld_minimo = dividiend_yeld_minimo
        self.p_vp_minimo = p_vp_minimo
        self.valor_mercado_minimo = valor_mercado_minimo
        self.liquidez_minima = liquidez_minima
        self.qt_minima_imoveis = qt_minima_imoveis
        self.valor_minimo_preco_m2 = valor_minimo_preco_m2
        self.valor_minimo_aluguel_m2 = valor_minimo_aluguel_m2
        self.valor_minimo_cap_rate = valor_minimo_cap_rate
        self.maxima_vacancia_media = maxima_vacancia_media

    #crio uma função para aplicar a estratégia, passo fundo como parametro e indico 'FundoImobiliario' para que o Python
    #ja reconheça a maneira como eu quero trabalhar, no caso com metos e parametros do maxima_vacancia_media
    def aplica_estrategia(self, fundo: FundoImobiliario):  # apenas pergunto se o fundo passa ou não na regra definida
        # pela classe 'Estrategia' como teria que usar if e else para retornar True se passa e False se não passa
        # em cada um dos atrbutos posso ultilizar o 'or' e colocar cada um dos atributos e sua estrategia especifica,
        # mas so precisarei usar o if e else uma vez

        if self.segmento != '':  # defini essa função para todos os segmentos então ele virão com 'string' vazia
            # caso não venha, ou seja, diferente '!' quero que ele retorne False e que esses não entrem na
            #cadeia de funções maix abaixo

            if fundo.segmento != self.segmento:
                return False
        #caso seja uma 'string' vazia ela vai percorrer essa cadeia de comandos
        if fundo.cotacao_atual < self.cotacao_atual_minima \
                or fundo.ffo_yeild < self.ffo_yeild_minimo \
                or fundo.dividiend_yeld < self.dividiend_yeld_minimo \
                or fundo.p_vp < self.p_vp_minimo \
                or fundo.valor_mercado < self.valor_mercado_minimo \
                or fundo.liquidez < self.liquidez_minima \
                or fundo.qt_imoveis < self.qt_minima_imoveis \
                or fundo.preco_m2 < self.valor_minimo_preco_m2 \
                or fundo.aluguel_m2 < self.valor_minimo_aluguel_m2 \
                or fundo.cap_rate < self.valor_minimo_cap_rate \
                or fundo.vacancia_media < self.maxima_vacancia_media:
            return False
        else:
            return True
