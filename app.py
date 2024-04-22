from config import config
from nest.core.app import App
from src.facebook.facebook_module import FacebookModule

app = App(
    description="PyNest Service", modules=[FacebookModule], title="Mediahub Application"
)


@app.on_event("startup")
async def startup():
    await config.create_all()
