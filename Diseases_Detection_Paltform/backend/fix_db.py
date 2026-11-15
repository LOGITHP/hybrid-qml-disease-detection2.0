import asyncio
import motor.motor_asyncio

async def update():
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://mongodb:27017')
    db = client['hybrid_qml_db']
    async for doc in db.models.find():
        new_desc = doc.get('description', '').replace('uploaded dataset version', 'Lung Cancer Survey dataset')
        await db.models.update_one({'_id': doc['_id']}, {'$set': {'description': new_desc}})
    print('Updated existing models')

if __name__ == '__main__':
    asyncio.run(update())
