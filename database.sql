-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.9.1-beta
-- PostgreSQL version: 10.0
-- Project Site: pgmodeler.com.br
-- Model Author: ---


-- Database creation must be done outside an multicommand file.
-- These commands were put in this file only for convenience.
-- -- object: new_database | type: DATABASE --
-- -- DROP DATABASE IF EXISTS new_database;
-- CREATE DATABASE new_database
-- ;
-- -- ddl-end --
--

-- object: public.quarto | type: TABLE --
-- DROP TABLE IF EXISTS public.quarto CASCADE;
CREATE TABLE public.quarto(
	id_quarto serial NOT NULL,
	id_hotel integer NOT NULL,
	id_tipo_quarto integer NOT NULL,
	nu_quarto smallint,
	CONSTRAINT pk_quarto PRIMARY KEY (id_quarto)

);
-- ddl-end --
ALTER TABLE public.quarto OWNER TO postgres;
-- ddl-end --

-- object: public.hotel | type: TABLE --
-- DROP TABLE IF EXISTS public.hotel CASCADE;
CREATE TABLE public.hotel(
	id_hotel serial NOT NULL,
	nome_hotel varchar,
	id_preco_temporada integer NOT NULL,
	cidade varchar,
	CONSTRAINT pk_hotel PRIMARY KEY (id_hotel)

);
-- ddl-end --
ALTER TABLE public.hotel OWNER TO postgres;
-- ddl-end --

-- object: public.tipo_quarto | type: TABLE --
-- DROP TABLE IF EXISTS public.tipo_quarto CASCADE;
CREATE TABLE public.tipo_quarto(
	id_tipo serial NOT NULL,
	tipo varchar,
	CONSTRAINT pk_tipo_quarto PRIMARY KEY (id_tipo)
);
-- ddl-end --
ALTER TABLE public.tipo_quarto OWNER TO postgres;
-- ddl-end --

-- object: public.preco_temporada | type: TABLE --
-- DROP TABLE IF EXISTS public.preco_temporada CASCADE;
CREATE TABLE public.preco_temporada(
	id_preco_temporada serial NOT NULL,
	nu_preco_diaria double precision,
	nome_temporada varchar,
	CONSTRAINT pk_preco_diaria PRIMARY KEY (id_preco_temporada)

);
-- ddl-end --
ALTER TABLE public.preco_temporada OWNER TO postgres;
-- ddl-end --

-- object: hotel_fk | type: CONSTRAINT --
-- ALTER TABLE public.quarto DROP CONSTRAINT IF EXISTS hotel_fk CASCADE;
ALTER TABLE public.quarto ADD CONSTRAINT hotel_fk FOREIGN KEY (id_hotel)
REFERENCES public.hotel (id_hotel) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: tipo_quarto_fk | type: CONSTRAINT --
-- ALTER TABLE public.quarto DROP CONSTRAINT IF EXISTS tipo_quarto_fk CASCADE;
ALTER TABLE public.quarto ADD CONSTRAINT tipo_quarto_fk FOREIGN KEY (id_tipo_quarto)
REFERENCES public.tipo_quarto (id_tipo) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: preco_temporada_fk | type: CONSTRAINT --
-- ALTER TABLE public.hotel DROP CONSTRAINT IF EXISTS preco_temporada_fk CASCADE;
ALTER TABLE public.hotel ADD CONSTRAINT preco_temporada_fk FOREIGN KEY (id_preco_temporada)
REFERENCES public.preco_temporada (id_preco_temporada) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --


-- object: public.reserva_hotel | type: TABLE --
-- DROP TABLE IF EXISTS public.reserva_hotel CASCADE;
CREATE TABLE public.reserva_hotel(
	dt_inicio date DEFAULT now(),
	dt_fim date DEFAULT now(),
	id_reserva_hotel serial NOT NULL,
	id_quarto_quarto integer NOT NULL,
	CONSTRAINT pk_reserva_hotel PRIMARY KEY (id_reserva_hotel)

);
-- ddl-end --
ALTER TABLE public.reserva_hotel OWNER TO postgres;
-- ddl-end --

-- object: quarto_fk | type: CONSTRAINT --
-- ALTER TABLE public.reserva_hotel DROP CONSTRAINT IF EXISTS quarto_fk CASCADE;
ALTER TABLE public.reserva_hotel ADD CONSTRAINT quarto_fk FOREIGN KEY (id_quarto_quarto)
REFERENCES public.quarto (id_quarto) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.reserva_pacote | type: TABLE --
-- DROP TABLE IF EXISTS public.reserva_pacote CASCADE;
CREATE TABLE public.reserva_pacote(
	id_reserva_hotel_reserva_hotel integer NOT NULL,
	id_reserva_carro integer
);
-- ddl-end --
ALTER TABLE public.reserva_pacote OWNER TO postgres;
-- ddl-end --

-- object: reserva_hotel_fk | type: CONSTRAINT --
-- ALTER TABLE public.reserva_pacote DROP CONSTRAINT IF EXISTS reserva_hotel_fk CASCADE;
ALTER TABLE public.reserva_pacote ADD CONSTRAINT reserva_hotel_fk FOREIGN KEY (id_reserva_hotel_reserva_hotel)
REFERENCES public.reserva_hotel (id_reserva_hotel) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: reserva_pacote_uq | type: CONSTRAINT --
-- ALTER TABLE public.reserva_pacote DROP CONSTRAINT IF EXISTS reserva_pacote_uq CASCADE;
ALTER TABLE public.reserva_pacote ADD CONSTRAINT reserva_pacote_uq UNIQUE (id_reserva_hotel_reserva_hotel);
-- ddl-end --

--manual insertions

INSERT INTO preco_temporada (nu_preco_diaria, nome_temporada) VALUES(999.9, 'inverno');
INSERT INTO preco_temporada (nu_preco_diaria, nome_temporada) VALUES(1999.9, 'verão');

INSERT INTO hotel (id_preco_temporada, nome_hotel) VALUES(1, 'Mil Maravilhas');
INSERT INTO hotel (id_preco_temporada, nome_hotel) VALUES(2, 'Midland');
INSERT INTO hotel (id_preco_temporada, nome_hotel) VALUES(1, 'Paukimia');
INSERT INTO hotel (id_preco_temporada, nome_hotel) VALUES(1, 'Nascero Branco');
INSERT INTO hotel (id_preco_temporada, nome_hotel) VALUES(2, 'Ananab');
INSERT INTO hotel (id_preco_temporada, nome_hotel) VALUES(2, 'Zilligod');

INSERT INTO tipo_quarto (tipo) VALUES('Quarto Solteiro');
INSERT INTO tipo_quarto (tipo) VALUES('Quarto Duplo Solteiro');
INSERT INTO tipo_quarto (tipo) VALUES('Quarto Casal');
INSERT INTO tipo_quarto (tipo) VALUES('Dormitório');
INSERT INTO tipo_quarto (tipo) VALUES('Suite');