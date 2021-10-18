from app.core.config import settings
import os
import json
import errno
import subprocess as sp
import configparser
from functools import wraps
from loguru import logger
import traceback
import sys

DEFAULT_NEWRELIC_CONFIG_OUTPUT_DIR = '/var/app/config'

def _update_config(newrelic_conf_path, newrelic_license, newrelic_appname):
    if not os.path.exists(newrelic_conf_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), newrelic_conf_path)

    config = configparser.ConfigParser()
    config.read(newrelic_conf_path)

    config['newrelic']['license_key'] = newrelic_license
    config['newrelic']['app_name'] = newrelic_appname
    config['newrelic']['distributed_tracing.enabled'] = 'true'

    # remove env specific sections
    for section in ['newrelic:development', 'newrelic:test', 'newrelic:test', 'newrelic:production',
                    'newrelic:staging']:
        if config.has_section(section):
            config.pop(section, None)

    with open('/tmp/newrelinc.ini', 'w') as f:
        config.write(f)

    os.rename('/tmp/newrelinc.ini', newrelic_conf_path)


def wrap_exc(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        ret = 1
        try:
            ret = func(*args, **kwargs)
        except Exception:
            exc_type, exc_val, tb = sys.exc_info()
            err = {
                'exc_type': str(exc_type),
                'exc_val': str(exc_val),
                'exc_tb': traceback.format_tb(tb)
            }
            print(json.dumps(err))
        return ret

    return decorator


@wrap_exc
def setup_newrelic(newrelic_config_output_dir: str=None) -> int:
    """
    Args:
        config: config dict with newrelic key
        newrelic_config_output_dir: Directory where newrelic config file is generated

    Raises:
        IOError
        OSError
        ValueError
        sp.CalledProcessError

    Returns:
        0 on success, 1 on failure
    """
    newrelic_conf_path = '%s/%s' % (newrelic_config_output_dir, 'newrelic.ini')

    logger.info("create the output dir where newrelinc.ini should reside if doesn't exist already")
    os.makedirs(newrelic_config_output_dir, mode=0o766, exist_ok=True)

    logger.info("generate newrelic config")
    sp.check_output(['newrelic-admin', 'generate-config', settings.NEWRELIC_LICENSE, newrelic_conf_path])

    logger.info("update newrelic license and app_name")
    _update_config(newrelic_conf_path, settings.NEWRELIC_LICENSE, settings.NEWRELIC_APPNAME)

    return 0
