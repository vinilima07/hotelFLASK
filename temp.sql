--lista quartos
SELECT id_quarto, nu_quarto, tipo, nome_hotel, nu_preco_diaria, nome_temporada FROM
	(SELECT * FROM quarto
	NATURAL JOIN 
		(SELECT * FROM hotel
		NATURAL JOIN preco_temporada) hp
	) qh
NATURAL JOIN
	(SELECT * FROM quarto
	NATURAL JOIN tipo_quarto) qp;

--lista hoteis com precos por temporada
SELECT (id_hotel, nome_hotel, nu_preco_diaria, nome_temporada) FROM hotel
NATURAL JOIN preco_temporada;