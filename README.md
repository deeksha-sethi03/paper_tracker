# Paper Tracker

A Python script that tracks and sends email updates about new papers related to humanoid robotics from arXiv.

## Features

- Fetches papers from arXiv
- Filters papers by date (currently set to fetch papers from 2025)
- Sends email updates with paper details including title, abstract, and URL
- Configurable through environment variables

## Requirements

- Python 3.x
- Required Python packages:
  - arxiv
  - python-dotenv
  - smtplib (built-in)
  - email (built-in)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/paper_tracker.git
cd paper_tracker
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your email credentials:
```
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_PASSWORD=your-app-password
RECIPIENT_EMAIL=recipient@email.com
```

Note: If using Gmail, you'll need to generate an App Password:
1. Enable 2-Step Verification in your Google Account
2. Generate an App Password for "Mail"
3. Use the 16-digit code as your EMAIL_PASSWORD

## Usage

Run the script:
```bash
python paper_tracker.py
```

The script will:
1. Fetch papers from arXiv
2. Format them into an email
3. Send the email to the specified recipient

## Configuration

You can modify the following in the code:
- Search query (currently "humanoid")
- Date range for papers
- Number of papers to fetch
- Email subject and formatting
