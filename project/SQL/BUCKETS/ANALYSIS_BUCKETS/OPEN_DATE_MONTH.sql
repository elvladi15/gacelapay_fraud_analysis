SELECT
	ID,
	MONTH(OPEN_DATE)	AS BUCKET
FROM
	joined_tables_for_analysis