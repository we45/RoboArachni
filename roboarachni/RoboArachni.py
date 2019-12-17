from robot.api import logger
import requests
import json
import sys
import docker
import time



class RoboArachni(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, rest_port = 7331, proxy_port=9090, arachni_username = "arachni", arachni_pw = "password"):
        self.results = None
        self.process_id = []
        self.rest_port = rest_port
        self.proxy_port = proxy_port
        self.username = arachni_username
        self.password = arachni_pw
        self.client = docker.from_env()   

    def start_arachni_docker(self):

        cobj = self.client.containers.run("arachni/arachni", ports = {'7331/tcp': self.rest_port, '9090/tcp': self.proxy_port}, detach=True)
        time.sleep(5)
        arachni_url = 'http://localhost:{0}'.format(self.rest_port)
        requests.get(arachni_url, auth = (self.username, self.password))
        self.container_id = cobj.id

    def start_arachni_proxy(self, target):
        try:
            data = {'audit': {
                'exclude_vector_patterns': [],
                'include_vector_patterns': [],
                'link_templates': [],
                'parameter_values': True
            },
                'authorized_by': None,
                'browser_cluster': {
                    'ignore_images': True,
                    'job_timeout': 25,
                    'pool_size': 6,
                    'screen_height': 1200,
                    'screen_width': 1600,
                    'wait_for_elements': {},
                    'worker_time_to_live': 100
                },
                'checks': ["code_injection", "code_injection_php_input_wrapper", "code_injection_timing",
                           "csrf", "file_inclusion", "ldap_injection", "no_sql_injection",
                           "no_sql_injection_differential",
                           "os_cmd_injection", "os_cmd_injection_timing", "path_traversal", "response_splitting", "rfi",
                           "session_fixation", "source_code_disclosure", "sql_injection", "sql_injection_differential",
                           "sql_injection_timing", "trainer", "unvalidated_redirect", "unvalidated_redirect_dom",
                           "xpath_injection",
                           "xss", "xss_dom", "xss_dom_script_context", "xss_event", "xss_path", "xss_script_context",
                           "xss_tag", "xxe",
                           "allowed_methods", "backdoors", "backup_directories", "backup_files", "captcha",
                           "common_admin_interfaces",
                           "common_directories", "common_files", "cookie_set_for_parent_domain", "credit_card",
                           "cvs_svn_users",
                           "directory_listing", "emails", "form_upload", "hsts", "htaccess_limit", "html_objects",
                           "http_only_cookies",
                           "http_put", "insecure_client_access_policy", "insecure_cookies", "insecure_cors_policy",
                           "insecure_cross_domain_policy_access", "insecure_cross_domain_policy_headers",
                           "interesting_responses",
                           "localstart_asp", "mixed_resource", "origin_spoof_access_restriction_bypass",
                           "password_autocomplete",
                           "private_ip", "ssn", "unencrypted_password_forms", "webdav", "x_frame_options", "xst"],
                'http': {
                    'cookies': {},
                    'request_concurrency': 20,
                    'request_headers': {},
                    'request_queue_size': 100,
                    'request_redirect_limit': 5,
                    'request_timeout': 10000,
                    'response_max_size': 500000,
                    'user_agent': 'Arachni/v2.0dev'
                },
                'no_fingerprinting': False,
                'platforms': [],
                'plugins': {'proxy': {'bind_address': '0.0.0.0', 'port': self.proxy_port}},
                'scope': {
                    'dom_depth_limit': 5,
                    'page_limit': 0,
                    'exclude_content_patterns': [],
                    'exclude_path_patterns': [],
                    'extend_paths': [],
                    'include_path_patterns': [],
                    'redundant_path_patterns': {},
                    'restrict_paths': [],
                    'exclude_file_extensions': ['gif', 'png', 'ico', 'bmp', 'jpeg', 'css', 'js'],
                    'url_rewrites': {}
                },
                'session': {},
                'url': target
            }
            res = requests.post('http://127.0.0.1:7331/scans', json=data, auth=(self.username, self.password))
            if res.status_code != 200:
                raise Exception("Unable to set proxy", res.content)
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))

    def get_arachni_scanid(self):
        try:
            r = requests.get('http://127.0.0.1:7331/scans', auth = (self.username, self.password))
            if r.status_code == 200:
                for k, v in r.json().iteritems():
                    return str(k)
            else:
                return None
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))

    def initiate_scan(self):
        try:
            arachni_id = self.get_arachni_scanid()
            if arachni_id:
                arachni_session = requests.Session()
                arachni_proxy = {'http': 'http://127.0.0.1:{0}'.format(self.proxy_port)}
                arachni_session.proxies.update(arachni_proxy)
                try:
                    arachni_session.get('http://Arachni.proxy/shutdown')
                except BaseException as e:
                    pass
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))

    def get_scan_status(self):
        try:
            arachni_id = self.get_arachni_scanid()
            if arachni_id:
                scan = True
                while scan:
                    r = requests.get('http://127.0.0.1:7331/scans/{0}/summary'.format(arachni_id), auth = (self.username, self.password))
                    if r.status_code == 200:
                        status = r.json().get('status')
                        if status == 'scanning':
                            status = {'status': 'Scanning'}
                            logger.info('{0}'.format(status))
                            time.sleep(10)
                        elif status == 'paused':
                            status = {'status': 'Paused'}
                            logger.info('{0}'.format(status))
                        elif status == 'done':
                            status = {'status': 'Completed'}
                            logger.info('{0}'.format(status))
                            scan = False
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))

    def get_results(self):
        try:
            arachni_id = self.get_arachni_scanid()
            if arachni_id:
                r = requests.get('http://127.0.0.1:7331/scans/{0}/report.json'.format(arachni_id), auth = (self.username, self.password))
                with open('arachni_report.json', 'w') as f:
                    json.dump(r.json(), f)
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))


    def stop_arachni_kill_container(self):
        target_container = self.client.containers.get(self.container_id)
        target_container.stop()


