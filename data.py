class Database:
    def __init__(self, file_name='base.txt'):
        self.file_name = file_name
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.file_name, 'r') as file:
                data = eval(file.read())
            return data
        except (FileNotFoundError, SyntaxError):
            return {}

    def save_data(self):
        with open(self.file_name, 'w') as file:
            file.write(str(self.data))

    def add_text(self, _id):
        self.data.setdefault(_id, {'text': 0, 'img': 0})
        self.data[_id]['text'] += 1
        self.save_data()

    def add_img(self, _id):
        self.data.setdefault(_id, {'text': 0, 'img': 0})
        self.data[_id]['img'] += 1
        self.save_data()

    def get_text(self, _id):
        return self.data.get(_id, {'text': 0, 'img': 0})['text']

    def get_img(self, _id):
        return self.data.get(_id, {'text': 0, 'img': 0})['img']

    def in_base(self, _id):
        return _id in self.data
