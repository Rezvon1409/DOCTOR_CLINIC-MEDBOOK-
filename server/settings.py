from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import timedelta
from dotenv import load_dotenv
from pathlib import Path
import os

# Директорияи асосии лоиҳа
BASE_DIR = Path(__file__).resolve().parent.parent

# Бор кардани муҳити кор аз .env бо кодинги дуруст
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(env_path, encoding='utf-8-sig')
else:
    print(f"Warning: .env file not found at {env_path}")

# SQLite барои соддагӣ; дар production PostgreSQL ё MySQL истифода кунед
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./clinic_tj.db")

# Эҷоди движак (барои пайвастшавӣ ба базаи додаҳо)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal як фабрика барои сессияҳои базаи додаҳо аст
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Барои debugging, маълумоти .env-ро чоп кунем
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

print(f"=== DEBUG ===")
print(f"JWT_SECRET_KEY from env: {repr(JWT_SECRET_KEY)}")
print(f"JWT_ALGORITHM from env: {repr(JWT_ALGORITHM)}")
print(f"DATABASE_URL from env: {repr(os.getenv('DATABASE_URL'))}")
print(f"=== END DEBUG ===")

ACCESSTOKEN_EXPIRED_TIME = timedelta(minutes=15)
REFRESHTOKEN_EXPIRED_TIME = timedelta(days=7)
