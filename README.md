# Bibliotech Analytics & Management

## Boas-Vindas ao Projeto!

Este repositório marca o início do desenvolvimento do **Bibliotech Analytics & Management**, um sistema abrangente para gerenciamento e análise de dados de bibliotecas. O projeto visa modernizar a administração de acervos, empréstimos, reservas, usuários e funcionários, além de fornecer *insights* valiosos através de relatórios e logs de auditoria.

### Propósito do Projeto

O objetivo principal é informatizar as operações de uma biblioteca, superando desafios como lentidão, perda de informações e dificuldade em controlar prazos de devolução e atividades dos colaboradores. Além disso, busca-se gerar relatórios gerenciais para otimização da gestão.

### Visão Geral do Sistema

O sistema será composto por:

* **Backend (API Central):** Uma API RESTful em Python (FastAPI/Flask) que será a espinha dorsal do sistema, gerenciando toda a lógica de negócio e o acesso ao banco de dados. Este backend será hospedado na nuvem.
* **Banco de Dados:** PostgreSQL, também hospedado na nuvem, para garantir a consistência e acessibilidade dos dados para todas as partes do sistema.
* **Frontend Desktop:** Uma aplicação desktop robusta desenvolvida em Python (PyQt) para uso exclusivo de funcionários e administradores da biblioteca, com funcionalidades completas de gerenciamento e relatórios.
* **Frontend Web:** Uma interface web simplificada, desenvolvida em Python (Flask), destinada a usuários finais para consulta do acervo e operações básicas como reservas.

### Funcionalidades Chave (Inicial)

* **Autenticação e Autorização:** Sistema de login seguro com tokens de acesso e diferentes níveis de permissão (funcionário, administrador, usuário).
* **Gestão de Acervo:** Cadastro e gerenciamento de Livros (títulos, ano de publicação), Autores, Editoras, Gêneros literários e Exemplares físicos (cópias disponíveis, localização).
* **Operações Bibliotecárias:** Registro e controle de Empréstimos, Devoluções e Reservas de livros.
* **Gerenciamento de Usuários:** Cadastro de membros e funcionários da biblioteca.
* **Logs de Auditoria:** Registro de atividades importantes realizadas no sistema.
* **Geração de Relatórios:** Produção de relatórios sobre Livros mais populares, Frequência de usuários, Atrasos e multas, e Estatísticas de circulação do acervo.

### Tecnologias Previstas

* **Banco de Dados:** PostgreSQL
* **Backend:** Python (FastAPI/Flask, SQLAlchemy, PyJWT, Pandas)
* **Frontend Desktop:** Python (PyQt/PySide)
* **Frontend Web:** Python (Flask, Jinja2)
* **Versionamento:** Git & GitHub

## Status do Projeto

Este projeto está em sua fase inicial de desenvolvimento.

## Contribuindo

Contribuições são bem-vindas! Se você tiver ideias para melhorias, novas funcionalidades ou correção de bugs, sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
