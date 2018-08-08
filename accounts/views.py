from aiohttp import web

import aiohttp_jinja2

from core.routes import routes
from core.utils import redirect

from .forms import SignUpForm, LogInForm
from .models import User
from .utils import encrypt_password, verify_password, login_user, logout
from .decorators import login_required

routes_prefix = '/accounts'


@routes.view(f'{routes_prefix}/signup/', name='signup')
class SignUp(web.View):
    """
    View for register users
    """
    template = 'accounts/signup.html'

    @aiohttp_jinja2.template(template)
    async def post(self):
        data = await self.request.post()
        form = SignUpForm(data)
        if form.validate():
            return await self.form_valid(form)
        return await self.form_invalid(form)
    
    @aiohttp_jinja2.template(template)
    async def get(self):
        form = SignUpForm()
        return {'form': form}
    
    async def form_valid(self, form):
        password = encrypt_password(form.password.data)
        await User.create(
            username=form.username.data,
            email=form.email.data,
            password=password
        )
        redirect(self.request, 'login')
    
    async def form_invalid(self, form):
        print('form invalid')
        return {'form': form}


@routes.view(f'{routes_prefix}/login/', name='login')
class SignIn(web.View):
    """ 
    View for login users 
    """

    template = 'accounts/signin.html'

    @aiohttp_jinja2.template(template)
    async def post(self):
        data = await self.request.post()
        form = LogInForm(data)
        if form.validate():
            return await self.form_valid(form)
        return await self.form_invalid(form)
    
    @aiohttp_jinja2.template(template)
    async def get(self):
        form = LogInForm()
        # print(self.request.session)
        return {'form': form}
    
    async def form_valid(self, form):
        password = form.password.data
        email = form.email.data

        user = await User.query.where(User.email == email).gino.first()
        if not user or not verify_password(password, user.password):
            return {'form': form, 'error_msg': 'Email or password is incorect'}
        login_user(self.request, user)
        redirect(self.request, 'home')
        
    
    async def form_invalid(self, form):
        return {'form': form}


@routes.view(f'{routes_prefix}/logout/')
class LogOut(web.View):
    """
    Views for logout user
    """
    @login_required
    async def get(self):
        logout(self.request)
        redirect(self.request, 'login')


@routes.view(f'/', name='home')
class Index(web.View):
    template = 'index.html'

    @login_required
    @aiohttp_jinja2.template(template)
    async def get(self):
        return {'user': self.request.user}