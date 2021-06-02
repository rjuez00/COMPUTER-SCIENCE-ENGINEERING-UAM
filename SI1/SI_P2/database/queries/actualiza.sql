/*Add primary key actorid, movieid and foreign key actorid to imdb_actormovies*/
ALTER TABLE imdb_actormovies ADD CONSTRAINT imdb_actormovies_pkey PRIMARY KEY (actorid,
                                                                               movieid,
                                                                               CHARACTER), ADD CONSTRAINT imdb_actormovies_actorid_fkey
FOREIGN KEY (actorid) REFERENCES public.imdb_actors (actorid) MATCH SIMPLE ON
UPDATE NO ACTION ON
DELETE CASCADE,
       ADD CONSTRAINT imdb_actormovies_movieid_fkey
FOREIGN KEY (movieid) REFERENCES public.imdb_movies (movieid) MATCH SIMPLE ON
UPDATE NO ACTION ON
DELETE CASCADE;


/*Remove foreign keys and add foreign keys directorid, movieid to imdb_directormovies*/
ALTER TABLE imdb_directormovies
DROP CONSTRAINT imdb_directormovies_directorid_fkey,
DROP CONSTRAINT imdb_directormovies_movieid_fkey,
                ADD CONSTRAINT imdb_directormovies_directorid_fkey
FOREIGN KEY (directorid) REFERENCES public.imdb_directors (directorid) MATCH SIMPLE ON
UPDATE NO ACTION ON
DELETE CASCADE,
       ADD CONSTRAINT imdb_directormovies_movieid_fkey
FOREIGN KEY (movieid) REFERENCES public.imdb_movies (movieid) MATCH SIMPLE ON
UPDATE NO ACTION ON
DELETE CASCADE;


/*Remove foreign key and add foreign key movieid to imdb_movielanguages*/
ALTER TABLE imdb_movielanguages
DROP CONSTRAINT imdb_movielanguages_movieid_fkey,
                ADD CONSTRAINT imdb_movielanguages_movieid_fkey
FOREIGN KEY (movieid) REFERENCES public.imdb_movies (movieid) MATCH SIMPLE ON
UPDATE NO ACTION ON
DELETE CASCADE;


/*Remove foreign key and add foreign key movieid to imdb_moviegenres*/
ALTER TABLE imdb_moviegenres
DROP CONSTRAINT imdb_moviegenres_movieid_fkey,
                ADD CONSTRAINT imdb_moviegenres_movieid_fkey
FOREIGN KEY (movieid) REFERENCES public.imdb_movies (movieid) MATCH SIMPLE ON
UPDATE NO ACTION ON
DELETE CASCADE;


/*Remove foreign key and add foreign key movieid to imdb_moviecountries*/
ALTER TABLE imdb_moviecountries
DROP CONSTRAINT imdb_moviecountries_movieid_fkey,
                ADD CONSTRAINT imdb_moviecountries_movieid_fkey
FOREIGN KEY (movieid) REFERENCES public.imdb_movies (movieid) MATCH SIMPLE ON
UPDATE NO ACTION ON
DELETE CASCADE;


/*Remove foreign key and add foreign key movieid to products*/
ALTER TABLE products
DROP CONSTRAINT products_movieid_fkey,
                ADD CONSTRAINT products_movieid_fkey
FOREIGN KEY (movieid) REFERENCES public.imdb_movies (movieid) MATCH SIMPLE ON
UPDATE NO ACTION ON
DELETE CASCADE;


/*Add foreign keys orderid, prod_id to orderdetail*/
ALTER TABLE orderdetail ADD CONSTRAINT orderdetail_orderid_fkey
FOREIGN KEY (orderid) REFERENCES public.orders (orderid) MATCH SIMPLE ON
UPDATE NO ACTION ON
DELETE CASCADE,
       ADD CONSTRAINT orderdetail_prod_id_fkey
FOREIGN KEY (prod_id) REFERENCES public.products (prod_id) ON
UPDATE NO ACTION ON
DELETE CASCADE;


/*Add foreign key prod_id to inventory*/
ALTER TABLE inventory ADD CONSTRAINT products_inventory_fkey
FOREIGN KEY (prod_id) REFERENCES public.products (prod_id) ON
UPDATE NO ACTION ON
DELETE CASCADE;


/*Add foreign key customerid to orders*/
ALTER TABLE orders ADD CONSTRAINT customer_products_fkey
FOREIGN KEY (customerid) REFERENCES public.customers (customerid) ON
UPDATE NO ACTION ON
DELETE CASCADE;

/*GENRES*/

/*Rename table imdb_moviegenres to imdb_genremovies*/
ALTER TABLE imdb_moviegenres RENAME TO imdb_genremovies;


/*Create table imdb_genres*/
CREATE TABLE imdb_genres (genreid SERIAL NOT NULL PRIMARY KEY,
                                                          genre CHARACTER varying(32) NOT NULL);


/*Insert into imdb_genres all disctinct genres from imdb_genremovies*/
INSERT INTO imdb_genres (genre)
SELECT DISTINCT genre
FROM imdb_genremovies;


/*Add genreid column to imdb_genremovies*/
ALTER TABLE imdb_genremovies ADD COLUMN genreid integer NOT NULL DEFAULT 0;


/*Set genreid column from imdb_genremovies*/
UPDATE imdb_genremovies
SET genreid = imdb_genres.genreid
FROM imdb_genres
WHERE imdb_genres.genre = imdb_genremovies.genre;


/*Add foreign key genre to imdb_genremovies*/
ALTER TABLE imdb_genremovies
DROP COLUMN genre,
            ADD CONSTRAINT imdb_genremovies_genreid_fkey
FOREIGN KEY (genreid) REFERENCES public.imdb_genres (genreid) MATCH SIMPLE ON
UPDATE NO ACTION ON
DELETE CASCADE;


/*LANGUAGES*/

/*Rename table imdb_movielanguages to imdb_languagemovies*/
ALTER TABLE imdb_movielanguages RENAME TO imdb_languagemovies;


/*Create table imdb_languages*/
CREATE TABLE imdb_languages (languageid SERIAL NOT NULL PRIMARY KEY,
                                                                LANGUAGE CHARACTER varying(32) NOT NULL,
                                                                                               extrainformation CHARACTER varying(128) NOT NULL);


/*Insert into imdb_languages all disctinct language from imdb_languagemovies*/
INSERT INTO imdb_languages (language, extrainformation)
SELECT DISTINCT language,
                extrainformation
FROM imdb_languagemovies;


/*Add languageid column to imdb_languagemovies*/
ALTER TABLE imdb_languagemovies ADD COLUMN languageid integer NOT NULL DEFAULT 0;


/*Set languageid column from imdb_languagemovies*/
UPDATE imdb_languagemovies
SET languageid = imdb_languages.languageid
FROM imdb_languages
WHERE imdb_languages.language = imdb_languagemovies.language
  AND imdb_languages.extrainformation = imdb_languagemovies.extrainformation;


/*Add foreign key languageid to imdb_languagemovies*/
ALTER TABLE imdb_languagemovies
DROP COLUMN LANGUAGE,
DROP COLUMN extrainformation,
            ADD CONSTRAINT imdb_languagemovies_languageid_fkey
FOREIGN KEY (languageid) REFERENCES public.imdb_languages (languageid) MATCH SIMPLE ON
UPDATE NO ACTION ON
DELETE CASCADE;


/*COUNTRIES*/

/*Rename table imdb_moviecountries to imdb_countrymovies*/
ALTER TABLE imdb_moviecountries RENAME TO imdb_countrymovies;


/*Create table imdb_countries*/
CREATE TABLE imdb_countries (countryid SERIAL NOT NULL PRIMARY KEY,
                                                               country CHARACTER varying(32) NOT NULL);


/*Insert into imdb_countries all disctinct country from imdb_countrymovies*/
INSERT INTO imdb_countries (country)
SELECT DISTINCT country
FROM imdb_countrymovies;


/*Add countryid column to imdb_countrymovies*/
ALTER TABLE imdb_countrymovies ADD COLUMN countryid integer NOT NULL DEFAULT 0;


/*Set countryid column from imdb_countrymovies*/
UPDATE imdb_countrymovies
SET countryid = imdb_countries.countryid
FROM imdb_countries
WHERE imdb_countries.country = imdb_countrymovies.country;


/*Add foreign key countryid to imdb_countrymovies*/
ALTER TABLE imdb_countrymovies
DROP COLUMN country,
            ADD CONSTRAINT imdb_countrymovies_countryid_fkey
FOREIGN KEY (countryid) REFERENCES public.imdb_countries (countryid) MATCH SIMPLE ON
UPDATE NO ACTION ON
DELETE CASCADE;


/*ALERTAS*/

/*Create table alertas*/
CREATE TABLE alertas
  (prod_id integer NOT NULL PRIMARY KEY,
                                    CONSTRAINT imdb_prodid_products
   FOREIGN KEY (prod_id) REFERENCES public.products (prod_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE);