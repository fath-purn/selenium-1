from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
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
# chrome_options.add_experimental_option("detach", True)

# Inisialisasi Chrome service dan driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Buka 
driver.get("https://otakudesu.cloud/anime/2-5-jigen-sub-indo/")

# Tunggu sebentar agar halaman dimuat
time.sleep(2)

# Ambil elemen pagination
while True:
    try:
        # Cari pagination dan tombol next
        pagination = driver.find_element(By.CLASS_NAME, "pagenaxix")
        next_button = pagination.find_element(By.CLASS_NAME, "next")
        
        # Klik tombol next
        next_button.click()
        
        # Tunggu sebentar untuk memuat halaman berikutnya
        time.sleep(2)

        # Cari semua elemen anime
        anime_list = driver.find_elements(By.CSS_SELECTOR, "ul li div.thumb a")

        # Loop melalui setiap anime
        for anime in anime_list:
            try:
                # Pindah ke tab baru
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(2)
                
                # Ambil detail anime
                try:
                    # judul utama
                    judul = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
                    print(judul)
                    # poster
                    poster = driver.find_element(By.CSS_SELECTOR, "div.fotoanime img").get_attribute("src")
                    print(poster)

                    # info
                    for i in range(1, 12):
                        info = driver.find_element(By.CSS_SELECTOR, f"div.infozingle p:nth-child({i}) span").text.replace("\n", " ").strip()
                        print(info)

                    # sinopsis
                    sinopsis = driver.find_element(By.CSS_SELECTOR, "div.sinopc p").text.replace("\n", " ").strip()
                    print(sinopsis)

                    # episode list
                    # Cari semua elemen episode
                    episode_list = driver.find_elements(By.CSS_SELECTOR, "div.episodelist ul li")

                    # Loop melalui setiap episode
                    for episode in episode_list:
                        # Ambil judul dan link episode
                        judul = episode.find_element(By.CSS_SELECTOR, "span a").text.strip()
                        link = episode.find_element(By.CSS_SELECTOR, "span a").get_attribute("href")
                        rilis = episode.find_element(By.CSS_SELECTOR, "span.zeebr").text.strip()
                        print(f"Judul: {judul}")
                        print(f"Link: {link}")
                        print(f"Rilis: {rilis}")

                        # Buka link di tab baru
                        driver.execute_script(f"window.open('{link}', '_blank')")
                        time.sleep(2)    

                        # Pindah ke tab baru
                        driver.switch_to.window(driver.window_handles[-1])

                        try:
                            # judul
                            judul = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
                            print(judul)

                            # release
                            try:
                                posted = driver.find_element(By.CSS_SELECTOR, "div.kategoz")
                                posted_by = posted.find_element(By.CSS_SELECTOR, "span:nth-child(2)").text.strip()
                                release_time = posted.find_element(By.CSS_SELECTOR, "span:nth-child(4)").text.strip()
                                print(f"Posted by: {posted_by}")
                                print(f"Release time: {release_time}")
                            except:
                                print("Tidak dapat menemukan informasi release")

                            # Cari elemen video 
                            try:
                                video = driver.find_element(By.CSS_SELECTOR, "iframe").get_attribute("src")
                                print(video)
                            except:
                                print("Tidak dapat menemukan video")

                            # deskripsi
                            try:
                                deskripsiEpisode = driver.find_element(By.CSS_SELECTOR, "div.infozingle")
                                for desk in deskripsiEpisode:
                                    deskEpisode = desk.find_element(By.CSS_SELECTOR, "p span").text.replace("\n", " ").strip()
                                    print(deskEpisode)
                            except:
                                print("Tidak dapat menemukan deskripsi")

                        except Exception as e:
                            print(f"Terjadi error: {str(e)}")

                        # Tutup tab saat ini
                        driver.close()
                        
                        # Kembali ke tab utama
                        driver.switch_to.window(driver.window_handles[0])
                        time.sleep(1)

                    
                    

                except:
                    print("Gagal mengambil detail")
                    
                # Tutup tab dan kembali ke tab utama
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)


            except:
                continue


    
        
    except:
        # Jika tombol next tidak ditemukan, keluar dari loop
        print("Halaman terakhir telah dicapai")
        break








# Tutup browser
driver.quit()
