import requests, json

class TelegramBot:
    def __init__(self, chat_id, token) -> None:
        self.__chat_id = chat_id
        self.__url     = f'https://api.telegram.org/bot{token}/'

    def get_updates(self):
        return self.__get_content(f'{self.__url}getUpdates')

    def get_last_message(self):
        return json.loads(self.get_updates()['result'][-1]['message'])

    def get_last_message_username(self):
        return json.loads(self.get_updates()['from']['username'])

    def send_message(self, text, buttons=None, one_time_keyboard=False):
        url = f'{self.__url}sendMessage?text={text}&chat_id{self.__chat_id}&parse_mode=Markdown'
        if buttons:
            keyboard = [[button] for button in buttons]
            url = f"{url}&reply_markup=json.dumps({'inline_keyboard': {keyboard}, 'one_time_keyboard': {one_time_keyboard}})"
        return self.__get_content(url)

    def get_file_content(self, file_id):
        file_path = json.loads(self.__get_content(f'{self.__url}getFile?file_id={file_id}'))['result']['file_path']
        return self.__get_content(f'{self.__url}{file_path}')

    def save_file(self, file_content, file_name):
        with open(file_name, 'wb') as file:
            file.write(file_content.content)

    def __get_content(self, url):
        response = requests.get(url)
        return response.content.decode('utf8')

    #def __create_buttons(self, buttons, one_time_keyboard):
    #    keyboard = [[button] for button in buttons]
    #    return json.dumps({'inline_keyboard': keyboard, 'one_time_keyboard': one_time_keyboard})
