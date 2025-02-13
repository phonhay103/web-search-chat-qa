from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import streamlit as st
from models_config import MODEL_CONFIG


def generate_response(context, query, chat_history, model_name, temperature):
    """Generates response from LLM based on provided context and query.

    Returns:
        str: The LLM-generated response as a string, or None if an error occurs.
    """
    provider = MODEL_CONFIG.get(model_name)
    if provider == "groq":
        model = ChatGroq(model=model_name, temperature=temperature)
    else:
        model = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)

    # Format the prompt to include context and chat history (if any)
    prompt = (
        f"Context:\n{context}\n\nChat History:\n{chat_history}\n\nUser Query: {query}"
    )

    try:
        response = model.invoke(prompt)
        return response.content  # Return only the text content
    except Exception as e:
        st.error(f"Error during LLM generation: {e}")
        return None
