"""
Alert System - Send alerts via email, Telegram, etc.
"""
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import config

logger = logging.getLogger(__name__)

class AlertManager:
    """Manages sending alerts through various channels"""
    
    def __init__(self):
        self.email_enabled = config.ALERT_CHANNELS.get('email', False)
        self.telegram_enabled = config.ALERT_CHANNELS.get('telegram', False)
        self.webhook_enabled = config.ALERT_CHANNELS.get('webhook', False)
    
    def send_email_alert(self, predictions):
        """
        Send email alert with predictions
        
        Args:
            predictions: Dict with prediction summary
            
        Returns:
            bool: Success status
        """
        if not self.email_enabled or not config.EMAIL_SENDER:
            logger.warning("Email alerts not configured")
            return False
        
        try:
            # Build email content
            subject = f"NSE Market Prediction Alert - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            body = self._build_email_body(predictions)
            
            # Create email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = config.EMAIL_SENDER
            msg['To'] = ', '.join(config.EMAIL_RECIPIENTS)
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
                server.starttls()
                server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
                server.sendmail(
                    config.EMAIL_SENDER,
                    config.EMAIL_RECIPIENTS,
                    msg.as_string()
                )
            
            logger.info(f"Email alert sent to {config.EMAIL_RECIPIENTS}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email alert: {str(e)}")
            return False
    
    def send_telegram_alert(self, predictions):
        """
        Send Telegram alert with predictions
        
        Args:
            predictions: Dict with prediction summary
            
        Returns:
            bool: Success status
        """
        if not self.telegram_enabled or not config.TELEGRAM_BOT_TOKEN:
            logger.warning("Telegram alerts not configured")
            return False
        
        try:
            import requests
            
            message = self._build_telegram_message(predictions)
            
            url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': config.TELEGRAM_CHAT_ID,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                logger.info("Telegram alert sent successfully")
                return True
            else:
                logger.error(f"Telegram alert failed: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending Telegram alert: {str(e)}")
            return False
    
    def send_webhook_alert(self, predictions, webhook_url):
        """
        Send webhook alert (integration with trading platforms)
        
        Args:
            predictions: Dict with prediction summary
            webhook_url: Webhook URL to send data to
            
        Returns:
            bool: Success status
        """
        if not self.webhook_enabled:
            logger.warning("Webhook alerts not enabled")
            return False
        
        try:
            import requests
            import json
            
            payload = {
                'timestamp': datetime.now().isoformat(),
                'predictions': predictions
            }
            
            response = requests.post(webhook_url, json=payload)
            
            if response.status_code in [200, 201]:
                logger.info(f"Webhook alert sent to {webhook_url}")
                return True
            else:
                logger.error(f"Webhook alert failed: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending webhook alert: {str(e)}")
            return False
    
    def send_all_alerts(self, predictions):
        """Send alerts through all enabled channels"""
        try:
            results = {}
            
            if self.email_enabled:
                results['email'] = self.send_email_alert(predictions)
            
            if self.telegram_enabled:
                results['telegram'] = self.send_telegram_alert(predictions)
            
            logger.info(f"Alert results: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Error sending alerts: {str(e)}")
            return None
    
    def _build_email_body(self, predictions):
        """Build HTML email body"""
        html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .header {{ background-color: #2c3e50; color: white; padding: 20px; }}
                    .summary {{ background-color: #ecf0f1; padding: 15px; margin: 10px 0; }}
                    .bull {{ color: green; font-weight: bold; }}
                    .bear {{ color: red; font-weight: bold; }}
                    .alert {{ background-color: #fff3cd; padding: 10px; margin: 10px 0; border-left: 4px solid #ffc107; }}
                    table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                    th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
                    th {{ background-color: #34495e; color: white; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>NSE Market Prediction Alert</h1>
                    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div class="summary">
                    <h2>Summary</h2>
                    <p><strong>Total Predictions:</strong> {predictions.get('total_predictions', 0)}</p>
                    <p><span class="bull">Bull Signals: {predictions.get('bull_signals', 0)}</span></p>
                    <p><span class="bear">Bear Signals: {predictions.get('bear_signals', 0)}</span></p>
                    <p><strong>Triggered Alerts:</strong> {predictions.get('triggered_alerts', 0)}</p>
                    <p><strong>Average Confidence:</strong> {predictions.get('average_confidence', 0):.2%}</p>
                </div>
                
                <div class="details">
                    <h2>Detailed Predictions</h2>
                    <table>
                        <tr>
                            <th>Instrument</th>
                            <th>Signal</th>
                            <th>Confidence</th>
                            <th>Alert</th>
                        </tr>
        """
        
        for detail in predictions.get('details', []):
            signal_class = 'bull' if detail['signal'] == 'BULL' else 'bear'
            alert_status = '⚠️ YES' if detail['alert_triggered'] else 'No'
            
            html += f"""
                        <tr>
                            <td>{detail['instrument']}</td>
                            <td class="{signal_class}">{detail['signal']}</td>
                            <td>{detail['confidence']:.2%}</td>
                            <td>{alert_status}</td>
                        </tr>
            """
        
        html += """
                    </table>
                </div>
            </body>
        </html>
        """
        
        return html
    
    def _build_telegram_message(self, predictions):
        """Build Telegram message"""
        message = f"""
<b>NSE Market Prediction Alert</b>
📊 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

<b>Summary:</b>
• Total Predictions: {predictions.get('total_predictions', 0)}
• 🟢 Bull Signals: {predictions.get('bull_signals', 0)}
• 🔴 Bear Signals: {predictions.get('bear_signals', 0)}
• ⚠️ Triggered Alerts: {predictions.get('triggered_alerts', 0)}
• Average Confidence: {predictions.get('average_confidence', 0):.1%}

<b>Details:</b>
        """
        
        for detail in predictions.get('details', []):
            emoji = '🟢' if detail['signal'] == 'BULL' else '🔴'
            alert = '✅' if detail['alert_triggered'] else '❌'
            message += f"\n{emoji} <b>{detail['instrument']}</b>: {detail['signal']} ({detail['confidence']:.1%}) {alert}"
        
        return message
