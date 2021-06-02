/*Declarar función con sus argumentos*/
CREATE OR REPLACE FUNCTION getTopVentas(año1 double precision, año2 double precision) RETURNS TABLE (Año DOUBLE PRECISION, Pelicula CHARACTER varying(255),
                                                                                                                                              Ventas BIGINT) AS $$

    SELECT
        /*Selecccionar año, título y número de ventas*/
        result2.year,
        imdb_movies.movietitle,
        sales
    FROM(
            /*Seleccionar todas las pelícluas con distinto año y mayor número de ventas*/
            SELECT DISTINCT ON(year)
                    year, movie, sales
            FROM (
                    SELECT
                        /*Seleccionar año, película y ventas de esa película por año, ordenado por año y película*/
                        EXTRACT(year from orders.orderdate) as year,
                        products.movieid as movie,
                        sum(orderdetail.quantity) as sales

                    FROM orderdetail
                    INNER JOIN orders ON
                        orderdetail.orderid = orders.orderid
                    INNER JOIN products ON
                        products.prod_id = orderdetail.prod_id
                    GROUP BY year, products.movieid) as result
	        WHERE
                /*Filtrar y ordenar por años pasados como argumento*/
                year >= $1
                and year <= $2
            ORDER BY year, sales DESC) as result2

    INNER JOIN imdb_movies on
        imdb_movies.movieid = result2.movie


$$ LANGUAGE SQL;