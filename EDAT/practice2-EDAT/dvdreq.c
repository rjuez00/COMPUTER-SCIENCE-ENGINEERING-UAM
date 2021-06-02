#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sql.h>
#include <sqlext.h>
#include "odbc.h"
#define LENGTH 3072
#define MAX_COLS 30
#define MAX_ROWS 1024
#define MAX_COL_NAME_LEN 256
#define NAMELEN 45

/*
 * example 1 with a fixed query, results retrieved with SQLGetData
 */

int customer (SQLHSTMT stmt, SQLHENV env, SQLHDBC dbc, SQLRETURN ret, char *name, char *surname);
int film(SQLHSTMT stmt, SQLHENV env, SQLHDBC dbc, SQLRETURN ret, char* film_title);
int rent(SQLHSTMT stmt, SQLHENV env, SQLHDBC dbc, SQLRETURN ret, char* date1, char *date2, int customer_id);
int recommend(SQLHSTMT stmt, SQLHENV env, SQLHDBC dbc, SQLRETURN ret, int customer_id);


int main(int argc, char** argv) {
    SQLHENV env;
    SQLHDBC dbc;
    SQLHSTMT stmt;
    SQLRETURN ret; /* ODBC API return status */

  
    if(argc < 2) {printf("Please select: customer, film, rent or recommend\n"); return EXIT_FAILURE;}

    /* CONNECT */
        ret = odbc_connect(&env, &dbc);
        if (!SQL_SUCCEEDED(ret)) {
            return EXIT_FAILURE;
        }

    /* ALLOCATE QUERY*/
        SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
        


    if(!strcmp(argv[1], "customer")){
        if(argc < 6){printf("please follow: %s %s -n <name> -a <surname>\n", argv[0], argv[1]); return EXIT_FAILURE;}
        customer(stmt, env, dbc, ret, argv[3], argv[5]);
    }

    else if(!strcmp(argv[1], "film")){
        if(argc < 3){printf("please follow: %s %s <film>\n", argv[0], argv[1]); return EXIT_FAILURE;}
        film(stmt, env, dbc, ret, argv[2]);
    }

    else if(!strcmp(argv[1], "rent")){
        if(argc < 5){printf("please follow: %s %s <customer_id> <init date> <end date>\n", argv[0], argv[1]); return EXIT_FAILURE;}
        rent(stmt,env,dbc,ret, argv[3], argv[4], atoi(argv[2]));

    }

    else if(!strcmp(argv[1], "recommend")){
        if(argc < 3){printf("please follow: %s %s <customer_id>\n", argv[0], argv[1]); return EXIT_FAILURE;}
        recommend(stmt, env, dbc, ret, atoi(argv[2]));

    }

    else {printf("Please select: customer, film, rent or recommend");
            /*FREE*/
            SQLFreeHandle(SQL_HANDLE_STMT, stmt);
            
            /* DISCONNECT */
            ret = odbc_disconnect(env, dbc);
            if (!SQL_SUCCEEDED(ret)) {
                return EXIT_FAILURE;
            }

            return EXIT_FAILURE; 
    }

    /*FREE*/
        SQLFreeHandle(SQL_HANDLE_STMT, stmt);
        

    /* DISCONNECT */
        ret = odbc_disconnect(env, dbc);
        if (!SQL_SUCCEEDED(ret)) {
            return EXIT_FAILURE;
        }
    return EXIT_SUCCESS; 
}



int customer (SQLHSTMT stmt, SQLHENV env, SQLHDBC dbc, SQLRETURN ret, char *name, char *surname) {

    SQLSMALLINT numCols; /* number of columns in result-set */
    SQLCHAR *      ColumnName[MAX_COLS];
    SQLSMALLINT    ColumnNameLen[MAX_COLS];
    SQLSMALLINT    ColumnDataType[MAX_COLS];
    SQLULEN        ColumnDataSize[MAX_COLS];
    SQLSMALLINT    ColumnDataDigits[MAX_COLS];
    SQLSMALLINT    ColumnDataNullable[MAX_COLS];
    SQLCHAR *      ColumnData[MAX_COLS];
    SQLLEN         ColumnDataLen[MAX_COLS];
    SQLSMALLINT    i,j;
    char printout[LENGTH], printtemp[LENGTH];
    char execute66[LENGTH];
        
        for (i=0;i<MAX_COLS;i++) {
            ColumnName[i]=NULL;
            ColumnData[i]=NULL;
        }
        sprintf(execute66, "SELECT customer.customer_id, customer.first_name, customer.last_name, customer.create_date, address.address, address.address2\
                            FROM customer, address\
                            WHERE (customer.first_name LIKE '%s' OR customer.last_name LIKE '%s')\
                            AND customer.address_id = address.address_id", name, surname);

        /*PREPARE QUERY*/
           SQLPrepare(stmt, (SQLCHAR*)execute66, SQL_NTS);
        /*OBTAIN NUMBER OF COLUMNS*/
            ret = SQLNumResultCols (stmt, &numCols);
        
        /*OBTAIN DATA FROM COLUMNS AND BINDING IT*/
            for (i=0;i<numCols;i++) {
                ColumnName[i] = (SQLCHAR *) malloc (LENGTH);
                if(ColumnName[i]==NULL) {
                    /*FREE*/
                        SQLFreeHandle(SQL_HANDLE_STMT, stmt);
                    /* DISCONNECT */
                        ret = odbc_disconnect(env, dbc);
                        if (!SQL_SUCCEEDED(ret)) {
                            return EXIT_FAILURE;
                        }
                    return EXIT_FAILURE;
                }
                /*I FILL ALL THE ARRAYS WITH THE VARIABLES USED FOR THE BINDING FUNCTION*/
                ret = SQLDescribeCol (
                            stmt,                    /* Select Statement (Prepared)*/
                            i+1,                      /* Columnn Number */
                            ColumnName[i],            /* Column Name (returned) */
                            MAX_COL_NAME_LEN,         /* size of Column Name buffer*/
                            &ColumnNameLen[i],        /* Actual size of column name*/
                            &ColumnDataType[i],       /* SQL Data type of column*/
                            &ColumnDataSize[i],       /* Data size of column in table*/
                            &ColumnDataDigits[i],     /* Number of decimal digits*/
                            &ColumnDataNullable[i]);  /* Whether column nullable*/

                /*I TRANSFORM THE SQL TYPES TO C TYPES*/
                ColumnData[i] = (SQLCHAR *) malloc (ColumnDataSize[i]+1);
                if(ColumnData[i]==NULL) {
                    /*FREE*/
                        SQLFreeHandle(SQL_HANDLE_STMT, stmt);
                    /* DISCONNECT */
                        ret = odbc_disconnect(env, dbc);
                        if (!SQL_SUCCEEDED(ret)) {
                            return EXIT_FAILURE;
                        }
                    return EXIT_FAILURE;
                }
                switch (ColumnDataType[i]) {
                    case SQL_INTEGER:
                        ColumnDataType[i]=SQL_C_LONG;
                    break;
                    case SQL_VARCHAR:
                        ColumnDataType[i]=SQL_C_CHAR;
                    break;
                    case SQL_TYPE_DATE:
                        ColumnDataType[i]=SQL_C_CHAR;
                    break;
                    case SQL_TYPE_TIMESTAMP:
                        ColumnDataType[i]=SQL_C_CHAR;
                    break;
                }
                /*I BIND WITH THE PRIEVIOUSLY RETRIEVED DATA*/
                ret = SQLBindCol (stmt,                  /* Statement handle*/
                                i+1,                    /* Column number*/
                                ColumnDataType[i],      /* C Data Type*/
                                ColumnData[i],          /* Data buffer*/
                                ColumnDataSize[i],      /* Size of Data Buffer*/
                                &ColumnDataLen[i]); /* Size of data returned*/
            }
        /*EXECUTE THE QUERY*/
            SQLExecute(stmt);

        /*PRINT COLUMNS*/
            printf("|");
            for (j=0;j<numCols;j++) {
                printf("%18s|", ColumnName[j]);
            }
            printf("\n");
            for(i=0; i<18*6+6; i++){printf("_");}
            /*PRINT THE RESULT*/
            for (i=0; ; i++) {
                if(!SQL_SUCCEEDED( ret = SQLFetch(stmt) )) break;

                /*END OF OUTPUT*/
                if (ret == SQL_NO_DATA) break;
                
                /*PRINT OUTPUT*/
                printout[0]='\0';
                printf("\n");
                sprintf(printtemp,"|");
                strcat(printout,printtemp);
                for (j=0;j<numCols;j++) {
                    if (ColumnDataType[j]==SQL_INTEGER) {
                        sprintf(printtemp,"%18i|", (int)*ColumnData[j]);
                    } else {
                        sprintf(printtemp,"%18s|", ColumnData[j]);
                    }
                    strcat(printout,printtemp);
                }
                printf("%s", printout);

            }
            printf("\n");
            for(i=0; i<18*6+6; i++){printf("_");}
            printf("\n");

            /*FREE*/
                for(i=0; i<numCols; i++){
                    if(ColumnName[i]) free(ColumnName[i]);
                    if(ColumnData[i]) free(ColumnData[i]);
                }
            return EXIT_SUCCESS;
}

int film(SQLHSTMT stmt, SQLHENV env, SQLHDBC dbc, SQLRETURN ret, char* film_title){
    SQLSMALLINT numCols; /* number of columns in result-set */

    SQLCHAR *      ColumnName[MAX_COLS];
    SQLSMALLINT    ColumnNameLen[MAX_COLS];
    SQLSMALLINT    ColumnDataType[MAX_COLS];
    SQLULEN        ColumnDataSize[MAX_COLS];
    SQLULEN        columnsize;
    SQLSMALLINT    ColumnDataDigits[MAX_COLS];
    SQLSMALLINT    ColumnDataNullable[MAX_COLS];
    SQLCHAR *      ColumnData[MAX_COLS];
    SQLLEN         ColumnDataLen[MAX_COLS];
    SQLSMALLINT    i,j,k,x, numberofmovies=0;
    SQLINTEGER  SQLreturn;
    SQLINTEGER severalresults[MAX_ROWS];
    
    char printout[LENGTH], printtemp[LENGTH];
    char execute66[LENGTH];
    char actorname[NAMELEN], actorsurname[NAMELEN];

    for (i=0;i<MAX_COLS;i++) {
            ColumnName[i]=NULL;
            ColumnData[i]=NULL;
        }
    sprintf(execute66, "SELECT film_id\
                            FROM film\
                            WHERE film.title LIKE '%s%s%s'", "%", film_title, "%");
    /*PREPARE QUERY*/
            SQLPrepare(stmt, (SQLCHAR*)execute66, SQL_NTS);
    /*BIND*/
            ret = SQLBindCol (stmt,                 /* Statement handle*/
                            1,                    /* Column number*/
                            SQL_C_SLONG,          /* C Data Type*/
                            &SQLreturn,          /* Data buffer*/
                            sizeof(SQLINTEGER),   /* Size of Data Buffer*/
                            NULL); 
            
        /*EXECUTE THE QUERY*/
            SQLExecute(stmt);

        /*RETRIEVE DATA*/
            for(i=0; ;i++){
                if(!SQL_SUCCEEDED( ret = SQLFetch(stmt) )) break;
                
                if (ret == SQL_NO_DATA) break;
                numberofmovies++;
                severalresults[i]=SQLreturn;
            }
      
        /*SECOND QUERY*/
        for(k=0; k<numberofmovies; k++){ 
            SQLFreeStmt(stmt, SQL_UNBIND);
            SQLFreeStmt(stmt, SQL_CLOSE);
            sprintf(execute66, "SELECT film.film_id, film.title, film.release_year, film.length, language.name as language, film.description\
                                FROM film, language\
                                WHERE film.language_id = language.language_id AND\
                                film.film_id = %i", severalresults[k]);

            /*PREPARE QUERY*/
                SQLPrepare(stmt, (SQLCHAR*)execute66, SQL_NTS);
            /*OBTAIN NUMBER OF COLUMNS*/
                ret = SQLNumResultCols (stmt, &numCols);
            
            /*OBTAIN DATA FROM COLUMNS AND BINDING IT*/
                for (i=0;i<numCols;i++) { 
                    ColumnName[i] = (SQLCHAR *) malloc (LENGTH);
                    if(ColumnName[i]==NULL) {
                        /*FREE*/
                            SQLFreeHandle(SQL_HANDLE_STMT, stmt);
                        /* DISCONNECT */
                            ret = odbc_disconnect(env, dbc);
                            if (!SQL_SUCCEEDED(ret)) {
                                return EXIT_FAILURE;
                            }
                        return EXIT_FAILURE;
                    }
                    /*I FILL ALL THE ARRAYS WITH THE VARIABLES USED FOR THE BINDING FUNCTION*/
                    ret = SQLDescribeCol (
                                stmt,                    /* Select Statement (Prepared)*/
                                i+1,                      /* Columnn Number */
                                ColumnName[i],            /* Column Name (returned) */
                                MAX_COL_NAME_LEN,         /* size of Column Name buffer*/
                                &ColumnNameLen[i],        /* Actual size of column name*/
                                &ColumnDataType[i],       /* SQL Data type of column*/
                                &ColumnDataSize[i],       /* Data size of column in table*/
                                &ColumnDataDigits[i],     /* Number of decimal digits*/
                                &ColumnDataNullable[i]);  /* Whether column nullable*/

                    /*I TRANSFORM THE SQL TYPES TO C TYPES*/
                    ColumnData[i] = (SQLCHAR *) malloc (ColumnDataSize[i]+1);
                    if(ColumnData[i]==NULL) {
                        /*FREE*/
                            SQLFreeHandle(SQL_HANDLE_STMT, stmt);
                        /* DISCONNECT */
                            ret = odbc_disconnect(env, dbc);
                            if (!SQL_SUCCEEDED(ret)) {
                                return EXIT_FAILURE;
                            }
                        return EXIT_FAILURE;
                    }
                    switch (ColumnDataType[i]) {
                        case SQL_INTEGER:
                            ColumnDataType[i]=SQL_C_LONG;
                        break;
                        case SQL_SMALLINT:
                            ColumnDataType[i]=SQL_C_LONG;
                        break;
                        case SQL_VARCHAR:
                            ColumnDataType[i]=SQL_C_CHAR;
                        break;
                        case SQL_LONGVARCHAR:
                            ColumnDataType[i]=SQL_C_CHAR;
                        break;
                        case SQL_TYPE_DATE:
                            ColumnDataType[i]=SQL_C_CHAR;
                        break;
                        case SQL_TYPE_TIMESTAMP:
                            ColumnDataType[i]=SQL_C_CHAR;
                        break;
                    }
                    /*I BIND WITH THE PRIEVIOUSLY RETRIEVED DATA*/
                    ret = SQLBindCol (stmt,                  /* Statement handle*/
                                    i+1,                    /* Column number*/
                                    ColumnDataType[i],      /* C Data Type*/
                                    ColumnData[i],          /* Data buffer*/
                                    ColumnDataSize[i],      /* Size of Data Buffer*/
                                    &ColumnDataLen[i]); /* Size of data returned*/
                }
            /*EXECUTE THE QUERY*/
                SQLExecute(stmt);

            /*PRINT THE RESULT*/
                if(!SQL_SUCCEEDED( ret = SQLFetch(stmt) )) break;

                printout[0]='\0';
                printf("\n");
                printf("%s: %i\n", ColumnName[0], (int)*ColumnData[0]);
                for (j=1;j<numCols;j++) {
                    if (ColumnDataType[j]==SQL_INTEGER) sprintf(printtemp,"     %s: %i\n",ColumnName[j] ,(int)*ColumnData[j]);
                    else sprintf(printtemp,"     %s: %s\n",ColumnName[j], ColumnData[j]);
                    strcat(printout,printtemp);
                }
                printf("%s", printout);

                /*ACTORS*/
                printf("     Actors:\n");
                SQLFreeStmt(stmt, SQL_UNBIND);
                SQLFreeStmt(stmt, SQL_CLOSE);
                sprintf(execute66, "SELECT actor.first_name, actor.last_name\
                                    FROM film_actor, actor\
                                    WHERE film_actor.actor_id = actor.actor_id AND\
                                    film_id = %i", severalresults[k]);
                /*PREPARE QUERY*/
                    SQLPrepare(stmt, (SQLCHAR*)execute66, SQL_NTS);
                
                /*BINDING*/
                    ret = SQLDescribeCol (
                                stmt,                    /* Select Statement (Prepared)*/
                                1,                      /* Columnn Number */
                                NULL,            /* Column Name (returned) */
                                MAX_COL_NAME_LEN,         /* size of Column Name buffer*/
                                NULL,        /* Actual size of column name*/
                                NULL,       /* SQL Data type of column*/
                                &columnsize,       /* Data size of column in table*/
                                NULL,     /* Number of decimal digits*/
                                NULL);  /* Whether column nullable*/
    
                    ret = SQLBindCol (stmt,                 /* Statement handle*/
                                        1,                    /* Column number*/
                                        SQL_C_CHAR,          /* C Data Type*/
                                        actorname,          /* Data buffer*/
                                        columnsize,   /* Size of Data Buffer*/
                                        NULL);
                    ret = SQLBindCol (stmt,                 /* Statement handle*/
                                        2,                    /* Column number*/
                                        SQL_C_CHAR,          /* C Data Type*/
                                        actorsurname,          /* Data buffer*/
                                        columnsize,   /* Size of Data Buffer*/
                                        NULL);
                /*EXECUTE THE QUERY*/
                    SQLExecute(stmt);

                /*RETRIEVE DATA*/
                    for(x=0; ;x++){
                        if(!SQL_SUCCEEDED( ret = SQLFetch(stmt) )) break;
                        if (ret == SQL_NO_DATA) break;
                        printf("            %s %s\n", actorname, actorsurname);
                    }
                    
            /*FREE*/
                for(i=0; i<numCols; i++){
                    if(ColumnName[i]) free(ColumnName[i]);
                    if(ColumnData[i]) free(ColumnData[i]);
                }    
        }
        printf("\n");
        return EXIT_SUCCESS;
}

int rent(SQLHSTMT stmt, SQLHENV env, SQLHDBC dbc, SQLRETURN ret, char* date1, char *date2, int customer_id){

    SQLSMALLINT numCols; /* number of columns in result-set */

    SQLCHAR *      ColumnName[MAX_COLS];
    SQLSMALLINT    ColumnNameLen[MAX_COLS];
    SQLSMALLINT    ColumnDataType[MAX_COLS];
    SQLULEN        ColumnDataSize[MAX_COLS];
    SQLSMALLINT    ColumnDataDigits[MAX_COLS];
    SQLSMALLINT    ColumnDataNullable[MAX_COLS];
    SQLCHAR *      ColumnData[MAX_COLS];
    SQLLEN         ColumnDataLen[MAX_COLS];
    SQLSMALLINT    i,j;
    char printout[LENGTH], printtemp[LENGTH];
    char execute66[LENGTH];
    
    for (i=0;i<MAX_COLS;i++) {
            ColumnName[i]=NULL;
            ColumnData[i]=NULL;
        }

    sprintf(execute66, "SELECT\
                        rental.rental_id,\
                        rental.rental_date,\
                        film.film_id,\
                        film.title,\
                        rental.staff_id,\
                        staff.first_name,\
                        staff.last_name,\
                        inventory.store_id,\
                        payment.amount\
                        FROM rental, payment, film, inventory, staff\
                        WHERE(\
                                rental.staff_id = staff.staff_id AND\
                                rental.inventory_id = inventory.inventory_id AND\
                                rental.rental_id = payment.rental_id AND\
                                rental.rental_date >= DATE '%s' AND\
                                rental.rental_date <= DATE '%s' AND\
                                inventory.film_id = film.film_id AND\
                                rental.staff_id = staff.staff_id AND\
                                rental.customer_id = %i\
                            )\
                            ORDER BY rental.rental_date", date1, date2, customer_id);
        /*PREPARE QUERY*/
           SQLPrepare(stmt, (SQLCHAR*)execute66, SQL_NTS);
        /*OBTAIN NUMBER OF COLUMNS*/
            ret = SQLNumResultCols (stmt, &numCols);
        
        /*OBTAIN DATA FROM COLUMNS AND BINDING IT*/
            for (i=0;i<numCols;i++) {
                ColumnName[i] = (SQLCHAR *) malloc (LENGTH);
                if(ColumnName[i]==NULL) {
                    /*FREE*/
                        SQLFreeHandle(SQL_HANDLE_STMT, stmt);
                    /* DISCONNECT */
                        ret = odbc_disconnect(env, dbc);
                        if (!SQL_SUCCEEDED(ret)) {
                            return EXIT_FAILURE;
                        }
                    return EXIT_FAILURE;
                }
                /*I FILL ALL THE ARRAYS WITH THE VARIABLES USED FOR THE BINDING FUNCTION*/
                ret = SQLDescribeCol (
                            stmt,                    /* Select Statement (Prepared)*/
                            i+1,                      /* Columnn Number */
                            ColumnName[i],            /* Column Name (returned) */
                            MAX_COL_NAME_LEN,         /* size of Column Name buffer*/
                            &ColumnNameLen[i],        /* Actual size of column name*/
                            &ColumnDataType[i],       /* SQL Data type of column*/
                            &ColumnDataSize[i],       /* Data size of column in table*/
                            &ColumnDataDigits[i],     /* Number of decimal digits*/
                            &ColumnDataNullable[i]);  /* Whether column nullable*/

                /*I TRANSFORM THE SQL TYPES TO C TYPES*/
                ColumnData[i] = (SQLCHAR *) malloc (ColumnDataSize[i]+1);
                if(ColumnData[i]==NULL) {
                    /*FREE*/
                        SQLFreeHandle(SQL_HANDLE_STMT, stmt);
                    /* DISCONNECT */
                        ret = odbc_disconnect(env, dbc);
                        if (!SQL_SUCCEEDED(ret)) {
                            return EXIT_FAILURE;
                        }
                    return EXIT_FAILURE;
                }
                switch (ColumnDataType[i]) {
                    case SQL_NUMERIC:
                        ColumnDataType[i]=SQL_C_CHAR;
                    break;
                    case SQL_INTEGER:
                        ColumnDataType[i]=SQL_C_LONG;
                    break;
                    case SQL_VARCHAR:
                        ColumnDataType[i]=SQL_C_CHAR;
                    break;
                    case SQL_TYPE_DATE:
                        ColumnDataType[i]=SQL_C_CHAR;
                    break;
                    case SQL_TYPE_TIMESTAMP:
                        ColumnDataType[i]=SQL_C_CHAR;
                    break;
                    case SQL_DOUBLE:
                        ColumnDataType[i]=SQL_C_DOUBLE;
                    break;
                    case SQL_FLOAT:
                        ColumnDataType[i]=SQL_C_FLOAT;
                        break;
                    case SQL_SMALLINT:
                        ColumnDataType[i]=SQL_C_LONG;
                    break;
                }
                /*I BIND WITH THE PRIEVIOUSLY RETRIEVED DATA*/
                ret = SQLBindCol (stmt,                  /* Statement handle*/
                                i+1,                    /* Column number*/
                                ColumnDataType[i],      /* C Data Type*/
                                ColumnData[i],          /* Data buffer*/
                                ColumnDataSize[i],      /* Size of Data Buffer*/
                                &ColumnDataLen[i]); /* Size of data returned*/
            }
        /*EXECUTE THE QUERY*/
            SQLExecute(stmt);

        /*PRINT COLUMNS*/
            printf("|");
            for (j=0;j<numCols;j++) {
                        switch(j){
                            case 0:
                            case 2:
                            case 4:
                            case 7:
                            case 8: 
                                printf("%9s|", ColumnName[j]);
                                break;
                            case 5:
                            case 6:
                                printf("%10s|", ColumnName[j]);
                                break;
                            default:
                                printf("%20s|", ColumnName[j]);
                                break; 
                        }

        }
            printf("\n");
            for(i=0; i<18*6+6; i++){printf("_");}
        /*PRINT THE RESULT*/
            for (i=0; ; i++) {
                if(!SQL_SUCCEEDED( ret = SQLFetch(stmt) )) break;

                /*END OF OUTPUT*/
                if (ret == SQL_NO_DATA) break;
                
                /*PRINT OUTPUT*/
                printout[0]='\0';
                printf("\n");
                sprintf(printtemp,"|");
                strcat(printout,printtemp);
                for (j=0;j<numCols;j++) {
                        switch(j){
                            case 0:
                            case 2:
                            case 4:
                            case 7:
                            case 8: 
                                if (ColumnDataType[j]==SQL_INTEGER) sprintf(printtemp,"%9i|", (int)*ColumnData[j]);
                                else if (ColumnDataType[j]==SQL_C_FLOAT) {sprintf(printtemp,"%9f|", (float)*ColumnData[j]);}
                                else sprintf(printtemp,"%9s|", ColumnData[j]);
                                break;

                            case 5:
                            case 6:
                                if (ColumnDataType[j]==SQL_INTEGER) sprintf(printtemp,"%10i|", (int)*ColumnData[j]);
                                else sprintf(printtemp,"%10s|", ColumnData[j]);
                                break;

                            default:
                                if (ColumnDataType[j]==SQL_INTEGER) sprintf(printtemp,"%20i|", (int)*ColumnData[j]);
                                else sprintf(printtemp,"%20s|", ColumnData[j]);
                                break; 
                        }                   
                    strcat(printout,printtemp);
                }
                printf("%s", printout);

                }  
            printf("\n");
            for(i=0; i<18*6+6; i++){printf("_");}
            printf("\n");

        /*FREE*/
            for(j=0; j<numCols; j++){
                if(ColumnName[j])free(ColumnName[j]);
                if(ColumnData[j])free(ColumnData[j]);
            }

    return EXIT_SUCCESS;
}

int recommend(SQLHSTMT stmt, SQLHENV env, SQLHDBC dbc, SQLRETURN ret, int customer_id){
    SQLSMALLINT numCols; /* number of columns in result-set */
    SQLCHAR *      ColumnName[MAX_COLS];
    SQLSMALLINT    ColumnNameLen[MAX_COLS];
    SQLSMALLINT    ColumnDataType[MAX_COLS];
    SQLULEN        ColumnDataSize[MAX_COLS];
    SQLSMALLINT    ColumnDataDigits[MAX_COLS];
    SQLSMALLINT    ColumnDataNullable[MAX_COLS];
    SQLCHAR *      ColumnData[MAX_COLS];
    SQLLEN         ColumnDataLen[MAX_COLS];
    SQLSMALLINT    i,j;
    char printout[LENGTH], printtemp[LENGTH];
    char execute66[LENGTH], view1[LENGTH], view2[LENGTH], view3[LENGTH];
    
    for (i=0;i<MAX_COLS;i++) {
            ColumnName[i]=NULL;
            ColumnData[i]=NULL;
        }
    sprintf(view1, "CREATE OR REPLACE VIEW listofrentings AS\
                                SELECT category_id, count(category_id) \
                                FROM film_category, (\
                                        SELECT film_id\
                                        FROM rental, inventory\
                                        WHERE\
                                        rental.customer_id = %i AND\
                                        rental.inventory_id = inventory.inventory_id) AS CustomerRented\
                                WHERE CustomerRented.film_id = film_category.film_id\
                                GROUP BY\
                                    category_id\
                                ORDER BY count DESC\
                                ;", customer_id);
        sprintf(view2, "CREATE OR REPLACE VIEW CustomerFavorite AS\
                                SELECT listofrentings.category_id\
                                FROM listofrentings, (SELECT count FROM listofrentings LIMIT 1) AS MAX\
                                WHERE listofrentings.count = MAX.count\
                                ;");
        sprintf(view3, "CREATE OR REPLACE VIEW finalfilms AS\
                                SELECT film_id\
                                FROM (\
                                    SELECT film_category.film_id, count(rental.inventory_id)\
                                    FROM film_category, inventory, rental, CustomerFavorite\
                                    WHERE\
                                    film_category.category_id = CustomerFavorite.category_id AND\
                                    film_category.film_id = inventory.film_id AND\
                                    inventory.inventory_id = rental.rental_id\
                                    GROUP BY\
                                    film_category.film_id\
                                    ORDER BY\
                                    count DESC) AS x\
                                EXCEPT (SELECT film_id\
                                    FROM rental, inventory\
                                    WHERE\
                                        rental.customer_id = %i AND\
                                        rental.inventory_id = inventory.inventory_id)\
                                LIMIT 3\
                                ;", customer_id);
        sprintf(execute66, "SELECT finalfilms.film_id, film.title, category.name as category_name\
                            FROM finalfilms, film, film_category, category\
                            WHERE finalfilms.film_id = film.film_id AND\
                                film_category.film_id = finalfilms.film_id AND\
                                film_category.category_id = category.category_id\
                            ");
        /*PREPARE QUERY*/
           SQLPrepare(stmt, (SQLCHAR*)view1, SQL_NTS);
           SQLExecute(stmt);
           SQLPrepare(stmt, (SQLCHAR*)view2, SQL_NTS);
           SQLExecute(stmt);
           SQLPrepare(stmt, (SQLCHAR*)view3, SQL_NTS);
           SQLExecute(stmt);
           SQLPrepare(stmt, (SQLCHAR*)execute66, SQL_NTS);

        /*OBTAIN NUMBER OF COLUMNS*/
            ret = SQLNumResultCols (stmt, &numCols);
        /*OBTAIN DATA FROM COLUMNS AND BINDING IT*/
            for (i=0;i<numCols;i++) {
                ColumnName[i] = (SQLCHAR *) malloc (LENGTH);
                if(ColumnName[i]==NULL) {
                    /*FREE*/
                        SQLFreeHandle(SQL_HANDLE_STMT, stmt);
                    /* DISCONNECT */
                        ret = odbc_disconnect(env, dbc);
                        if (!SQL_SUCCEEDED(ret)) {
                            return EXIT_FAILURE;
                        }
                    return EXIT_FAILURE;
                }
                /*I FILL ALL THE ARRAYS WITH THE VARIABLES USED FOR THE BINDING FUNCTION*/
                ret = SQLDescribeCol (
                            stmt,                    /* Select Statement (Prepared)*/
                            i+1,                      /* Columnn Number */
                            ColumnName[i],            /* Column Name (returned) */
                            MAX_COL_NAME_LEN,         /* size of Column Name buffer*/
                            &ColumnNameLen[i],        /* Actual size of column name*/
                            &ColumnDataType[i],       /* SQL Data type of column*/
                            &ColumnDataSize[i],       /* Data size of column in table*/
                            &ColumnDataDigits[i],     /* Number of decimal digits*/
                            &ColumnDataNullable[i]);  /* Whether column nullable*/

                /*I TRANSFORM THE SQL TYPES TO C TYPES*/
                ColumnData[i] = (SQLCHAR *) malloc (ColumnDataSize[i]+1);
                if(ColumnData[i]==NULL) {
                    /*FREE*/
                        SQLFreeHandle(SQL_HANDLE_STMT, stmt);
                    /* DISCONNECT */
                        ret = odbc_disconnect(env, dbc);
                        if (!SQL_SUCCEEDED(ret)) {
                            return EXIT_FAILURE;
                        }
                    return EXIT_FAILURE;
                }
                switch (ColumnDataType[i]) {
                    case SQL_SMALLINT:
                        ColumnDataType[i]=SQL_C_CHAR;
                    break;
                    case SQL_INTEGER:
                        ColumnDataType[i]=SQL_C_LONG;
                    break;
                    case SQL_VARCHAR:
                        ColumnDataType[i]=SQL_C_CHAR;
                    break;
                }
                /*I BIND WITH THE PRIEVIOUSLY RETRIEVED DATA*/
                ret = SQLBindCol (stmt,                  /* Statement handle*/
                                i+1,                    /* Column number*/
                                ColumnDataType[i],      /* C Data Type*/
                                ColumnData[i],          /* Data buffer*/
                                ColumnDataSize[i],      /* Size of Data Buffer*/
                                &ColumnDataLen[i]); /* Size of data returned*/
            }
         SQLExecute(stmt);
        /*PRINT COLUMNS*/
            printf("|");
            for (j=0;j<numCols;j++) {
                if(j==0) printf("%7s|", ColumnName[j]);
                else printf("%20s|", ColumnName[j]);
            }
            printf("\n");
            for(i=0; i<7+2+20*2+2; i++){printf("_");}
        /*PRINT THE RESULT*/
            for (i=0; ; i++) {
                if(!SQL_SUCCEEDED( ret = SQLFetch(stmt) )) break;

                /*END OF OUTPUT*/
                if (ret == SQL_NO_DATA) break;
                
                /*PRINT OUTPUT*/
                printout[0]='\0';
                printf("\n");
                sprintf(printtemp,"|");
                strcat(printout,printtemp);
                for (j=0;j<numCols;j++) {
                    if(j==0) sprintf(printtemp,"%7s|", ColumnData[j]);
                    else if (ColumnDataType[j]==SQL_INTEGER) sprintf(printtemp,"%20i|", (int)*ColumnData[j]);
                    else sprintf(printtemp,"%20s|", ColumnData[j]);
                    strcat(printout,printtemp);
                }
                printf("%s", printout);

                }  
            printf("\n");
            for(i=0; i<7+2+20*2+2; i++){printf("_");}
            printf("\n");

        /*FREE*/
            for(j=0; j<numCols; j++){
                if(ColumnName[j])free(ColumnName[j]);
                if(ColumnData[j])free(ColumnData[j]);
            }
        return EXIT_SUCCESS;
}