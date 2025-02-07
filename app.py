from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Setup Chrome options
chrome_options = Options()
# Tambahkan opsi untuk menghindari deteksi
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')

# Hapus atau sembunyikan tanda-tanda otomasi
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Atur izin situs (block notifikasi, izin lokasi, dll.)
prefs = {
    "profile.default_content_setting_values.notifications": 2,  # Block notifikasi
    "profile.default_content_setting_values.geolocation": 2,    # Block lokasi
    "profile.default_content_setting_values.camera": 2,         # Block kamera
    "profile.default_content_setting_values.microphone": 2,     # Block mikrofon
}
chrome_options.add_experimental_option("prefs", prefs)

# Inisialisasi Chrome service dan driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Setelah inisialisasi driver, tambahkan script untuk menyembunyikan otomasi
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# Buka 
driver.get("https://otakudesu.cloud/complete-anime/")

# Tunggu sebentar agar halaman dimuat
time.sleep(2)

# List untuk menyimpan data anime
anime_data = []

# Fungsi untuk mengambil detail anime
def get_anime_details():
    try:
        anime_info = {}

        # Judul utama
        try:
            judul = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
            anime_info["judul"] = judul
            print("Judul:", judul)
        except:
            anime_info["judul"] = None
            print("Judul tidak ditemukan")

        # Poster
        try:
            poster = driver.find_element(By.CSS_SELECTOR, "div.fotoanime img").get_attribute("src")
            anime_info["poster"] = poster
            print("Poster:", poster)
        except:
            anime_info["poster"] = None
            print("Poster tidak ditemukan")

        # Info anime
        info_list = []
        for i in range(1, 12):
            try:
                info = driver.find_element(By.CSS_SELECTOR, f"div.infozingle p:nth-child({i}) span").text.replace("\n", " ").strip()
                info_list.append(info)
                print(f"Info {i}:", info)
            except:
                info_list.append(None)
                print(f"Info {i} tidak ditemukan")
        anime_info["info"] = info_list

        # Sinopsis
        try:
            sinopsis = driver.find_element(By.CSS_SELECTOR, "div.sinopc p").text.replace("\n", " ").strip()
            anime_info["sinopsis"] = sinopsis
            print("Sinopsis:", sinopsis)
        except:
            anime_info["sinopsis"] = None
            print("Sinopsis tidak ditemukan")

        # Daftar episode
        episode_list = driver.find_elements(By.CSS_SELECTOR, "div.episodelist ul li")
        episodes = []
        for episode in episode_list:
            try:
                episode_info = {}

                try:
                    judul_episode = episode.find_element(By.CSS_SELECTOR, "span a").text.strip()
                    episode_info["judul_episode"] = judul_episode
                    print(f"Judul Episode: {judul_episode}")
                except:
                    episode_info["judul_episode"] = None
                    print("Judul episode tidak ditemukan")

                try:
                    link_episode = episode.find_element(By.CSS_SELECTOR, "span a").get_attribute("href")
                    episode_info["link_episode"] = link_episode
                    print(f"Link Episode: {link_episode}")
                except:
                    episode_info["link_episode"] = None
                    print("Link episode tidak ditemukan")

                try:
                    rilis = episode.find_element(By.CSS_SELECTOR, "span.zeebr").text.strip()
                    episode_info["rilis"] = rilis
                    print(f"Rilis: {rilis}")
                except:
                    episode_info["rilis"] = None
                    print("Tanggal rilis tidak ditemukan")

                # Buka link episode di tab baru jika link ditemukan
                if episode_info["link_episode"]:
                    driver.execute_script(f"window.open('{episode_info['link_episode']}', '_blank')")
                    driver.switch_to.window(driver.window_handles[-1])

                    # Ambil detail episode
                    try:
                        judul_episode_detail = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
                        episode_info["judul_episode_detail"] = judul_episode_detail
                        print("Judul Episode Detail:", judul_episode_detail)
                    except:
                        episode_info["judul_episode_detail"] = None
                        print("Judul episode detail tidak ditemukan")

                    # Release info
                    try:
                        posted = driver.find_element(By.CSS_SELECTOR, "div.kategoz")
                        posted_by = posted.find_element(By.CSS_SELECTOR, "span:nth-child(2)").text.strip()
                        release_time = posted.find_element(By.CSS_SELECTOR, "span:nth-child(4)").text.strip()
                        episode_info["posted_by"] = posted_by
                        episode_info["release_time"] = release_time
                        print(f"Posted by: {posted_by}")
                        print(f"Release time: {release_time}")
                    except:
                        episode_info["posted_by"] = None
                        episode_info["release_time"] = None
                        print("Informasi release tidak ditemukan")

                    # Video
                    try:
                        video = driver.find_element(By.CSS_SELECTOR, "iframe").get_attribute("src")
                        episode_info["video"] = video
                        print("Video:", video)
                    except:
                        episode_info["video"] = None
                        print("Video tidak ditemukan")

                    # Deskripsi
                    try:
                        deskripsi = driver.find_element(By.CSS_SELECTOR, "div.infozingle p").text.replace("\n", " ").strip()
                        episode_info["deskripsi"] = deskripsi
                        print("Deskripsi:", deskripsi)
                    except:
                        episode_info["deskripsi"] = None
                        print("Deskripsi tidak ditemukan")

                    # Tutup tab episode
                    driver.close()
                    driver.switch_to.window(driver.window_handles[1])

                # Tambahkan episode ke list
                episodes.append(episode_info)

            except Exception as e:
                print(f"Error saat mengambil episode: {str(e)}")
                continue

        anime_info["episodes"] = episodes

        # Tambahkan anime ke list
        anime_data.append(anime_info)

        return True

    except Exception as e:
        print(f"Error saat mengambil detail anime: {str(e)}")
        return False

# Loop melalui pagination
while True:
    try:
        # Cari semua elemen anime
        anime_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul li div.thumb a"))
        )

        # Loop melalui setiap anime
        for anime in anime_list:
            try:
                # Pindah ke tab baru
                driver.execute_script(f"window.open('{anime.get_attribute('href')}', '_blank')")
                driver.switch_to.window(driver.window_handles[-1])
                
                # Tunggu hingga halaman dimuat
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
                )

                # Ambil detail anime dan tunggu hasilnya
                if not get_anime_details():
                    print("Gagal mendapatkan detail anime, melewati...")
                    continue

                # Tutup tab saat ini
                driver.close()  
                
                # Pindah ke tab baru
                driver.switch_to.window(driver.window_handles[0])

                # Tunggu sebentar sebelum lanjut ke anime berikutnya
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul li div.thumb a"))
                )

            except Exception as e:
                print(f"Error saat memproses anime: {str(e)}")
                continue


        # Cari tombol "Next"
        next_button = driver.find_element(By.CSS_SELECTOR, "a.next")
        if "disabled" in next_button.get_attribute("class"):
            print("Halaman terakhir telah dicapai")
            break

        # Buka link di tab baru
        driver.execute_script(f"window.open('{next_button.get_attribute('href')}', '_blank')")
        time.sleep(2)
        
        # Tutup tab saat ini
        driver.close()
        
        # Pindah ke tab baru
        driver.switch_to.window(driver.window_handles[0])

        # Tunggu halaman berikutnya dimuat
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))

    except Exception as e:
        print(f"Error saat navigasi pagination: {str(e)}")
        break

# Simpan data ke file JSON
with open("anime_data.json", "w", encoding="utf-8") as f:
    json.dump(anime_data, f, ensure_ascii=False, indent=4)

print("Data anime telah disimpan ke anime_data.json")

# Tutup browser
driver.quit()
