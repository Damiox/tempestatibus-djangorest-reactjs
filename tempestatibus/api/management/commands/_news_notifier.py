from django.conf import settings
from ._email_service import EmailService


# News Notifier
# Based on the Weather, it will send the proper notification via e-mail
class NewsNotifier:
    __weather = None
    __temp_curr = None
    __temp_diff_avg = None
    __is_precipitating = None

    def __init__(self, weather_data):
        self.__weather = weather_data.get_weather().lower()
        self.__temp_curr = weather_data.get_temp_curr()
        self.__temp_diff_avg = (
            weather_data.get_temp_high_avg()
            + weather_data.get_temp_low_avg()) / 2
        self.__is_precipitating = weather_data.get_precipitating() != 0

    def is_weather_sunny(self):
        return any(weather_type in self.__weather
                   for weather_type in ['sunny', 'clear', 'fair'])

    def is_weather_cloudy(self):
        return 'cloudy' in self.__weather

    def send_newsletter(self, receipt, city_name):
        imageAttachment = self.define_image_attachment()
        news = self.define_news()
        news_description = self.define_news_description(receipt, city_name)

        # Reading the newsletter from disk...
        with open('./tempestatibus/api' +
                  '/management/commands/templates/newsletter.txt') as file:
            news_txt = file.read()
        with open('./tempestatibus/api' +
                  '/management/commands/templates/newsletter.html') as file:
            news_html = file.read()

        # Building the newsletter txt and html version
        unsubscribe_url = settings.API_URL + '/unsubscribe/' + receipt
        news_txt = news_txt.format(receipt, city_name,
                                   self.__temp_curr, self.__weather,
                                   unsubscribe_url)
        news_html = news_html.format(news_description, unsubscribe_url)

        # Sending email...
        emailService = EmailService()
        emailService.send(receipt, news, news_txt, news_html, imageAttachment)

    def define_image_attachment(self):
        imageAttachment = None
        if self.is_weather_sunny():
            imageAttachment = './tempestatibus/static/images/sunny.png'
        elif self.is_weather_cloudy():
            imageAttachment = './tempestatibus/static/images/cloudy.png'
        else:
            imageAttachment = './tempestatibus/static/images/stayathome.png'
        return imageAttachment

    def define_news(self):
        news = None
        # Calculating the diff between
        # the current temperature and the historical average temperature
        temp_curr_diff = self.__temp_curr - self.__temp_diff_avg

        if self.is_weather_sunny() or temp_curr_diff >= 5:
            news = "It's nice out! Enjoy a discount on us."
        elif self.__is_precipitating is True or temp_curr_diff <= -5:
            news = "Not so nice out? That's okay, enjoy a discount on us."
        else:
            news = "Enjoy a discount on us."

        return news

    def define_news_description(self, receipt, city_name):
        news_description = ('Hi {}!' +
                            ' - Weather today for {} is {}' +
                            ' degrees, {}.').format(
                receipt, city_name, self.__temp_curr, self.__weather)
        return news_description
