# encoding:utf8
from flask import current_app


def get_ip_info(ip):
    import requests
    try:
        r = requests.get('http://ip.taobao.com/service/getIpInfo.php?ip=%s' % ip)
    except Exception as e:
        current_app.logger.error(e)

    if r.json()['code'] == 0:
        info = r.json()['data']

        country = info['country']
        area = info['area']
        region = info['region']
        city = info['city']
        isp = info['isp']

    else:
        current_app.logger.info("ERRO! ip: %s" + ip)
    return info
