from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

# Setup Chrome options
chrome_options = Options()
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

# Buka website
driver.get("https://otakudesu.cloud/anime/2-5-jimen-sub-indo/")

# List untuk menyimpan data anime
anime_data = []

# Fungsi untuk mengambil detail anime
def get_anime_details():
    try:
        anime_info = {}

        # Judul utama
        judul = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
        anime_info["judul"] = judul
        print("Judul:", judul)

        # Poster
        poster = driver.find_element(By.CSS_SELECTOR, "div.fotoanime img").get_attribute("src")
        anime_info["poster"] = poster
        print("Poster:", poster)

        # Info anime
        info_list = []
        for i in range(1, 12):
            try:
                info = driver.find_element(By.CSS_SELECTOR, f"div.infozingle p:nth-child({i}) span").text.replace("\n", " ").strip()
                info_list.append(info)
                print(f"Info {i}:", info)
            except:
                print(f"Info {i} tidak ditemukan")
        anime_info["info"] = info_list

        # Sinopsis
        sinopsis = driver.find_element(By.CSS_SELECTOR, "div.sinopc p").text.replace("\n", " ").strip()
        anime_info["sinopsis"] = sinopsis
        print("Sinopsis:", sinopsis)

        # Daftar episode
        episode_list = driver.find_elements(By.CSS_SELECTOR, "div.episodelist ul li")
        episodes = []
        for episode in episode_list:
            try:
                episode_info = {}

                judul_episode = episode.find_element(By.CSS_SELECTOR, "span a").text.strip()
                link_episode = episode.find_element(By.CSS_SELECTOR, "span a").get_attribute("href")
                rilis = episode.find_element(By.CSS_SELECTOR, "span.zeebr").text.strip()
                episode_info["judul_episode"] = judul_episode
                episode_info["link_episode"] = link_episode
                episode_info["rilis"] = rilis
                print(f"Judul Episode: {judul_episode}")
                print(f"Link Episode: {link_episode}")
                print(f"Rilis: {rilis}")

                # Buka link episode di tab baru
                driver.execute_script(f"window.open('{link_episode}', '_blank')")
                driver.switch_to.window(driver.window_handles[-1])

                # Ambil detail episode
                try:
                    judul_episode_detail = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
                    episode_info["judul_episode_detail"] = judul_episode_detail
                    print("Judul Episode Detail:", judul_episode_detail)

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
                        print("Informasi release tidak ditemukan")

                    # Video
                    try:
                        video = driver.find_element(By.CSS_SELECTOR, "iframe").get_attribute("src")
                        episode_info["video"] = video
                        print("Video:", video)
                    except:
                        print("Video tidak ditemukan")

                    # Deskripsi
                    try:
                        deskripsi = driver.find_element(By.CSS_SELECTOR, "div.infozingle p").text.replace("\n", " ").strip()
                        episode_info["deskripsi"] = deskripsi
                        print("Deskripsi:", deskripsi)
                    except:
                        print("Deskripsi tidak ditemukan")

                except Exception as e:
                    print(f"Error saat mengambil detail episode: {str(e)}")

                # Tutup tab episode
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                # Tambahkan episode ke list
                episodes.append(episode_info)

            except Exception as e:
                print(f"Error saat mengambil episode: {str(e)}")

        anime_info["episodes"] = episodes

        # Tambahkan anime ke list
        anime_data.append(anime_info)

    except Exception as e:
        print(f"Error saat mengambil detail anime: {str(e)}")

# Loop melalui pagination
while True:
    try:
        # Ambil detail anime di halaman saat ini
        get_anime_details()

        # Cari tombol "Next"
        next_button = driver.find_element(By.CSS_SELECTOR, "a.next")
        if "disabled" in next_button.get_attribute("class"):
            print("Halaman terakhir telah dicapai")
            break

        # Klik tombol "Next"
        next_button.click()

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