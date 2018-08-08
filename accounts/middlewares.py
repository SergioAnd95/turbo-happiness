from aiohttp import web

from aiohttp_session import get_session

from .models import User


@web.middleware
async def request_user_middleware(request, handler):
    request.session = await get_session(request)
    request.user = None

    user_id = request.session.get('user')
    if user_id:
        user = await User.get(user_id)
        if not user:
            request.session.remove('user')
        request.user = user
    return await handler(request)
