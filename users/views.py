from fastapi import Request
from ..main import templates

async def login_view(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context={"id": 1}
    )