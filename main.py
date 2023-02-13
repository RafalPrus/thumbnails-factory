import os

from PIL import Image
from views import Progress, CategoryCounter, MainMenu
from repositories import EntryRepository


class Application:
    EXISTING_FOLDERS: list[str] = []

    def main(self):
        menu = MainMenu()
        menu.draw()

        screen = menu.get_screen()
        if isinstance(screen, CategoryCounter):
            self.create_thumbnails(screen)
        else:
            self.display_statistics(screen)

    def create_thumbnails(self, screen: CategoryCounter):
        progress = Progress()
        progress.welcome()
        os.chdir('images')  # a specific folder where the folders to create thumbnails must be located
        current_path = os.getcwd()
        folders = os.listdir(current_path)
        entry_repository = self.get_entry_repository()
        self.process_folders(folders, current_path, progress, screen)
        if Application.EXISTING_FOLDERS:  # if there were already files with created thumbnails
            print(f'w tych folderach byly juz miniaturki: {Application.EXISTING_FOLDERS}')
        screen.show_result()
        screen.show_processed_folders()
        os.chdir('..')
        entry_repository.save(screen.CATEGORIES_COUNTER)

    @staticmethod
    def display_statistics(screen):
        screen.show_statistic()

    @staticmethod
    def get_entry_repository():
        return EntryRepository()

    def process_folders(self, folders: list, path, progress: Progress, screen, directory: str = 'small'):
        for folder in folders:
            if os.path.isfile(os.path.join(path, folder)):  # to skip and store files that are not folders
                continue
            print(folder)
            print(os.getcwd())
            os.chdir(folder)
            path_in_folder = os.getcwd()
            files = os.listdir(path_in_folder)
            new_folder_path = os.path.join(path_in_folder, directory)
            if os.path.exists(new_folder_path):
                Application.EXISTING_FOLDERS.append(folder)
                os.chdir('..')
                continue
            os.mkdir(new_folder_path)
            progress.start_process(folder)
            self.process_images(files, screen)
            progress.finish_folder(folder)
            screen.count_folder()
            os.chdir('..')


    def process_images(self, files: list, screen):
        for img in files:
            match img:
                case 'info.txt':
                    with open('info.txt') as text_info:
                        category = text_info.readline().strip()
                        screen.count_for_category(category)
                        continue
                case _:
                    if Application.is_image(img):
                        Application.run_thumbnails_creator(img)

    @staticmethod
    def is_image(file_name: str):
        return file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png')

    @staticmethod
    def run_thumbnails_creator(image, directory: str = 'small'):
        with Image.open(image) as img:
            names = image.split('.')
            img.thumbnail((1400, 1040))
            os.chdir(directory)
            img.save(f'{names[0]}_small.jpg')
            os.chdir('..')


if __name__ == '__main__':
    app = Application()
    app.main()
