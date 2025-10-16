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

### 2. Criar ambiente virtual
```bash
python -m venv venv
```

Ativar:
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```

### 3. Instalar o Django
```bash
pip install django
```

Verificar instalação:
```bash
python -m django --version
```

### 4. Instalar dependências do projeto (se houver)
```bash
pip install -r requirements.txt
```

### 5. Aplicar migrações
```bash
python manage.py migrate
```

### 6. Criar superusuário
```bash
python manage.py createsuperuser
```

### 7. Rodar o servidor
```bash
python manage.py runserver
```

Acesse em:
```
http://127.0.0.1:8000/
```

Para parar o servidor, pressione **Ctrl + C**.

### 8. Desativar o ambiente virtual
```bash
deactivate
```

---

## Autores
Projeto desenvolvido por Lucca Rosal, Guilerhme Lompa e Davi Tomasini
