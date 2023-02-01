/*
This query returns regions in which the datasource "cheap_mobile" appeared
*/

select distinct region
from trips
where datasource = 'cheap_mobile'
