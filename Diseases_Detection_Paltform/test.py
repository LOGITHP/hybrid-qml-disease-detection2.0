import motor.motor_asyncio, asyncio, os
async def run():
    db = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGODB_URL'))['hybrid_qml']
    models = await db.models.find().to_list(100)
    for m in models: print(str(m.get('_id')), m.get('name'), m.get('model_type'), m.get('is_default'))
asyncio.run(run())
