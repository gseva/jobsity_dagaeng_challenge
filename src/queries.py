

TEMPORARY_TABLE_STATEMENT = '''
create temporary table temp_trips (
  region TEXT,
  origin TEXT,
  destination TEXT,
  datetime TIMESTAMP,
  datasource TEXT
)
'''

COPY_STATEMENT = '''
copy temp_trips (region, origin, destination, datetime, datasource)
from stdin with delimiter ',' header
'''

INSERT_STATEMENT = '''
with rows as (
    insert into trips
    select region, ST_PointFromText(origin), ST_PointFromText(destination), datetime, datasource
    from temp_trips
    returning 1
)
select count(*) from rows
'''

WEEKLY_AVG_BY_REGION_QUERY = '''
select
    round(avg(cnt), 2) as weekly_average
from (
    select
        count(*) as cnt
    from trips
    where region = %s
    group by date_trunc('week', datetime)
) s
'''

WEEKLY_AVG_BY_BOUNDING_BOX_QUERY = '''
select
    round(avg(cnt), 2) as weekly_average
from (
    select
        count(*) as cnt
    from trips
    where ST_MakeLine(origin, destination) @
        ST_MakeEnvelope(%s, %s, %s, %s)
    group by date_trunc('week', datetime)
) s
'''
