from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Chuẩn hoá URL kết nối cho asyncpg và Supabase Pooler
db_url = settings.DATABASE_URL
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
if "sslmode=require" in db_url:
    db_url = db_url.replace("sslmode=require", "ssl=require")

# Khi kết nối qua Supabase Connection Pooler (Supavisor / PgBouncer cổng 6543),
# cần tắt statement cache để tránh xung đột prepared statements giữa các phiên kết nối.
connect_args = {}
if "pooler.supabase.com" in db_url or ":6543" in db_url:
    connect_args["statement_cache_size"] = 0

engine = create_async_engine(
    db_url,
    echo=settings.DEBUG,
    connect_args=connect_args,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_tables():
    """
    Kiểm tra kết nối database khi server khởi động.

    QUAN TRỌNG: Các bảng được tạo thông qua schema.sql (chạy setup_db.ps1)
    và quản lý migrations bằng Alembic.
    KHÔNG dùng Base.metadata.create_all() vì schema.sql có các tính năng
    PostgreSQL-native (ENUM types, triggers, GENERATED columns) mà
    SQLAlchemy create_all không thể tái tạo chính xác.
    """
    from sqlalchemy import text
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'"))
            count = result.scalar()
            print(f"[OK] Ket noi PostgreSQL thanh cong - {count} bang dang hoat dong trong database.")
    except Exception as e:
        print(f"[ERROR] Khong the ket noi den PostgreSQL: {e}")
        raise e
