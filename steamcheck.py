import os
import requests

drives = ['C:', 'D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 'M:', 'N:', 'O:', 'P:', 'Q:', 'R:', 'S:', 'T:', 'U:', 'V:', 'W:', 'X:', 'Y:', 'Z:']

steam_user_data_folder = None

def search_userdata_folder(root_folder):
    for root, dirs, files in os.walk(root_folder):
        if "Steam" in dirs:
            steam_path = os.path.join(root, "Steam")
            for steam_root, steam_dirs, steam_files in os.walk(steam_path):
                if "userdata" in steam_dirs:
                    return os.path.join(steam_root, "userdata")
    return None

for drive in drives:
    userdata_folder = search_userdata_folder(drive)
    if userdata_folder:
        steam_user_data_folder = userdata_folder
        break

def check_steam_accounts():
    if steam_user_data_folder is None:
        print("Steam 'userdata' folder not found on this computer.")
        return
    
    accounts = os.listdir(steam_user_data_folder)
    print(f'Всего аккаутов: ', len(accounts))
    for account_id in accounts:
        steam_id64 = int(account_id) + 76561197960265728
        print('----------------------------------')
        print(f"Steam ID64: {steam_id64}")

        def get_player_summary(steam_id64, api_key):
            url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id64}'
            response = requests.get(url)
            data = response.json()
            player_data = data['response']['players'][0]
            
            player_info = {
                'avatar': player_data.get('avatarmedium'),
                'account_name': player_data.get('personaname'),
                'vac_bans': player_data.get('NumberOfVACBans')
            }
            
            return player_info

        api_key = 'YOUR STEAM API CODE HERE '

        player_info = get_player_summary(steam_id64, api_key)
        print("Аватар:", player_info['avatar'])
        print("Имя аккаунта:", player_info['account_name'])
        print("Количество VAC банов:", player_info['vac_bans'])
        
check_steam_accounts()
