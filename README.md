# Deep Search Q&A App

An interactive Q&A web application that combines web search, markdown scraping, and LLM responses.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Setup](#setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview
This project enables users to perform comprehensive web searches and scrape markdown content. It leverages [Firecrawl](https://www.firecrawl.dev/) for searching and scraping, and integrates with Google’s generative AI models to generate contextual responses based on the scraped data.

## Features
- **Web Search & Scraping**: Query Firecrawl to retrieve markdown content.
- **Model Selection**: Choose from multiple LLM models to tailor responses.
- **Adjustable Temperature**: Fine-tune the randomness of LLM outputs.
- **Q&A Interface**: Pose questions based on the scraped content.
- **Chat History**: View the conversation history in an expandable panel.
- **Streamlit UI**: Enjoy a fast, user-friendly interface.

## Setup
1. **Requirements**: Ensure Python 3.12 is installed.
2. **Install Dependencies**:
   - Using pip:
     ```
     pip install -r requirements.txt
     ```
   - Alternatively, using uv:
     ```
     uv install -r requirements.txt
     ```
3. **Environment Variables**: Create a `.env` file at the project root with the following:
   - **FIRECRAWL_API_KEY**: Your Firecrawl API key.
   - **GOOGLE_API_KEY**: Your Google API key.

## Configuration
- **LLM Models**: See the list of available models in `app.py` and modify as required.
- **Temperature Setting**: Adjust the slider in the UI for desired response variability.
- **Search Parameters**: Change the `top_k` value in the search form to control the number of results.

## Usage
Launch the app using:
```
streamlit run app.py
```
Then:
1. Enter a search query and set the number of results.
2. View scraped data and corresponding URLs.
3. Select the LLM model and set the temperature.
4. Ask a question based on the scraped data.
5. Review the response and access the chat history.

## Contributing
Contributions are welcome! Fork the repository and submit a pull request with detailed explanations of your changes.

## License
This project is licensed under the MIT License.
