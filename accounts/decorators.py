from aiohttp import web

from core.utils import redirect


def login_required(func):
    """ Allow only auth user """

    async def wrapper(self, *args, **kwargs):
        if not self.request.user:
            redirect(self.request, 'login')
        
        return await func(self, *args, **kwargs)
    
    return wrapper


def anonymous_required(func):
    """ Allow anonymous user """

    async def wrapper(self, *args, **kwargs):
        if self.request.user:
            redirect(self.request, 'home')
        
        return await func(self, *args, **kwargs)
    return wrapper