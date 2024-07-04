SELECT count(*) 
FROM sent
WHERE time_sent >= (CURRENT_TIMESTAMP - INTERVAL '1 day');