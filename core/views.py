from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import folium
import matplotlib.pyplot as plt
import io, base64

def home(request):
    m = folium.Map(location=[23.8, 121], zoom_start=8, control_scale=True)

    df = pd.read_csv('core/dataset/yahoo_news_points_5days.csv', sep='|')
    df['date'] = pd.to_datetime(df['date'])

    city_keywords = ['台北','新北','桃園','臺中','臺南','高雄','新竹','苗栗','彰化','南投',
                     '雲林','嘉義','屏東','宜蘭','花蓮','臺東','澎湖','金門','連江','基隆']

    def extract_city(text):
        for city in city_keywords:
            if city in text:
                return city
        return '未知'

    df['city'] = df['content'].apply(extract_city)

    for city in city_keywords:
        city_data = df[df['city'] == city]
        if city_data.empty:
            continue

        # 繪製新聞數折線圖
        fig, ax = plt.subplots()
        date_counts = city_data['date'].value_counts().sort_index()
        date_counts.plot(kind='line', marker='o', ax=ax)
        ax.set_title('daily news count')
        ax.set_xlabel('date')
        ax.set_ylabel('news count')
        plt.xticks(rotation=45)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        img_html = f'<img src="data:image/png;base64,{img_base64}" width="450" height="350">'

        # Marker popup：顯示城市與圖表，點擊時自動載入新聞
        city_news = city_data.sort_values(by='date', ascending=False).head(5)
        news_titles = ''.join([
            f"<li>{row['date'].strftime('%m/%d')}: {row['title']}</li>"
            for _, row in city_news.iterrows()
        ])

        
        popup_html = f"""
        <div style="display: flex; gap: 10px; align-items: flex-start; max-width: 600px;">
            <div style="flex: 1;">
                <img src="data:image/png;base64,{img_base64}" width="300" height="250">
            </div>
            <div style="flex: 1;">
                <h6 style="margin-top: 0; font-size: 16px;">近期新聞：</h6>
                <ul style="font-size: 15px; padding-left: 18px; margin-top: 0;">
                    {news_titles}
                </ul>
            </div>
        </div>
        """

        lat = city_data.iloc[0]['latitude']
        lon = city_data.iloc[0]['longitude']

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=800)
        ).add_to(m)

    map_html = m._repr_html_()
    return render(request, 'home.html', {'map_html': map_html})


@csrf_exempt
def get_city_news_titles(request):
    city = request.GET.get('city')
    df = pd.read_csv('core/dataset/yahoo_news_points_5days.csv', sep='|')
    df['date'] = pd.to_datetime(df['date'])

    city_keywords = ['台北','新北','桃園','臺中','臺南','高雄','新竹','苗栗','彰化','南投',
                     '雲林','嘉義','屏東','宜蘭','花蓮','臺東','澎湖','金門','連江','基隆']

    def extract_city(text):
        for c in city_keywords:
            if c in text:
                return c
        return '未知'

    df['city'] = df['content'].apply(extract_city)
    city_data = df[df['city'] == city][['title', 'date']].sort_values(by='date', ascending=False)
    data = [{'date': row['date'].strftime('%m/%d'), 'title': row['title']} for _, row in city_data.iterrows()]

    return JsonResponse({'titles': data})
