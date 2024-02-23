class Database:
        def __init__(self, file_name='base.lock'):
          try:
            self.file_name = file_name
            self.data = self.load_data()
          except Exception as e:
            print(f"!Database init-error: {e}")
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
            self.data.setdefault(_id, {'text': 0, 'img': 0, 'subscribe': 'free'})
            self.data[_id]['text'] += 1
            self.save_data()

        def add_img(self, _id):
            self.data.setdefault(_id, {'text': 0, 'img': 0, 'subscribe': 'free'})
            self.data[_id]['img'] += 1
            self.save_data()

        def pay_subscribe(self, _id):
            self.data.setdefault(_id, {'text': 0, 'img': 0, 'subscribe': 'free'})
            self.data[_id]['subscribe'] = 'premium'
            self.save_data()

        def free_subscribe(self, _id):
            self.data.setdefault(_id, {'text': 0, 'img': 0, 'subscribe': 'premium'})
            self.data[_id]['subscribe'] = 'free'
            self.save_data()

        def get_text(self, _id):
            return self.data.get(_id, {'text': 0, 'img': 0, 'subscribe': 'free'})['text']

        def get_img(self, _id):
            return self.data.get(_id, {'text': 0, 'img': 0, 'subscribe': 'free'})['img']

        def get_subscribe(self, _id):
            return self.data.get(_id, {'text': 0, 'img': 0, 'subscribe': 'free'})['subscribe']

        def in_base(self, _id):
            if _id in self.data:
                return True
            else:
                self.data.setdefault(_id, {'text': 0, 'img': 0, 'subscribe': 'free'})
                self.save_data()