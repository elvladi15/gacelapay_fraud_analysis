SELECT
	ID,
	DAY(DATE)	AS BUCKET
FROM
	data_source_to_analyze_iv