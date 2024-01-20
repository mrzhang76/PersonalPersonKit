import logging 
import os 
import time 

current_time = time.strftime('%Y_%m_%d',time.gmtime())
current_path = os.path.dirname(__file__)
if not os.path.exists("logs/"):
    os.makedirs("logs/")
log_path = current_path + '/logs/test_' + current_time + '.log'
logger = logging.getLogger(__name__)

class log():
    def __init__(self,logfile_path = log_path):
        self.logfile_path = logfile_path
    
    def print_file_log(self,level,message):
        file_log = logging.FileHandler(log_path)
        logger.setLevel(level = logging.DEBUG)
        formatter = logging.Formatter(
            fmt= '[%(asctime)s.%(msecs)03d] %(filename)s:%(lineno)d [%(levelname)s]: %(message)s',
            datefmt = '%Y-%m-%d %H:%M:%S'
        )
        file_log.setFormatter(formatter)

        console = logging.StreamHandler()
        console.setLevel(level = logging.DEBUG)
        logger.addHandler(file_log)
        logger.addHandler(console)

        if level == 'info': logger.info(message)
        elif level == 'debug': logger.debug(message)
        elif level == 'warning': logger.warning(message)
        elif level == 'error': logger.error(message)

        logger.removeHandler(file_log)
        logger.removeHandler(console)
        file_log.close()
        console.close()

    def info(self,message):
        self.print_file_log(message)

    def debug(self,message):
        self.print_file_log(message)

    def warning(self,message):
        self.print_file_log(message)

    def error(self,message):
        self.print_file_log(message)


if __name__ == '__main__':
    log = log()
    log.print_file_log('debug','debug')
    log.print_file_log('info','info')
    log.print_file_log('warning','warning')
    log.print_file_log('error','error')
    print(current_time)