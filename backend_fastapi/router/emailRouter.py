import os

from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from backend_fastapi.schema.emailSchema import ContactForm

load_dotenv('.env')


class Envs:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_SERVER = os.getenv('MAIL_SERVER')


conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_PORT=587,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


router = APIRouter()


@router.post('/email')
async def simple_send(form: ContactForm, background_tasks: BackgroundTasks):
    html = f"""
        <h3>Nova mensagem de contato</h3>
        <p><strong>Nome:</strong> {form.nome}</p>
        <p><strong>Email:</strong> {form.email}</p>
        <p><strong>Mensagem:</strong><br>{form.menssagem}</p>
        """

    message = MessageSchema(subject='Contato via site', recipients=[Envs.MAIL_USERNAME], body=html, subtype=MessageType.html)

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
    return JSONResponse(status_code=200, content={'message': 'Mensagem enviada com sucesso!'})
