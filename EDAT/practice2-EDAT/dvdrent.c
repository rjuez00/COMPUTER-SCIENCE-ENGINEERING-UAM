#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sql.h>
#include <sqlext.h>
#include "odbc.h"
#define LENGTH 1024
#define MAX_COLS 30
#define MAX_COL_NAME_LEN 256
#define MAX_ROWS 1024

int new (SQLHSTMT stmt, SQLHENV env, SQLHDBC dbc, SQLRETURN ret, int customer_id, int film_id, int staff_id, int store_id, int amount);
int rentremove (SQLHSTMT stmt, SQLHENV env, SQLHDBC dbc, SQLRETURN ret, int rent_id);

int main(int argc, char** argv) {
    SQLHENV env;
    SQLHDBC dbc;
    SQLHSTMT stmt;
    SQLRETURN ret; /* ODBC API return status */
    int rent_id, customer_id, film_id, staff_id, store_id, amount;
    if(argc < 2){printf("please select new or remove\n"); return EXIT_FAILURE;}
    /* CONNECT */
        ret = odbc_connect(&env, &dbc);
        if (!SQL_SUCCEEDED(ret)) {
            return EXIT_FAILURE;
        }
        SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);


    if(!strcmp(argv[1], "new")){
        if(argc < 7){printf("%s %s customer_id film_id staff_id store_id amount\n",argv[0], argv[1]); return EXIT_FAILURE;}
        customer_id=atoi(argv[2]);
        film_id = atoi(argv[3]);
        staff_id = atoi(argv[4]);
        store_id = atoi(argv[5]);
        amount = atoi(argv[6]);
        new (stmt,env,dbc,ret,customer_id,film_id,staff_id,store_id,amount);

    }

    else if(!strcmp(argv[1], "remove")){
        if(argc<3){printf("%s %s rent_id\n",argv[0], argv[1]); return EXIT_FAILURE;}
        rent_id=atoi(argv[2]);
        rentremove (stmt,env,dbc,ret,rent_id);


    }
    /*FINISH HIM*/
        SQLFreeHandle(SQL_HANDLE_STMT, stmt);
        
        ret = odbc_disconnect(env, dbc);
        if (!SQL_SUCCEEDED(ret)) {
            return EXIT_FAILURE;
        }
    return EXIT_SUCCESS;
}

int new (SQLHSTMT stmt, SQLHENV env, SQLHDBC dbc, SQLRETURN ret, int customer_id, int film_id, int staff_id, int store_id, int amount){
    char order1[LENGTH], order2[LENGTH];
    SQLINTEGER  SQLreturn;
    SQLINTEGER severalresults[MAX_ROWS];
    int i=0, j=0;
    printf("Film: %i\nStore_id:%i\n", film_id, store_id);
   
    /*NUMBER OF COPIES UNRENTED RIGHT NOW:*/
        sprintf(order1, "   SELECT inventory_id\
                            FROM inventory\
                            WHERE film_id = '%i' AND store_id='%i'\
                            EXCEPT\
                                SELECT rental.inventory_id\
                                FROM rental, inventory\
                                WHERE return_date IS NULL AND\
                                rental.inventory_id = inventory.inventory_id AND\
                                inventory.film_id = '%i' AND inventory.store_id = '%i'\
                        ", film_id, store_id, film_id, store_id);
        /*EXECUTE ORDER1*/
        SQLPrepare(stmt, (SQLCHAR*)order1, SQL_NTS);
        ret = SQLBindCol (stmt,                 /* Statement handle*/
                          1,                    /* Column number*/
                          SQL_C_SLONG,          /* C Data Type*/
                          &SQLreturn,          /* Data buffer*/
                          sizeof(SQLINTEGER),   /* Size of Data Buffer*/
                          NULL);                /* Size of data returned*/   
        SQLExecute(stmt);
        printf("Copies avaliable: \n");
        for(i=0; ;i++){
            if(!SQL_SUCCEEDED( ret = SQLFetch(stmt) )) break;
            
            if (ret == SQL_NO_DATA) break;

            severalresults[i]=SQLreturn;
            printf("--> %i\n", severalresults[i]);
        }
        printf("\n");

        if(i >= amount){
            SQLFreeStmt(stmt, SQL_UNBIND);
            SQLFreeStmt(stmt, SQL_CLOSE);
            for(j=0; j<amount; j++){
                    sprintf(order2, "INSERT INTO rental VALUES (DEFAULT, NOW(), %i, %i, NULL, %i, NOW())", severalresults[j], customer_id, staff_id);
                    SQLPrepare(stmt, (SQLCHAR*)order2, SQL_NTS);
                    SQLExecute(stmt);
            }
            if(i-amount) printf("Number of copies available in store %i after renting film %i: %i\n", store_id, film_id, i-amount);
            else printf("You just rented the last copy of film %i in store %i\n", film_id, store_id);
        }
        else printf("Sorry we could not process your query, no copies of film %i in store %i are left\n", film_id, store_id);
        
        return EXIT_SUCCESS;
}

int rentremove (SQLHSTMT stmt, SQLHENV env, SQLHDBC dbc, SQLRETURN ret, int rent_id){
    char order1[LENGTH];

    printf("Remove rent %i with it's associated payment\n", rent_id);

    /*NUMBER OF COPIES UNRENTED RIGHT NOW:*/
        sprintf(order1, "   DELETE FROM payment\
                            WHERE payment.rental_id = %i;\
                            DELETE FROM rental\
                            WHERE rental.rental_id = %i;", rent_id, rent_id);
    /*EXECUTE ORDER1*/
        SQLPrepare(stmt, (SQLCHAR*)order1, SQL_NTS);
        SQLExecute(stmt);
    
    return EXIT_SUCCESS;
}