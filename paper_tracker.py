import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from scholarly import scholarly
import arxiv
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# def get_google_scholar_papers():
#     """Search for new papers on Google Scholar."""
#     papers = []
#     max_retries = 2
#     
#     while retry_count < max_retries:
#         try:
#             search_query = scholarly.search_keyword('humanoid')
#             
#             # Get the first 5 results instead of 10
#             for i in range(5):
#                 try:
#                     paper = next(search_query)
#                     if paper and isinstance(paper, dict):
#                         title = paper.get('title', '')
#                         # Only add papers that have a non-empty title
#                         if title and title.strip():
#                             papers.append({
#                                 'title': title,
#                                 'abstract': paper.get('abstract', 'No abstract available'),
#                                 'url': paper.get('url', '#'),
#                                 'year': paper.get('year', 'N/A')
#                             })
#                 except StopIteration:
#                     break
#                 except Exception as e:
#                     print(f"Error processing paper: {str(e)}")
#                     continue
#             
#             # If we got any valid papers, break the retry loop
#             if papers:
#                 break
#                 
#         except Exception as e:
#             print(f"Error searching Google Scholar (attempt {retry_count + 1}/{max_retries}): {str(e)}")
#             retry_count += 1
#             if retry_count < max_retries:
#                 print("Retrying after a short delay...")
#                 time.sleep(3)  # Reduced from 5 to 3 seconds
#     
#     return papers if papers else [{'title': 'No new papers found on Google Scholar'}]

def get_arxiv_papers():
    """Search for new papers on arXiv from the start of 2025."""
    # Set the start date to January 1st, 2025
    start_date = datetime.date(2025, 1, 1)
    
    # Create the search query with reduced max_results
    search = arxiv.Search(
        query="humanoid",
        max_results=30,  # Reduced from 100 to 30
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    papers = []
    client = arxiv.Client()
    for result in client.results(search):
        paper_date = result.published.date()
        if paper_date >= start_date:
            papers.append({
                'title': result.title,
                'abstract': result.summary,
                'url': result.entry_id,
                'year': result.published.year,
                'date': paper_date.strftime('%Y-%m-%d')
            })
    
    # Sort papers by date (newest first)
    papers.sort(key=lambda x: x['date'], reverse=True)
    
    return papers if papers else [{'title': 'No new papers found on arXiv since January 1st, 2025'}]

def format_email_content(scholar_papers, arxiv_papers):
    """Format the email content with the papers found."""
    content = "New Papers on Humanoid Robotics\n\n"
    
    # content += "=== Google Scholar Papers ===\n\n"
    # for paper in scholar_papers:
    #     if paper['title'] == 'No new papers found on Google Scholar':
    #         content += paper['title'] + "\n"
    #     else:
    #         content += f"Title: {paper['title']}\n"
    #         content += f"Year: {paper['year']}\n"
    #         content += f"URL: {paper['url']}\n"
    #         content += f"Abstract: {paper['abstract']}\n"
    #     content += "-" * 80 + "\n\n"
    
    content += "=== arXiv Papers ===\n\n"
    for paper in arxiv_papers:
        if paper['title'] == 'No new papers found on arXiv since January 1st, 2025':
            content += paper['title'] + "\n"
        else:
            content += f"Title: {paper['title']}\n"
            content += f"Year: {paper['year']}\n"
            content += f"URL: {paper['url']}\n"
            content += f"Abstract: {paper['abstract']}\n"
        content += "-" * 80 + "\n\n"
    
    return content

def send_email(content):
    """Send email with the papers found."""
    sender_email = os.getenv('EMAIL_ADDRESS')
    sender_password = os.getenv('EMAIL_PASSWORD')
    recipient_email = os.getenv('RECIPIENT_EMAIL')
    
    if not all([sender_email, sender_password, recipient_email]):
        print("Error: Missing email credentials in environment variables")
        return False
    
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"Humanoid Robotics Papers Update - {datetime.date.today()}"
    
    msg.attach(MIMEText(content, 'plain'))
    
    # Send the email
    try:
        # Create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        
        # Start TLS for security
        server.starttls()
        
        # Authentication
        server.login(sender_email, sender_password)
        
        # Convert message to string and send
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        
        # Terminate the session
        server.quit()
        print("Email sent successfully!")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("Error: Authentication failed. Please check your email credentials.")
        print("Note: If using Gmail, make sure to use an App Password instead of your regular password.")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    
    return False

def main():
    # Get papers from arXiv only
    # scholar_papers = get_google_scholar_papers()
    arxiv_papers = get_arxiv_papers()
    
    # If we found any papers, send the email
    if arxiv_papers:  # Removed scholar_papers check
        content = format_email_content([], arxiv_papers)  # Pass empty list for scholar_papers
        send_email(content)
    else:
        print("No new papers found today.")

if __name__ == "__main__":
    main() 