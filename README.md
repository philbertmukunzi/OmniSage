# OmniSage: Multimodal Discord LLM Chatbot

OmniSage is a versatile Discord bot that leverages Language Learning Models (LLMs) to generate intelligent responses, join voice channels, and provide text-to-speech functionality. It's designed to be your all-knowing companion in Discord servers.

**🚀 Hobby Project Disclaimer 🛸**
> Warning: This bot may occasionally produce wisdom beyond human comprehension or just utter nonsense. It's a hobby project built to learn and practice LLM integration in a fun way . Expect the unexpected, embrace the chaos, and don't be surprised if you find some "optimized" spaghetti code.😉

## Table of Contents
1. [Features](#features)
2. [Features in Detail](#features-in-detail)
3. [Planned Features](#planned-features)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Usage](#usage)
8. [Command Details](#command-details)
9. [Grounding Data](#grounding-data)
10. [Troubleshooting](#troubleshooting)
11. [Contributing](#contributing)
12. [License](#license)

## Features

OmniSage comes packed with a variety of features:

- Intelligent responses using various LLM providers (OpenAI, Anthropic, local models)
- Voice channel integration
- Text-to-Speech (TTS) functionality
- Support for image analysis (if LLM supports it)
- Rate limiting and cooldowns
- Configurable through environment variables
- Admin commands for bot management
- Multi-channel and role-based permissions
- Conversation history management
- Translation command
- Grounding with custom data (local files, S3, or Azure Blob Storage)

## Features in Detail

### Intelligent Responses
OmniSage utilizes state-of-the-art Language Learning Models to generate human-like responses. It supports multiple LLM providers:
- OpenAI (GPT-3.5, GPT-4, GPT-4o)
- Anthropic (Claude, Claude Instant)
- Local models (with appropriate setup)

The bot maintains conversation history to provide context-aware responses, enhancing the chat experience.

### Voice Integration
- Join and leave voice channels on command
- Text-to-Speech (TTS) functionality to read out responses in voice channels
- Configurable TTS settings (model, voice)

### Configurability
- Extensive configuration options via environment variables
- Customizable command prefix, cooldowns, and rate limits
- Ability to restrict bot usage to specific channels and roles

### Admin Features
- Set bot status
- Toggle TTS on/off
- View current LLM configuration
- Clear conversation history
- Reload grounding data

### Grounding Data
- Enhance OmniSage's knowledge with custom data
- Support for multiple data sources:
  - Local files
  - Amazon S3
  - Azure Blob Storage
- Dynamic reloading of grounding data without bot restart

### Security and Performance
- Rate limiting to prevent API abuse
- Cooldowns on commands to manage usage
- Secure handling of API keys and sensitive information

### Utility Features
- Translation command to translate text to English
- Comprehensive help command for user guidance

### Extensibility
- Modular code structure for easy additions and modifications
- Support for adding new commands and features

## Prerequisites

- Python 3.8 or higher
- FFmpeg (for voice functionality)
- Discord Bot Token
- API key(s) for chosen LLM provider(s)

## Planned Features

We're constantly working to improve OmniSage and expand its capabilities. Here are some features we're planning to implement in the future:

1. **Multi-language Support**: Extend OmniSage's capabilities to understand and respond in multiple languages.

2. **Custom Personality Profiles**: Allow server admins to customize OmniSage's personality and behavior for their specific community needs.

3. **Integration with External APIs**: Connect OmniSage to various external APIs like Slack , Teams and other API's.

4. **Advanced Conversation Memory**: Implement long-term memory storage to remember user preferences and past interactions across sessions.

5. **Voice Recognition**: Add the ability for OmniSage to understand voice commands in voice channels.

6. **Interactive Tutorials**: Create interactive tutorials to help new users learn how to use OmniSage effectively.

7. **Sentiment Analysis**: Implement sentiment analysis to allow OmniSage to better understand and respond to user emotions.

8. **Role-play Modes**: Add specific role-play modes where OmniSage can act as different characters or entities.

9. **Customizable Command Creation**: Allow admins to create custom commands specific to their server needs.

10. **Integration with Server Events**: Enable OmniSage to manage and interact with Discord server events.

11. **Data Visualization**: Implement the ability to generate and share graphs or charts based on conversational data or external information.

12. **Scheduled Messages**: Allow users to schedule messages or reminders through OmniSage.





## Installation

1. Clone the repository:

### Linux

1. Update package list and install required system packages:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip ffmpeg
2. Clone the repository:
    ```bash
    git clone https://github.com/philbertmukunzi/OmniSage
    cd discord-llm-chatbot
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
    cd discord-llm-chatbot
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
    cd discord-llm-chatbot
4. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate
5. Install required Python packages:
    ```bash
    pip install -r requirements.txt

## Configuration
1. Copy the .env.example file to a new file named .env:
    ```bash
    cp .env.example .env
2. Open the `.env` file and fill in all the required values. Refer to the comments in the file for guidance on each setting.

3. Make sure to keep your `.env` file secure and never commit it to version control.

## Usage
1. Activate the virtual environment (if not already activated):
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
| `!chathelp` | Displays help information for chat commands | All users |

To interact with OmniSage, either mention it or use it in allowed channels.

## Grounding Data

OmniSage supports grounding with custom data from three sources:

1. Local files
2. Amazon S3
3. Azure Blob Storage

To use grounding:

1. Set `USE_GROUNDING=true` in your `.env` file.
2. Choose the `GROUNDING_SOURCE` (local, s3, or azure) and set the corresponding configuration variables.
3. For local grounding, place your text files in the directory specified by `GROUNDING_PATH`.
4. For S3 or Azure, upload your text files to the specified bucket or container.

Use the `!reload_grounding` command to refresh OmniSage's grounding data without restarting the bot.

## Troubleshooting

- If OmniSage doesn't respond, check if it has the necessary permissions in your Discord server.
- Verify that the channel or user role is in the allowed list in the `.env` file.
- For voice command issues, ensure FFmpeg is correctly installed and accessible.
- Check the console output for any error messages.

## Contributing

Contributions to OmniSage are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.