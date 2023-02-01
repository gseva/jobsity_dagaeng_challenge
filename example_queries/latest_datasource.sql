/*
This query returns the latest datasource (by datetime) from the two
most common regions.

distinct on is a postgres feature, in other databases it can be solved
using row_number() window function.
*/

with two_most_common_regions as (
    select
        region
    from trips
    group by region
    order by count(*) desc
    limit 2
)

select distinct on (region)
    region,
    datasource
from trips
where region in (select region from two_most_common_regions)
order by region, datetime desc
