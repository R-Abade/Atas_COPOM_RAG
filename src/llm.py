from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("API_KEY"))

FALLBACK_NO_CONTEXT = "Não encontrei informações suficientes nas atas do Copom para responder a essa pergunta."
FALLBACK_LLM_ERROR  = "O modelo de linguagem está temporariamente indisponível. Tente novamente em alguns instantes."

def get_interaction(context: dict, question: str):
    documents_list = context.get("documents", [[]])[0]

    if not documents_list:
        return FALLBACK_NO_CONTEXT

    documents = "\n\n".join(documents_list)

    try:
        interaction = client.interactions.create(
            model="gemini-3.5-flash-lite",
            system_instruction=(
                "Você é um assistente especializado em finanças, economia e política monetária "
                "com base nas atas do Copom. Responda apenas com base no contexto fornecido. "
                "Se o contexto não for suficiente para responder, diga que não encontrou a informação."
            ),
            input=f"Contexto:\n{documents}\n\nPergunta: {question}"
        )
        return interaction.output_text or FALLBACK_LLM_ERROR

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return FALLBACK_LLM_ERROR