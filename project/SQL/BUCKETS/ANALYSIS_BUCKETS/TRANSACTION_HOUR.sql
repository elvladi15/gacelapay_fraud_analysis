SELECT
	ID,
	EXTRACT('hour' FROM TIME::TIME)	AS BUCKET,
FROM
	data_source_to_analyze_iv