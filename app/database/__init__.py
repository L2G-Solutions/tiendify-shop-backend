from prisma.client import Prisma

db = Prisma(auto_register=True)


async def get_db():
    yield db
