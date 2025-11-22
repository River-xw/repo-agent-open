# API Documentation

## Overview

This API provides endpoints for interacting with the Repo-Agent backend, which is built using FastAPI. It allows for health checks, document generation, and listing of generated documentation files. The API serves a web application for repository analysis and documentation.

Base URL: `http://localhost:8000` (default FastAPI port)

## Endpoints

### GET /

**Description:** Root endpoint, returns a welcome message.

**Response:**
- Status: 200 OK
- Content-Type: application/json
- Body:
  ```json
  {
    "message": "Welcome to Repo-Agent API"
  }
  ```

**Example Request:**
```bash
curl http://localhost:8000/
```

### GET /health

**Description:** Health check endpoint to verify the service is running.

**Response:**
- Status: 200 OK
- Content-Type: application/json
- Body:
  ```json
  {
    "status": "healthy"
  }
  ```

**Example Request:**
```bash
curl http://localhost:8000/health
```

### GET /wikis

**Description:** Static file serving for generated wiki documentation. This is a mounted static directory.

**Response:**
- Status: 200 OK (for valid files)
- Content-Type: varies (e.g., text/html, application/json)
- Body: The content of the requested wiki file.

**Example Request:**
```bash
curl http://localhost:8000/wikis/facebook_zstd/index.html
```

### POST /agents/generate

**Description:** Triggers the generation of documentation for a repository.

**Request:**
- Content-Type: application/json
- Body: JSON object conforming to `GenerateRequest` model.
  - `owner` (string): Repository owner (e.g., "facebook")
  - `repo` (string): Repository name (e.g., "zstd")
  - `wiki_path` (string): Local path for generated wiki (e.g., "./.wikis/facebook_zstd")
  - `wiki_url` (string): URL for accessing the wiki (e.g., "http://localhost:8000/wikis/facebook_zstd")
  - `files` (array of strings): Optional list of specific files to analyze (default: [])

**Response:**
- Status: 200 OK
- Content-Type: application/json
- Body: JSON object conforming to `BaseResponse` model.
  - `success` (boolean): Indicates if the operation was successful
  - `message` (string): Response message
  - `data` (object): Additional data if applicable

**Example Request:**
```bash
curl -X POST http://localhost:8000/agents/generate \
  -H "Content-Type: application/json" \
  -d '{
    "owner": "facebook",
    "repo": "zstd",
    "wiki_path": "./.wikis/facebook_zstd",
    "wiki_url": "http://localhost:8000/wikis/facebook_zstd",
    "files": []
  }'
```

**Example Response:**
```json
{
  "success": true,
  "message": "Documentation generated successfully",
  "data": {}
}
```

### GET /agents/list

**Description:** Lists the generated wiki documentation files.

**Response:**
- Status: 200 OK
- Content-Type: application/json
- Body: JSON object conforming to `BaseResponse` model.
  - `success` (boolean): Indicates if the operation was successful
  - `message` (string): Response message
  - `data` (array): List of wiki file paths or metadata

**Example Request:**
```bash
curl http://localhost:8000/agents/list
```

**Example Response:**
```json
{
  "success": true,
  "message": "Wiki files listed",
  "data": [
    "facebook_zstd",
    "other_repo"
  ]
}
```

## Data Models

### GenerateRequest
- `owner`: string - Repository owner
- `repo`: string - Repository name
- `wiki_path`: string - Local path for wiki
- `wiki_url`: string - URL for wiki access
- `files`: array of strings - Optional files to analyze

### BaseResponse
- `success`: boolean - Operation success status
- `message`: string - Response message
- `data`: object - Response data

## Error Handling

All endpoints may return error responses with appropriate HTTP status codes (e.g., 400 Bad Request, 500 Internal Server Error) and a JSON body containing error details.

## Authentication

Currently, no authentication is required for these endpoints.

## Notes

- The server runs on port 8000 by default.
- Static wiki files are served from the `/.wikis` directory.
- Ensure the backend is running before making requests.