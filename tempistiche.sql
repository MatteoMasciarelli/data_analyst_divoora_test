WITH PROCESSED_DATA AS (
SELECT 
	order_id,
	departed,
	(julianday(delivered) - julianday(departed))*24*60 AS delivery_time
FROM order_timing
)
SELECT 
	p.order_id,
	departed,
	CASE 
		WHEN delivery_time < 40 THEN '<40 Minutes'
		WHEN delivery_time > 60 THEN '>60 Minutes'
		ELSE 'Between 40 and 60 Minutes'
	END AS delivery_time_cluster,
	CASE 
		WHEN delivery_time <= 90 THEN delivery_time
		ELSE (
			SELECT AVG(delivery_time)
			FROM PROCESSED_DATA
			WHERE delivery_time BETWEEN 60 AND 90
		)
	END AS delivery_time_for_average,
	CASE
            WHEN a.area_id = 1 THEN 'Lugano'
            WHEN a.area_id = 2 THEN 'Locarno'
            WHEN a.area_id = 3 THEN 'Bellinzona'
            ELSE 'Mendrisio'
        END AS area_name
FROM PROCESSED_DATA AS p
	JOIN geo_data AS g ON g.order_id = p.order_id
	JOIN address AS a ON a.driver_id = g.driver_id