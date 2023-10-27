from speedtest import Speedtest
servers = []
threads = None
st =Speedtest()
st.get_servers(servers)
st.get_best_server(servers)
download_speed = round(st.download(threads=threads) / (10**6), 2)
upload_speed = round(st.upload(threads=threads) / (10**6), 2)

print(f"Download speed: {download_speed} Mbps")
print(f"Upload speed: {upload_speed} Mbps")
