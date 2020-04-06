#!/usr/bin/env python
import sys
from zabbix.api import ZabbixAPI

def check_input():
    if len(sys.argv) < 8:
        print '\nERROR: Missing arguments:'
        print '\nProper usage ./update_host.py \'https://zabbix_host_api\' \'username\' \'password\' \'host|tempalte\' \'host_name|template_name\' \'psk_agent_identity\' \'psk_key\' \n' 
        sys.exit(1)  # abort because of error

def list_hosts():
    zbx_host = sys.argv[1]
    zbx_user = sys.argv[2]
    zbx_pass = sys.argv[3]
    zbx_filter = sys.argv[4]
    zbx_filter_value = sys.argv[5]
    zbx_psk_identity = sys.argv[6]
    zbx_psk = sys.argv[7]

    zapi = ZabbixAPI(url=zbx_host, user=zbx_user, password=zbx_pass)
    if zbx_filter == 'host':
        res1 = zapi.do_request('host.get', { 'search': { 'host': zbx_filter_value }, 'output': ['hostid','name']})
        hosts = res1.get(u'result')
    if zbx_filter == 'template':
        res1 = zapi.do_request('template.get', { 'filter': { 'host': zbx_filter_value }, 'selectHosts': 'extend', 'output': ['hostid','name']})
        hosts = res1.get(u'result')[0].get(u'hosts') 
    if zbx_filter == 'host' or zbx_filter == 'template':
        print('Following hosts will be updated:')
        for host in hosts:       
            print(host.get(u'name'))
        zapi.do_request('host.massupdate', {'hosts': hosts, 'tls_connect': 2, 'tls_accept': 2, 'tls_psk_identity': zbx_psk_identity, 'tls_psk': zbx_psk}) 

check_input()
list_hosts()
