import logging
import json
import zmq

from src.core.config import Config

config = Config()


def send_mail(subject: str, text: str):
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.connect(f"tcp://{config.MAIL_STORM_SERVER}:{config.MAIL_STORM_PORT}")

    message = {
        "to": f"{config.MAIL_STORM_TO}",
        "subject": subject,
        "template": "dev-alert",
        "arg": {
            "content": text,
            "title": "Image Server"
        },
        "who": "image"
    }
    request = json.dumps(message, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)
    zmq_socket.send_json(request)
    logging.info("Send Mail to MailStorm Server.")
