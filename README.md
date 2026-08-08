# NuEmpresas — Inteligência Financeira Empresarial

Projeto acadêmico de Programação Orientada a Objetos (POO) que simula uma plataforma de gestão financeira para empresas, inspirada em bancos digitais como o Nubank. O projeto é composto por um back-end em Python, que modela todo o domínio financeiro com classes e objetos, e uma interface web em HTML/CSS/JS que demonstra visualmente o funcionamento do sistema.

## 📌 Sobre o projeto

O NuEmpresas simula as principais operações de uma conta empresarial digital: contas, cartões, pagamentos, faturas, investimentos, empréstimos, fluxo de caixa e muito mais — tudo modelado seguindo os quatro pilares da Programação Orientada a Objetos.

## 🧱 Pilares de POO aplicados

- **Encapsulamento** — atributos sensíveis (senha, saldo, CNPJ, salário etc.) protegidos com `__atributo` e expostos via `@property`
- **Herança** — `ContaMovimento` e `ContaReserva` herdam de `Conta`; `PagamentoBoleto`, `PagamentoPix` e `PagamentoDebito` herdam de `Pagamento`
- **Abstração** — `Conta` e `Pagamento` são classes abstratas (`ABC`), obrigando as subclasses a implementar seus métodos
- **Polimorfismo** — `sacar()` se comporta de forma diferente em `ContaMovimento` (usa limite); `processar()` tem uma implementação distinta em cada tipo de pagamento

## 🗂️ Estrutura de classes

O sistema conta com **25 classes** e **5 objetos instanciados por classe** (125+ objetos no total):

| Categoria | Classes |
|---|---|
| Identidade e acesso | `Empresa`, `Usuario`, `Autenticacao`, `Endereco` |
| Contas | `Conta` (abstrata), `ContaMovimento`, `ContaReserva` |
| Pagamentos | `Pagamento` (abstrata), `PagamentoBoleto`, `PagamentoPix`, `PagamentoDebito` |
| Movimentação financeira | `Transacao`, `Fatura`, `FluxoCaixa`, `HistoricoLancamento` |
| Produtos financeiros | `CartaoEmpresarial`, `LimiteCartao`, `Emprestimo`, `Investimento`, `ReservaFinanceira` |
| Gestão e suporte | `Dashboard`, `Notificacao`, `Funcionario`, `Atendimento`, `AgenciaDigital` |
| Enums | `TipoTransacao`, `StatusFatura`, `TipoInvestimento` |

## 🚀 Como executar

### Back-end (Python)

Requer apenas Python 3 (não há dependências externas).

```bash
python nuempresas.py
```

O script executa uma demonstração completa no terminal: cadastro e login, KPIs do dashboard, operações de conta, pagamentos, fatura, fluxo de caixa, cartão empresarial, empréstimo, investimento, reserva financeira, notificações, funcionários, histórico de lançamentos e agências.

### Front-end (HTML)

Basta abrir o arquivo `nuempresas.html` diretamente no navegador — não requer servidor.

```bash
nuempresas.html
```

## 🛠️ Tecnologias

- **Python 3** — modelagem das classes e regras de negócio (`enum`, `abc`, `datetime`)
- **HTML, CSS e JavaScript** — interface visual do sistema

## 📁 Arquivos

```
├── nuempresas.py     # Modelagem completa em POO + demonstração no terminal
└── nuempresas.html   # Interface web do sistema
```

## 🎓 Contexto

Projeto desenvolvido para a disciplina de Programação Orientada a Objetos, com foco em aplicar de forma prática os quatro pilares do paradigma em um domínio realista (fintech empresarial).
