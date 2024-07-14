# OmniSage: AI-Powered Discord Bot

OmniSage is a versatile Discord bot that leverages Language Learning Models (LLMs) to generate intelligent responses, join voice channels, provide text-to-speech functionality, and includes an interactive, AI-powered trivia game. It's designed to be your all-knowing companion in Discord servers.

**🚀 Hobby Project Disclaimer 🛸**
> Warning: This bot may occasionally produce wisdom beyond human comprehension or just utter nonsense. It's a hobby project built to learn and practice LLM integration. Expect the unexpected, embrace the chaos, and don't be surprised if you find some "optimized" spaghetti code.  😉

## Table of Contents
1. [Features](#features)
2. [Features in Detail](#features-in-detail)
3. [Retrieval-Augmented Generation (RAG) System](#retrieval-augmented-generation-rag-system)
3. [Planned Features](#planned-features)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Docker Usage](#docker-usage-preferred)
8. [Usage](#usage)
9. [Command Details](#command-details)
10. [Grounding Data](#grounding-data)
11. [Troubleshooting](#troubleshooting)
12. [Contributing](#contributing)
13. [License](#license)

## Features

- AI-powered conversations using various LLM providers
- Voice channel integration with Text-to-Speech (TTS)
- Interactive AI-generated trivia game
- Image analysis capabilities (LLM-dependent)
- Multi-language support with translation
- Custom data grounding for enhanced knowledge
- Advanced conversation management
- Robust admin controls and customization options

## Features in Detail

### Intelligent Conversations
OmniSage utilizes state-of-the-art Language Learning Models to generate human-like responses. It supports multiple LLM providers:
- OpenAI (GPT-3.5, GPT-4, GPT-4o)
- Anthropic (Claude, Claude Instant)
- Local models (with appropriate setup)

The bot maintains conversation history to provide context-aware responses, enhancing the chat experience.

### Voice Integration
- Join and leave voice channels on command
- Text-to-Speech (TTS) functionality to read out responses in voice channels
- Configurable TTS settings (model, voice)

### Multi-Language Support
- Translate command for quick translations to English
- Potential for multi-language conversations (LLM-dependent)

### Custom Knowledge Grounding
- Enhance OmniSage's knowledge with custom data. BYOD (Bring your Own Data)
- Support for multiple data sources:
  - Local files (.txt, .pdf and .docx)
  - Amazon S3
  - Azure Blob Storage
- Dynamic reloading of grounding data without bot restart
- Detailed logging of loaded grounding files
- Improved chunking and metadata for more relevant information retrieval

### Advanced Conversation Management
- Conversation history tracking for context-aware responses
- Channel-specific conversation handling
- Admin command to clear conversation history

### Customization and Admin Controls
- Configurable command prefix and cooldowns
- Rate limiting to prevent API abuse
- Role-based access control for commands
- Admin commands for bot management (status setting, TTS toggling, etc.)

### Security and Performance
- Secure handling of API keys and sensitive information
- Docker support for easy deployment and management
- Optimized for performance with rate limiting and cooldowns

### AI-Powered Trivia Game
An exciting trivia game feature that showcases OmniSage's AI capabilities:
- Start a game with `!trivia <topic>` on any subject
- AI generates 5 unique, topic-specific multiple-choice questions
- Players answer by typing A, B, C, or D (case-insensitive)
- 30-second answer window for each question
- Multiple players can answer and earn points
- Administrators can stop the game at any time with `!stop_trivia`
- Detailed end-game summary with scores and statistics


## Retrieval-Augmented Generation (RAG) System

OmniSage employs a sophisticated RAG system to enhance its responses with relevant information from its knowledge base. This system combines the power of large language models with efficient information retrieval techniques.

### Key Components:

1. **LangChain**: We use LangChain, a powerful framework for developing applications powered by language models. LangChain provides the backbone for our RAG system, offering tools for document loading, text splitting, and chain creation.

2. **ChromaDB**: Our vector store of choice is ChromaDB, an open-source embedding database. ChromaDB allows us to efficiently store and retrieve vector representations of our knowledge base.

3. **OpenAI Embeddings**: We utilize OpenAI's text embedding model to convert text into high-dimensional vector representations. These embeddings capture semantic meanings, enabling more accurate information retrieval.

4. **Custom Text Splitter**: We implement a `RecursiveCharacterTextSplitter` to break down large documents into manageable chunks while maintaining context.

### How It Works:

1. **Document Ingestion**: When grounding data is loaded, each document is split into smaller chunks using the `RecursiveCharacterTextSplitter`.

2. **Embedding Generation**: Each chunk is then converted into a vector embedding using OpenAI's embedding model.

3. **Vector Storage**: These embeddings are stored in ChromaDB along with metadata about their source.

4. **Query Processing**: When a user query comes in, it's also converted to an embedding.

5. **Similarity Search**: The system performs a similarity search in ChromaDB to find the most relevant chunks of information.

6. **Context-Enhanced Generation**: The retrieved information is then used to augment the prompt sent to the language model, allowing it to generate more informed and accurate responses.

7. **Source Attribution**: The bot can provide information about the sources of its knowledge, increasing transparency and trustworthiness.

This RAG system allows OmniSage to leverage its extensive knowledge base effectively, providing responses that are both contextually relevant and factually grounded.

### Custom Knowledge Grounding

OmniSage's knowledge can be enhanced with custom data, truly embracing the BYOD (Bring Your Own Data) concept.

- **Multiple Data Sources**: 
  - Local files (.txt and .docx)
  - Amazon S3
  - Azure Blob Storage

- **Dynamic Reloading**: Grounding data can be reloaded without restarting the bot, allowing for real-time knowledge updates.

- **Detailed Logging**: The grounding process is accompanied by comprehensive logging, providing insights into the data loading and processing steps.

- **Improved Chunking and Metadata**: 
  - Uses `RecursiveCharacterTextSplitter` for intelligent text splitting
  - Chunk size: 300 characters
  - Chunk overlap: 100 characters
  - Metadata includes source filename and start index for precise attribution

- **Flexible File Handling**: The system attempts multiple encodings (UTF-8, Latin-1, ASCII) when reading files, increasing compatibility with various file formats.



## Planned Features

1. **Multi-Model Support**: Extend OmniSage's capabilities to use multiple models.

2. **Custom Personality Profiles**: Allow server admins to customize OmniSage's personality and behavior for their specific community needs.

3. **Integration with External APIs**: Connect OmniSage to various external APIs liek Slack and Teams.

4. **Advanced Conversation Memory**: Implement long-term memory storage to remember user preferences and past interactions across sessions.

5. **Voice Recognition**: Add the ability for OmniSage to understand voice commands in voice channels.

6. **Interactive Tutorials**: Create interactive tutorials to help new users learn how to use OmniSage effectively.

7. **Sentiment Analysis**: Implement sentiment analysis to allow OmniSage to better understand and respond to user emotions.

8. **Role-play Modes**: Add specific role-play modes where OmniSage can act as different characters or entities.

9. **Customizable Command Creation**: Allow admins to create custom commands specific to their server needs.

10. **Integration with Server Events**: Enable OmniSage to manage and interact with Discord server events.

11. **Data Visualization**: Implement the ability to generate and share graphs or charts based on conversational data or external information.

12. **Scheduled Messages**: Allow users to schedule messages or reminders through OmniSage.

## Prerequisites

- Python 3.8 or higher
- FFmpeg (for voice functionality)
- Discord Bot Token
- API key(s) for chosen LLM provider(s)
- Docker (optional, for containerized deployment)


## Configuration
1. Copy the .env.example file to a new file named .env:
    ```bash
    cp .env.example .env
2. Open the `.env` file and fill in all the required values. Refer to the comments in the file for guidance on each setting.

3. Make sure to keep your `.env` file secure and never commit it to version control.

4. Additional environment variables for grounding:
    - `USE_GROUNDING`: Set to 'true' to enable grounding, 'false' to disable
    - `GROUNDING_SOURCE`: Set to 'local', 's3', or 'azure'
    - `GROUNDING_PATH`: Path to local grounding files or prefix for remote storage

### RAG System Configuration

To configure the RAG system, you need to set the following environment variables:

- `USE_GROUNDING`: Set to `true` to enable the RAG system
- `GROUNDING_SOURCE`: Choose from `local`, `s3`, or `azure`
- `GROUNDING_PATH`: Path to local grounding files or prefix for remote storage
- `OPENAI_API_KEY`: Your OpenAI API key (used for embeddings)

For S3:

- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_BUCKET_NAME`: Your S3 bucket name

For Azure:

- `AZURE_STORAGE_CONNECTION_STRING`: Your Azure storage connection string
- `AZURE_CONTAINER_NAME`: Your Azure container name
## Installation


## Docker Usage (Preferred)

OmniSage can be run as a Docker container for easy deployment and management.

1. Build the Docker image:
    ```
    docker build -t omnisage .
    ```
2. Run the container:
    ```
    docker run --env-file .env omnisage
    ```


1. Activate the virtual environment (if not using Docker):
### Linux

1. Update package list and install required system packages:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip ffmpeg
2. Clone the repository:
    ```bash
    git clone https://github.com/philbertmukunzi/OmniSage
    cd OmniSage
3. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
4. Install required Python packages:
    ```bash
    pip install -r requirements.txt

### MacOS
1. Install Homebrew if not already installed:
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
2. Install required system packages:
    ```bash
    brew install python ffmpeg
3. Clone the repository:
    ```bash
    git clone https://github.com/philbertmukunzi/OmniSage
    cd OmniSage
4. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
5. Install required Python packages:
    ```bash
    pip install -r requirements.txt

### Windows
1. Install Python from the official website.

2. Install FFmpeg:
    Download FFmpeg from the official website.
    Extract the downloaded file and add the bin folder to your system PATH.
3. Clone the repository:
    ```bash
    git clone https://github.com/philbertmukunzi/OmniSage
    cd OmniSage
4. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate
5. Install required Python packages:
    ```bash
    pip install -r requirements.txt



## Usage
1. Activate the virtual environment (if not using Docker):
    Linux/macOS:
    ```bash
    source venv/bin/activate

     ```
    Windows:
    ```
    venv\Scripts\activate
    ```
2. Run the OmniSage:
    ```
    python3 main.py
    ```
## Command Details

| Command | Description | Permissions |
|---------|-------------|-------------|
| `!join` | OmniSage joins your current voice channel | All users |
| `!leave` | OmniSage leaves the current voice channel | All users |
| `!toggle_tts` | Toggles Text-to-Speech on/off | Admin only |
| `!setstatus <new_status>` | Sets a new status for OmniSage | Admin only |
| `!llm_info` | Displays current LLM configuration | Admin only |
| `!clear_history` | Clears conversation history for the current channel | Admin only |
| `!translate <text>` | Translates the given text to English | All users |
| `!reload_grounding` | Reloads grounding data | Admin only |
| `!trivia <topic>` | Starts a multiple-choice trivia game on the specified topic | All users |
| `!stop_trivia` | Stops the current trivia game | Admin only |
| `!chathelp` | Displays help information for chat commands | All users |

To interact with OmniSage, either mention it or use it in allowed channels.

## Grounding Data

(Grounding data section here)

## Troubleshooting

- If OmniSage doesn't respond, check if it has the necessary permissions in your Discord server.
- Verify that the channel or user role is in the allowed list in the `.env` file.
- For voice command issues, ensure FFmpeg is correctly installed and accessible.
- Check the console output for any error messages.
- If using Docker, ensure all necessary environment variables are properly set in your `.env` file.
- For translation issues, make sure the LLM API is properly configured and accessible.

## Grounding Data

OmniSage supports grounding with custom data from three sources:

1. Local files (.txt and .docx)
2. Amazon S3
3. Azure Blob Storage

To use grounding:

1. Set `USE_GROUNDING=true` in your `.env` file.
2. Choose the `GROUNDING_SOURCE` (local, s3, or azure) and set the corresponding configuration variables.
3. For local grounding, place your text files in the directory specified by `GROUNDING_PATH`.
4. For S3 or Azure, upload your text files to the specified bucket or container.

The grounding system now uses improved chunking and metadata for more relevant information retrieval. The bot will mention the source of information in its responses when using grounded knowledge.

Use the `!reload_grounding` command to refresh OmniSage's grounding data without restarting the bot.

## Troubleshooting

- If OmniSage doesn't respond, check if it has the necessary permissions in your Discord server.
- Verify that the channel or user role is in the allowed list in the `.env` file.
- For voice command issues, ensure FFmpeg is correctly installed and accessible.
- Check the console output for any error messages.
- If using Docker, ensure all necessary environment variables are properly set in your `.env` file.
- For grounding issues, verify that your grounding files are in the correct format (.txt or .docx) and the `GROUNDING_PATH` is set correctly.
- If encountering encoding errors with grounding files, ensure they are in UTF-8 encoding or update the `read_file_with_fallback_encoding` function in `grounding_utils.py` to include the correct encoding.

## Contributing

Contributions to OmniSage are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

- If OmniSage doesn't respond, check if it has the necessary permissions in your Discord server.
- Verify that the channel or user role is in the allowed list in the `.env` file.
- For voice command issues, ensure FFmpeg is correctly installed and accessible.
- Check the console output for any error messages.
- If using Docker, ensure all necessary environment variables are properly set in your `.env` file.

## Contributing

Contributions to OmniSage are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
