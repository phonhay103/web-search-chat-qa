# web-search-chat-qa

An interactive Q&A web application that combines web search, markdown scraping, and LLM responses.

## Overview
This project enables users to perform web searches and scrape markdown content. It then uses a language model to generate responses based on the scraped data. The application leverages Firecrawl for search and scraping, and integrates with Google’s generative AI models.

## Features
- **Web Search & Scraping**: Query Firecrawl to search and retrieve markdown content.
- **Model Selection**: Choose from multiple LLM models.
- **Adjustable Temperature**: Fine-tune the LLM response randomness.
- **Q&A Interface**: Ask questions based on scraped data.
- **Chat History**: View ongoing conversation history in an expandable view.
- **Streamlit UI**: Fast, interactive interface for end users.

## Setup
1. **Requirements**: Ensure you have Python 3.12 installed.
2. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```
3. **Environment Variables**: Create a `.env` file at the project root and define the following variables:
   - FIRECRAWL_API_KEY: Your Firecrawl API key.
   - GOOGLE_API_KEY: Your Google API key.

## Configuration
- **LLM Models**: See the list of available models in `app.py`.
- **Temperature Setting**: Adjust the slider on the UI to set the response temperature.
- **Search Parameters**: Modify `top_k` via the input field to scrape the desired number of results.

## Usage
Launch the app using:
```
streamlit run app.py
```
1. Enter a search query and set the number of results.
2. View scraped data and URLs.
3. Choose the LLM model and temperature.
4. Ask questions based on the scraped data.
5. Check the generated answer and review the chat history.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with detailed changes and updates.

## License
This project is licensed under the MIT License.
