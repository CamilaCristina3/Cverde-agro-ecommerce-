import json
from datetime import datetime, timezone

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.html import escape

from .models import ChatMessage, ChatRoom


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close(code=4401)
            return

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room = await self._get_room(self.room_name)
        if not self.room:
            await self.close(code=4404)
            return
        self.group_name = f"chat_room_{self.room.id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        messages = await self._get_last_messages(self.room.id, limit=50)
        await self.send(
            text_data=json.dumps(
                {
                    "type": "history",
                    "messages": messages,
                }
            )
        )

        if self.room.name.startswith("secretaria_") and not messages:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "message",
                        "username": "Secretária Coverde",
                        "content": "Olá! Sou a Secretária Virtual da Coverde. Pergunte-me sobre produtos, entregas, pagamentos ou horário de atendimento.",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                )
            )

    async def disconnect(self, close_code):
        if getattr(self, "group_name", None):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close(code=4401)
            return

        try:
            payload = json.loads(text_data or "{}")
        except json.JSONDecodeError:
            return

        message = (payload.get("message") or "").strip()
        if not message:
            return

        if len(message) > 2000:
            message = message[:2000]

        created = await self._create_message(self.room.id, user.id, message)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "username": created["username"],
                "content": created["content"],
                "timestamp": created["timestamp"],
            },
        )

        if self.room.name.startswith("secretaria_"):
            response = self._assistant_response(message)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat.message",
                    "username": "Secretária Coverde",
                    "content": escape(response),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "message",
                    "username": event["username"],
                    "content": event["content"],
                    "timestamp": event["timestamp"],
                }
            )
        )

    @database_sync_to_async
    def _get_room(self, room_name: str) -> ChatRoom:
        try:
            return ChatRoom.objects.get(name=room_name)
        except ChatRoom.DoesNotExist:
            return None

    def _assistant_response(self, message: str) -> str:
        text = message.lower()

        if any(term in text for term in ["olá", "oi", "ola", "bom dia", "boa tarde", "boa noite"]):
            return "Olá! Sou a Secretária Virtual da Coverde. Posso ajudar com horários, entregas, pagamentos ou pedidos de produtos."

        if "horário" in text or "abertura" in text or "horas" in text:
            return "Estamos abertos de segunda a sexta, das 08:00 às 18:00, e aos sábados das 08:00 às 13:00."

        if "entrega" in text or "envio" in text or "frete" in text:
            return "As entregas normalmente são realizadas em 24-48 horas úteis. O custo depende da sua localização e do valor do pedido."

        if "pagamento" in text or "cartão" in text or "mb way" in text or "transferência" in text or "pix" in text:
            return "Aceitamos pagamentos por MB WAY, cartão de crédito/débito e transferência bancária. Se precisar de ajuda para finalizar a compra, posso orientar."

        if "produto" in text or "produtos" in text or "fruta" in text or "legume" in text:
            return "Temos uma seleção de produtos orgânicos e frescos. Diga-me o que procura e eu posso sugerir algo."

        if "onde" in text or "localização" in text or "loja" in text or "endereço" in text:
            return "A Coverde está disponível online, com entrega em várias regiões. Se precisar de informações mais específicas, escreva onde está."

        if "ajuda" in text or "suporte" in text or "atendimento" in text:
            return "Posso ajudar com dúvidas sobre pedidos, pagamento, produtos e taxas de entrega. Em que posso ajudar?"

        return "Desculpe, não entendi. Pode reformular a pergunta?"
    @database_sync_to_async
    def _create_message(self, room_id: int, user_id: int, content: str):
        msg = ChatMessage.objects.create(room_id=room_id, user_id=user_id, content=content)
        timestamp = msg.created_at.astimezone(timezone.utc).isoformat()
        return {
            "username": escape(getattr(msg.user, "username", str(msg.user_id))),
            "content": escape(msg.content),
            "timestamp": timestamp,
        }

    @database_sync_to_async
    def _get_last_messages(self, room_id: int, limit: int = 50):
        qs = (
            ChatMessage.objects.filter(room_id=room_id)
            .select_related("user")
            .order_by("-created_at")[:limit]
        )
        items = []
        for msg in reversed(list(qs)):
            items.append(
                {
                    "username": escape(getattr(msg.user, "username", str(msg.user_id))),
                    "content": escape(msg.content),
                    "timestamp": msg.created_at.astimezone(timezone.utc).isoformat(),
                }
            )
        return items
