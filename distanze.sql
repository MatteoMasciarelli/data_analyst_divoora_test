WITH CLEAN_DATA AS (
	SELECT 
	g.*,
	a.area_id,
	CASE
			WHEN row_number() OVER(PARTITION BY g.shift_id, g.driver_id ORDER BY g.order_id ASC) = 1 THEN a.address_id
			ELSE LAG(g.destination_id,1) OVER (PARTITION BY g.shift_id, g.driver_id ORDER BY g.order_id ASC)
	END AS actual_origin
	FROM geo_data AS g
		JOIN address AS a ON a.driver_id = g.driver_id		
),
DIM_ADDRESS AS (
SELECT DISTINCT 
	address_id, 
	lat,
	lng 
FROM address
UNION
SELECT DISTINCT 
	destination_id,
	lat,
	lng
FROM geo_data
)
SELECT 
		c.order_id,
		c.driver_id,
		c.shift_id,
		c.actual_origin,
		c.pickup_id,
		c.destination_id,
		c.area_id,
        CASE
            WHEN c.area_id = 1 THEN 'Lugano'
            WHEN c.area_id = 2 THEN 'Locarno'
            WHEN c.area_id = 3 THEN 'Bellinzona'
            ELSE 'Mendrisio'
        END AS area_name,
		o.departed,
		c.lat_y AS pickup_lat,
		c.lng_y AS pickup_lng,
		c.lat AS destination_lat,
		c.lng AS destination_lng, 
		a.lat AS origin_lat, 
		a.lng AS origin_lon
FROM CLEAN_DATA AS c
	 JOIN DIM_ADDRESS AS a ON c.actual_origin = a.address_id
	 JOIN order_timing AS o ON o.order_id = c.order_id		