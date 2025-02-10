import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
from datetime import datetime
import threading

class EmailService:
    def __init__(self, smtp_server, smtp_port, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(self, recipient, subject, content):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = recipient
            msg['Subject'] = subject

            msg.attach(MIMEText(content, 'html'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

    def send_daily_digest(self, user_email, news_data):
        subject = f"Stock Market Daily Digest - {datetime.now().strftime('%Y-%m-%d')}"
        
        content = """
        <html>
            <head>
                <style>
                    .digest {
                        font-family: Arial, sans-serif;
                        max-width: 600px;
                        margin: 0 auto;
                    }
                    .news-item {
                        margin-bottom: 20px;
                        padding: 10px;
                        border-bottom: 1px solid #eee;
                    }
                    .sentiment {
                        font-weight: bold;
                    }
                    .positive { color: green; }
                    .negative { color: red; }
                    .neutral { color: gray; }
                </style>
            </head>
            <body>
                <div class="digest">
                    <h2>Your Daily Stock Market Update</h2>
        """
        
        for _, news in news_data.iterrows():
            content += f"""
                <div class="news-item">
                    <h3>{news['title']}</h3>
                    <p>{news['summary'][:200]}...</p>
                    <p>Sentiment: <span class="sentiment {news['overall_sentiment_label'].lower()}">
                        {news['overall_sentiment_label']} ({news['overall_sentiment_score']:.2f})
                    </span></p>
                    <a href="{news['url']}">Read more</a>
                </div>
            """

        content += """
                </div>
            </body>
        </html>
        """

        return self.send_email(user_email, subject, content)

    def schedule_daily_digest(self, user_email, news_service):
        def send_digest():
            news_data = news_service.get_news()
            self.send_daily_digest(user_email, news_data)

        schedule.every().day.at("08:00").do(send_digest)

        def run_schedule():
            while True:
                schedule.run_pending()
                time.sleep(60)

        thread = threading.Thread(target=run_schedule, daemon=True)
        thread.start()
