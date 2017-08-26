# encoding:utf8
def get_ip_info(ip):
    import requests

    r = requests.get('http://ip.taobao.com/service/getIpInfo.php?ip=%s' % ip)
    if r.json()['code'] == 0:
        info = r.json()['data']

        country = info['country']
        area = info['area']
        region = info['region']
        city = info['city']
        isp = info['isp']

        print u'国家: %s\n区域: %s\n省份: %s\n城市: %s\n运营商: %s\n' % (country, area, region, city, isp)
    else:
        print "ERRO! ip: %s" % ip
    return info
