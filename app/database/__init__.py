from prisma.client import Prisma

db = Prisma()


async def get_db():
    yield db
