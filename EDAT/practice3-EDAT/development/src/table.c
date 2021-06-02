/*
    Project: EDAT Lab 3 test program
    File:    table.h
    Author:  Simone Santini
    Rev.     1.0
    Date:    10/13/2019  (check it out: it's Sunday! 
                          and I am here, working for you.
                          Praise to the commmitted professor.)
    
    File in which YOU (Yes: you!) have to implement the functions defined in 
    the file table.h. The functions are defined in this file, but they are 
    elft empty or return dummy values. It is up to you to implement them
    to guarantee the functionality expressed in table.h 
*/
#include "table.h"
#include "type.h"



/*
    This is the structure that contains the data relative to a table. You 
    have to implement it. Keep in mind that all the information about the table 
    that the functions have is in this structure, so you must put in there 
    all that is needed for the correct work of the functions.
*/

struct table_ {
    long currentpos;
    void* record;
    int length;
    long firstpos;
    long lastpos;


    int numCols;
    type_t* types;

    char* path;
};

/* 
    void table_create(char* path, int ncols, type_t* types);

    Stores an empty table in a newly created file.

    Note that this function does not return any value nor does it do anything 
    in memory. It creates a new file, stores in it a header that indicates
    the number of columns, the types of these columns, and that the table 
    has 0 records. Then closes the file and returns.
    
    Parameters:
    path:    path name (referred to the current directory) of the file
             where the table is to be stored.
    ncols:   number of columns of the table.
    types:   array of ncols elements of type type_t with the type of each
             one of the columns (see type.h and type.c for details on the 
             types recognized by the table).
    
    Returns:
        1: table created
        0: error in creation
    
    WARNING: if the file specified in path already exists, this function
    erases it and creates a new one. That is, all the data contained in the 
    file will be lost.
*/
int table_create(char* path, int ncols, type_t* types) {
    void* ptr = NULL;
    FILE* filept = NULL;
    int flag=0, i=0;

    if (!path || ncols<1 || !types) return 0;
    filept = fopen(path, "w");
    if(!filept) return 0;

    flag = fwrite(&ncols, sizeof(int), 1, filept);
    if(flag<1) {fclose(filept);
                return 0;}
    
    flag = fwrite(types, sizeof(int), ncols, filept);
    if(flag<1) {fclose(filept);
                return 0;}
    fclose(filept);
    return 1;
}

/*
    table_t* table_open(char* path)
    
    Opens a table and returns the structure necessary to use it. The file
    <path> must exist for this function to succeeds. This functions 
    allocates a table_t structure and fills in the necessary fields so that
    the other functions defined here can operate on the table.
    
    Parameters: 
    path:   path name (referred to the current directory) of the file
            where the table is stored. The file must exist.
            
    Returns:
    A pointer to a newly allocated table_t structure with the information
    necessary to operate on the table (the table is NOT read in memory), or 
    NULL is the file <path> does not exist.
    
    NOTE: The calling program should not release the structure returned
    by this function. Use table_close instead.

*/
table_t* table_open(char* path) {
    void* ptr = NULL;
    FILE* filept = NULL;
    int flag=0, ncols=0;
    table_t* newtable = NULL;
    type_t* types=NULL;

    if (!path) return NULL;
    filept = fopen(path, "r");
    if(!filept) return NULL;
    newtable = (table_t*)malloc(sizeof(table_t));
    if(!newtable){
        fclose(filept);
        return NULL;
    }
    newtable->length=0;
    newtable->currentpos=0;
    newtable->record=NULL;
    newtable->types=NULL;
    newtable->path=path;
    flag = fread(&(newtable->numCols), sizeof(int), 1, filept);
    if(flag<0){
        fclose(filept);
        free(newtable);
        return NULL;
    }
    if((newtable->numCols)<1) {
        fclose(filept);
        free(newtable);
        return NULL;
    }
    newtable->types = (type_t*)malloc(sizeof(type_t)*(newtable->numCols));
    if(!(newtable->types)) {
        fclose(filept);
        free(newtable);
        return NULL;
    }
    
    flag = fread(newtable->types, sizeof(int), newtable->numCols, filept);
    if(flag<0){
        fclose(filept);
        free(newtable->types);
        free(newtable);
        return NULL;
    }
    newtable->firstpos = sizeof(int) + (sizeof(int))*(newtable->numCols);
    fseek(filept, 0L, SEEK_END); 
    newtable->lastpos = ftell(filept);
    
    fclose(filept);

    return newtable; 
}

/* 
    void table_close(table_t* table);
    
    Closes a table freeing all the resources allocated. This function must 
    leave the whole system in the state it was before the table was opened:
    all files closed, all memory released.
    
    Note that after calling this function, it will no longer be possible
    to operate on the table <table>.
    
    Parameters:
    table:  The table that we eant to close.
    
    Returns:
        Nothing
*/

void table_close(table_t* table) {
    int i=0;
    if(!table) return;
    if(table->record) free(table->record);
    if(table->types) free(table->types);
    free(table);
    return;
}

/* 
    int table_ncols(table_t* table);

    Returns the number of columns of the table <table>
    
    Parameters:
    table:  The table on which we want to operate.
    
    Returns:
        n>0:    The table has n columns
        n<0:    Incorrect parameter
*/
int table_ncols(table_t* table) {
    if(!table) return -1;
    return table->numCols;
}


/* 
    type_t*table_types(table_t* table);
    
    Returns an array containing the types of the columns of the table 
    <table>.

    Parameters:
    table:  The table on which we want to operate.
    
    Returns:
    An array of table_ncols(table) element. Each element is of type type_t, 
    and contains the type of the corresponding column. For the definition 
    of type_t, see the file type.h/type.c. Returns NULL if the parameter 
    is invalid.
    
    WARNING: The array that is returned is not a copy of the one used 
    internally by these functions, but a pointer to the same array. The 
    caller should not free the pointer returned by this function nor 
    should it modify it in any way.
*/
type_t*table_types(table_t* table) {
    if(!table) return NULL;

    return table->types;
}

/* 
    long table_first_pos(table_t* table);

    Returns the position of the file where the first record begin. Calling 
    table_read_record with this value as position will result in reading
    the first record of the table (see the example at the beginning of this 
    file.
    
    Parameters:
    table:  The table on which we want to operate.
    
    Returns:
    n>0:    the first record begins at position n in the file
    n<0:    error in the parameter
*/
long table_first_pos(table_t* table) {
    if(!table) return -1;

    return table->firstpos;
}

/* 
    long table_last_pos(table_t* table);

    Returns the last position of the file, that is, the position where a new
    record will be inserted upon calling table_insert_record. Note that 
    table_insert_record does not use this function, which is used simply to
    give information to the calling program.

    Parameters:
    table:  The table on which we want to operate.
    
    Returns:
    n>0:    the new record begins at position n in the file
    n<=0:   error in the parameter
*/
long table_last_pos(table_t* table) {
    if(!table) return -1;
    
    return table->lastpos;
}

/* 
    long table_read_record(table_t* table, long pos);
     
    Reads a record that begins at a given position in the table file. 

    Parameters:
    table:  The table on which we want to operate.
    pos:    Position in the file where the record begins. The pos-th byte
            in the file must be the beginning of a record; if it is not, the 
            result of the call will be unpredictable.
            
    Returns:
    n>0:     The next record in the file begins at position n 
    n<0:     No record read, we had already reached the end of the file 
    
    Note: this function reads the record, but it returns no data from that 
    record. Use the function table_get_col to read the data of the record 
    after it has been read.
*/
long table_read_record(table_t* t, long pos) {
    FILE *file=NULL;
    int flag=0;
    if(!t || pos<0) return -1;
    
    if(pos >= t->lastpos) return -1;

    file = fopen(t->path, "r");
    if(!file) return -1;

    if(t->record) free(t->record);
    t->record=NULL;

    fseek(file, pos, SEEK_SET);
    flag = fread(&(t->length), sizeof(int), 1, file);
    if(flag<1) {fclose(file);
                    return 0;}

    t->record = (char*) malloc (t->length*sizeof(char));
    if(!(t->record)){fclose(file);
                    return 0;}
                    
    flag = fread(t->record, sizeof(char), t->length, file);
    if(flag<1) {fclose(file); free(t->record);  
                    return 0;}
	fclose(file);
    t->currentpos = pos;
    return pos+(t->length)+sizeof(int);
}


/*
    void *table_get_col(table_t* table, int col)
    
    Returns the pointer to the data contained in the col-th column of the 
    record currently in memory. The record must have been previously read
    using table_read_record. If no record was read in memory, the result
    will be unpredictable.

    Parameters:
    table:  The table on which we want to operate.
    col:    The column that we want to read, 0<=col<ncol,
    
    Returns:
    A pointer to the data that is contained in the column, or NULL if the 
    column number is out of range. The way the data are interpreted 
    depends on the type of the column, as specified by the col-th element
    of the array returned by table_types (see the example at the beginning
    of the file).
*/

void *table_get_col(table_t* table, int col) {
    
    int i;
    int index=0;
    char *string=NULL;

    if(!table || 0>col || col>table->numCols ){
      return NULL;
    }
    
    for(i=0;i<col;i++){
        if(table->types[i]==INT) index += sizeof(int);
        else if(table->types[i]==STR) index += (1+strlen(index + table->record)) * sizeof(char);
        else if(table->types[i]==LLNG) index += sizeof(long long);
        else if(table->types[i]==DBL) index += sizeof(double);
        else return NULL;
        
    }
    
    if(table->types[col] == STR){
        string = (char*)malloc(sizeof(char) * strlen(table->record + index) +1);
        if(!string) return NULL;

        strcpy(string, table->record + index);
        return string;
    }
    return table->record + index;
}

/*  void table_insert_record(table_t* table, void** values);

    Inserts a record at the end of the file given the pointers to the 
    values of each column. 
    
    Parameters:
    table:  The table on which we want to operate.
    values: Array of ncol pointers to the data that are to be stored in the 
            record. The element values[i] must be a pointer to a datum of the 
            same type as the i-th column of the file. If this constraint is 
            not respected, the results will be unpredictable.
    
    Returns:
    1: inserted OK 
    0: error
*/
int table_insert_record(table_t* t, void** values) {
    int i=0, flag=0, newlastpos=0;
    FILE *file=NULL;
    if(!t || !values) return 0;

    file = fopen(t->path, "a");
    if(!file) return 0;
    for(i=0; i<(t->numCols); i++){
        if(t->types[i] == INT) newlastpos += sizeof(int);
        else if(t->types[i] == LLNG) newlastpos += sizeof(long long);
        else if(t->types[i] == DBL) newlastpos += sizeof(double);
        else if(t->types[i] == STR) newlastpos += (strlen(values[i])+1)*sizeof(char);
    }

    flag = fwrite(&newlastpos, sizeof(int), 1, file); 
    if(flag<1) {fclose(file);
                    return 0;}
    for(i=0; i<(t->numCols); i++){
        if(t->types[i]==INT)       flag = fwrite(values[i], sizeof(int), 1, file); 
        else if(t->types[i]==LLNG) flag = fwrite(values[i], sizeof(long long), 1, file); 
        else if(t->types[i]==DBL)  flag = fwrite(values[i], sizeof(double), 1, file); 
        else if (t->types[i]==STR) flag = fwrite(values[i], sizeof(char), strlen(values[i])+1, file);
                                    
                                    
        if(flag<1) {fclose(file);
                    return 0;}
    }
    t->lastpos += newlastpos+sizeof(int);

    fclose(file);
    return 1;
} 
