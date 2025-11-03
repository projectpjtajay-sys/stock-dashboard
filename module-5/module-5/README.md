# GenAI Research & Writing Assistant

A powerful dual-model AI assistant that combines **Claude** for comprehensive research and **OpenAI** for intelligent summarization. Built with Streamlit for an intuitive web interface.

## Features

### Research Assistant (Claude)
- **Comprehensive Research**: Conduct in-depth research on any topic
- **Thread Management**: Organize research sessions with conversation history
- **Follow-up Questions**: Continue research with contextual follow-up queries
- **Specific Inquiries**: Ask targeted questions about your research topic

### Summary Generator (OpenAI)
- **Multiple Summary Types**: Brief, bullet-point, and executive summaries
- **Creative Summaries**: Narrative, poetic, dialogue, and analogy-based summaries
- **Content Sources**: Summarize current research, pasted content, or uploaded files
- **Export Options**: Download summaries and research threads

### Professional Features
- **Thread Management**: Save and organize research sessions
- **Export Functionality**: Download research and summaries as text files
- **Metrics Dashboard**: Track word count, reading time, and content metrics
- **Settings Panel**: Configure API keys and view application statistics

## Quick Start

### Prerequisites
- Python 3.8+
- Anthropic Claude API key
- OpenAI API key

### Installation

1. **Clone/Download the project**
   ```bash
   cd module-5
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys**
   ```bash
   cp .env.example .env
   # Edit .env file with your actual API keys
   ```

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`

## API Keys Setup

### Get Claude API Key
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up/login to your account
3. Navigate to API Keys section
4. Create a new API key

### Get OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up/login to your account
3. Go to API Keys section
4. Create a new API key

### Configure Environment
Create a `.env` file in the project root:
```env
ANTHROPIC_API_KEY=your_claude_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage Guide

### 1. Research Assistant
- Enter your research topic in the main form
- Optionally add up to 3 specific questions
- Click "Start Research" to begin
- Use follow-up questions to dive deeper
- Export research results as text files

### 2. Summary Generator
- Select content source (current research, paste, or upload)
- Choose summary type (brief, bullet, executive)
- Optionally select a creative style
- Generate and download summaries

### 3. Thread Manager
- View all your research sessions
- Export individual threads
- Delete old research threads
- Track message counts and dates

### 4. Settings
- View API configuration status
- Check application statistics
- Clear all data if needed
- Access setup instructions

## Project Structure

```
module-5/
├── main.py              # Main Streamlit application
├── config.py            # Configuration and API key management
├── claude_client.py     # Claude API integration
├── openai_client.py     # OpenAI API integration
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment file
└── README.md           # This file
```

## Configuration

### Model Settings
- **Claude Model**: `claude-3-sonnet-20240229`
- **OpenAI Model**: `gpt-3.5-turbo`
- **Max Tokens**: 4000 (Claude), 1000 (OpenAI)
- **Temperature**: 0.7

### Customization
Edit `config.py` to modify:
- Model versions
- Token limits
- Temperature settings
- Other API parameters

## Use Cases

### Academic Research
- Literature reviews
- Topic exploration
- Fact gathering
- Source summarization

### Business Intelligence
- Market research
- Competitive analysis
- Executive summaries
- Report generation

### Creative Writing
- Story research
- Character development
- World building
- Creative summaries

### Professional Development
- Industry trends
- Technology research
- Learning summaries
- Knowledge management

## Privacy & Security

- API keys are stored locally in environment variables
- No data is stored on external servers
- Research threads are kept in session state
- All communication is direct with AI providers

## Troubleshooting

### Common Issues

**API Key Errors**
- Ensure API keys are correctly set in `.env` file
- Check API key validity and quotas
- Verify environment variables are loaded

**Import Errors**
- Run `pip install -r requirements.txt`
- Check Python version compatibility
- Ensure all dependencies are installed

**Streamlit Issues**
- Clear browser cache
- Restart the Streamlit server
- Check console for error messages

## Features Overview

| Feature | Claude | OpenAI | Description |
|---------|--------|--------|-------------|
| Research | Yes | No | Comprehensive topic research |
| Summarization | No | Yes | Brief content summaries |
| Thread Management | Yes | No | Research conversation history |
| Creative Writing | No | Yes | Creative summary styles |
| Follow-up Questions | Yes | No | Contextual research continuation |
| Export Functions | Yes | Yes | Download research and summaries |

## Contributing

This is an educational project for the consultant program. Feel free to:
- Suggest improvements
- Report bugs
- Share use cases
- Propose new features

## License

This project is created for educational purposes as part of the consultant program curriculum.

---

**Happy Researching!**