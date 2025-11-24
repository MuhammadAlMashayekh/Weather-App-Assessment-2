import json
import requests
from googleapiclient.discovery import build

weather_api_key = "59aca0d5837dad8c55aff93a6e3a5f28"
youtube_api_key = "AIzaSyByOr28In65N9pegHlV2DjT309de_WG-r8"
map_api_key = "PECFPNGQ"
news_api_key = "834a3ee8fbda4535a9b0fe5dba19d40f"

def get_weather(location,result = 10):
    URL_weather = f"https://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={weather_api_key}"
    x = requests.get(URL_weather)
    data = x.json()
   
    if data.get("cod") != 200:
        return {"error": data.get("message", "City not found")}

    weather_info = {
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
    
    }
    youtube = build("youtube", "v3", developerKey = youtube_api_key)
    request = youtube.search().list( part = "snippet", q = location, type = "video", maxResults = result)
    response = request.execute()
    results = []
    for item in response["items"]:
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        link = f"https://youtube.com/watch?v={video_id}"
        results.append({"title":title, "link":link})
    URL_news = f"https://newsapi.org/v2/everything?q={location}&language=en&sortBy=publishedAt&pageSize=10&apiKey={news_api_key}"
    y = requests.get(URL_news)
    data_news = y.json()
    news_results = []
    for article in data_news.get("articles", []):
        news_results.append({
            "title": article["title"],
            "source": article["source"]["name"],
            "url": article["url"]})
     
    return {"weather": weather_info, "youtube_results": results, "news_results": news_results}
    
def get_forecast(location, result = 10):
    URL_weather = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&units=metric&appid={weather_api_key}"
    x = requests.get(URL_weather)
    data = x.json()
    if data.get("cod") != "200":
        return {"error": data.get("message", "City not found")}, 404

    forecast_list = []
    for x in data["list"]:
        forecast_info = {
            "date": x["dt_txt"],
            "temperature": x["main"]["temp"],
            "description": x["weather"][0]["description"],
            "humidity": x["main"]["humidity"],
            "wind_speed": x["wind"]["speed"],
        }
        forecast_list.append(forecast_info)
    forecast= [row for row in forecast_list if row["date"].endswith("12:00:00")]
    youtube = build("youtube", "v3", developerKey = youtube_api_key)
    request = youtube.search().list( part = "snippet", q = location, type = "video", maxResults = result)
    response = request.execute()
    results = []
    for item in response["items"]:
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        link = f"https://youtube.com/watch?v={video_id}"
        results.append({"title":title, "link":link})
    URL_news = f"https://newsapi.org/v2/everything?q={location}&language=en&sortBy=publishedAt&pageSize=10&apiKey={news_api_key}"
    y = requests.get(URL_news)
    data_news = y.json()
    news_results = []
    for article in data_news.get("articles", []):
        news_results.append({
            "title": article["title"],
            "source": article["source"]["name"],
            "url": article["url"]})

    return {"forecast": forecast, "youtube_results": results, "news_results": news_results}
