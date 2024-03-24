import logging, sys

logging.basicConfig(level='WARNING',
                    filename='my_log_for_U_Bot.log',
                    encoding='utf-8',
                    filemode='w',
                    format='[{asctime}] #{levelname:8} {filename}:'
                           '{lineno} - {name} - {message}',
                    style='{'
                    )

class My_DATA_LogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname == 'WARNING'

logger = logging.getLogger('LOGGER_BOSS')
logger.setLevel("WARNING")
file_handler = logging.FileHandler('my_log_for_U_Bot', mode='w', encoding='utf-8')
file_handler.addFilter(My_DATA_LogFilter())
logger.addHandler(file_handler)

std_out_logger = logging.getLogger('STD_out')
std_out_logger.setLevel("INFO")
std_out_handler = logging.StreamHandler(sys.stdout)
std_out_logger.addHandler(std_out_handler)

std_err_logger = logging.getLogger('ERR_out')
std_err_logger.setLevel("INFO")
std_err_handler = logging.StreamHandler(sys.stderr)
std_err_logger.addHandler(std_err_handler)