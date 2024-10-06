from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends
from app.chat.dao import MessagesDAO
from app.chat.schemas import MessageCreate, MessageRead
from app.users.dao import UsersDAO
from app.users.dependensies import get_current_user
from app.users.models import User
import asyncio


router = APIRouter(prefix='/chat', tags=['Chat'])
active_connections: dict[int, WebSocket] = {}


# HTTP

@router.get('/', summary='Chat Page')
async def get_chat_page(request: Request, user_data: User = Depends(get_current_user)):
    users_all = await UsersDAO.find_all()
    return {"request": request, "user": user_data, 'users_all': users_all}



@router.get("/messages/{user_id}", response_model=list[MessageRead])
async def get_messages(user_id: int, current_user: User = Depends(get_current_user)):
    return await MessagesDAO.get_messages_between_users(user_id_1=user_id, user_id_2=current_user.id) or []


@router.post("/messages", response_model=MessageCreate)
async def send_message(message: MessageCreate, current_user: User = Depends(get_current_user)):
    await MessagesDAO.add(
        sender_id=current_user.id,
        content=message.content,
        recipient_id=message.recipient_id
    )
    message_data = {
        'sender_id': current_user.id,
        'recipient_id': message.recipient_id,
        'content': message.content,
    }

    await notify_user(message.recipient_id, message_data)
    await notify_user(current_user.id, message_data)

    return {'recipient_id': message.recipient_id, 'content': message.content, 'status': 'ok', 'msg': 'Message saved!'}


# WebSocket

async def notify_user(user_id: int, message: dict):
    """Отправить сообщение пользователю, если он подключен."""
    if user_id in active_connections:
        websocket = active_connections[user_id]
        await websocket.send_json(message)


@router.websocket('/ws/{user_id}')
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections[user_id] = websocket
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        active_connections.pop(user_id, None)