import motor.motor_asyncio, asyncio, os
from app.services.model_service import ModelService
from app.repositories.model_repository import ModelRepository
from app.database.models.model import Model
from beanie import init_beanie

async def run():
    db = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGODB_URL', 'mongodb://admin:admin123@mongo:27017/hybrid_qml?authSource=admin'))['hybrid_qml']
    await init_beanie(database=db, document_models=[Model])
    srv = ModelService(ModelRepository())
    res = await srv.seed_default_models()
    print([(str(m.id), m.name) for m in res])
asyncio.run(run())
