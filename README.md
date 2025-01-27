# Research Helper

Research Helper is a Streamlit-based application designed to assist researchers in analyzing and discussing research papers. The bot is capable of processing PDF documents and answering questions related to them.

## Features
- Upload and process PDF documents up to 100 pages.
- Ask questions about the research paper and receive detailed answers.
- The bot is capable of handling documents in a user-friendly way.
- Provides an intuitive and interactive chat-based interface powered by Streamlit.

## How It Works
1. Upload your PDF files through the **File Upload** section in the sidebar.
2. Ask questions related to the document you have uploaded.
3. The bot will process the document and return relevant answers, based on the content of the document.

## Installation

To run the app locally, you'll need to have Python 3.x and pip installed.

1. Clone the repository or download the project files:
   ```
   git clone https://github.com/sriraj66/Research-paper-analysis.git
   ```

2. Navigate to the project directory:
   ```
   cd Research-paper-analysis
   ```
   Create a ```.env``` file and put your open ai api key

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the app:
   ```
   streamlit run app.py
   ```

5. or if you have Docker and docker compose
   ```
   docker compose up -d --build
   ```

## Usage
- Once the app is running, you can upload PDFs from your local device.
- Ask questions related to the content of your uploaded PDFs and the bot will respond with relevant information from the documents.

## Contributions
Contributions are welcome! Feel free to fork the repository and submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- OpenAI for providing the GPT-4 model.
- Embedchain for handling the knowledge base and document management.