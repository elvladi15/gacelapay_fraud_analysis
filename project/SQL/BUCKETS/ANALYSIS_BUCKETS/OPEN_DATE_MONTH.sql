SELECT
	ID,
	MONTH(OPEN_DATE)	AS BUCKET
FROM
	data_source_to_analyze_iv