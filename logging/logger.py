import logging.config
# 读取日志配置文件内容
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# 创建一个日志器logger
log = logging.getLogger('PTTKnock')