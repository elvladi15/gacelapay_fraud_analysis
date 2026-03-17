SELECT
	CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), ID, REPEAT(' ', CAST(floor(random() * 9) AS int)))	AS ID,
	CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), CUSTOMER_ID, REPEAT(' ', CAST(floor(random() * 9) AS int)))	AS CUSTOMER_ID,
	CASE
		WHEN TYPE = 'checking' THEN
			CASE CAST(FLOOR(random() * (2 - 1 + 1)) + 1 AS int)
				WHEN 1 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'checking', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				WHEN 2 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'CHECKING', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				ELSE CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'CH', REPEAT(' ', CAST(floor(random() * 9) AS int)))
			END

		WHEN TYPE = 'credit' THEN
			CASE CAST(FLOOR(random() * (2 - 1 + 1)) + 1 AS int)
				WHEN 1 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'credit', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				WHEN 2 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'CREDIT', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				ELSE CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'CR', REPEAT(' ', CAST(floor(random() * 9) AS int)))
			END

		WHEN TYPE = 'savings' THEN
			CASE CAST(FLOOR(random() * (2 - 1 + 1)) + 1 AS int)
				WHEN 1 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'savings', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				WHEN 2 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'SAVINGS', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				ELSE CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'S', REPEAT(' ', CAST(floor(random() * 9) AS int)))
			END

		WHEN TYPE = 'virtual_wallet' THEN
			CASE CAST(FLOOR(random() * (2 - 1 + 1)) + 1 AS int)
				WHEN 1 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'virtual_wallet', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				WHEN 2 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'VIRTUAL_WALLET', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				ELSE CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'VW', REPEAT(' ', CAST(floor(random() * 9) AS int)))
			END

		WHEN TYPE = 'wallet' THEN
			CASE CAST(FLOOR(random() * (2 - 1 + 1)) + 1 AS int)
				WHEN 1 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'wallet', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				WHEN 2 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'WALLET', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				ELSE CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'W', REPEAT(' ', CAST(floor(random() * 9) AS int)))
			END
		ELSE TYPE
	END	AS TYPE,
	
	CASE
		WHEN CURRENCY = 'BRL' THEN
			CASE CAST(FLOOR(random() * (3 - 1 + 1)) + 1 AS int)
				WHEN 1 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'brl', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				WHEN 2 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), '$R', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				WHEN 3 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'REAL', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				ELSE CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'BRL', REPEAT(' ', CAST(floor(random() * 9) AS int)))
			END

		WHEN CURRENCY = 'EUR' THEN
			CASE CAST(FLOOR(random() * (2 - 1 + 1)) + 1 AS int)
				WHEN 1 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'eur', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				WHEN 2 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'EUR', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				ELSE CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'EURO', REPEAT(' ', CAST(floor(random() * 9) AS int)))
			END

		WHEN CURRENCY = 'GBP' THEN
			CASE CAST(FLOOR(random() * (2 - 1 + 1)) + 1 AS int)
				WHEN 1 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'gbp', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				WHEN 2 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'pound sterling', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				ELSE CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'GBP', REPEAT(' ', CAST(floor(random() * 9) AS int)))
			END

		WHEN CURRENCY = 'MXN' THEN
			CASE CAST(FLOOR(random() * (3 - 1 + 1)) + 1 AS int)
				WHEN 1 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'mxn', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				WHEN 2 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'MXN', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				WHEN 3 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'MEX', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				ELSE CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'MEXICAN_PESO', REPEAT(' ', CAST(floor(random() * 9) AS int)))
			END

		WHEN CURRENCY = 'USD' THEN
			CASE CAST(FLOOR(random() * (3 - 1 + 1)) + 1 AS int)
				WHEN 1 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'usd', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				WHEN 2 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'USD', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				WHEN 3 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'us_dollar', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				ELSE CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), '$US', REPEAT(' ', CAST(floor(random() * 9) AS int)))
			END
		ELSE CURRENCY
	END	AS CURRENCY,

	CASE CAST(FLOOR(random() * (2 - 1 + 1)) + 1 AS int)
		WHEN 1 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), CONCAT('"', CASE BALANCE WHEN 0 THEN 0 ELSE BALANCE + RANDOM() END, '"'), REPEAT(' ', CAST(floor(random() * 9) AS int)))
		WHEN 2 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), CONCAT('''', CASE BALANCE WHEN 0 THEN 0 ELSE BALANCE + RANDOM() END, ''''), REPEAT(' ', CAST(floor(random() * 9) AS int)))
		ELSE CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), CONCAT('$', CASE BALANCE WHEN 0 THEN 0 ELSE BALANCE + RANDOM() END), REPEAT(' ', CAST(floor(random() * 9) AS int)))
	END AS BALANCE,

	CASE CAST(FLOOR(random() * (2 - 1 + 1)) + 1 AS int)
		WHEN 1 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), CONCAT('"', CAST(STRFTIME(OPEN_DATE, '%m/%d/%Y') AS varchar), '"'), REPEAT(' ', CAST(floor(random() * 9) AS int)))
		WHEN 2 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), CONCAT('"', CAST(STRFTIME(OPEN_DATE, '%Y-%m-%d') AS varchar), '"'), REPEAT(' ', CAST(floor(random() * 9) AS int)))
		ELSE CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), CONCAT('"', CAST(STRFTIME(OPEN_DATE, '%d-%m-%Y') AS varchar), '"'), REPEAT(' ', CAST(floor(random() * 9) AS int)))
	END	AS OPEN_DATE,

	CASE
		WHEN STATUS = 'Active' THEN
			CASE CAST(FLOOR(random() * (2 - 1 + 1)) + 1 AS int)
				WHEN 1 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'Active', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				WHEN 2 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'ACTIVE', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				ELSE CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'A', REPEAT(' ', CAST(floor(random() * 9) AS int)))
			END

		WHEN STATUS = 'Inactive' THEN
			CASE CAST(FLOOR(random() * (2 - 1 + 1)) + 1 AS int)
				WHEN 1 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'Inactive', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				WHEN 2 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'INACTIVE', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				ELSE CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'I', REPEAT(' ', CAST(floor(random() * 9) AS int)))
			END

		WHEN STATUS = 'Blocked' THEN
			CASE CAST(FLOOR(random() * (2 - 1 + 1)) + 1 AS int)
				WHEN 1 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'Blocked', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				WHEN 2 THEN CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'BLOCKED', REPEAT(' ', CAST(floor(random() * 9) AS int)))
				ELSE CONCAT(REPEAT(' ', CAST(floor(random() * 9) AS int)), 'B', REPEAT(' ', CAST(floor(random() * 9) AS int)))
			END
		ELSE STATUS
	END	AS STATUS
FROM
	'misc/STEP_2/accounts.csv'