from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def search_and_scrape(query, top_k) -> str:
    """Searches using Firecrawl and scrapes markdown content.

    Returns:
        str: A string containing all the scraped markdown content concatenated,
             or an empty string if scraping fails.
    """
    app = FirecrawlApp()
    try:
        result = app.search(
            query,
            params={
                "limit": top_k,
                "scrapeOptions": {
                    "formats": ["markdown"],
                },
            },
        )
        if result and result["success"]:
            urls = [item["url"] for item in result["data"]]
            return result["data"], urls
        else:
            st.warning(
                f"Search was not successful: {result.get('error', 'Unknown error')}"
            )
            return [], []
    except Exception as e:
        st.error(f"Error during search and scraping: {e}")
        return [], []


def generate_response(context, query, chat_history, model_name, temperature):
    """Generates response from LLM based on provided context and query.

    Returns:
        str: The LLM-generated response as a string, or None if an error occurs.
    """
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


def main():
    st.title("🦜🔗 Firecrawl Q&A App")

    # Sidebar for feature selection
    # feature = st.sidebar.radio("Choose a feature:", ("Search and Scrape", "Q&A"))

    # Initialize session state
    if "scraped_data" not in st.session_state:
        st.session_state["scraped_data"] = []
    if "scraped_urls" not in st.session_state:
        st.session_state["scraped_urls"] = []
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = (
            ""  # Initialize an empty string for chat history
        )

    # Step 1: Search and Scrape
    with st.form("search_form"):
        search_query = st.text_input("Enter search query:")
        top_k = st.number_input(
            "Enter top_k (number of results to scrape):",
            min_value=1,
            value=10,
        )
        search_submitted = st.form_submit_button("Search and Scrape")

        if search_submitted:
            if search_query:
                with st.spinner("Searching and scraping..."):
                    (
                        st.session_state["scraped_data"],
                        st.session_state["scraped_urls"],
                    ) = search_and_scrape(search_query, top_k)

                if st.session_state["scraped_data"]:
                    st.success("Successfully scraped data!")

                    with st.expander("Show Scraped Data"):
                        markdown_list = "\n".join(
                            [f"- {url}" for url in st.session_state["scraped_urls"]]
                        )
                        st.markdown(markdown_list)
                else:
                    st.warning(
                        "No data scraped. Check your query and top_k value. Also verify Firecrawl API key and quota."
                    )
            else:
                st.error("Please enter a search query.")

    # Model selection
    model_name = st.selectbox(
        "Select model:",
        [
            "gemini-2.0-flash",
            "gemini-2.0-flash-lite-preview-02-05",
            "gemini-2.0-pro-exp-02-05",
            "gemini-2.0-flash-thinking-exp-01-21",
        ],
    )

    # Temperature selection
    temperature = st.slider(
        "Select temperature:", min_value=0.0, max_value=1.0, value=0.7, step=0.1
    )

    # Step 2: Q&A
    st.subheader("Q&A")
    with st.form("qa_form"):
        question = st.text_input("Ask a question about the scraped data:")
        qa_submitted = st.form_submit_button("Ask")
        include_chat_history = st.checkbox("Include Chat History", value=False)

        if qa_submitted:
            if question and st.session_state["scraped_data"]:
                with st.spinner("Generating answer..."):
                    chat_history_input = (
                        st.session_state["chat_history"] if include_chat_history else ""
                    )
                    # Get the LLM response
                    response = generate_response(
                        st.session_state["scraped_data"],
                        question,
                        chat_history_input,
                        model_name,
                        temperature,
                    )

                    if response:
                        st.info(response)

                        # Update chat history
                        st.session_state[
                            "chat_history"
                        ] += f"\nUser: {question}\nAssistant: {response}"
                    else:
                        st.error(
                            "Failed to generate a response.  Check your LLM configuration."
                        )

            elif not st.session_state["scraped_data"]:
                st.warning("Please scrape data first by submitting a search query.")
            else:
                st.error("Please enter a question.")

    # Display Chat History
    if st.session_state["chat_history"]:
        with st.expander("Show Chat History"):
            st.markdown(st.session_state["chat_history"])


if __name__ == "__main__":
    main()
