#ifndef LOG_H
#define LOG_H 

#define LOGNAME "miniserver"


/**
 * @brief Función para iniciar el loger
 * 
 */
void log_ini();


/**
 * @brief Función para logear un error
 * 
 * @param error Causante del error
 * @param errno_code Errno value
 */
void log_error(char *error, int errno_code);


/**
 * @brief Función para logear un msg
 * 
 * @param error Error a logear
 */
void log_error_msg(char *error);


/**
 * @brief Función para logear un msg
 * 
 * @param msg Mensaje a logear
 */
void log_msg(char *msg);


/**
 * @brief Función para logear un mensaje e información
 * 
 * @param msg Mensaje
 * @param info Información adicional
 */
void log_msg_and_info(char *msg, char *info);


/**
 * @brief Función para logear un mensaje e información,
 * siendo la información un número
 * 
 * @param msg Mensaje
 * @param info Información adicional
 */
void log_msg_and_info_int(char *msg, int info);


#endif