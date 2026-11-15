import motor.motor_asyncio, asyncio, os
async def run():
    db = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGODB_URL', 'mongodb://admin:admin123@localhost:27017'))['hybrid_qml']
    models = await db.models.find().to_list(100)
    print([(str(m.get('_id')), m.get('name'), m.get('model_type'), m.get('is_default')) for m in models])
asyncio.run(run())
