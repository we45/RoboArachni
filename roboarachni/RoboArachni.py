from robot.api import logger
import requests
import json
import os
import sys
reload(sys)
sys.setdefaultencoding('UTF8')
import time
import subprocess
import psutil


class RoboArachni(object):
	ROBOT_LIBRARY_SCOPE = 'GLOBAL'

	def __init__(self):
		self.results = None
		self.process_id = []

	def start_arachni_restserver(self, arachni_path):
		try:
			proc = subprocess.Popen(arachni_path.split(),stdout=open(os.devnull, 'w'),stderr=subprocess.STDOUT)
			time.sleep(30)
			self.process_id.append(proc.pid)
		except BaseException as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))


	def start_arachni_proxy(self, target, proxy_port):
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
						"csrf", "file_inclusion", "ldap_injection", "no_sql_injection", "no_sql_injection_differential", 
						"os_cmd_injection", "os_cmd_injection_timing", "path_traversal", "response_splitting", "rfi", 
						"session_fixation", "source_code_disclosure", "sql_injection", "sql_injection_differential", 
						"sql_injection_timing", "trainer", "unvalidated_redirect", "unvalidated_redirect_dom", "xpath_injection",
						"xss", "xss_dom", "xss_dom_script_context", "xss_event", "xss_path", "xss_script_context", "xss_tag", "xxe", 
						"allowed_methods", "backdoors", "backup_directories", "backup_files", "captcha", "common_admin_interfaces", 
						"common_directories", "common_files", "cookie_set_for_parent_domain", "credit_card", "cvs_svn_users", 
						"directory_listing", "emails", "form_upload", "hsts", "htaccess_limit", "html_objects", "http_only_cookies", 
						"http_put", "insecure_client_access_policy", "insecure_cookies", "insecure_cors_policy", 
						"insecure_cross_domain_policy_access", "insecure_cross_domain_policy_headers", "interesting_responses", 
						"localstart_asp", "mixed_resource", "origin_spoof_access_restriction_bypass", "password_autocomplete", 
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
				'plugins': {'proxy': {'bind_address': '0.0.0.0', 'port': int(proxy_port)}},
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
			requests.post('http://127.0.0.1:7331/scans', json=data)
		except BaseException as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))


	def get_arachni_scanid(self):
		try:
			r = requests.get('http://127.0.0.1:7331/scans')
			if r.status_code == 200:
				for k,v in r.json().iteritems():
					return str(k)
			else:
				return None
		except BaseException as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))


	def initiate_scan(self, proxy_port):
		try:
			arachni_id = self.get_arachni_scanid()
			if arachni_id:
				arachni_session = requests.Session()
				arachni_proxy = {'http': 'http://127.0.0.1:{0}'.format(proxy_port)}
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
					r = requests.get('http://127.0.0.1:7331/scans/{0}/summary'.format(arachni_id))
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
				r = requests.get('http://127.0.0.1:7331/scans/{0}/report.json'.format(arachni_id))
				with open('arachni_report.json', 'w') as f:
					json.dump(r.json(), f)
		except BaseException as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))


	def delete_scan(self):
		try:
			for p_id in self.process_id:
				psutil.Process(p_id).terminate()
		except BaseException as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			logger.info('Error: {0} {1}'.format(e, exc_traceback.tb_lineno))

