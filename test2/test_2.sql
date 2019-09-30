
-- Original sql query
with event as (
  select
    device_id,
    time_stamp,
    lead(time_stamp) over (partition by device_id order by time_stamp) as next_time_stamp
  from events_table
  where month = '201908'
  and app_id = 1
  and event_id = 4
),
per_event as (
  select
    device_id,
    datediff('second', time_stamp, next_time_stamp) as time_diff
  from
    events
)
select
  device_id,
  avg(time_diff) as avg_per_user
from
  per_event
group by 1
;





-- Adapted query
with per_event as (
    select
        ev.device_id,
        ev.time_stamp,
        min(ev2.time_stamp) next_time_stamp, -- get the minimum time_stamp
        datediff('second', next_time_stamp, ev.time_stamp) time_diff
    
    from
        events_table ev
        left outer join events_table ev2 on 
            ev2.device_id=ev.device_id 
            and ev2.month=ev.month
            and ev2.app_id=ev.app_id
            and ev2.event_id=ev.event_id
            and ev2.time_stamp>ev.time_stamp --key to get the inmediate superior timestamp
    
    where 
        ev.month = '201908'
        and ev.app_id = 1
        and ev.event_id = 4
    
    group by 
      1,2
)
select
  device_id,
  avg(time_diff) as avg_per_user
from
  per_event
group by 1
;



