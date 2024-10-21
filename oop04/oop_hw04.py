import pickle 


# дескрипторы 
class Name:
    '''
    Дескриптор для имени. 
    Проверяет, чтобы имя было строкой длиной не менее 2 символов
    '''
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str) or len(value.strip()) < 2:
            raise ValueError('Имя должно быть строкой длиной не менее 2 символов')
        instance.__dict__[self.name] = value


class Age:
    '''
    Дескриптор для возраста. 
    Проверяет, чтобы возраст был числом от 1 до 99.
    '''
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, int) or not (0 < value < 100):
            raise ValueError('Возраст должен быть числом от 1 до 99')
        instance.__dict__[self.name] = value


class Phone:
    '''
    Дескриптор для номера телефона.
    Проверяет, чтобы номер состоял только из цифр и был длиной от 10 до 11 символов.
    '''
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str) or not value.isdigit() or not (10 <= len(value) <= 11):
            raise ValueError('Номер телефона должен содержать от 10 до 11 цифр')
        instance.__dict__[self.name] = value


class Pet:
    '''Питомец клиента'''
    name = Name()
    age = Age()

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.scheduled_appointment = None
        self.past_appointments = [] 

    def add_appointment(self, date):
        '''Добавляет дату приема'''
        if self.scheduled_appointment is not None:
            raise ValueError('Прием уже запланирован')
        self.scheduled_appointment = date

    def complete_appointment(self, comment):
        '''Завершает прием и сохраняет комментарий'''
        self.past_appointments.append({
            'date': self.scheduled_appointment,
            'comment': comment
        })
        self.scheduled_appointment = None

    def __str__(self):
        return f'Питомец {self.name}, возраст: {self.age}'


class Client:
    '''Клиент ветеринарной клиники'''
    name = Name()
    phone = Phone()

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.pets = [] 

    def add_pet(self, pet):
        self.pets.append(pet)

    def __str__(self):
        return f'Клиент {self.name}, телефон: {self.phone}'


class Database:
    '''База данных клиентов'''
    def __init__(self, filename='database.pkl'):
        self.filename = filename
        self.clients = []
        self.load()
    
    def load(self):
        '''Загружает данные из файла'''
        try:
            with open(self.filename, 'rb') as f:
                self.clients = pickle.load(f)
        except FileNotFoundError:
            self.clients = []

    def add_client(self, client):
        self.clients.append(client)

    def find_clients_by_name(self, name):
        return [client for client in self.clients if client.name.lower() == name.lower()]

    def find_clients_by_phone(self, phone):
        return [client for client in self.clients if client.phone == phone]

    def save(self):
        '''Сохраняет данные в файл'''
        with open(self.filename, 'wb') as f:
            pickle.dump(self.clients, f)

    def __str__(self):
        return f'База данных: {len(self.clients)} клиентов'


def print_menu():
    print('\nВетеринарная клиника')
    print('1. Просмотреть всех клиентов')
    print('2. Добавить клиента')
    print('3. Установить дату нового приема')
    print('4. Завершить прием и добавить комментарий')
    print('5. Просмотреть записи о приемах')
    print('6. Сохранить и выйти')
    print('7. Выйти без сохранения')


def main():
    '''Основная функция'''
    db = Database()
    while True:
        print_menu()
        choice = input('Выберите действие: ')
        if choice == '1':
            view_clients(db)
        elif choice == '2':
            add_client(db)
        elif choice == '3':
            new_appointment(db)
        elif choice == '4':
            complete_appointment(db)
        elif choice == '5':
            view_appointments(db)
        elif choice == '6':
            db.save()
            print('База данных сохранена')
            break
        elif choice == '7':
            print('Выход без сохранения')
            break
        else:
            print('Неверный выбор. Попробуйте снова.')


def view_clients(db):
    '''Отображает список всех клиентов'''
    if not db.clients:
        print('Нет клиентов в базе')
        return
    for i, client in enumerate(db.clients, 1):
        print(f'{i}. {client}')
        if client.pets:
            for pet in client.pets:
                print(pet)
        else:
            print('Нет питомцев')


def find_client(db):
    '''Ищет клиента по имени или номеру телефона'''
    choice = input('Искать по имени (1) или телефону (2)? ')
    if choice == '1':
        name = input('Введите имя клиента: ')
        results = db.find_clients_by_name(name)
    elif choice == '2':
        phone = input('Введите телефон клиента: ')
        results = db.find_clients_by_phone(phone)
    else:
        print('Неверный выбор')
        return []

    if not results:
        print('Клиент не найден')
    return results


def add_client(db):
    '''Добавляет нового клиента и его питомцев в базу данных'''
    try:
        name = input('Введите имя клиента: ')
        phone = input('Введите телефон клиента: ')
        client = Client(name, phone)
        
        while True:
            add_pet = input('Добавить питомца? (да/нет): ').lower()
            if add_pet == 'да':
                pet_name = input('Введите имя питомца: ')
                pet_age = int(input('Введите возраст питомца: '))
                pet = Pet(pet_name, pet_age)
                client.add_pet(pet)
                print('Питомец добавлен')
            elif add_pet == 'нет':
                break
            else:
                print('Введите "да" или "нет"')
        
        db.add_client(client)
        print('Клиент добавлен')
    except ValueError as e:
        print(f'Произошла ошибка: {e}')


def new_appointment(db):
    '''Новый прием'''
    results = find_client(db)
    if not results:
        return
    client = select_from_list(results)
    if not client:
        return
    if not client.pets:
        print('У клиента нет питомцев')
        return
    pet = select_pet(client)
    if not pet:
        return
    
    date = input('Введите дату приема: ')
    pet.add_appointment(date)
    print('Дата приема установлена')


def complete_appointment(db):
    '''Завершает прием и добавляет комментарий ветеринара'''
    results = find_client(db)
    if not results:
        return
    client = select_from_list(results)
    if not client:
        return
    if not client.pets:
        print('У клиента нет питомцев')
        return
    pet = select_pet(client)
    if not pet:
        return
    if pet.scheduled_appointment is None:
        print('У питомца нет запланированного приема')
        return
    
    comment = input('Введите комментарий ветеринара: ')
    pet.complete_appointment(comment)
    print('Прием завершен и комментарий добавлен')


def view_appointments(db):
    '''Отображает записи о приемах питомца'''
    results = find_client(db)
    if not results:
        return
    client = select_from_list(results)
    if not client:
        return
    if not client.pets:
        print('У клиента нет питомцев')
        return
    pet = select_pet(client)
    if not pet:
        return
    
    print(f'\nПитомец {pet.name}')
    print('Прошедшие приемы:')
    if not pet.past_appointments:
        print('Нет прошедших приемов')
    else:
        for a in pet.past_appointments:
            print(f"Дата: {a['date']}. Комментарий: {a['comment']}")
    print('Запланированный прием:')
    if pet.scheduled_appointment:
        print(f'Дата: {pet.scheduled_appointment}')
    else:
        print('Нет запланированного приема')


def select_from_list(lst):
    '''выбрать клиента из списка результатов поиска'''
    for idx, item in enumerate(lst, 1):
        print(f'{idx}. {item}')
    
    choice = int(input('Введите номер: '))
    if 1 <= choice <= len(lst):
        return lst[choice - 1]
    else:
        print('Неверный ввод')
        return None


def select_pet(client):
    '''Выбор питомца клиента'''
    for idx, pet in enumerate(client.pets, 1):
        print(f'{idx}. {pet}')
    
    choice = int(input('Введите номер: '))
    if 1 <= choice <= len(client.pets):
        return client.pets[choice - 1]
    else:
        print('Неверный ввод')
        return None


main()