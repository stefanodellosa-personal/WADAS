import random
import string
from typing import List, Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from telegram_client import TelegramClient

database = {"2a6d4cd8-8832-458f-bf3b-c3febfa3c33a": []}

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.server = None


def generate_random_string(length=16):
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choices(characters, k=length))
    return random_string


class Organization(BaseModel):
    org_code: str


class User(BaseModel):
    user_id: str


class TelegramNotification(BaseModel):
    org_code: str
    user_ids: List[str]
    message: str
    image_b64: Optional[str] = None


class NotificationAck(BaseModel):
    org_code: str
    user_ids: List[str]
    status: str
    error_msgs: List[str]


@app.post("/api/v1/telegram/users")
async def create_user(organization: Organization):
    if organization.org_code in database:
        user_id = generate_random_string()
        database[organization.org_code].append(user_id)
        return User(user_id=user_id)
    else:
        print(f"organization: {organization.org_code} not found")
        raise HTTPException(status_code=404, detail="Organization does not exist")


@app.get("/api/v1/telegram/users")
async def get_users(org_code: str):
    if org_code in database:
        return database[org_code]
    else:
        print(f"organization: {org_code} not found")
        raise HTTPException(status_code=404, detail="Organization does not exist")


@app.delete("/api/v1/telegram/users", status_code=status.HTTP_204_NO_CONTENT)
async def del_user(org_code: str, user_id: str):
    if org_code in database and user_id in database[org_code]:
        database[org_code].remove(user_id)
        return
    else:
        raise HTTPException(status_code=404, detail="Organization or user not found")


@app.post("/api/v1/telegram/notifications")
async def send_notification(notification: TelegramNotification):
    tg_client: TelegramClient = app.server.telegram_client
    error_str_list = []
    valid_user_ids = []
    if notification.org_code in database:
        for user_id in notification.user_ids:
            if user_id in database[notification.org_code]:
                if tg_client.is_user_registered(user_id):
                    valid_user_ids.append(user_id)
                else:
                    error_str_list.append(f"{user_id} not yet registered via Telegram bot")
            else:
                error_str_list.append(f"{user_id} not found")

        if len(valid_user_ids) > 0:
            print(f"send notification to {valid_user_ids}: {notification.message}")
            await tg_client.send_notifications(
                valid_user_ids, notification.message, image_b64=notification.image_b64
            )

        status = "ok"
        if len(error_str_list) > 0:
            status = "error"
        return NotificationAck(
            org_code=notification.org_code,
            user_ids=notification.user_ids,
            status=status,
            error_msgs=error_str_list,
        )
    else:
        print("organization or user not found")
        raise HTTPException(status_code=404, detail="Organization or user does not exist")
