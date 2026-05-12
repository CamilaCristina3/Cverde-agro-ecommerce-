from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views.decorators.http import require_http_methods

from .models import ChatRoom


@login_required
def chat_index(request):
    rooms = ChatRoom.objects.all()
    return render(request, "chat/index.html", {"rooms": rooms})


@login_required
@require_http_methods(["POST"])
def chat_create_room(request):
    raw_name = (request.POST.get("name") or "").strip()
    raw_title = (request.POST.get("title") or "").strip()
    slug = slugify(raw_name)[:64]
    if not slug:
        return redirect("chat:index")
    room, _ = ChatRoom.objects.get_or_create(name=slug, defaults={"title": raw_title})
    return redirect("chat:room", room_name=room.name)


@login_required
def chat_room(request, room_name: str):
    room = get_object_or_404(ChatRoom, name=room_name)
    return render(request, "chat/room.html", {"room": room})


@login_required
def chat_assistant(request):
    room_name = f"secretaria_{request.user.id}"
    room, _ = ChatRoom.objects.get_or_create(
        name=room_name,
        defaults={"title": "Secretária Virtual"},
    )
    return render(request, "chat/assistant.html", {"room": room})

