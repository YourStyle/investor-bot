from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

mult_commands = ['pe', 'cap', 'cash', 'debt', 'sales', 'fcf', 'ebitda', 'ps', 'pb', 'eve', 'nde', 'dividend',
                 'earnin',
                 'roa', 'ros']

max_commands_commands = len(mult_commands)

redis = {
    'address': (IP, 6379),
    'encoding': 'utf8'
}
