#include <syslog.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#define LOGNAME "miniserver"


void log_ini() {
    /* Inicializamos el LOGGER */
    umask(0);
    setlogmask(LOG_UPTO(LOG_INFO));

    /* Abrimos el LOG y escribimos */
    openlog(LOGNAME, LOG_PID | LOG_CONS | LOG_PID | LOG_NDELAY, LOG_LOCAL3);
    syslog(LOG_INFO, "Initiating new server.");
}


void log_error(char *error, int errno_code) {
    /* Abrimos el LOG, escribimos y lo cerramos */
    openlog(LOGNAME, LOG_PID | LOG_CONS | LOG_PERROR, LOG_DAEMON);
    syslog(LOG_ERR, "%s: %s", error, strerror(errno_code));
    closelog();
}


void log_error_msg(char *error) {
    /* Abrimos el LOG, escribimos y lo cerramos */
    openlog(LOGNAME, LOG_PID | LOG_CONS | LOG_PERROR, LOG_DAEMON);
    syslog(LOG_ERR, "%s", error);
    closelog();
}


void log_msg(char *msg) {
    /* Abrimos el LOG, escribimos y lo cerramos */
    openlog(LOGNAME, LOG_PID | LOG_CONS | LOG_PID | LOG_NDELAY, LOG_LOCAL3);
    syslog(LOG_INFO, "%s",msg);
    closelog();
}


void log_msg_and_info(char *msg, char *info) {
    /* Abrimos el LOG, escribimos y lo cerramos */
    openlog(LOGNAME, LOG_PID | LOG_CONS | LOG_PID | LOG_NDELAY, LOG_LOCAL3);
    syslog(LOG_INFO, "%s: %s\n",msg, info);
    closelog();
}


void log_msg_and_info_int(char *msg, int info) {
    /* Abrimos el LOG, escribimos y lo cerramos */
    openlog(LOGNAME, LOG_PID | LOG_CONS | LOG_PID | LOG_NDELAY, LOG_LOCAL3);
    syslog(LOG_INFO, "%s: %d\n",msg, info);
    closelog();
}