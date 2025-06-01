import requests

def get_random_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        if response.status_code == 200:
            data = response.json()[0]
            quote = f'"{data["q"]}" — {data["a"]}'
            return quote
        else:
            return "Không thể lấy dữ liệu."
    except Exception as e:
        return f"Lỗi: {e}"