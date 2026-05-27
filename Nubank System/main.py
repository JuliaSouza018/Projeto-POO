from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod

# Importações:
# datetime -> trabalhar com datas
# Enum -> criar valores padronizados
# ABC e abstractmethod -> criar classes abstratas


# ============================================================
# ENUMERADORES
# ============================================================

# Enum para estados da fatura
class EstadoFatura(Enum):
    ABERTA  = "Aberta"
    FECHADA = "Fechada"
    VENCIDA = "Vencida"
    PAGA    = "Paga"


# Enum para tipos de transações
class TipoTransacao(Enum):
    ENTRADA          = "Entrada"
    SAIDA            = "Saída"
    GUARDAR_CAIXINHA = "GuardarCaixinha"
    COMPRA_ACOES     = "CompraAções"


# Enum para tipos de investimento
class TipoInvestimento(Enum):
    RENDA_FIXA     = "Renda Fixa"
    RENDA_VARIAVEL = "Renda Variável"
    FUNDO          = "Fundo"


# ============================================================
# CLASSE CLIENTE
# ============================================================

class Cliente:

    # Método construtor
    def __init__(self, nome: str, cpf: str, email: str, telefone: str):

        self.nome = nome

        # Encapsulamento -> CPF privado
        self.__cpf = cpf

        self.email = email
        self.telefone = telefone


    # Getter -> Acesar o CPF de uma forma mascarada
    @property
    def cpf(self) -> str:
        return f"***.{self.__cpf[4:7]}.***-{self.__cpf[-2:]}"


    # Setter -> valida o CPF
    @cpf.setter
    def cpf(self, novo_cpf: str):

        if len(novo_cpf.replace(".", "").replace("-", "")) == 11:
            self.__cpf = novo_cpf
        else:
            raise ValueError("CPF inválido.")


    def __str__(self):
        return f"Cliente({self.nome}, CPF: {self.cpf})"


# ============================================================
# CLASSE CONTA (CLASSE ABSTRATA)
# ============================================================

# Classe mãe das contas
class Conta(ABC):

    def __init__(self, numero: str, saldo: float, cliente: Cliente):

        self._numero = numero

        # Saldo privado -> encapsulamento
        self.__saldo = float(saldo)

        self.cliente = cliente


    # Getter do saldo encapsulado
    @property
    def saldo(self) -> float:
        return self.__saldo


    # Setter com validação para impedir valores negativos
    @saldo.setter
    def saldo(self, valor: float):

        if valor < 0:
            raise ValueError("Saldo não pode ser negativo.")

        self.__saldo = valor


    @property
    def numero(self) -> str:
        return self._numero


    # Método abstrato -> obriga as classes filhas implementarem
    @abstractmethod
    def tipo_conta(self) -> str:
        pass


    # Método para depósito encapsulado
    def depositar(self, valor: float):

        if valor > 0:

            self.__saldo += valor

            print(f"Depósito realizado.")

        else:
            print("Valor inválido.")


    # Método para saque
    def sacar(self, valor: float):

        if 0 < valor <= self.__saldo:

            self.__saldo -= valor

            print(f"Saque realizado.")

        else:
            print("Saldo insuficiente.")


    def __str__(self):

        return f"{self.tipo_conta()} - Saldo: R${self.__saldo:.2f}"


# ============================================================
# CONTA CORRENTE
# ============================================================

# Herança -> ContaCorrente herda de Conta
class ContaCorrente(Conta):

    def __init__(self, numero: str, saldo: float,
                 cliente: Cliente,
                 limite_cheque_especial: float = 500.0):

        super().__init__(numero, saldo, cliente)

        self.limite_cheque_especial = limite_cheque_especial


    def tipo_conta(self) -> str:
        return "ContaCorrente"


    # Polimorfismo -> sobrescrevendo método sacar
    def sacar(self, valor: float):

        # Soma saldo + cheque especial
        limite_total = self.saldo + self.limite_cheque_especial

        if 0 < valor <= limite_total:

            self.saldo = max(0.0, self.saldo - valor)

            print("Saque realizado com cheque especial.")

        else:
            print("Limite insuficiente.")


# ============================================================
# CONTA POUPANÇA
# ============================================================

# Herança da classe Conta
class ContaPoupanca(Conta):

    def __init__(self, numero: str, saldo: float,
                 cliente: Cliente,
                 taxa_rendimento: float = 0.005):

        super().__init__(numero, saldo, cliente)

        # Taxa de rendimento da poupança
        self.taxa_rendimento = taxa_rendimento


    def tipo_conta(self) -> str:
        return "ContaPoupanca"


    # Método para aplicar rendimento
    def aplicar_rendimento(self):

        rendimento = self.saldo * self.taxa_rendimento

        self.saldo += rendimento

        print("Rendimento aplicado.")


# ============================================================
# CLASSE 5 — TRANSAÇÃO
# ============================================================
class Transacao:
    def __init__(self, tipo: TipoTransacao, meio: str, valor: float,
                 destinatario: str, remetente: str):
        self.tipo         = tipo
        self.meio         = meio
        self.__valor      = valor      # privado
        self.data         = datetime.now()
        self.destinatario = destinatario
        self.remetente    = remetente

    @property
    def valor(self) -> float:
        return self.__valor

    def __str__(self):
        return (f"{self.tipo.value} | R${self.__valor:.2f} | "
                f"{self.remetente} → {self.destinatario} | {self.meio}")


# ============================================================
# CLASSE 6 — PAGAMENTO  (abstrata — abstração + polimorfismo)
# ============================================================
class Pagamento(ABC):
    def __init__(self, valor: float):
        self._valor     = valor
        self.data       = datetime.now()
        self.confirmado = False

    @property
    def valor(self) -> float:
        return self._valor

    @abstractmethod
    def processar(self):
        """Cada subclasse processa o pagamento à sua maneira (polimorfismo)."""
        pass

    def __str__(self):
        status = "Confirmado" if self.confirmado else "Pendente"
        return f"Pagamento(R${self._valor:.2f}, {status})"


# CLASSE 7 — PAGAMENTO BOLETO  (herança de Pagamento)
class PagamentoBoleto(Pagamento):
    def __init__(self, valor: float, codigo_barras: str):
        super().__init__(valor)
        self.codigo_barras = codigo_barras

    def processar(self):
        print(f"Processando Boleto: {self.codigo_barras} | Valor: R${self._valor:.2f}")
        self.confirmado = True


# CLASSE 8 — PAGAMENTO PIX  (herança de Pagamento)
class PagamentoPix(Pagamento):
    def __init__(self, valor: float, chave_pix: str):
        super().__init__(valor)
        self.chave_pix = chave_pix

    def processar(self):
        print(f"Processando PIX → {self.chave_pix} | Valor: R${self._valor:.2f}")
        self.confirmado = True


# CLASSE 9 — PAGAMENTO DÉBITO  (herança de Pagamento — nova classe)
class PagamentoDebito(Pagamento):
    def __init__(self, valor: float, conta: 'ContaCorrente'):
        super().__init__(valor)
        self.__conta = conta

    def processar(self):
        print(f"Processando Débito | Conta: {self.__conta.numero} | Valor: R${self._valor:.2f}")
        self.__conta.sacar(self._valor)
        self.confirmado = True


# ============================================================
# CLASSE 10 — FATURA
# ============================================================
class Fatura:
    def __init__(self, mes: int, dia_fechamento: int, data_vencimento: datetime):
        self.mes              = mes
        self.dia_fechamento   = dia_fechamento
        self.data_vencimento  = data_vencimento
        self.estado           = EstadoFatura.ABERTA
        self.__transacoes     = []    # privado

    @property
    def transacoes(self):
        return list(self.__transacoes)   # cópia — não permite alteração direta

    @property
    def valor_total(self) -> float:
        return sum(t.valor for t in self.__transacoes)

    @property
    def pagamento_minimo(self) -> float:
        return self.valor_total * 0.15

    def adicionar_compra(self, transacao: Transacao):
        if self.estado == EstadoFatura.ABERTA:
            self.__transacoes.append(transacao)
        else:
            print(f"Fatura do mês {self.mes} já está {self.estado.value}. Compra não registrada.")

    def fechar(self):
        if self.estado == EstadoFatura.ABERTA:
            self.estado = EstadoFatura.FECHADA
            print(f"Fatura de mês {self.mes} fechada. Total: R${self.valor_total:.2f}")

    def pagar_fatura(self, pagamento: Pagamento):
        pagamento.processar()
        if pagamento.confirmado:
            self.estado = EstadoFatura.PAGA
            print(f"Fatura do mês {self.mes} paga com sucesso! Total: R${self.valor_total:.2f}\n")

    def __str__(self):
        return (f"Fatura(Mês {self.mes}, Estado: {self.estado.value}, "
                f"Total: R${self.valor_total:.2f})")


# ============================================================
# CLASSE 11 — CARTÃO DE CRÉDITO
# ============================================================
class CartaoCredito:
    def __init__(self, numero: str, titular: str, cvc: str,
                 data_validade: str, limite: float, bandeira: str, nfc: bool):
        self.__numero    = numero     # privado
        self.__cvc       = cvc       # privado
        self.titular     = titular
        self.data_validade = data_validade
        self.__limite    = limite    # privado com getter
        self.bandeira    = bandeira
        self.nfc         = nfc
        self.fatura_atual: Fatura | None = None

    @property
    def limite(self) -> float:
        return self.__limite

    @property
    def limite_disponivel(self) -> float:
        if self.fatura_atual:
            return self.__limite - self.fatura_atual.valor_total
        return self.__limite

    def numero_seguro(self) -> str:
        return f"**** **** **** {self.__numero[-4:]}"

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
        print(f"Compra de R${transacao.valor:.2f} aprovada no cartão {self.numero_seguro()}.")

    def __str__(self):
        return (f"CartaoCredito({self.bandeira}, Titular: {self.titular}, "
                f"Limite: R${self.__limite:.2f}, NFC: {self.nfc})")


# ============================================================
# CLASSE 12 — LIMITE CARTÃO  (encapsulamento total)
# ============================================================
class LimiteCartao:
    def __init__(self, id: int, cliente: Cliente, limite_total: float, gasto_atual: float):
        self.id       = id
        self.cliente  = cliente
        self.__total  = limite_total
        self.__gasto  = gasto_atual

    def calcular_disponivel(self) -> float:
        return self.__total - self.__gasto

    def gastar(self, valor: float):
        if valor > 0 and valor <= self.calcular_disponivel():
            self.__gasto += valor
            print(f"Gasto de R${valor:.2f} realizado. Disponível: R${self.calcular_disponivel():.2f}")
        else:
            print("Limite insuficiente ou valor inválido.")

    def pagar_fatura(self, valor: float):
        if valor > 0:
            self.__gasto = max(0.0, self.__gasto - valor)
            print(f"Pagamento de R${valor:.2f} realizado.")
        else:
            print("Valor inválido.")

    def __str__(self):
        return (f"LimiteCartao({self.cliente.nome}, "
                f"Total: R${self.__total:.2f}, "
                f"Disponível: R${self.calcular_disponivel():.2f})")


# ============================================================
# CLASSE 13 — HISTÓRICO DE TRANSFERÊNCIA
# ============================================================
class HistoricoTransferencia:
    def __init__(self, id: int, data: str, valor: float, recebedor: str, tipo: str):
        self.id        = id
        self.data      = data
        self.__valor   = valor      # privado
        self.recebedor = recebedor
        self.tipo      = tipo

    @property
    def valor(self) -> float:
        return self.__valor

    def __str__(self):
        return f"[{self.data}] R${self.__valor:.2f} → {self.recebedor} ({self.tipo})"


# ============================================================
# CLASSE 14 — USUÁRIO
# ============================================================
class Usuario:
    def __init__(self, id: int, nome: str, email: str, telefone: str, senha: str):
        self.id        = id
        self.nome      = nome
        self.email     = email
        self.telefone  = telefone
        self.__senha   = senha     # privado

    def verificar_senha(self, tentativa: str) -> bool:
        return self.__senha == tentativa

    def alterar_senha(self, senha_atual: str, nova_senha: str):
        if self.verificar_senha(senha_atual):
            self.__senha = nova_senha
            print("Senha alterada com sucesso.")
        else:
            print("Senha atual incorreta.")

    def __str__(self):
        return f"Usuário({self.id}, {self.nome}, {self.email})"


# ============================================================
# CLASSE 15 — ENDEREÇO
# ============================================================
class Endereco:
    def __init__(self, id: int, rua: str, numero: int, bairro: str,
                 cidade: str, estado: str, cep: str):
        self.id     = id
        self.rua    = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep    = cep

    def __str__(self):
        return f"{self.rua}, {self.numero} — {self.bairro}, {self.cidade}/{self.estado}"


# ============================================================
# CLASSE 16 — NOTIFICAÇÃO  (corrigido __str__)
# ============================================================
class Notificacao:
    def __init__(self, id: int, mensagem: str, tipo: str, lida: bool = False):
        self.id       = id
        self.mensagem = mensagem
        self.tipo     = tipo     # "email", "push", "sms"
        self.lida     = lida
        self.data     = datetime.now()

    def marcar_lida(self):
        self.lida = True

    def __str__(self):                            # CORRIGIDO: era _str_
        status = "✓" if self.lida else "●"
        return f"Notificação [{self.tipo.upper()}] {status} — {self.mensagem}"


# ============================================================
# CLASSE 17 — ATENDIMENTO  (referências a Usuario corrigidas)
# ============================================================
class Atendimento:
    def __init__(self, id: int, usuario: Usuario, descricao: str, status: str):
        self.id        = id
        self.usuario   = usuario    # CORRIGIDO: era u1, u2 (NameError)
        self.descricao = descricao
        self.status    = status
        self.data      = datetime.now()

    def encerrar(self):
        self.status = "fechado"
        print(f"Atendimento #{self.id} encerrado.")

    def __str__(self):
        return f"Atendimento(#{self.id}, {self.usuario.nome}, Status: {self.status})"


# ============================================================
# CLASSE 18 — FUNCIONÁRIO  (enriquecido)
# ============================================================
class Funcionario:
    def __init__(self, id: int, nome: str, cargo: str, salario: float, agencia: 'AgenciaDigital'):
        self.id      = id
        self.nome    = nome
        self.cargo   = cargo
        self.__salario = salario   # privado
        self.agencia = agencia

    @property
    def salario(self) -> float:
        return self.__salario

    def reajuste(self, percentual: float):
        if percentual > 0:
            self.__salario *= (1 + percentual / 100)
            print(f"Novo salário de {self.nome}: R${self.__salario:.2f}")

    def __str__(self):
        return f"Funcionario({self.nome}, {self.cargo}, Agência: {self.agencia.codigo})"


# ============================================================
# CLASSE 19 — AGÊNCIA DIGITAL  (enriquecida)
# ============================================================
class AgenciaDigital:
    def __init__(self, codigo: int, cidade: str, estado: str, telefone: str):
        self.codigo   = codigo
        self.cidade   = cidade
        self.estado   = estado
        self.telefone = telefone

    def __str__(self):
        return f"AgenciaDigital({self.codigo}, {self.cidade}/{self.estado})"


# ============================================================
# CLASSE 20 — EMPRÉSTIMO  (nova classe)
# ============================================================
class Emprestimo:
    def __init__(self, id: int, cliente: Cliente, valor: float,
                 parcelas: int, taxa_juros: float):
        self.id          = id
        self.cliente     = cliente
        self.__valor     = valor       # privado
        self.parcelas    = parcelas
        self.__taxa      = taxa_juros  # privado (ex: 0.02 = 2% ao mês)
        self.ativo       = True
        self.data        = datetime.now()

    @property
    def valor(self) -> float:
        return self.__valor

    @property
    def valor_total_com_juros(self) -> float:
        return self.__valor * ((1 + self.__taxa) ** self.parcelas)

    @property
    def valor_parcela(self) -> float:
        return self.valor_total_com_juros / self.parcelas

    def quitar(self):
        self.ativo = False
        print(f"Empréstimo #{self.id} quitado.")

    def __str__(self):
        return (f"Emprestimo(#{self.id}, {self.cliente.nome}, "
                f"R${self.__valor:.2f} em {self.parcelas}x de R${self.valor_parcela:.2f})")


# ============================================================
# CLASSE BÔNUS — INVESTIMENTO  (excede os 20, mas agrega valor)
# ============================================================
class Investimento:
    def __init__(self, id: int, cliente: Cliente, tipo: TipoInvestimento,
                 valor_aplicado: float, rentabilidade_anual: float):
        self.id                  = id
        self.cliente             = cliente
        self.tipo                = tipo
        self.__valor_aplicado    = valor_aplicado
        self.rentabilidade_anual = rentabilidade_anual
        self.data_aplicacao      = datetime.now()

    @property
    def valor_aplicado(self) -> float:
        return self.__valor_aplicado

    def projetar_rendimento(self, anos: int) -> float:
        return self.__valor_aplicado * ((1 + self.rentabilidade_anual) ** anos)

    def __str__(self):
        return (f"Investimento({self.tipo.value}, {self.cliente.nome}, "
                f"R${self.__valor_aplicado:.2f})")


# ============================================================
# CLASSE BÔNUS — CAIXINHA  (cofre virtual)
# ============================================================
class Caixinha:
    def __init__(self, id: int, cliente: Cliente, nome: str, meta: float):
        self.id        = id
        self.cliente   = cliente
        self.nome      = nome
        self.meta      = meta
        self.__saldo   = 0.0

    @property
    def saldo(self) -> float:
        return self.__saldo

    @property
    def progresso(self) -> float:
        return (self.__saldo / self.meta * 100) if self.meta > 0 else 0

    def guardar(self, valor: float):
        if valor > 0:
            self.__saldo += valor
            print(f"R${valor:.2f} guardado na caixinha '{self.nome}'. "
                  f"Progresso: {self.progresso:.1f}%")

    def resgatar(self, valor: float):
        if 0 < valor <= self.__saldo:
            self.__saldo -= valor
            print(f"R${valor:.2f} resgatado da caixinha '{self.nome}'.")
        else:
            print("Saldo insuficiente na caixinha.")

    def __str__(self):
        return (f"Caixinha('{self.nome}', {self.cliente.nome}, "
                f"R${self.__saldo:.2f} / R${self.meta:.2f} "
                f"[{self.progresso:.1f}%])")


# ============================================================
# INSTÂNCIAS — 5 objetos por classe
# ============================================================

# --- AgenciaDigital (criada antes de Funcionario) ---
agencia1 = AgenciaDigital(101, "São Paulo",       "SP", "(11) 3000-0001")
agencia2 = AgenciaDigital(102, "Rio de Janeiro",  "RJ", "(21) 3000-0002")
agencia3 = AgenciaDigital(103, "Belo Horizonte",  "MG", "(31) 3000-0003")
agencia4 = AgenciaDigital(104, "Curitiba",        "PR", "(41) 3000-0004")
agencia5 = AgenciaDigital(105, "Porto Alegre",    "RS", "(51) 3000-0005")

# --- Funcionario ---
funcionario1 = Funcionario(1, "Carlos Silva",   "Gerente",      8500.00, agencia1)
funcionario2 = Funcionario(2, "Ana Souza",      "Atendente",    3200.00, agencia2)
funcionario3 = Funcionario(3, "Bruno Lima",     "Analista",     5400.00, agencia3)
funcionario4 = Funcionario(4, "Juliana Costa",  "Supervisora",  6700.00, agencia1)
funcionario5 = Funcionario(5, "Pedro Alves",    "Caixa",        2900.00, agencia4)

# --- Cliente ---
cliente1 = Cliente("João Silva",    "123.456.789-01", "joao@email.com",    "11999999999")
cliente2 = Cliente("Maria Souza",   "234.567.890-12", "maria@email.com",   "11988888888")
cliente3 = Cliente("Carlos Lima",   "345.678.901-23", "carlos@email.com",  "11977777777")
cliente4 = Cliente("Ana Costa",     "456.789.012-34", "ana@email.com",     "11966666666")
cliente5 = Cliente("Pedro Alves",   "567.890.123-45", "pedro@email.com",   "11955555555")

# --- ContaCorrente (herda Conta) ---
contaCorrente1 = ContaCorrente("CC-001", 2100.00, cliente1, 500.00)
contaCorrente2 = ContaCorrente("CC-002", 2200.00, cliente2, 300.00)
contaCorrente3 = ContaCorrente("CC-003", 2300.00, cliente3, 700.00)
contaCorrente4 = ContaCorrente("CC-004", 2400.00, cliente4, 200.00)
contaCorrente5 = ContaCorrente("CC-005", 2500.00, cliente5, 1000.00)

# --- ContaPoupanca (herda Conta) ---
contaPoupanca1 = ContaPoupanca("CP-001", 3300.00, cliente1, 0.005)
contaPoupanca2 = ContaPoupanca("CP-002", 3400.00, cliente2, 0.006)
contaPoupanca3 = ContaPoupanca("CP-003", 3500.00, cliente3, 0.005)
contaPoupanca4 = ContaPoupanca("CP-004", 3600.00, cliente4, 0.007)
contaPoupanca5 = ContaPoupanca("CP-005", 3700.00, cliente5, 0.005)

# --- Transacao ---
transacao1 = Transacao(TipoTransacao.SAIDA,    "Crédito", 150.50,  "Supermercado Bom Preço", "João Silva")
transacao2 = Transacao(TipoTransacao.SAIDA,    "Crédito",  89.90,  "Livraria Leitura",       "João Silva")
transacao3 = Transacao(TipoTransacao.SAIDA,    "Crédito",  25.00,  "Padaria Central",        "João Silva")
transacao4 = Transacao(TipoTransacao.SAIDA,    "Crédito", 200.00,  "Posto Ipiranga",         "João Silva")
transacao5 = Transacao(TipoTransacao.ENTRADA,  "Pix",    1500.00,  "João Silva",             "Empresa XYZ")

# --- PagamentoBoleto (herda Pagamento) ---
boleto1 = PagamentoBoleto(150.50, "34191.09008 61713.957308 71444.640008 1 90000000015050")
boleto2 = PagamentoBoleto( 89.90, "03399.87362 54000.000000 00018.234567 8 80000000008990")
boleto3 = PagamentoBoleto( 25.00, "23793.38128 60064.093409 83000.041011 5 70000000002500")
boleto4 = PagamentoBoleto(200.00, "10499.12345 67890.123456 78901.234567 2 60000000020000")
boleto5 = PagamentoBoleto( 59.99, "00190.00009 01234.567890 12345.678901 3 50000000005999")

# --- PagamentoPix (herda Pagamento) ---
pix1 = PagamentoPix(150.50, "joao.silva@email.com")
pix2 = PagamentoPix( 89.90, "123.456.789-00")
pix3 = PagamentoPix( 25.00, "+5511999999999")
pix4 = PagamentoPix(200.00, "d2b456-123f-45g7-89h0-1234567890ab")
pix5 = PagamentoPix( 59.99, "maria.souza@email.com")

# --- PagamentoDebito (herda Pagamento) ---
debito1 = PagamentoDebito( 50.00, contaCorrente1)
debito2 = PagamentoDebito( 30.00, contaCorrente2)
debito3 = PagamentoDebito(120.00, contaCorrente3)
debito4 = PagamentoDebito( 80.00, contaCorrente4)
debito5 = PagamentoDebito( 15.00, contaCorrente5)

# --- Fatura ---
fatura_jan = Fatura(mes=1, dia_fechamento=25, data_vencimento=datetime(2026, 2, 5))
fatura_fev = Fatura(mes=2, dia_fechamento=25, data_vencimento=datetime(2026, 3, 5))
fatura_mar = Fatura(mes=3, dia_fechamento=25, data_vencimento=datetime(2026, 4, 5))
fatura_abr = Fatura(mes=4, dia_fechamento=25, data_vencimento=datetime(2026, 5, 5))
fatura_mai = Fatura(mes=5, dia_fechamento=25, data_vencimento=datetime(2026, 6, 5))

# --- CartaoCredito ---
cartao1 = CartaoCredito("1111222233334444", "João Silva",  "123", "12/29",  1500.00, "Mastercard", True)
cartao2 = CartaoCredito("5555666677778888", "Maria Souza", "456", "10/30",  3000.00, "Visa",       True)
cartao3 = CartaoCredito("9999000011112222", "Carlos Lima", "789", "05/27",   800.00, "Elo",        False)
cartao4 = CartaoCredito("3333444455556666", "Ana Costa",   "321", "08/28",  5000.00, "Mastercard", True)
cartao5 = CartaoCredito("7777888899990000", "Pedro Alves", "654", "01/31", 10000.00, "Visa",       False)

# --- LimiteCartao ---
limiteCartao1 = LimiteCartao(1, cliente1,  5000.00, 1200.00)
limiteCartao2 = LimiteCartao(2, cliente2,  2500.00, 2450.00)
limiteCartao3 = LimiteCartao(3, cliente3, 10000.00,    0.00)
limiteCartao4 = LimiteCartao(4, cliente4,  1500.00,  800.00)
limiteCartao5 = LimiteCartao(5, cliente5,  3000.00, 3100.00)

# --- HistoricoTransferencia ---
histTransf1 = HistoricoTransferencia(1, "20/03/2026",  150.00, "Mercado Central",    "Pix")
histTransf2 = HistoricoTransferencia(2, "21/03/2026",   45.90, "Netflix",            "Crédito")
histTransf3 = HistoricoTransferencia(3, "22/03/2026", 1200.00, "Aluguel",            "TED")
histTransf4 = HistoricoTransferencia(4, "23/03/2026",   15.00, "Padaria Pão de Mel", "Débito")
histTransf5 = HistoricoTransferencia(5, "24/03/2026",  350.00, "Posto Combustível",  "Crédito")

# --- Usuario ---
user1 = Usuario(1, "João Silva",   "joao@email.com",   "11999999999", "senha123")
user2 = Usuario(2, "Maria Souza",  "maria@email.com",  "11988888888", "abc456")
user3 = Usuario(3, "Carlos Lima",  "carlos@email.com", "11977777777", "pass789")
user4 = Usuario(4, "Ana Costa",    "ana@email.com",    "11966666666", "ana2024")
user5 = Usuario(5, "Pedro Alves",  "pedro@email.com",  "11955555555", "pedro99")

# --- Endereco ---
endereco1 = Endereco(1, "Rua das Flores",    100, "Centro",       "São Paulo",      "SP", "01310-100")
endereco2 = Endereco(2, "Av. Copacabana",    200, "Copacabana",   "Rio de Janeiro", "RJ", "22070-011")
endereco3 = Endereco(3, "Rua da Bahia",      300, "Lourdes",      "Belo Horizonte", "MG", "30160-010")
endereco4 = Endereco(4, "Rua XV de Nov.",    400, "Centro",       "Curitiba",       "PR", "80020-310")
endereco5 = Endereco(5, "Av. Borges de Med.",500, "Cidade Baixa", "Porto Alegre",   "RS", "90020-021")

# --- Notificacao (corrigido __str__) ---
notificacao1 = Notificacao(1, "Seu pix foi enviado com sucesso",    "push")
notificacao2 = Notificacao(2, "Nova mensagem do suporte",           "push")
notificacao3 = Notificacao(3, "Pagamento da fatura confirmado",     "sms")
notificacao4 = Notificacao(4, "Atualização de segurança disponível","email")
notificacao5 = Notificacao(5, "Senha alterada com sucesso",         "email")

# --- Atendimento (corrigido: user1~5 em vez de u1~5) ---
atendimento1 = Atendimento(1, user1, "Problema no login",         "aberto")
atendimento2 = Atendimento(2, user2, "Erro no pagamento",         "fechado")
atendimento3 = Atendimento(3, user3, "Dúvida sobre produto",      "aberto")
atendimento4 = Atendimento(4, user4, "Solicitação de reembolso",  "fechado")
atendimento5 = Atendimento(5, user5, "Alteração de dados",        "aberto")

# --- Emprestimo ---
emprestimo1 = Emprestimo(1, cliente1,  5000.00, 12, 0.018)
emprestimo2 = Emprestimo(2, cliente2,  2000.00,  6, 0.025)
emprestimo3 = Emprestimo(3, cliente3, 15000.00, 24, 0.015)
emprestimo4 = Emprestimo(4, cliente4,  1000.00,  3, 0.030)
emprestimo5 = Emprestimo(5, cliente5,  8000.00, 18, 0.020)

# --- Investimento ---
invest1 = Investimento(1, cliente1, TipoInvestimento.RENDA_FIXA,      1000.00, 0.12)
invest2 = Investimento(2, cliente2, TipoInvestimento.RENDA_VARIAVEL,  5000.00, 0.20)
invest3 = Investimento(3, cliente3, TipoInvestimento.FUNDO,           2500.00, 0.15)
invest4 = Investimento(4, cliente4, TipoInvestimento.RENDA_FIXA,      3000.00, 0.11)
invest5 = Investimento(5, cliente5, TipoInvestimento.RENDA_VARIAVEL, 10000.00, 0.25)

# --- Caixinha ---
caixinha1 = Caixinha(1, cliente1, "Viagem para Europa",  15000.00)
caixinha2 = Caixinha(2, cliente2, "Notebook Novo",        4500.00)
caixinha3 = Caixinha(3, cliente3, "Reserva de Emergência",10000.00)
caixinha4 = Caixinha(4, cliente4, "Casamento",            30000.00)
caixinha5 = Caixinha(5, cliente5, "Fundo para Carro",     25000.00)


# ============================================================
# DEMONSTRAÇÃO — mostra o sistema funcionando
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("        NUBANCK — Sistema Bancário Digital")
    print("=" * 60)

    # Herança + Polimorfismo: ContaCorrente vs ContaPoupanca
    print("\n[CONTAS]")
    print(contaCorrente1)
    print(contaPoupanca1)
    contaCorrente1.depositar(500)
    contaCorrente1.sacar(200)
    contaPoupanca1.aplicar_rendimento()

    # Cartão + Fatura
    print("\n[CARTÃO DE CRÉDITO]")
    cartao1.vincular_fatura(fatura_jan)
    cartao1.passar_cartao(transacao1)
    cartao1.passar_cartao(transacao2)
    print(f"  Fatura Jan: {fatura_jan}")
    print(f"  Limite disponível: R${cartao1.limite_disponivel:.2f}")
    fatura_jan.pagar_fatura(pix1)

    # Polimorfismo nos pagamentos
    print("\n[PAGAMENTOS — polimorfismo]")
    for pgto in [boleto3, pix3, debito1]:
        pgto.processar()

    # Empréstimo
    print("\n[EMPRÉSTIMO]")
    print(emprestimo1)
    print(f"  Total com juros: R${emprestimo1.valor_total_com_juros:.2f}")

    # Investimento
    print("\n[INVESTIMENTO]")
    print(invest2)
    print(f"  Projeção em 5 anos: R${invest2.projetar_rendimento(5):.2f}")

    # Caixinha
    print("\n[CAIXINHA]")
    caixinha1.guardar(3000)
    caixinha1.guardar(2000)
    print(caixinha1)

    # Notificações corrigidas
    print("\n[NOTIFICAÇÕES]")
    for n in [notificacao1, notificacao2, notificacao3]:
        print(f"  {n}")

    # LimiteCartao
    print("\n[LIMITE CARTÃO]")
    print(limiteCartao1)
    limiteCartao1.gastar(500)
    limiteCartao1.pagar_fatura(700)

    # Atendimentos (referência corrigida)
    print("\n[ATENDIMENTOS]")
    for at in [atendimento1, atendimento2, atendimento3]:
        print(f"  {at}")
    atendimento1.encerrar()

    print("\n" + "=" * 60)
    print("  Resumo das classes implementadas (22 classes):")
    classes = [
        "1.  Cliente", "2.  Conta (ABC)", "3.  ContaCorrente",
        "4.  ContaPoupanca", "5.  Transacao", "6.  Pagamento (ABC)",
        "7.  PagamentoBoleto", "8.  PagamentoPix", "9.  PagamentoDebito",
        "10. Fatura", "11. CartaoCredito", "12. LimiteCartao",
        "13. HistoricoTransferencia", "14. Usuario", "15. Endereco",
        "16. Notificacao", "17. Atendimento", "18. Funcionario",
        "19. AgenciaDigital", "20. Emprestimo",
        "21. Investimento (bônus)", "22. Caixinha (bônus)"
    ]
    for c in classes:
        print(f"  {c}")
    print("=" * 60)
