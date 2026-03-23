import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ─── CONFIG — À adapter avec vos identifiants ───────────────────
SMTP_HOST     = "smtp.gmail.com"
SMTP_PORT     = 587
SMTP_USER     = "votre-email@gmail.com"      # ← Votre email
SMTP_PASSWORD = "votre-mot-de-passe-app"     # ← Mot de passe d'application Gmail
FROM_NAME     = "APEX Sport & Tech"

def _send(to: str, subject: str, html: str):
    """Fonction interne d'envoi d'email."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = f"{FROM_NAME} <{SMTP_USER}>"
        msg["To"]      = to
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to, msg.as_string())

        print(f"✅ Email envoyé à {to} : {subject}")
    except Exception as e:
        # En prod, logger l'erreur sans crasher l'API
        print(f"⚠️  Email non envoyé ({to}) : {e}")

# ─── TEMPLATES ──────────────────────────────────────────────────
def send_welcome_email(to: str, name: str):
    subject = "Bienvenue chez APEX Sport & Tech 🚀"
    html = f"""
    <div style="font-family:sans-serif;max-width:600px;margin:auto;background:#0a0a0a;color:#f0f0f0;padding:40px;border-radius:8px">
      <h1 style="font-size:2rem;color:#c8f135;margin-bottom:8px">APEX</h1>
      <h2 style="font-weight:300;margin-bottom:24px">Bienvenue, {name} ! 👋</h2>
      <p style="color:#aaa;line-height:1.7">
        Votre compte a été créé avec succès.<br>
        Découvrez notre catalogue d'accessoires sport & tech et commencez votre première commande.
      </p>
      <a href="https://votre-site.com/boutique"
         style="display:inline-block;margin-top:32px;padding:12px 28px;background:#c8f135;color:#000;font-weight:600;text-decoration:none;border-radius:4px">
        Découvrir la boutique →
      </a>
      <p style="margin-top:40px;color:#555;font-size:0.8rem">© 2025 APEX Sport & Tech</p>
    </div>
    """
    _send(to, subject, html)

def send_order_confirmation(to: str, name: str, order_id: int, total: float):
    subject = f"Confirmation de votre commande #{order_id} ✅"
    html = f"""
    <div style="font-family:sans-serif;max-width:600px;margin:auto;background:#0a0a0a;color:#f0f0f0;padding:40px;border-radius:8px">
      <h1 style="font-size:2rem;color:#c8f135;margin-bottom:8px">APEX</h1>
      <h2 style="font-weight:300;margin-bottom:24px">Merci pour votre commande, {name} !</h2>
      <div style="background:#141414;padding:24px;border-radius:6px;margin-bottom:24px">
        <p style="margin:0;color:#aaa">Numéro de commande</p>
        <p style="margin:4px 0 16px;font-size:1.5rem;font-weight:600">#{order_id}</p>
        <p style="margin:0;color:#aaa">Total</p>
        <p style="margin:4px 0 0;font-size:1.5rem;color:#c8f135;font-weight:600">{total:.2f} €</p>
      </div>
      <p style="color:#aaa;line-height:1.7">
        Votre commande est confirmée et sera expédiée sous 24h.<br>
        Vous recevrez un email de suivi dès l'expédition.
      </p>
      <a href="https://votre-site.com/commandes/{order_id}"
         style="display:inline-block;margin-top:32px;padding:12px 28px;background:#c8f135;color:#000;font-weight:600;text-decoration:none;border-radius:4px">
        Suivre ma commande →
      </a>
      <p style="margin-top:40px;color:#555;font-size:0.8rem">© 2025 APEX Sport & Tech</p>
    </div>
    """
    _send(to, subject, html)
