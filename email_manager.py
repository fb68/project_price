# ------------------------- LES IMPORTATIONS NECESSAIRES -------------------------#

import smtplib
from email.mime.text import MIMEText

class EmailManager:
    def __init__(self):
        pass

    def create_email_body(self, df_auchan, df_carrefour, savings, auchan_msg, carrefour_msg):
        """
        Crée le corps de l'e-mail à envoyer

        Paramètres
        ----------
        df_auchan : pandas.DataFrame
            DataFrame contenant les produits d'Auchan.
        df_carrefour : pandas.DataFrame
            DataFrame contenant les produits de Carrefour.
        savings : str
            Informations sur les économies réalisées.
        auchan_msg : str
            Message sur la variation de prix chez Auchan.
        carrefour_msg : str
            Message sur la variation de prix chez Carrefour.

        Returns
        -------
        str
            Corps de l'e-mail.
        """
        body = f"Voici le panier Auchan :\n\n{df_auchan.to_string()}\n\nVoici le panier Carrefour:\n\n{df_carrefour.to_string()}\n\n{savings}\n\n"
        body += "\nInformations sur la variation de prix :"
        body += f"\nAuchan : {auchan_msg}" if auchan_msg else "\nAucune variation de prix chez Auchan."
        body += f"\nCarrefour : {carrefour_msg}" if carrefour_msg else "\nAucune variation de prix chez Carrefour."
        return body

    def send_email_with_hotmail(self, df_auchan, df_carrefour, savings, auchan_msg, carrefour_msg):
        """
        Envoie un e-mail avec les données fournies

        Paramètres
        ----------
        df_auchan : pandas.DataFrame
            DataFrame contenant les produits d'Auchan.
        df_carrefour : pandas.DataFrame
            DataFrame contenant les produits de Carrefour.
        savings : str
            Informations sur les économies réalisées.
        auchan_msg : str
            Message sur la variation de prix chez Auchan.
        carrefour_msg : str
            Message sur la variation de prix chez Carrefour.
        """
        smtp_server = 'smtp-mail.outlook.com'
        port = 587
        sender_email = 'ferventbatina07@gmail.com'
        sender_password = 'qttovcccoqqgteem'
        recipient_email = 'saisir_votre_mail'
        
        email_body = self.create_email_body(df_auchan, df_carrefour, savings, auchan_msg, carrefour_msg)
        
        msg = MIMEText(email_body)
        
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = 'Comparaison des coûts de panier'
        
        try:
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
            print("E-mail envoyé avec succès!")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'e-mail : {e}")
