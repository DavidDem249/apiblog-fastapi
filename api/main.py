from fastapi import FastAPI
from .routes import users, auth, password_reset, blog_content

app = FastAPI()


app.include_router(router=users.router)
app.include_router(router=auth.router)
app.include_router(router=password_reset.router)
app.include_router(router=blog_content.router)
