import os
from PIL import Image
from views import Progress, FolderCounter, MainMenu
from repositories import EntryRepository


class Application:
    def main(self):
        menu = MainMenu()
        menu.draw()

        screen = menu.get_screen()
        if isinstance(screen, FolderCounter):
            self.create_thumbnails(screen)
        else:
            self.get_statistics(screen)

    def create_thumbnails(self, screen):
        already_exist = [] # for listing folders that already contained thumbnails
        progress = Progress()
        progress.welcome()
        os.chdir('images') # a specific folder where the folders to create thumbnails must be located
        path = os.getcwd()
        folders = os.listdir(path)
        directory = 'small' # thumbnail folder name
        entry_repository = self.get_entry_repository()
        for folder in folders:
            if os.path.isfile(os.path.join(path, folder)): # to skip and store files that are not folders
                continue
            os.chdir(folder)
            path_in_folder = os.getcwd()
            files = os.listdir(path_in_folder)
            new_folder_path = os.path.join(path_in_folder, directory)
            try:
                os.mkdir(new_folder_path)
            except FileExistsError:
                already_exist.append(folder)
                os.chdir('..')
                continue
            progress.start_process(folder)
            for img in files:
                if img == 'info.txt':
                    with open('info.txt') as text_info:
                        category = text_info.readline().strip()
                        screen.count_for_category(category)
                        continue
                if os.path.isfile(os.path.join(path_in_folder, img)) == False:
                    continue
                names = img.split('.')
                with Image.open(img) as image:
                    image.thumbnail((1400, 1040))
                    os.chdir(directory)
                    image.save(f'{names[0]}_small.jpg')
                    os.chdir('..')
            progress.finish_folder(folder)
            screen.count_folder()
            os.chdir('..')
        if already_exist: # if there were already files with created thumbnails
            print(f'w tych folderach byly juz miniaturki: {already_exist}')
        screen.show_result()
        screen.show_processed_folders()
        os.chdir('..')
        entry_repository.save(screen.CATEGORIES_COUNTER)

    def get_statistics(self, screen):
        screen.show_statistic()


    def get_entry_repository(self):
        return EntryRepository()

if __name__ == '__main__':
    app = Application()
    app.main()










