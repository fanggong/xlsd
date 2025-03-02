import yaml


class Config:
    @classmethod
    def load_config(cls):
        with open('config.yml', 'r') as file:
            config = yaml.safe_load(file)
            return config

    @classmethod
    def get_mysql_url(cls):
        config = cls.load_config()['database']['mysql_own']
        return f"mysql+pymysql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"

    @classmethod
    def get_feishu_cfg(cls):
        config = cls.load_config()['feishu']
        return {
            'app_id': config['app_id'],
            'app_secret': config['app_secret']
        }
    
    @classmethod
    def get_ks_cfg(cls):
        config = cls.load_config()['ks']
        return {
            'app_key': config['app_key'],
            'app_secret': config['app_secret'],
            'sign_secret':config['sign_secret'], 
            'sign_method': config['sign_method']
        }
