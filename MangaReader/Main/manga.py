from models import *

def add_chapter(manga, foldername: str) -> None:
    number, name = foldername.split(' ')
    chapter = Chapter(manga=manga, number=int(number), name=name)
    print(chapter)

if __name__ == "__main__":
    import os
    manga = Manga.objects.get(slug='Chainsaw-Man')
    os.chdir('./chsmn/')
    print(os.listdir())
    add_chapter(manga, '1 Пёс и бензопила')