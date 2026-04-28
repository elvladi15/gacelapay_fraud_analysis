SELECT
	ID,
	EXTRACT('hour' FROM TIME::TIME)	AS BUCKET,
FROM
	joined_tables_for_analysis