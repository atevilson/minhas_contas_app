# Minhas Contas App

Uma aplicação web simples para controle de contas e despesas mensais, desenvolvida em Python/Flask e Bootstrap, com banco de dados PostgreSQL gerenciado pelo Supabase e deploy automatizado no Vercel.

---

## 🚀 Funcionalidades

- 📋 **Cadastro de Usuários**: Registro e autenticação segura via Flask-Login.
- 💰 **Gestão de Contas**: Criar, visualizar e excluir contas mensais (origem, vencimento, valor, status, quem paga, tipo, parcelas).
- ✅ **Marcar como Pago**: Alternar status da conta entre "A pagar" e "Pago" diretamente na tabela.
- 📅 **Filtro por Mês**: Selecionar o mês desejado para visualizar somente as contas daquele período.
- 📊 **Total Mensal**: Cálculo automático do total em aberto e pago para o mês selecionado.
- 📱 **Layout Responsivo**: Formulários e tabelas adaptáveis a diferentes tamanhos de tela usando grid e breakpoints do Bootstrap.

---

## 🛠 Tecnologias

- **Linguagem**: Python 3.9+
- **Framework Web**: [Flask](https://flask.palletsprojects.com/)
- **Formulários**: [Flask-WTF](https://flask-wtf.readthedocs.io/) + WTForms
- **Banco de Dados**: PostgreSQL (via [Supabase](https://supabase.io/))
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Autenticação**: [Flask-Login](https://flask-login.readthedocs.io/)
- **Frontend**: [Bootstrap 5](https://getbootstrap.com/) + Bootstrap Icons
- **Deploy**: [Vercel](https://vercel.com/) + pooler Supabase para conexões IPv4
- **Controle de Versão**: Git / GitHub

---

## 🎯 Usabilidade

1. **Cadastro e Login**: O usuário se registra e faz login para acessar o dashboard.
2. **Dashboard**: Exibe todas as contas do mês selecionado, totaliza valores e permite criação de novas contas.
3. **Nova Conta**: Adicione uma conta nova sempre informando o valor total da dívida, o calculo é cima das parcelas, para criar uma conta unica no mês sete tipo `Fixa` e `Parcelas` = 0.
4. **Tabela de Contas**: Lista interativa com ações de alternar status e excluir cada registro.
5. **Responsividade**: Em dispositivos pequenos, o formulário e tabela adaptam-se usando colunas `col-12 col-md-8 col-lg-6`, garantindo uma experiência legal no celular.

---

## ⚙️ Como Executar Localmente

### Pré-requisitos

- Python 3.12.10 instalado
- Conta no [Supabase](https://supabase.io/) com projeto PostgreSQL
- [Vercel CLI](https://vercel.com/docs/cli) (para deploy)

### Passos

1. Clone o repositório:

   ```bash
   git clone https://github.com/SEU_USUARIO/minhas_contas_app.git
   cd minhas_contas_app
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # linuxao/macZão
   venv\Scripts\activate     # windowsZão
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure variáveis de ambiente (arquivo `.env`):

   ```env
   SECRET_KEY=uma_chave_secreta
   DATABASE_URL=postgresql://usuario:senha@host:porta/dbname
   ```

5. Rode as migrações (se usar SQLite local ou Supabase de teste):

   ```bash
   flask db upgrade
   ```

6. Inicie o servidor:

   ```bash
   flask run
   ```

7. Acesse `http://localhost:5000` no navegador.

---

## ☁️ Deploy no Vercel

1. Configure as mesmas variáveis de ambiente no dashboard do Vercel.
2. Garanta o uso da connection string via _Session Pooler_ do Supabase (IPv4).
3. Push no GitHub e o Vercel fará o deploy automático.

---

 <sub><b>Atevilson Freitas</b></sub></a> <a href="">🧑‍💻</a>