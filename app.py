from dotenv import load_dotenv
import streamlit as st
from search import search_and_scrape
from response import generate_response

load_dotenv()


def main():
    st.title("Deep Search Q&A App")

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
            value=20,
        )
        retain_data = st.toggle("Retain previous search data", value=True)
        search_submitted = st.form_submit_button("Search and Scrape")

        if search_submitted:
            if search_query:
                with st.spinner("Searching and scraping..."):
                    new_data, new_urls = search_and_scrape(search_query, top_k)
                    if retain_data:
                        st.session_state["scraped_data"].extend(new_data)
                        st.session_state["scraped_urls"].extend(new_urls)
                    else:
                        st.session_state["scraped_data"] = new_data
                        st.session_state["scraped_urls"] = new_urls

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
        include_chat_history = st.toggle("Include Chat History", value=False)
        qa_submitted = st.form_submit_button("Ask")

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
