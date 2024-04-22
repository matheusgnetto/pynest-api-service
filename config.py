from nest.core.database.orm_provider import AsyncOrmProvider
import json

from secrets.get_token import AURORA, get_secret

config = AsyncOrmProvider(
    db_type="postgresql",
    config_params=dict(
        host=json.loads(get_secret(AURORA))['host'],
        db_name=json.loads(get_secret(AURORA))['dbname'],
        user=json.loads(get_secret(AURORA))['username'],
        password=json.loads(get_secret(AURORA))['password'],
        port=json.loads(get_secret(AURORA))['port']
    )
)
