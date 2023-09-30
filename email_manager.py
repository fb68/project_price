import smtplib
from email.mime.text import MIMEText

class EmailManager:
    def __init__(self):
        pass

    def create_email_body(self, df_auchan, df_carrefour, savings, auchan_msg, carrefour_msg):
        body = f"Voici le panier Auchan :\n\n{df_auchan.to_string()}\n\nVoici le panier Carrefour:\n\n{df_carrefour.to_string()}\n\n{savings}\n\n"
        body += "\nInformations sur la variation de prix :"
        body += f"\nAuchan : {auchan_msg}" if auchan_msg else "\nAucune variation de prix chez Auchan."
        body += f"\nCarrefour : {carrefour_msg}" if carrefour_msg else "\nAucune variation de prix chez Carrefour."
        return body


    def send_email_with_hotmail(self, df_auchan, df_carrefour, savings, auchan_msg, carrefour_msg):
        smtp_server = 'smtp-mail.outlook.com'
        port = 587
        sender_email = 'ferventbatina07@gmail.com'
        sender_password = 'qttovcccoqqgteem'
        recipient_email = 'projetpythonm2@gmail.com'
        
        email_body = self.create_email_body(df_auchan, df_carrefour, savings, auchan_msg, carrefour_msg)
        
        msg = MIMEText(email_body)
        
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = 'Comparaison des coûts de panier'
        
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        
        print("E-mail envoyé avec succès!")
