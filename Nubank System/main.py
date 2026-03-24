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
#vinicius 

class Usuario:
    def __init__(self, id, nome, email, telefone):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone

    def _str_(self):
        return f"Usuário({self.id}, {self.nome})"

class Endereco:
    def __init__(self, id, rua, numero, cidade, estado):
        self.id = id
        self.rua = rua
        self.numero = numero
        self.cidade = cidade
        self.estado = estado

    def _str_(self):
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

    def _str_(self):
        return f"Atendimento({self.id}, {self.status})"        


#Matheus 
#kauá

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

contaC1 = ContaCorrente("00123456-1" , "2100")
contaC2 = ContaCorrente("00123456-2" , "2200")
contaC3 = ContaCorrente("00123456-3" , "2300")
contaC4 = ContaCorrente("00123456-4" , "2400")
contaC5 = ContaCorrente("00123456-5" , "2500")

contaP1 = ContaPoupanca("000543210-1" , "3300")
contaP2 = ContaPoupanca("000543210-2" , "3400")
contaP3 = ContaPoupanca("000543210-3" , "3500")
contaP4 = ContaPoupanca("000543210-4" , "3600")
contaP5 = ContaPoupanca("000543210-5" , "3700")


##gabriel
#vinicius
class Transferencia():
    def __init__(self, descricao, valor):
        self.descricao = descricao
        self.valor = valor
transf = Transferencia("Transferencia automatica", 100)
transf1 = Transferencia("Transferencia automatica", 500)
transf2 = Transferencia("Transferencia automatica", 200)
transf3 = Transferencia("Transferencia automatica", 350)
transf4 = Transferencia("Transferencia automatica", 1.000)

class Pix():
    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor
pic = Pix("11981353251", 1.000)
pic1 = Pix("21981353251", 2.000)
pic2 = Pix("31981353251", 2.500)
pic3 = Pix("88779956896", 3.700)
pic4 = Pix("55662256896", 500)

class Emprestimo():
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
emp = Emprestimo("Consignado", 10.000)
emp1 = Emprestimo("Com garantia", 20.000)
emp2 = Emprestimo("Com FGTS", 15.000)
emp3 = Emprestimo("Cheque Especial", 11.000)
emp4 = Emprestimo("Pessoal", 13.500)

class Investimento():
    def __init__ (self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
inv = Investimento("LCI/LCA", 100.000)
inv1 = Investimento("CDB", 150.000)
inv2 = Investimento("IPCA+", 120.000)
inv3 = Investimento("Acoes", 130.000)
inv4 = Investimento("FIIs", 500.000)
# vinicius ↑

u1 = Usuario(1, "João Silva", "joao@email.com", "11999999999")
u2 = Usuario(2, "Maria Souza", "maria@email.com", "11988888888")
u3 = Usuario(3, "Carlos Lima", "carlos@email.com", "11977777777")
u4 = Usuario(4, "Ana Costa", "ana@email.com", "11966666666")
u5 = Usuario(5, "Pedro Alves", "pedro@email.com", "11955555555")

e1 = Endereco(1, "Rua A", 100, "São Paulo", "SP")
e2 = Endereco(2, "Rua B", 200, "Rio de Janeiro", "RJ")
e3 = Endereco(3, "Rua C", 300, "Belo Horizonte", "MG")
e4 = Endereco(4, "Rua D", 400, "Curitiba", "PR")
e5 = Endereco(5, "Rua E", 500, "Porto Alegre", "RS")

n1 = Notificacao(1, "Seu pedido foi enviado", "email")
n2 = Notificacao(2, "Nova mensagem recebida", "push")
n3 = Notificacao(3, "Pagamento aprovado", "sms")
n4 = Notificacao(4, "Atualização disponível", "push")
n5 = Notificacao(5, "Senha alterada com sucesso", "email")

a1 = Atendimento(1, u1, "Problema no login", "aberto")
a2 = Atendimento(2, u2, "Erro no pagamento", "fechado")
a3 = Atendimento(3, u3, "Dúvida sobre produto", "aberto")
a4 = Atendimento(4, u4, "Solicitação de reembolso", "fechado")
a5 = Atendimento(5, u5, "Alteração de dados", "aberto")

#Matheus 
#kauá
