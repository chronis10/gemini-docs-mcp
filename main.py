"""
FastMCP Google Docs Manager with File Listing
"""

from fastmcp import FastMCP
from typing import List
import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


# ✅ Create MCP server
mcp = FastMCP("Google Docs Manager")


# ✅ Google API setup for Docs + Drive
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]

script_dir = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(script_dir, 'credentials.json')
token_path = os.path.join(script_dir, 'token.pickle')


def get_services():
    creds = None
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    docs_service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    return docs_service, drive_service


# ✅ List available Google Docs files
@mcp.tool
def list_documents(max_results: int = 10) -> List[dict]:
    """
    List Google Docs files from your Google Drive.
    """
    _, drive_service = get_services()

    query = "mimeType='application/vnd.google-apps.document'"

    results = drive_service.files().list(
        q=query,
        pageSize=max_results,
        fields="files(id, name)"
    ).execute()

    files = results.get('files', [])

    doc_list = []
    for file in files:
        doc_list.append({
            'name': file.get('name'),
            'id': file.get('id'),
            'url': f"https://docs.google.com/document/d/{file.get('id')}/edit"
        })

    return doc_list


# ✅ Read content from a Google Doc
@mcp.tool
def read_document(doc_id: str) -> str:
    """
    Read the text content of a Google Doc by its document ID.
    """
    docs_service, _ = get_services()

    document = docs_service.documents().get(documentId=doc_id).execute()

    content = document.get('body').get('content')
    text_output = ""

    for element in content:
        if 'paragraph' in element:
            elements = element.get('paragraph').get('elements')
            for elem in elements:
                text_run = elem.get('textRun')
                if text_run:
                    text_output += text_run.get('content')

    return text_output.strip()


# ✅ Create a new Google Doc
@mcp.tool
def create_document(title: str, content: str) -> dict:
    """
    Create a new Google Doc with a title and body content.
    """
    docs_service, _ = get_services()

    doc = docs_service.documents().create(body={'title': title}).execute()
    doc_id = doc.get('documentId')

    # Insert text into the document
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': content
            }
        }
    ]

    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': requests}
    ).execute()

    return {
        'documentId': doc_id,
        'title': title,
        'url': f"https://docs.google.com/document/d/{doc_id}/edit"
    }


# ✅ Run MCP server
if __name__ == "__main__":
    mcp.run()
