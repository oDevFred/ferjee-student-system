from app.database import Base, engine
from app.models.student import Student  # Importar o modelo explicitamente

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()