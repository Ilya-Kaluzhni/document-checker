from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.api.checks import router as checks_router

app = FastAPI(
    title="Document Checker API",
    version="1.0.0",
    openapi_version="3.0.3"
)

# Фикс схемы для корректной загрузки файлов через docs
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    schema["openapi"] = "3.0.3"

    files_schema = (
        schema["components"]
        ["schemas"]
        ["Body_create_check_api_checks_post"]
        ["properties"]
        ["files"]
        ["items"]
    )

    files_schema.pop("contentMediaType", None)
    files_schema["format"] = "binary"

    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi

app.include_router(
    checks_router
)

@app.get("/health")
def health():
    return {"status": "ok"}