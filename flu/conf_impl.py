# coding=utf-8

import os

from .log import setup_logger

import yaml

logger = setup_logger(__name__)

class ConfigDatabase(object):

    def __init__(self):
        self._db = {}

    def load_config(self, config_templates):
        for name, default in config_templates:
            if not name.replace('_', '').isalnum():
                raise Exception('config name [%s] is invalid , must consist of ALPHA or NUMBERS or UNDERLINE')
            self._db[name] = os.environ.get(name, default)
        self._load_from_config_file()

    def _load_from_config_file(self):
        if 'FLU_CONFIG_FILE' in self._db:
            if not self._db['FLU_CONFIG_FILE']:
                logger.info('config name FLU_CONFIG_FILE defined but value is empty, just fine?')
                return
            # 按照与flu文件夹平级路径拼出配置文件路径
            config_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', self._db['FLU_CONFIG_FILE'])
            config_filepath = os.path.abspath(config_filepath)
            if os.path.isfile(config_filepath):
                logger.info('load config from file : {}'.format(config_filepath))
                # 开始读取配置信息
                try:
                    config_data = yaml.load(open(config_filepath, 'r').read())
                except:
                    logger.warn('invalid config file format, should be yaml file')
                    return
                # 开始用配置文件中的内容来匹配环境变量名称
                for k in self._db:
                    slices = k.lower().split('_', 1)
                    if len(slices) == 2:
                        # eg. FLU_CONFIG_FILE => flu -> config_file
                        item_name, subitem_name = slices
                        item_data = config_data.get(item_name)
                        if isinstance(item_data, dict):
                            # try config_file
                            subitem_data = item_data.get(subitem_name)
                            if isinstance(subitem_data, (int, str, float)):
                                self._db[k] = str(subitem_data)
                                continue
                            # try flu_config_file
                            subitem_data = item_data.get(k.lower())
                            if isinstance(subitem_data, (int, str, float)):
                                self._db[k] = str(subitem_data)
                                continue
                    # eg. FLU_CONFIG_FILE => flu_config_file
                    item_data = config_data.get(slices[0])
                    if isinstance(item_data, (int, str, float)):
                        self._db[k] = str(item_data)
                        continue
            else:
                logger.warn('config file {} not found, maybe invalid environment variable?'.format(config_filepath))

    def __getattr__(self, name):
        val = self._db.get(name)
        if val is None:
            raise AttributeError('config name [%s] not found , try define it to environment variable'%(name))
        return val

    def put_config(self, name, value):
        if self._db.get(name) is None:
            raise AttributeError('config name [%s] not defined!' % (name))
        self._db[name] = value

conf = ConfigDatabase()

load_config = conf.load_config
