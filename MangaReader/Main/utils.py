def handle_manga_file(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return f"images/manga/{instance.slug}/{filename}"

def handle_chapter_file(instance, filename):
    filename = (instance.chapter.manga.slug + '_' + 
    str(instance.chapter.number) + '_' +
    str(instance.number) + 
    '.' + filename.split('.')[1])
    return f"images/manga/{instance.chapter.manga.slug}/{instance.chapter.number}/{filename}"