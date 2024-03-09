from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

class DataBaseHelper:
    def __init__(self, url, echo):
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
            autocommit=False
        )


db_helper = DataBaseHelper(url="sqlite+aiosqlite:///test.db", echo=True)
