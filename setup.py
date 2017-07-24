from cx_Freeze import setup, Executable

setup(
    name='TwitchBot',
    version='0.5',
    packages=[''],
    url='',
    license='',
    author='VabeNIZ(Twitch@nizpidor)',
    author_email='troll5261@gmail.com',
    description='Rabbit Twitch Bot',
    executables = [Executable("bot.py")]
)
