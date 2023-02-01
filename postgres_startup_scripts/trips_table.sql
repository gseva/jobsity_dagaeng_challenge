
CREATE EXTENSION postgis;

CREATE TABLE IF NOT EXISTS trips (
  region TEXT,
  origin GEOMETRY,
  destination GEOMETRY,
  datetime TIMESTAMP,
  datasource TEXT
);


CREATE VIEW trips_by_time_of_day_view AS
select
    extract(hour from datetime) as hour,
    (extract(minute from datetime)::int / 15) * 15 as minute_bucket,
    region,
    datasource,
    count(*)
from trips
group by 1, 2, 3, 4
;
