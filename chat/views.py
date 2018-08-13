from datetime import datetime

from aiohttp import web, WSMsgType

import aiohttp_jinja2

from core.routes import routes
from core.cbv import FormView
from core.utils import redirect
from accounts.models import User
from accounts.decorators import login_required

from .forms import ChatCreateForm
from .models import Room, Message


routes_prefix = '/chat'


@routes.view(f'{routes_prefix}/create_room')
class CreateRoom(FormView):

    template = 'chat/create_room.html'
    form_class = ChatCreateForm

    @login_required
    async def get(self):
        return await super().get()

    @login_required
    async def post(self):
        return await super().post()

    async def form_valid(self, form):
        name = form.name.data
        room = await Room.create(name=name, created_date=datetime.now())
        raise web.HTTPFound(f'/chat/{room.id}')



@routes.view(r'%s/{chat_id:\d+}' % routes_prefix)
class RoomDetailView(web.View):

    template = 'chat/detail_room.html'

    @login_required
    @aiohttp_jinja2.template(template)
    async def get(self):
        chat_id = self.request.match_info.get('chat_id')
        room = await Room.get(int(chat_id))
        if not room:
            raise web.HTTPNotFound(reason='Room with id #%s not found' % chat_id)
        
        return {'room': room}
        



@routes.view(r'%s/ws/{chat_id:\d+}' % routes_prefix, name='ws')
class RoomWebSocket(web.View):
    async def get(self):

        chat_id = self.request.match_info.get('chat_id')
        room = await Room.get(int(chat_id))

        if not room:
            raise web.HTTPNotFound(reason='Room with id #%s not found' % chat_id)

        print(room)
        self.room = room
        user = self.request.user
        app = self.request.app

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        if self.room.id not in app.wslist:
            app.wslist[self.room.id] = {}
        
        app.wslist[self.room.id][user.username] = ws
        
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                print(msg)
                if msg.data == 'close':
                    await ws.close()
                else:
                    text = msg.data.strip()
                    print(text)
                    message = await Message.create(
                        user_id=user.id,
                        room_id=room.id,
                        text=text,
                        created_date = datetime.now()
                    )
                    message.user = user
                    await self.broadcast(message)
        
        await self.disconnect(user.username, ws)
        
    
    async def broadcast(self, message):
        """ Send messages to all in this room """
        for peer in self.request.app.wslist[self.room.id].values():
            await peer.send_json({'text': message.text, 'username': message.user.username, 'time':str(message.created_date)})

    async def disconnect(self, username, socket, silent=False):
        """ Close connection and notify broadcast """
        app = self.request.app
        app.wslist.pop(username, None)
        if not socket.closed:
            await socket.close()
        if silent:
            return
        