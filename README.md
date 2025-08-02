# 📈 CriptoDashboard Automático com Power BI

Este projeto coleta dados atualizados de criptomoedas através da CoinGecko API, armazena em um banco de dados PostgreSQL e oferece suporte a dashboards profissionais no Power BI, atualizáveis de forma prática.

## 🚀 Objetivo

Construir uma pipeline de dados automatizada para alimentar dashboards de criptomoedas com informações como preço, volume, market cap, e variações percentuais — prontos para visualização em tempo real no Power BI.

---

## 📊 Funcionalidades

- Coleta de dados atualizados via API da CoinGecko:
  -Bitcoin, Ethereum, Ripple, Solana e Cardano.
- Inserção automática dos dados em banco de dados PostgreSQL.
- Script modular e reaproveitável, pronto para agendamento.
- Dashboard em Power BI (.pbix) integrado com o banco de dados local.
- Código limpo, documentado e fácil de expandir.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia       | Uso                                                   |
|------------------|--------------------------------------------------------|
| Python 3.11      | Lógica de coleta, visualização e envio                |
| CoinGecko API    | Fonte dos dados de criptomoedas                       |
| Pandas/Requests  | Manipulação e requisições de dados                    |
| SQLAlchemy       | Conexão com banco PostgreSQL                          |
| PostgreSQL           | Armazenamento dos dados para o Power BI           |
| Playwright       | Renderização e conversão de HTML → PNG                |
| Python-dotenv    | Leitura de variáveis de ambiente (.env)               |
| Power BI (.pbix)	   | Dashboard visual conectado ao banco de dados      |

---

## 📁 Estrutura do Projeto

```
├── .env                 # Variáveis sensíveis (senha do banco)
├── data_fetcher.py      # Script principal: coleta, armazena e organiza os dados
├── crypto_dashboard.pbix# Dashboard Power BI conectado ao banco
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação do projeto

```

## 🔐 Variáveis de Ambiente (.env)

Crie um arquivo .env com a seguinte variável:

```env
SENHA=sua_senha_postgres
```
Essa senha será utilizada para autenticação no banco de dados local PostgreSQL, com o usuário padrão postgres e o banco cryptoproject.

## 📊 Dashboard Power BI

O arquivo crypto_dashboard.pbix está pronto para uso. Ele se conecta diretamente ao banco PostgreSQL e exibe:

- Preço atual (USD)
- Variação 24h e 7d
- Volume de transações
- Market cap e ranking
- Oferta em circulação

```Basta abrir o arquivo .pbix no Power BI Desktop, garantir que o PostgreSQL esteja rodando localmente e clicar em "Atualizar".
```

## 🧪 Execução Local

### Clone o repositório:

```bash
git clone https://github.com/CaioViegas/cripto_dashboard.git
cd cripto_dashboard
```

### Crie e ative o ambiente virtual:

```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### Instale as dependências:

```
pip install -r requirements.txt
```

### Execute o script principal:

```
python data_fetcher.py
```

## 🚧 Possíveis Melhorias Futuras

- Suporte a mais moedas e filtros dinâmicos
- Agendamento automático com GitHub Actions ou CRON
- Suporte à exportação dos dados em CSV/Excel
- Dashboard em Streamlit como alternativa online


## 👨‍💻 Autor

Desenvolvido por **Caio Viegas**  
Contato: [LinkedIn](https://www.linkedin.com/in/caio-costa-viegas-593614219/) | caio.costaviegas@gmail.com

## 📝 Licença

Este projeto está licenciado sob a **MIT License**.