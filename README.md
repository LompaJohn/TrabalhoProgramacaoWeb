# Sistema de Gestão de Eventos Acadêmicos (SGEA)

O **SGEA** é um sistema web desenvolvido para gerenciar eventos acadêmicos, como seminários, palestras, minicursos e semanas acadêmicas. O projeto tem como objetivo oferecer aos usuários uma plataforma intuitiva e organizada, que facilite a visualização, inscrição e organização de eventos, promovendo uma gestão mais eficiente e acessível por meio de um portal integrado.

---

## Funcionalidades Principais

1. **Cadastro de usuários** (alunos, professores, organizadores)
   - Nome, telefone, instituição, login e senha.
2. **Autenticação de usuários**
   - Controle de acesso com base no perfil.
3. **Cadastro e gerenciamento de eventos**
   - Tipo, data, horário e local.
4. **Inscrição de usuários em eventos**
   - Participação vinculada ao evento.
5. **Emissão de certificados**
   - Somente para inscritos nos eventos.

---

## Funcionamento do Projeto

### 1. Verificar Python

Verifique se o **Python 3.13** está instalado:

```bash
python --version
```

### 2. Instlar o ambiente virtual

Esse projeto usa [pipenv](https://pypi.org/project/pipenv/)

```bash
pip install pipenv
pipenv install # instalar dependencias
pipenv shell # entrar no enviroment
```

### 3. Criar o arquivo .env

```bash
SECRET_KEY=sua-secret-key
```

### 4. Aplicar migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Criar superusuário

```bash
python manage.py createsuperuser
```

### 6. Rodar o servidor

```bash
python manage.py runserver
```

Acesse em: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Para criar contas, acesse a página [/admin](http://127.0.0.1:8000/admin) com sua conta de superusuário.
Para fazer login em uma conta de um usuário específico, acesse [/login](http://127.0.0.1:8000/login).
Acessando com a conta de organizador, será possível criar eventos e emitir certificados.
Com a conta de um aluno ou professor, é possível se inscrever em eventos, cancelar suas inscrições e ver seus certificados.

Para parar o servidor, pressione **Ctrl + C**.

### 8. Desativar o ambiente virtual

```bash
exit
```

---

## Autores

Projeto desenvolvido por Lucca Rosal, Guilerhme Lompa e Davi Tomasini
