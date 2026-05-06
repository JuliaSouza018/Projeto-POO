#imports NECESSÁRIOS para criar enumeradores e usar o método datetime
from datetime import datetime
from enum import Enum

class Cliente:
    def __init__(self,nome,cpf):
        self.nome = nome
        self.cpf = cpf
    def __str__(self):
        return f"Cliente({self.nome}, {self.cpf})"   


class Conta:
    def __init__(self,numero,saldo):
        self.numero = numero 
        self.saldo = saldo
    def __str__(self):
        return f"Conta({self.numero}, {self.saldo})" 

class ContaCorrente:
    def __init__(self,numero,saldo):
        self.numero = numero 
        self.saldo = saldo
    def __str__(self):
        return f"ContaCorrente({self.numero}, {self.saldo})"  

class ContaPoupanca:
    def __init__(self, numero, saldo):
        self.numero = numero 
        self.saldo = saldo    

    def __str__(self):
        return f"ContaPoupanca({self.numero}, {self.saldo})"   


#gabriel
# Lista de enumeradores para definir o estado da fatura
class EstadoFatura(Enum):
    ABERTA = "Aberta"
    FECHADA = "Fechada"
    VENCIDA = "Vencida"
    PAGA = "Paga"

# Lista de enumeradores para definir o tipo da transação
class TipoTransacao(Enum):
    ENTRADA = "Entrada"
    SAIDA = "Saída"
    GUARDAR_CAIXINHA = "GuardarCaixinha"
    COMPRA_ACOES = "CompraAções"


# 1. Classe TRANSAÇÃO 
class Transacao:
    def __init__(self, tipo: TipoTransacao, meio: str, valor: float, destinatario: str, remetente: str):
        self.tipo = tipo #recebe um variavel do tipo do enumerador
        self.meio = meio
        self.valor = valor
        self.data = datetime.now() #puxa data atual
        self.destinatario = destinatario
        self.remetente = remetente

    #isso é para printar o objeto todo
    def __str__(self):
        return f"{self.tipo.value} - R${self.valor:.2f} para {self.destinatario}"


# 2. Classe PAGAMENTOS 
# Classe Mãe
class Pagamento:
    def __init__(self, valor: float):
        self.valor = valor
        self.data = datetime.now()
        self.confirmado = False

    #método base, ele lança um erro
    def processar(self):
        raise NotImplementedError("Subclasses devem implementar o método processar()")

#subclasses para boleto e pix
class PagamentoBoleto(Pagamento):
    def __init__(self, valor: float, codigo_barras: str):
        super().__init__(valor)
        self.codigo_barras = codigo_barras

    def processar(self):
        print(f"Processando Boleto: {self.codigo_barras} | Valor: R${self.valor:.2f}")
        self.confirmado = True

class PagamentoPix(Pagamento):
    def __init__(self, valor: float, chave_pix: str):
        super().__init__(valor)
        self.chave_pix = chave_pix

    def processar(self):
        print(f"Processando PIX para chave: {self.chave_pix} | Valor: R${self.valor:.2f}")
        self.confirmado = True


# 3. classe FATURA 
class Fatura:
    def __init__(self, mes: int, dia_fechamento: int, data_vencimento: datetime):
        self.mes = mes
        self.dia_fechamento = dia_fechamento
        self.data_vencimento = data_vencimento
        self.estado = EstadoFatura.ABERTA
        self.lista_de_objetos = []

    @property
    def valor_total(self):
        return sum(transacao.valor for transacao in self.lista_de_objetos)

    @property
    def pagamento_minimo(self):
        return self.valor_total * 0.15 

    def adicionar_compra(self, transacao: Transacao):
        if self.estado == EstadoFatura.ABERTA:
            self.lista_de_objetos.append(transacao)
        else:
            print(f"Atenção: A fatura do mês {self.mes} já está {self.estado.value}.")

    def pagar_fatura(self, pagamento: Pagamento):
        pagamento.processar()
        if pagamento.confirmado:
            self.estado = EstadoFatura.PAGA
            print(f"Fatura do mês {self.mes} paga com sucesso!\n")


# --- 4. classe CARTÃO DE CRÉDITO ---
class CartaoCredito:
    def __init__(self, numero: str, titular: str, cvc: str, data_validade: str, limite: float, bandeira: str, nfc: bool):
        #dados privados
        self._numero = numero 
        self._cvc = cvc
        
        self.titular = titular
        self.data_validade = data_validade
        self.limite = limite
        self.bandeira = bandeira
        self.nfc = nfc
        self.fatura_atual = None 

    @property
    def limite_disponivel(self):
        if self.fatura_atual:
            return self.limite - self.fatura_atual.valor_total
        return self.limite

    def mostrar_cartao_seguro(self):
        return f"**** **** **** {self._numero[-4:]}"

    def vincular_fatura(self, fatura: Fatura):
        self.fatura_atual = fatura

    def passar_cartao(self, transacao: Transacao):
        if not self.fatura_atual or self.fatura_atual.estado != EstadoFatura.ABERTA:
            print("Não há fatura aberta para registrar a compra.")
            return

        if transacao.valor > self.limite_disponivel:
            print(f"Compra negada! Limite disponível: R${self.limite_disponivel:.2f}")
            return

        self.fatura_atual.adicionar_compra(transacao)
        print(f"Compra de R${transacao.valor:.2f} aprovada no cartão {self.mostrar_cartao_seguro()}.")

#vinicius 

class Usuario:
    def __init__(self, id, nome, email, telefone):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone

    def __str__(self):
        return f"Usuário({self.id}, {self.nome})"

class Endereco:
    def __init__(self, id, rua, numero, cidade, estado):
        self.id = id
        self.rua = rua
        self.numero = numero
        self.cidade = cidade
        self.estado = estado

    def __str__(self):
        return f"Endereço({self.rua}, {self.numero})"

class Notificacao:
    def __init__(self, id, mensagem, tipo):
        self.id = id
        self.mensagem = mensagem
        self.tipo = tipo  

    def _str_(self):
        return f"Notificação({self.tipo})"

class Atendimento:
    def __init__(self, id, usuario, descricao, status):
        self.id = id
        self.usuario = usuario
        self.descricao = descricao
        self.status = status 

    def __str__(self):
        return f"Atendimento({self.id}, {self.status})"        

#Matheus 
# Classe Funcionario
class Funcionario:
    def __init__(self, nome, cargo):
        self.nome = nome
        self.cargo = cargo

    def __str__(self):
        return f"Funcionario({self.nome}, {self.cargo})"

# Classe AgenciaDigital
class AgenciaDigital:
    def __init__(self, codigo, cidade):
        self.codigo = codigo
        self.cidade = cidade

    def __str__(self):
        return f"AgenciaDigital({self.codigo}, {self.cidade})"

#kauá
class LimiteCartao:
    def __init__(self, id, nome_cliente, limite_total, gasto_atual):
        self.id = id
        self.cliente = nome_cliente
        self._total = limite_total        # encapsulado
        self._gasto = gasto_atual         # encapsulado

    # método para calcular disponível (abstração)
    def calcular_disponivel(self):
        return self._total - self._gasto

    # método para gastar valor
    def gastar(self, valor):
        if valor > 0 and valor <= self.calcular_disponivel():
            self._gasto += valor
            print(f"Gasto de R${valor:.2f} realizado.")
        else:
            print("Limite insuficiente ou valor inválido.")

    # método para pagamento (reduz gasto)
    def pagar_fatura(self, valor):
        if valor > 0:
            self._gasto -= valor
            if self._gasto < 0:
                self._gasto = 0
            print(f"Pagamento de R${valor:.2f} realizado.")
        else:
            print("Valor inválido.")

    def __str__(self):
        return f"LimiteCartao({self.cliente}, Disponível: R${self.calcular_disponivel():.2f})"


class HistoricoTransferencia:
    def __init__(self, id, data, valor, recebedor, tipo):
        self.id = id
        self.data = data
        self.valor = valor
        self.recebedor = recebedor
        self.tipo = tipo

    def __str__(self):
        return f"{self.data} - R${self.valor:.2f} para {self.recebedor} ({self.tipo})"

# Matheus
# Funcionários
funcionario1 = Funcionario("Carlos Silva", "Gerente")
funcionario2 = Funcionario("Ana Souza", "Atendente")
funcionario3 = Funcionario("Bruno Lima", "Analista")
funcionario4 = Funcionario("Juliana Costa", "Supervisora")
funcionario5 = Funcionario("Pedro Alves", "Caixa")

# Agências Digitais
agencia1 = AgenciaDigital(101, "São Paulo")
agencia2 = AgenciaDigital(102, "Rio de Janeiro")
agencia3 = AgenciaDigital(103, "Belo Horizonte")
agencia4 = AgenciaDigital(104, "Curitiba")
agencia5 = AgenciaDigital(105, "Porto Alegre")

cliente1 = Cliente("cliente1" , "000.000.000-20")
cliente2 = Cliente("cliente2" , "111.111.111-21")
cliente3 = Cliente("cliente3" , "222.222.222-22")
cliente4 = Cliente("cliente4" , "333.333.333-23")
cliente5 = Cliente("cliente5" , "444.444.444-24")

conta1 = Conta("00123456-1" , "1700")
conta2 = Conta("00123456-2" , "1800")
conta3 = Conta("12345.67-3" , "1900")
conta4 = Conta("12345.67-4" , "2000")
conta5 = Conta("00012345-5" , "2100")

contaCorrente1 = ContaCorrente("00123456-1" , "2100")
contaCorrente2 = ContaCorrente("00123456-2" , "2200")
contaCorrente3 = ContaCorrente("00123456-3" , "2300")
contaCorrente4 = ContaCorrente("00123456-4" , "2400")
contaCorrente5 = ContaCorrente("00123456-5" , "2500")

contaPoupanca1 = ContaPoupanca("000543210-1" , "3300")
contaPoupanca2 = ContaPoupanca("000543210-2" , "3400")
contaPoupanca3 = ContaPoupanca("000543210-3" , "3500")
contaPoupanca4 = ContaPoupanca("000543210-4" , "3600")
contaPoupanca5 = ContaPoupanca("000543210-5" , "3700")


##gabriel
transacao1 = Transacao(TipoTransacao.SAIDA, "Crédito", 150.50, "Supermercado Bom Preço", "João Silva")
transacao2 = Transacao(TipoTransacao.SAIDA, "Crédito", 89.90, "Livraria Leitura", "João Silva")
transacao3 = Transacao(TipoTransacao.SAIDA, "Crédito", 25.00, "Padaria Central", "João Silva")
transacao4 = Transacao(TipoTransacao.SAIDA, "Crédito", 200.00, "Posto Ipiranga", "João Silva")
transacao5 = Transacao(TipoTransacao.SAIDA, "Crédito", 59.99, "Farmácia Drogasil", "João Silva")

boleto1 = PagamentoBoleto(150.50, "34191.09008 61713.957308 71444.640008 1 90000000015050")
boleto2 = PagamentoBoleto(89.90, "03399.87362 54000.000000 00018.234567 8 80000000008990")
boleto3 = PagamentoBoleto(25.00, "23793.38128 60064.093409 83000.041011 5 70000000002500")
boleto4 = PagamentoBoleto(200.00, "10499.12345 67890.123456 78901.234567 2 60000000020000")
boleto5 = PagamentoBoleto(59.99, "00190.00009 01234.567890 12345.678901 3 50000000005999")

pix1 = PagamentoPix(150.50, "joao.silva@email.com")
pix2 = PagamentoPix(89.90, "123.456.789-00")
pix3 = PagamentoPix(25.00, "+5511999999999")
pix4 = PagamentoPix(200.00, "d2b456-123f-45g7-89h0-1234567890ab") # Chave aleatória
pix5 = PagamentoPix(59.99, "maria.souza@email.com")


fatura_jan = Fatura(mes=1, dia_fechamento=25, data_vencimento=datetime(2026, 2, 5))
fatura_fev = Fatura(mes=2, dia_fechamento=25, data_vencimento=datetime(2026, 3, 5))
fatura_mar = Fatura(mes=3, dia_fechamento=25, data_vencimento=datetime(2026, 4, 5))
fatura_abr = Fatura(mes=4, dia_fechamento=25, data_vencimento=datetime(2026, 5, 5))
fatura_mai = Fatura(mes=5, dia_fechamento=25, data_vencimento=datetime(2026, 6, 5))

cartao1 = CartaoCredito("1111222233334444", "João Silva", "123", "12/29", 1500.00, "Mastercard", True)
cartao2 = CartaoCredito("5555666677778888", "Maria Souza", "456", "10/30", 3000.00, "Visa", True)
cartao3 = CartaoCredito("9999000011112222", "Carlos Lima", "789", "05/27", 800.00, "Elo", False)
cartao4 = CartaoCredito("3333444455556666", "Ana Costa", "321", "08/28", 5000.00, "Mastercard", True)
cartao5 = CartaoCredito("7777888899990000", "Pedro Alves", "654", "01/31", 10000.00, "Visa", False)

#vinicius

user1 = Usuario(1, "João Silva", "joao@email.com", "11999999999")
user2 = Usuario(2, "Maria Souza", "maria@email.com", "11988888888")
user3 = Usuario(3, "Carlos Lima", "carlos@email.com", "11977777777")
user4 = Usuario(4, "Ana Costa", "ana@email.com", "11966666666")
user5 = Usuario(5, "Pedro Alves", "pedro@email.com", "11955555555")

endereco1 = Endereco(1, "Rua A", 100, "São Paulo", "SP")
endereco2 = Endereco(2, "Rua B", 200, "Rio de Janeiro", "RJ")
endereco3 = Endereco(3, "Rua C", 300, "Belo Horizonte", "MG")
endereco4 = Endereco(4, "Rua D", 400, "Curitiba", "PR")
endereco5 = Endereco(5, "Rua E", 500, "Porto Alegre", "RS")

notificacao1 = Notificacao(1, "Seu pedido foi enviado", "email")
notificacao2 = Notificacao(2, "Nova mensagem recebida", "push")
notificacao3 = Notificacao(3, "Pagamento aprovado", "sms")
notificacao4 = Notificacao(4, "Atualização disponível", "push")
notificacao5 = Notificacao(5, "Senha alterada com sucesso", "email")

atendimento1 = Atendimento(1, u1, "Problema no login", "aberto")
atendimento2 = Atendimento(2, u2, "Erro no pagamento", "fechado")
atendimento3 = Atendimento(3, u3, "Dúvida sobre produto", "aberto")
atendimento4 = Atendimento(4, u4, "Solicitação de reembolso", "fechado")
atendimento5 = Atendimento(5, u5, "Alteração de dados", "aberto")

#kauá
limiteCartao1 = LimiteCartao(1, "João Silva", 5000.0, 1200.0)
limiteCartao2 = LimiteCartao(2, "Maria Oliveira", 2500.0, 2450.0)
limiteCartao3 = LimiteCartao(3, "Carlos Souza", 10000.0, 0.0)
limiteCartao4 = LimiteCartao(4, "Ana Costa", 1500.0, 800.0)
limiteCartao5 = LimiteCartao(5, "Bruno Alves", 3000.0, 3100.0)

histTransf1 = HistoricoTransferencia(1, "20/03/2026", 150.0, "Mercado Central", "Pix")
histTransf2 = HistoricoTransferencia(2, "21/03/2026", 45.90, "Netflix", "Crédito")
histTransf3 = HistoricoTransferencia(3, "22/03/2026", 1200.0, "Aluguel", "TED")
histTransf4 = HistoricoTransferencia(4, "23/03/2026", 15.00, "Padaria Pão de Mel", "Débito")
histTransf5 = HistoricoTransferencia(5, "24/03/2026", 350.0, "Posto Combustível", "Crédito")
