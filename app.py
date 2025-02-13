from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

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
            return result["data"]
        else:
            st.warning(
                f"Search was not successful: {result.get('error', 'Unknown error')}"
            )
            return ""
    except Exception as e:
        st.error(f"Error during search and scraping: {e}")
        return ""


def generate_response(context, query, chat_history):
    """Generates response from LLM based on provided context and query.

    Returns:
        str: The LLM-generated response as a string, or None if an error occurs.
    """
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

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

    # Initialize session state
    if "scraped_data" not in st.session_state:
        st.session_state["scraped_data"] = ""
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
            max_value=10,
            value=5,
            step=1,
        )
        search_submitted = st.form_submit_button("Search and Scrape")

        if search_submitted:
            if search_query:
                with st.spinner("Searching and scraping..."):
                    st.session_state["scraped_data"] = search_and_scrape(
                        search_query, top_k
                    )

                if st.session_state["scraped_data"]:
                    st.success("Successfully scraped data!")
                    # Display scraped data (optional, but good for debugging)
                    with st.expander("Show Scraped Data"):
                        st.markdown(st.session_state["scraped_data"])
                else:
                    st.warning(
                        "No data scraped.  Check your query and top_k value.  Also verify Firecrawl API key and quota."
                    )
            else:
                st.error("Please enter a search query.")

    # Step 2: Q&A
    st.subheader("Q&A")
    with st.form("qa_form"):
        question = st.text_input("Ask a question about the scraped data:")
        qa_submitted = st.form_submit_button("Ask")

        if qa_submitted:
            if question and st.session_state["scraped_data"]:
                with st.spinner("Generating answer..."):
                    # Get the LLM response
                    response = generate_response(
                        st.session_state["scraped_data"],
                        question,
                        st.session_state["chat_history"],
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
        st.subheader("Chat History")
        st.markdown(st.session_state["chat_history"])


if __name__ == "__main__":
    main()
