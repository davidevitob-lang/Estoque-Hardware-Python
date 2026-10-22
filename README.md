# Gerenciador de Estoque de Hardware

Um sistema simples e direto para gerenciamento de peças de computador, focado em operações CRUD e filtragem inteligente. Criado como objeto de estudo para integração de interfaces gráficas com banco de dados local.

## 🛠️ Tecnologias Utilizadas
* **Python 3**
* **Tkinter / ttk:** Para a interface gráfica nativa.
* **SQLite3:** Banco de dados relacional leve e sem necessidade de servidor.

## ⚙️ Funcionalidades
* **CRUD Completo:** Adicionar, ler, atualizar e deletar componentes de hardware.
* **Busca Otimizada:** Filtro de pesquisa que ignora letras maiúsculas/minúsculas e acentuação.
* **Prevenção de Erros:** Validação de inputs para evitar que strings sejam salvas em campos de valor financeiro ou quantidade.

## 🚀 Como executar
1. Clone o repositório: `git clone https://github.com/SEU_USUARIO/estoque-hardware-python.git`
2. Navegue até a pasta do projeto.
3. Execute o arquivo principal: `python estoque.py`
*(O banco de dados será gerado automaticamente na primeira execução).*