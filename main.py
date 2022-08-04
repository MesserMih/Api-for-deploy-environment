import core.models.model
from core.models.database import Base, engine
import uvicorn
from sqlalchemy_utils import database_exists, create_database

if not database_exists(engine.url):
    create_database(engine.url)
Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run("api.api:app", host="0.0.0.0", port=8000, reload=True)
