# Projeto-integrador-II

# Nome do Projeto
Plataforma Digital para Coordenação e Controle de Estoque Escolar (Confiro Já)

## Descrição
Este projeto consiste no desenvolvimento de uma aplicação web voltada à gestão e ao acompanhamento automatizado do estoque escolar na unidade Dr. Sérgio Benedito Fernandes de Almeida. O sistema substitui o registro manual em caderno por uma plataforma intuitiva que realiza o controle de entradas e saídas, emite alertas de estoque crítico, disponibiliza um assistente de leitura acessível para pessoas com baixa visão e gera gráficos dinâmicos para análise estatística dos materiais.

## Objetivo
Fornecer um meio prático, rápido e seguro para registrar, monitorar e planejar a reposição de suprimentos escolares, mitigando divergências de inventário e otimizando a rotina operacional dos colaboradores.

## Participantes
- Marcos Michel Amaral de Lima

## Tecnologias Utilizadas
- **Back-end:** Python 3, Django (Framework Web), SQLite / PostgreSQL
- **Front-end:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Visualização de Dados:** Chart.js (Gráfico Doughnut dinâmico)
- **Acessibilidade:** Web Speech API (Assistente de leitura por voz) & WCAG (HTML Semântico)
- **Controle de Versão & Deploy:** Git, GitHub, PythonAnywhere

## Funcionalidades Implementadas
- **Autenticação e Acesso:** Sistema de login/logout com controle de permissões.
- **Painel Principal (Dashboard):** Cards indicadores (Total, Reposição Necessária, Stock em Dia) e gráfico dinâmico de status.
- **Gestão de Produtos:** Cadastro (com definição de quantidade mínima), listagem, edição e exclusão de itens.
- **Gestão de Categorias:** Organização dos materiais por setores (Material escolar, Limpeza, Manutenção).
- **Movimentações de Estoque:** Registro de entradas (+ reposição) e saídas (- retirada) com trava de segurança para impedir saldo negativo.
- **Histórico & Auditoria:** Rastreabilidade em tempo real com registro de data, hora, usuário e observação.
- **Recurso de Acessibilidade:** Assistente de voz integrado para leitura de dados da tela.

## Documentação
O plano de ação do projeto está disponível no documento abaixo:

[Plano de Ação do Projeto](https://drive.google.com/file/d/1ZfknhcGqZevSflXkqRGKXdILMvLMS8vR/view?usp=drivesdk)

## Estrutura do Projeto
O projeto foi desenvolvido em arquitetura MVT (Model-View-Template) com o framework Django. O protótipo funcional foi testado junto aos colaboradores da unidade escolar e validado quanto à sua viabilidade técnica.

## Status do Projeto
**Protótipo Funcional Finalizado** — Em fase de documentação final para o Relatório do Projeto Integrador II.
