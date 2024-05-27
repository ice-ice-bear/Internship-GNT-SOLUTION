import subprocess

network_path = r'//192.168.0.77:8082//C:/Users/gnt/Desktop/release/번호판분석서버.exe'

try:
    subprocess.call(network_path)
    print("Exe file executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error occurred while executing the exe file: {e}")

