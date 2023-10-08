# Sansetto - art bot

The bot is represented by a Flask application that has Web-UI of uploading and scheduled task for sending image to the telegram channel.

## Getting Started

### Prerequisites
Before you begin, make sure you have the following installed:

- Python 3.x
- Minio Server (for local object storage)

### Installation

1. Clone the repository:

```bash

git clone https://github.com/your_username/project.git
cd project
````

2. Install dependencies:

```bash 
pip install -r requirements.txt
```

3. Configuration

Configure the application by editing the .env file. Provide the necessary information for Minio and Flask.

4. Running the Application

#### Local

```bash
python app.py
```
