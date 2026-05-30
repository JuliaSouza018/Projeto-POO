from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod

# ============================================================
# ENUMS
# ============================================================

class TipoTransacao(Enum):
    ENTRADA      = "Entrada"
    SAIDA        = "Saída"
    INVESTIMENTO = "Investimento"

class StatusFatura(Enum):
    ABERTA  = "Aberta"
    PAGA    = "Paga"
    VENCIDA = "Vencida"

class TipoInvestimento(Enum):
    RENDA_FIXA     = "Renda Fixa"
    RENDA_VARIAVEL = "Renda Variável"
    FUNDO          = "Fundo"

# ============================================================
# 1. EMPRESA
# ============================================================
class Empresa:
    def __init__(self, razao_social, nome_fantasia, cnpj, email, telefone, segmento):
        self.razao_social  = razao_social
        self.nome_fantasia = nome_fantasia
        self.email         = email
        self.telefone      = telefone
        self.segmento      = segmento
        self.__cnpj        = cnpj          # encapsulamento

    @property
    def cnpj(self):
        return f"**.***.***/****-{self.__cnpj[-2:]}"

    def cnpj_completo(self):
        return self.__cnpj

    def __str__(self):
        return f"Empresa: {self.nome_fantasia} | CNPJ: {self.cnpj}"

# ============================================================
# 2. USUARIO
# ============================================================
class Usuario:
    def __init__(self, id, nome, email, telefone, senha):
        self.id       = id
        self.nome     = nome
        self.email    = email
        self.telefone = telefone
        self.__senha  = senha              # encapsulamento

    def verificar_senha(self, tentativa):
        return self.__senha == tentativa

    def __str__(self):
        return f"Usuário: {self.nome} | Email: {self.email}"

# ============================================================
# 3. CONTA (ABSTRATA — abstração)
# ============================================================
class Conta(ABC):
    def __init__(self, numero, saldo, empresa):
        self._numero  = numero
        self.__saldo  = float(saldo)       # encapsulamento
        self.empresa  = empresa

    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self, valor):
        if valor >= 0:
            self.__saldo = valor

    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            print(f"  Depósito de R${valor:.2f} realizado.")

    def sacar(self, valor):
        if 0 < valor <= self.__saldo:
            self.__saldo -= valor
            print(f"  Saque de R${valor:.2f} realizado.")

    @abstractmethod
    def tipo_conta(self):
        pass

    def __str__(self):
        return f"{self.tipo_conta()} | Nº {self._numero} | Saldo: R${self.__saldo:.2f}"

# ============================================================
# 4. CONTA MOVIMENTO (herança de Conta)
# ============================================================
class ContaMovimento(Conta):
    def __init__(self, numero, saldo, empresa, limite=5000.0):
        super().__init__(numero, saldo, empresa)
        self.limite = limite

    def tipo_conta(self):
        return "Conta Movimento"

    # polimorfismo — sobrescreve sacar()
    def sacar(self, valor):
        if 0 < valor <= (self.saldo + self.limite):
            self.saldo = max(0.0, self.saldo - valor)
            print(f"  Pagamento de R${valor:.2f} realizado (com limite).")

# ============================================================
# 5. CONTA RESERVA (herança de Conta)
# ============================================================
class ContaReserva(Conta):
    def __init__(self, numero, saldo, empresa, taxa=0.005):
        super().__init__(numero, saldo, empresa)
        self.taxa = taxa

    def tipo_conta(self):
        return "Conta Reserva"

    def aplicar_rendimento(self):
        rendimento = self.saldo * self.taxa
        self.saldo += rendimento
        print(f"  Rendimento de R${rendimento:.2f} aplicado.")

# ============================================================
# 6. PAGAMENTO (ABSTRATA — abstração + polimorfismo)
# ============================================================
class Pagamento(ABC):
    def __init__(self, valor):
        self._valor     = valor
        self.confirmado = False
        self.data       = datetime.now().strftime("%d/%m/%Y")

    @abstractmethod
    def processar(self):
        pass

    def __str__(self):
        status = "Confirmado" if self.confirmado else "Pendente"
        return f"Pagamento R${self._valor:.2f} | {status}"

# ============================================================
# 7. PAGAMENTO BOLETO (herança de Pagamento)
# ============================================================
class PagamentoBoleto(Pagamento):
    def __init__(self, valor, codigo):
        super().__init__(valor)
        self.codigo = codigo

    def processar(self):
        self.confirmado = True
        print(f"  Boleto {self.codigo[:20]}... | R${self._valor:.2f} pago.")

# ============================================================
# 8. PAGAMENTO PIX (herança de Pagamento)
# ============================================================
class PagamentoPix(Pagamento):
    def __init__(self, valor, chave):
        super().__init__(valor)
        self.chave = chave

    def processar(self):
        self.confirmado = True
        print(f"  PIX → {self.chave} | R${self._valor:.2f} enviado.")

# ============================================================
# 9. PAGAMENTO DEBITO (herança de Pagamento)
# ============================================================
class PagamentoDebito(Pagamento):
    def __init__(self, valor, conta):
        super().__init__(valor)
        self.__conta = conta

    def processar(self):
        self.__conta.sacar(self._valor)
        self.confirmado = True

# ============================================================
# 10. TRANSACAO
# ============================================================
class Transacao:
    def __init__(self, tipo, valor, descricao, categoria="Geral"):
        self.tipo      = tipo
        self.__valor   = valor             # encapsulamento
        self.descricao = descricao
        self.categoria = categoria
        self.data      = datetime.now().strftime("%d/%m/%Y")

    @property
    def valor(self):
        return self.__valor

    def __str__(self):
        return f"[{self.data}] {self.tipo.value} | R${self.__valor:.2f} | {self.descricao}"

# ============================================================
# 11. FATURA
# ============================================================
class Fatura:
    def __init__(self, mes, vencimento):
        self.mes        = mes
        self.vencimento = vencimento
        self.status     = StatusFatura.ABERTA
        self.__itens    = []               # encapsulamento

    def adicionar(self, transacao):
        if self.status == StatusFatura.ABERTA:
            self.__itens.append(transacao)

    @property
    def total(self):
        return sum(t.valor for t in self.__itens)

    def pagar(self):
        self.status = StatusFatura.PAGA
        print(f"  Fatura de {self.mes} paga. Total: R${self.total:.2f}")

    def __str__(self):
        return f"Fatura {self.mes} | Status: {self.status.value} | Total: R${self.total:.2f}"

# ============================================================
# 12. CARTAO EMPRESARIAL
# ============================================================
class CartaoEmpresarial:
    def __init__(self, numero, titular, limite, bandeira):
        self.__numero  = numero            # encapsulamento
        self.titular   = titular
        self.__limite  = limite            # encapsulamento
        self.bandeira  = bandeira
        self.gasto     = 0.0

    @property
    def disponivel(self):
        return self.__limite - self.gasto

    def usar(self, valor):
        if valor <= self.disponivel:
            self.gasto += valor
            print(f"  Cartão *{self.__numero[-4:]} | R${valor:.2f} aprovado.")
        else:
            print(f"  Limite insuficiente. Disponível: R${self.disponivel:.2f}")

    def __str__(self):
        return f"Cartão {self.bandeira} | {self.titular} | Limite: R${self.__limite:.2f}"

# ============================================================
# 13. HISTORICO DE LANCAMENTO
# ============================================================
class HistoricoLancamento:
    def __init__(self, id, data, valor, descricao, tipo):
        self.id        = id
        self.data      = data
        self.__valor   = valor             # encapsulamento
        self.descricao = descricao
        self.tipo      = tipo

    @property
    def valor(self):
        return self.__valor

    def __str__(self):
        return f"[{self.data}] R${self.__valor:.2f} | {self.descricao} ({self.tipo})"

# ============================================================
# 14. NOTIFICACAO
# ============================================================
class Notificacao:
    def __init__(self, id, mensagem, tipo):
        self.id       = id
        self.mensagem = mensagem
        self.tipo     = tipo        # push, email, sms
        self.lida     = False

    def marcar_lida(self):
        self.lida = True

    def __str__(self):
        status = "✓" if self.lida else "●"
        return f"[{self.tipo.upper()}] {status} {self.mensagem}"

# ============================================================
# 15. FUNCIONARIO
# ============================================================
class Funcionario:
    def __init__(self, id, nome, cargo, salario, departamento):
        self.id           = id
        self.nome         = nome
        self.cargo        = cargo
        self.__salario    = salario        # encapsulamento
        self.departamento = departamento

    @property
    def salario(self):
        return self.__salario

    def reajuste(self, percentual):
        self.__salario *= (1 + percentual / 100)
        print(f"  Novo salário de {self.nome}: R${self.__salario:.2f}")

    def __str__(self):
        return f"Funcionário: {self.nome} | {self.cargo} | R${self.__salario:.2f}"

# ============================================================
# 16. ENDERECO
# ============================================================
class Endereco:
    def __init__(self, id, rua, numero, cidade, estado, cep):
        self.id     = id
        self.rua    = rua
        self.numero = numero
        self.cidade = cidade
        self.estado = estado
        self.cep    = cep

    def __str__(self):
        return f"{self.rua}, {self.numero} — {self.cidade}/{self.estado}"

# ============================================================
# 17. ATENDIMENTO
# ============================================================
class Atendimento:
    def __init__(self, id, usuario, descricao, status="aberto"):
        self.id        = id
        self.usuario   = usuario
        self.descricao = descricao
        self.status    = status
        self.data      = datetime.now().strftime("%d/%m/%Y")

    def encerrar(self):
        self.status = "fechado"
        print(f"  Atendimento #{self.id} encerrado.")

    def __str__(self):
        return f"Atendimento #{self.id} | {self.usuario.nome} | {self.status}"

# ============================================================
# 18. EMPRESTIMO
# ============================================================
class Emprestimo:
    def __init__(self, id, empresa, valor, parcelas, taxa):
        self.id       = id
        self.empresa  = empresa
        self.__valor  = valor              # encapsulamento
        self.parcelas = parcelas
        self.__taxa   = taxa

    @property
    def total_com_juros(self):
        return self.__valor * ((1 + self.__taxa) ** self.parcelas)

    @property
    def valor_parcela(self):
        return self.total_com_juros / self.parcelas

    def __str__(self):
        return f"Empréstimo #{self.id} | {self.empresa.nome_fantasia} | R${self.__valor:.2f} em {self.parcelas}x"

# ============================================================
# 19. INVESTIMENTO
# ============================================================
class Investimento:
    def __init__(self, id, empresa, tipo, valor, rentabilidade):
        self.id            = id
        self.empresa       = empresa
        self.tipo          = tipo
        self.__valor       = valor         # encapsulamento
        self.rentabilidade = rentabilidade

    def projetar(self, anos):
        return self.__valor * ((1 + self.rentabilidade) ** anos)

    def __str__(self):
        return f"Investimento {self.tipo.value} | {self.empresa.nome_fantasia} | R${self.__valor:.2f}"

# ============================================================
# 20. RESERVA FINANCEIRA
# ============================================================
class ReservaFinanceira:
    def __init__(self, id, empresa, nome, meta):
        self.id      = id
        self.empresa = empresa
        self.nome    = nome
        self.meta    = meta
        self.__saldo = 0.0                 # encapsulamento

    def guardar(self, valor):
        if valor > 0:
            self.__saldo += valor
            print(f"  R${valor:.2f} guardado em '{self.nome}'. Total: R${self.__saldo:.2f}")

    def resgatar(self, valor):
        if valor <= self.__saldo:
            self.__saldo -= valor
            print(f"  R${valor:.2f} resgatado de '{self.nome}'.")

    @property
    def progresso(self):
        return (self.__saldo / self.meta * 100) if self.meta > 0 else 0

    def __str__(self):
        return f"Reserva '{self.nome}' | R${self.__saldo:.2f} / R${self.meta:.2f} ({self.progresso:.0f}%)"

# ============================================================
# 21. AGENCIA DIGITAL
# ============================================================
class AgenciaDigital:
    def __init__(self, codigo, cidade, estado, telefone):
        self.codigo   = codigo
        self.cidade   = cidade
        self.estado   = estado
        self.telefone = telefone

    def __str__(self):
        return f"Agência {self.codigo} | {self.cidade}/{self.estado} | {self.telefone}"

# ============================================================
# 22. LIMITE CARTAO
# ============================================================
class LimiteCartao:
    def __init__(self, id, empresa, limite_total):
        self.id       = id
        self.empresa  = empresa
        self.__total  = limite_total       # encapsulamento
        self.__gasto  = 0.0

    def gastar(self, valor):
        if valor <= (self.__total - self.__gasto):
            self.__gasto += valor
            print(f"  Gasto R${valor:.2f}. Disponível: R${self.__total - self.__gasto:.2f}")

    def __str__(self):
        return f"Limite {self.empresa.nome_fantasia} | Total: R${self.__total:.2f} | Usado: R${self.__gasto:.2f}"

# ============================================================
# 23. FLUXO DE CAIXA
# ============================================================
class FluxoCaixa:
    def __init__(self, empresa):
        self.empresa       = empresa
        self.__lancamentos = []            # encapsulamento

    def adicionar(self, lancamento):
        self.__lancamentos.append(lancamento)

    def get_receitas(self):
        return sum(l.valor for l in self.__lancamentos if l.tipo == "Entrada")

    def get_despesas(self):
        return sum(l.valor for l in self.__lancamentos if l.tipo == "Saída")

    def get_saldo(self):
        return self.get_receitas() - self.get_despesas()

    def resumo(self):
        return {
            "receita": self.get_receitas(),
            "despesa": self.get_despesas(),
            "saldo":   self.get_saldo()
        }

    def __str__(self):
        return f"FluxoCaixa {self.empresa.nome_fantasia} | Saldo: R${self.get_saldo():.2f}"

# ============================================================
# 24. DASHBOARD
# ============================================================
class Dashboard:
    def __init__(self, empresa):
        self.empresa = empresa

    def get_kpis(self, receita, despesa, contas_pagar):
        lucro  = receita - despesa
        margem = (lucro / receita * 100) if receita > 0 else 0
        return {
            "receita":      round(receita, 2),
            "despesa":      round(despesa, 2),
            "lucro":        round(lucro, 2),
            "margem":       round(margem, 1),
            "contas_pagar": round(contas_pagar, 2)
        }

    def __str__(self):
        return f"Dashboard | {self.empresa.nome_fantasia}"

# ============================================================
# 25. AUTENTICACAO
# ============================================================
class Autenticacao:
    def __init__(self):
        self.__cadastros = {}              # encapsulamento

    def cadastrar(self, empresa, senha):
        cnpj = empresa.cnpj_completo()
        if cnpj not in self.__cadastros:
            self.__cadastros[cnpj] = {"senha": senha, "empresa": empresa}
            print(f"  {empresa.nome_fantasia} cadastrada com sucesso!")
        else:
            print("  CNPJ já cadastrado.")

    def login(self, cnpj, senha):
        dados = self.__cadastros.get(cnpj)
        if dados and dados["senha"] == senha:
            print(f"  Bem-vinda, {dados['empresa'].nome_fantasia}!")
            return dados["empresa"]
        print("  CNPJ ou senha incorretos.")
        return None

    def __str__(self):
        return f"Autenticacao | {len(self.__cadastros)} empresa(s) cadastrada(s)"


# ============================================================
# OBJETOS — 5 por classe
# ============================================================

# Empresa
empresa1 = Empresa("Tech Solutions Ltda.",      "TechSol",    "12345678000199", "techsol@email.com",    "(11)99001-0001", "Tecnologia")
empresa2 = Empresa("Mercado Bom Preço S.A.",    "BomPreço",   "23456789000188", "bompreco@email.com",   "(21)99002-0002", "Varejo")
empresa3 = Empresa("Construfix Engenharia.",    "Construfix", "34567890000177", "construfix@email.com", "(31)99003-0003", "Construção")
empresa4 = Empresa("AlimexFoods Ind. Com.",     "AlimexFoods","45678901000166", "alimex@email.com",     "(41)99004-0004", "Alimentação")
empresa5 = Empresa("Logística Rápida Ltda.",    "LogiRápida", "56789012000155", "logistica@email.com",  "(51)99005-0005", "Logística")

# Usuario
usuario1 = Usuario(1, "Carlos Silva",  "carlos@techsol.com",  "(11)91001-0001", "senha123")
usuario2 = Usuario(2, "Ana Souza",     "ana@bompreco.com",    "(21)92002-0002", "abc456")
usuario3 = Usuario(3, "Bruno Lima",    "bruno@construfix.com","(31)93003-0003", "pass789")
usuario4 = Usuario(4, "Juliana Costa", "juliana@alimex.com",  "(41)94004-0004", "jul2024")
usuario5 = Usuario(5, "Pedro Alves",  "pedro@logistica.com", "(51)95005-0005", "pedro99")

# ContaMovimento (herda Conta)
contaMovimento1 = ContaMovimento("CM-001", 85000.00, empresa1, 15000.00)
contaMovimento2 = ContaMovimento("CM-002", 42000.00, empresa2, 10000.00)
contaMovimento3 = ContaMovimento("CM-003",120000.00, empresa3, 25000.00)
contaMovimento4 = ContaMovimento("CM-004", 30000.00, empresa4,  8000.00)
contaMovimento5 = ContaMovimento("CM-005", 65000.00, empresa5, 12000.00)

# ContaReserva (herda Conta)
contaReserva1 = ContaReserva("CR-001", 50000.00, empresa1, 0.005)
contaReserva2 = ContaReserva("CR-002", 20000.00, empresa2, 0.006)
contaReserva3 = ContaReserva("CR-003", 80000.00, empresa3, 0.005)
contaReserva4 = ContaReserva("CR-004", 15000.00, empresa4, 0.007)
contaReserva5 = ContaReserva("CR-005", 35000.00, empresa5, 0.005)

# PagamentoBoleto (herda Pagamento)
boleto1 = PagamentoBoleto(12000.00, "34191.09008 61713.957308 71444.640008 1")
boleto2 = PagamentoBoleto( 8900.00, "03399.87362 54000.000000 00018.234567 8")
boleto3 = PagamentoBoleto( 4500.00, "23793.38128 60064.093409 83000.041011 5")
boleto4 = PagamentoBoleto(22000.00, "10499.12345 67890.123456 78901.234567 2")
boleto5 = PagamentoBoleto( 1800.00, "00190.00009 01234.567890 12345.678901 3")

# PagamentoPix (herda Pagamento)
pix1 = PagamentoPix(85000.00, "techsol@email.com")
pix2 = PagamentoPix(43200.00, "12345678000199")
pix3 = PagamentoPix( 4800.00, "+5511987654321")
pix4 = PagamentoPix(15000.00, "construfix@email.com")
pix5 = PagamentoPix( 3200.00, "bompreco@email.com")

# PagamentoDebito (herda Pagamento)
debito1 = PagamentoDebito( 5000.00, contaMovimento1)
debito2 = PagamentoDebito( 3000.00, contaMovimento2)
debito3 = PagamentoDebito(12000.00, contaMovimento3)
debito4 = PagamentoDebito( 8000.00, contaMovimento4)
debito5 = PagamentoDebito( 1500.00, contaMovimento5)

# Transacao
transacao1 = Transacao(TipoTransacao.ENTRADA,      85000.00, "Recebimento Cliente XYZ", "Receita")
transacao2 = Transacao(TipoTransacao.SAIDA,         12000.00, "Pagamento Fornecedor Alfa","Fornecedores")
transacao3 = Transacao(TipoTransacao.SAIDA,         35400.00, "Folha de Pagamento",       "Salários")
transacao4 = Transacao(TipoTransacao.SAIDA,          4800.00, "Aluguel Escritório",       "Operacional")
transacao5 = Transacao(TipoTransacao.ENTRADA,       43200.00, "Recebimento Cliente ABC",  "Receita")

# Fatura
fatura1 = Fatura("Janeiro",  "05/02/2026")
fatura2 = Fatura("Fevereiro","05/03/2026")
fatura3 = Fatura("Março",    "05/04/2026")
fatura4 = Fatura("Abril",    "05/05/2026")
fatura5 = Fatura("Maio",     "05/06/2026")

# CartaoEmpresarial
cartao1 = CartaoEmpresarial("1111222233334444", "TechSol",    15000.00, "Mastercard")
cartao2 = CartaoEmpresarial("5555666677778888", "BomPreço",   30000.00, "Visa")
cartao3 = CartaoEmpresarial("9999000011112222", "Construfix",  8000.00, "Elo")
cartao4 = CartaoEmpresarial("3333444455556666", "AlimexFoods",50000.00, "Mastercard")
cartao5 = CartaoEmpresarial("7777888899990000", "LogiRápida", 20000.00, "Visa")

# HistoricoLancamento
histLanc1 = HistoricoLancamento(1, "20/05/2026",  85000.00, "Recebimento Cliente XYZ", "Entrada")
histLanc2 = HistoricoLancamento(2, "21/05/2026",  12000.00, "Fornecedor Alfa",          "Saída")
histLanc3 = HistoricoLancamento(3, "22/05/2026",  35400.00, "Folha de Pagamento",       "Saída")
histLanc4 = HistoricoLancamento(4, "23/05/2026",   4800.00, "Aluguel Escritório",       "Saída")
histLanc5 = HistoricoLancamento(5, "24/05/2026",  43200.00, "Recebimento Cliente ABC",  "Entrada")

# Notificacao
notificacao1 = Notificacao(1, "Relatório de Maio disponível",       "push")
notificacao2 = Notificacao(2, "Anomalia detectada em Serviços",     "push")
notificacao3 = Notificacao(3, "Pagamento de fatura confirmado",     "sms")
notificacao4 = Notificacao(4, "Score financeiro atualizado: 85pts", "email")
notificacao5 = Notificacao(5, "Vencimento de conta em 3 dias",      "email")

# Funcionario
funcionario1 = Funcionario(1, "Carlos Silva",   "Gerente Financeiro",  8500.00, "Financeiro")
funcionario2 = Funcionario(2, "Ana Souza",      "Analista Contábil",   3200.00, "Contabilidade")
funcionario3 = Funcionario(3, "Bruno Lima",     "Analista de BI",      5400.00, "Tecnologia")
funcionario4 = Funcionario(4, "Juliana Costa",  "Supervisora Fiscal",  6700.00, "Financeiro")
funcionario5 = Funcionario(5, "Pedro Alves",    "Assistente Adm.",     2900.00, "Administrativo")

# Endereco
endereco1 = Endereco(1, "Av. Paulista",         1811, "São Paulo",      "SP", "01311-200")
endereco2 = Endereco(2, "Av. Rio Branco",          85, "Rio de Janeiro", "RJ", "20040-004")
endereco3 = Endereco(3, "Rua da Bahia",           550, "Belo Horizonte", "MG", "30160-010")
endereco4 = Endereco(4, "Rua XV de Novembro",     400, "Curitiba",       "PR", "80020-310")
endereco5 = Endereco(5, "Av. Borges de Medeiros",  80, "Porto Alegre",   "RS", "90020-021")

# Atendimento
atendimento1 = Atendimento(1, usuario1, "Erro na importação do Excel",        "aberto")
atendimento2 = Atendimento(2, usuario2, "Divergência no relatório de DRE",   "fechado")
atendimento3 = Atendimento(3, usuario3, "Dúvida sobre benchmark do setor",    "aberto")
atendimento4 = Atendimento(4, usuario4, "Solicitação de relatório fiscal",    "fechado")
atendimento5 = Atendimento(5, usuario5, "Configuração de alertas automáticos","aberto")

# Emprestimo
emprestimo1 = Emprestimo(1, empresa1,  50000.00, 12, 0.018)
emprestimo2 = Emprestimo(2, empresa2,  20000.00,  6, 0.025)
emprestimo3 = Emprestimo(3, empresa3, 150000.00, 24, 0.015)
emprestimo4 = Emprestimo(4, empresa4,  10000.00,  3, 0.030)
emprestimo5 = Emprestimo(5, empresa5,  80000.00, 18, 0.020)

# Investimento
investimento1 = Investimento(1, empresa1, TipoInvestimento.RENDA_FIXA,      10000.00, 0.12)
investimento2 = Investimento(2, empresa2, TipoInvestimento.RENDA_VARIAVEL,  50000.00, 0.20)
investimento3 = Investimento(3, empresa3, TipoInvestimento.FUNDO,           25000.00, 0.15)
investimento4 = Investimento(4, empresa4, TipoInvestimento.RENDA_FIXA,      30000.00, 0.11)
investimento5 = Investimento(5, empresa5, TipoInvestimento.RENDA_VARIAVEL, 100000.00, 0.25)

# ReservaFinanceira
reserva1 = ReservaFinanceira(1, empresa1, "Reserva de Emergência",  100000.00)
reserva2 = ReservaFinanceira(2, empresa2, "Expansão da Loja",        80000.00)
reserva3 = ReservaFinanceira(3, empresa3, "Equipamentos Novos",     200000.00)
reserva4 = ReservaFinanceira(4, empresa4, "Capital de Giro Extra",   50000.00)
reserva5 = ReservaFinanceira(5, empresa5, "Frota de Veículos",      150000.00)

# AgenciaDigital
agencia1 = AgenciaDigital(101, "São Paulo",      "SP", "(11)3000-0001")
agencia2 = AgenciaDigital(102, "Rio de Janeiro", "RJ", "(21)3000-0002")
agencia3 = AgenciaDigital(103, "Belo Horizonte", "MG", "(31)3000-0003")
agencia4 = AgenciaDigital(104, "Curitiba",       "PR", "(41)3000-0004")
agencia5 = AgenciaDigital(105, "Porto Alegre",   "RS", "(51)3000-0005")

# LimiteCartao
limiteCartao1 = LimiteCartao(1, empresa1,  15000.00)
limiteCartao2 = LimiteCartao(2, empresa2,  25000.00)
limiteCartao3 = LimiteCartao(3, empresa3, 100000.00)
limiteCartao4 = LimiteCartao(4, empresa4,  15000.00)
limiteCartao5 = LimiteCartao(5, empresa5,  30000.00)

# FluxoCaixa
fluxo1 = FluxoCaixa(empresa1)
fluxo2 = FluxoCaixa(empresa2)
fluxo3 = FluxoCaixa(empresa3)
fluxo4 = FluxoCaixa(empresa4)
fluxo5 = FluxoCaixa(empresa5)

# Alimentar fluxo1 com os lançamentos
for lanc in [histLanc1, histLanc2, histLanc3, histLanc4, histLanc5]:
    fluxo1.adicionar(lanc)

# Dashboard
dashboard1 = Dashboard(empresa1)
dashboard2 = Dashboard(empresa2)
dashboard3 = Dashboard(empresa3)
dashboard4 = Dashboard(empresa4)
dashboard5 = Dashboard(empresa5)

# Autenticacao
auth1 = Autenticacao()
auth2 = Autenticacao()
auth3 = Autenticacao()
auth4 = Autenticacao()
auth5 = Autenticacao()

# ============================================================
# MAIN — demonstração do sistema
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("   NuEmpresas — Inteligência Financeira Empresarial")
    print("=" * 55)

    # LOGIN / CADASTRO
    print("\n[LOGIN E CADASTRO]")
    auth1.cadastrar(empresa1, "senha123")
    auth1.cadastrar(empresa2, "abc456")
    auth1.login("12345678000199", "senha123")
    auth1.login("99999999000100", "errada")

    # DASHBOARD
    print("\n[DASHBOARD — KPIs]")
    kpis = dashboard1.get_kpis(128400.00, 93200.00, 15500.00)
    for chave, valor in kpis.items():
        print(f"  {chave}: {valor}")

    # CONTAS — Herança e Polimorfismo
    print("\n[CONTAS — Herança e Polimorfismo]")
    print(contaMovimento1)
    print(contaReserva1)
    contaMovimento1.depositar(10000)
    contaMovimento1.sacar(5000)      # polimorfismo (ContaMovimento sobrescreve sacar)
    contaReserva1.aplicar_rendimento()

    # PAGAMENTOS — Polimorfismo
    print("\n[PAGAMENTOS — Polimorfismo]")
    for pgto in [boleto1, pix1, debito1]:
        pgto.processar()             # mesmo método, comportamentos diferentes

    # FATURA
    print("\n[FATURA]")
    fatura1.adicionar(transacao2)
    fatura1.adicionar(transacao3)
    print(fatura1)
    fatura1.pagar()

    # FLUXO DE CAIXA
    print("\n[FLUXO DE CAIXA]")
    resumo = fluxo1.resumo()
    print(f"  Receita : R${resumo['receita']:,.2f}")
    print(f"  Despesa : R${resumo['despesa']:,.2f}")
    print(f"  Saldo   : R${resumo['saldo']:,.2f}")

    # CARTÃO
    print("\n[CARTÃO EMPRESARIAL]")
    cartao1.usar(3000.00)
    cartao1.usar(20000.00)           # deve negar — limite excedido
    print(cartao1)

    # EMPRÉSTIMO
    print("\n[EMPRÉSTIMO]")
    print(emprestimo1)
    print(f"  Total com juros : R${emprestimo1.total_com_juros:,.2f}")
    print(f"  Parcela mensal  : R${emprestimo1.valor_parcela:,.2f}")

    # INVESTIMENTO
    print("\n[INVESTIMENTO]")
    print(investimento1)
    print(f"  Projeção 3 anos : R${investimento1.projetar(3):,.2f}")

    # RESERVA
    print("\n[RESERVA FINANCEIRA]")
    reserva1.guardar(40000)
    reserva1.guardar(30000)
    print(reserva1)

    # NOTIFICAÇÕES
    print("\n[NOTIFICAÇÕES]")
    for n in [notificacao1, notificacao2, notificacao3]:
        print(f"  {n}")

    # FUNCIONÁRIOS
    print("\n[FUNCIONÁRIOS]")
    print(funcionario1)
    funcionario1.reajuste(10)

    # HISTÓRICO
    print("\n[HISTÓRICO DE LANÇAMENTOS]")
    for h in [histLanc1, histLanc2, histLanc3]:
        print(f"  {h}")

    # ENDEREÇOS
    print("\n[ENDEREÇOS]")
    for e in [endereco1, endereco2]:
        print(f"  {e}")

    # AGÊNCIAS
    print("\n[AGÊNCIAS DIGITAIS]")
    for a in [agencia1, agencia2, agencia3]:
        print(f"  {a}")

    print("\n" + "=" * 55)
    print("  Classes implementadas: 25 classes POO")
    print("  Objetos por classe  : 5")
    print("  Total de objetos    : 125+")
    print("  Pilares POO         : Encapsulamento, Herança,")
    print("                        Abstração, Polimorfismo")
    print("=" * 55)
