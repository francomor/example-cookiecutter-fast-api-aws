from alembic import autogenerate
from alembic.operations import ops
from sqlalchemy import MetaData, Table, create_engine

rds_server = 'server.aws-region.rds.amazonaws.com'
rds_user = 'user'
rds_password = 'password'
rds_db = 'db_name'
engine = create_engine(f"mysql+pymysql://{rds_user}:{rds_password}@{rds_server}/{rds_db}")

with engine.connect() as conn:
    m = MetaData()
    fake_table = Table('Fake', m, autoload_with=conn)
    second_table = Table('second', m, autoload_with=conn)

print(autogenerate.render_python_code(
    ops.UpgradeOps(
        ops=[
            ops.CreateTableOp.from_table(table) for table in m.tables.values()
        ] + [
            ops.CreateIndexOp.from_index(idx) for table in m.tables.values()
            for idx in table.indexes
        ]
    ))
)
