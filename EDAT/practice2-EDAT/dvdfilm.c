#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sql.h>
#include <sqlext.h>
#include "odbc.h"
#define LENGTH 2048
#define MAX_COLS 30
#define MAX_COL_NAME_LEN 256
#define MAX_ROWS 1024

/*
 * example 1 with a fixed query, results retrieved with SQLGetData
 */

int main(int argc, char** argv) {
    SQLHENV env;
    SQLHDBC dbc;
    SQLHSTMT stmt;
    SQLRETURN ret; /* ODBC API return status */

    /*VARIABLES FOR QUERY*/
    char order1[LENGTH];
    int film_id;

    if(argc < 2){printf("please select remove\n"); return EXIT_FAILURE;}

    if(!strcmp(argv[1], "remove")){
        if(argc < 3){printf("%s %s <film_id>\n",argv[0], argv[1]); return EXIT_FAILURE;}
        film_id=atoi(argv[2]);
    

        printf("Deletion of film %i\n", film_id);
        /* CONNECT */
            ret = odbc_connect(&env, &dbc);
            if (!SQL_SUCCEEDED(ret)) {
                return EXIT_FAILURE;
            }
        /*ALLOC HANDLE*/
            SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
        /*CHECK OF FILM EXISTS*/
            sprintf(order1, "SELECT film_id FROM film WHERE film_id = %i", film_id);
            SQLPrepare(stmt, (SQLCHAR*)order1, SQL_NTS);
            SQLExecute(stmt);
            ret = SQLFetch(stmt);
            if (ret == SQL_NO_DATA) {
                printf("The film %i does not exist in the database\n", film_id);
                /*FINISH HIM*/
                    SQLFreeHandle(SQL_HANDLE_STMT, stmt);
                    ret = odbc_disconnect(env, dbc);
                    if (!SQL_SUCCEEDED(ret)) {
                        return EXIT_FAILURE;
                    }
                    return EXIT_SUCCESS;
            }

        SQLFreeStmt(stmt, SQL_UNBIND);
        SQLFreeStmt(stmt, SQL_CLOSE);
        /*NUMBER OF COPIES UNRENTED RIGHT NOW:*/
            sprintf(order1, "\
                            DELETE\
                            FROM payment \
                            WHERE payment_id IN (SELECT payment.payment_id\
                                        FROM payment, rental, inventory\
                                        WHERE payment.rental_id = rental.rental_id AND\
                                        rental.inventory_id = inventory.inventory_id AND\
                                        inventory.film_id = %i);\
                            DELETE \
                            FROM rental\
                            WHERE rental_id IN (SELECT rental.rental_id\
                                        FROM rental, inventory\
                                        WHERE rental.inventory_id = inventory.inventory_id AND\
                                        inventory.film_id = %i);\
                            DELETE \
                            FROM inventory\
                            WHERE inventory_id IN (SELECT inventory_id\
                                        FROM inventory\
                                        WHERE inventory.film_id = %i);\
                            DELETE FROM film_category\
                            WHERE film_id = %i;\
                            DELETE FROM film_actor \
                            WHERE film_id = %i;\
                            DELETE FROM film\
                            WHERE film_id = %i;\
                            ", film_id, film_id, film_id, film_id, film_id, film_id);
            /*EXECUTE ORDER*/
            SQLPrepare(stmt, (SQLCHAR*)order1, SQL_NTS);
            SQLExecute(stmt);
            /*FINISH HIM*/
            SQLFreeHandle(SQL_HANDLE_STMT, stmt);
            
            ret = odbc_disconnect(env, dbc);
            if (!SQL_SUCCEEDED(ret)) {
                return EXIT_FAILURE;
            }
            
            
            return EXIT_SUCCESS;
    }

    printf("Please use ./dvdfilm remove <film_id>");
    return EXIT_FAILURE;
}

