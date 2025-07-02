
# 📄 FastMCP Google Docs Manager

Manage Google Docs using a FastMCP API server for Gemini-CLI. Supports listing documents, reading content, and creating new docs.

## 🚀 Features

- List Google Docs files
- Read document content
- Create new documents with title and content

## 🔧 Setup

### Install Dependencies

```bash
pip install uv
cd gemini-tasks-mcp
uv venv
source .venv/bin/activate
uv run main.py
```

### Generate Google API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable **Google Docs API** and **Google Drive API**.
3. Go to **APIs & Services → Credentials**.
4. Click **“Create Credentials” → “OAuth client ID” → Application type: Desktop App**.
5. Download `credentials.json` and place it in the project folder.

### Gemini-CLI Configuration

```bash
cd ~/.gemini
nano settings.json
```

```json
"mcpServers": {
    "docsManager": {
      "command": "uv",
      "args": ["run", "main.py"],
      "cwd": "<<full-path>>/gemini-docs-mcp",
      "timeout": 20000
    }
}
```

## ❤️ Powered by FastMCP + Google Docs API + Google Drive API