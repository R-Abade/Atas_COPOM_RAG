# Assistente Copom — RAG

Sistema de Recuperação Aumentada por Geração (RAG) construído do zero para responder perguntas sobre as atas do Comitê de Política Monetária (Copom) do Banco Central do Brasil.

O sistema busca automaticamente as atas mais recentes, processa e indexa o conteúdo, e responde perguntas em linguagem natural usando busca semântica + Gemini como modelo de geração.

---

## Como funciona

```
API do BCB → extração HTML → chunks → embeddings → ChromaDB
                                                        ↓
                         pergunta do usuário → embedding → busca vetorial → top-k chunks → Gemini → resposta
```

1. **Coleta** — busca as 5 atas mais recentes pela API pública do Banco Central
2. **Extração** — parseia o HTML da ata e separa seções, parágrafos e tabelas
3. **Chunking** — divide o texto em unidades menores (um chunk por parágrafo), cada um com metadados de ata, seção e número do parágrafo
4. **Embedding** — converte cada chunk em vetor numérico com `sentence-transformers`
5. **Indexação** — armazena vetores e textos no ChromaDB (banco de dados vetorial local)
6. **Consulta** — a pergunta do usuário é convertida em vetor, comparada com os chunks indexados, e os mais similares são enviados ao Gemini como contexto
7. **Geração** — o Gemini responde com base apenas no contexto recuperado

---

## Estrutura do projeto

```
RAG/
├── data/
│   ├── raw/              # JSONs brutos baixados da API do BCB
│   ├── processed/        # Textos extraídos das atas (.txt)
│   └── vector_db/        # Banco de dados vetorial (ChromaDB)
├── src/
│   ├── main.py           # Ponto de entrada — indexação + interface CLI
│   ├── requester.py      # Cliente HTTP com tratamento de erros
│   ├── json_handler.py   # Comunicação com a API do BCB
│   ├── text_handler.py   # Extração e limpeza do HTML das atas
│   ├── chunker.py        # Divisão do texto em chunks com metadados
│   ├── embedding.py      # Geração de embeddings com sentence-transformers
│   ├── vector_database.py# Indexação e busca no ChromaDB
│   └── llm.py            # Integração com o Gemini (geração de resposta)
├── .env                  # Chave de API (não versionado)
├── requirements.txt
└── README.md
```

---

## Requisitos

- Python 3.11 ou 3.12 (ChromaDB não suporta Python 3.14 ainda)
- Chave de API do Google Gemini

---

## Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd RAG

# Crie e ative o ambiente virtual
python3.12 -m venv .venv
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto:

```env
API_KEY=sua_chave_gemini_aqui
```

Para obter uma chave gratuita: [aistudio.google.com](https://aistudio.google.com)

---

## Uso

```bash
cd src
python main.py
```

Na primeira execução, o sistema baixa e indexa as atas automaticamente. Nas execuções seguintes, pula a indexação e vai direto para a interface de perguntas.

```
Obtendo números das 5 atas mais recentes...
Ata n°281 já existe, pulando indexação.
...

============================================================
  Assistente Copom — RAG
  Digite 'sair' para encerrar.
============================================================

Pergunta: O que o Copom decidiu sobre a taxa de juros na última reunião?

Gerando resposta...

------------------------------------------------------------
O Copom decidiu reduzir a taxa básica de juros para 13,75% a.a. ...
------------------------------------------------------------
```

---

## Dependências principais

| Pacote | Uso |
|---|---|
| `sentence-transformers` | Geração de embeddings localmente |
| `chromadb` | Banco de dados vetorial persistente |
| `google-genai` | Geração de resposta com o Gemini |
| `bs4` (BeautifulSoup) | Extração de texto do HTML das atas |
| `python-dotenv` | Leitura da chave de API do `.env` |
| `requests` | Requisições à API do Banco Central |

---

## Observações

- O sistema **não usa nenhuma biblioteca RAG pronta** (sem LangChain, sem LlamaIndex). A recuperação e o pipeline foram implementados manualmente.
- Os embeddings são gerados **localmente** com `all-MiniLM-L6-v2`, sem custo de API.
- O Gemini é usado **apenas para geração** da resposta final, com o contexto recuperado das atas.
- Se o Gemini estiver indisponível ou o contexto estiver vazio, o sistema retorna uma mensagem de fallback em vez de travar.
