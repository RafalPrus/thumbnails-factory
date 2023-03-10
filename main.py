import os
import random

from PIL import Image
from views import Progress, CategoryCounter, MainMenu, Statistics
from repositories import EntryRepository


class Application:
    EXISTING_FOLDERS: list[str] = []

    def main(self) -> bool:
        while True:
            menu = MainMenu()
            menu.draw()

            screen = menu.get_screen()
            if isinstance(screen, CategoryCounter):
                self.create_thumbnails(screen)
            elif isinstance(screen, Statistics):
                self.display_statistics(screen)
            else:
                print("See you next time!")
                return False

    def create_thumbnails(self, screen: CategoryCounter):
        progress = Progress()
        progress.welcome()
        os.chdir(
            "images"
        )  # a specific folder where the folders to create thumbnails must be located
        current_path = os.getcwd()
        folders = os.listdir(current_path)
        entry_repository = self.get_entry_repository()
        self.process_folders(folders, current_path, progress, screen)
        if (
            Application.EXISTING_FOLDERS
        ):  # if there were already files with created thumbnails
            print(
                f"w tych folderach byly juz miniaturki: {Application.EXISTING_FOLDERS}"
            )
        screen.show_result()
        screen.show_processed_folders()
        os.chdir("..")
        entry_repository.save(screen.CATEGORIES_COUNTER, screen.UNIQUE_NUMBERS)

    @staticmethod
    def display_statistics(screen):
        screen.show_statistic()

    @staticmethod
    def get_entry_repository() -> EntryRepository:
        return EntryRepository()

    def process_folders(
        self, folders: list, path: str, progress: Progress, screen, directory: str = "small"
    ):
        for folder in folders:
            if os.path.isfile(
                os.path.join(path, folder)
            ):  # to skip files that are not folders
                continue
            os.chdir(folder)
            path_in_folder = os.getcwd()
            files = os.listdir(path_in_folder)
            new_folder_path = os.path.join(path_in_folder, directory)
            if os.path.exists(new_folder_path):
                Application.EXISTING_FOLDERS.append(folder)
                os.chdir("..")
                continue
            os.mkdir(new_folder_path)
            progress.start_process(folder)
            self.process_images(files, screen)
            progress.finish_folder(folder)
            screen.count_folder()
            os.chdir("..")

    @staticmethod
    def process_images(files: list, screen):
        product_num = 0
        if Application.check_info_exist(files):
            product_num = Application.read_txt_file(screen)
        for num, img in enumerate(files):
            match img.lower():
                case "info.txt":
                    continue
                case _:
                    if Application.is_image(img):
                        Application.run_thumbnails_creator(img, product_num, num)

    @staticmethod
    def check_info_exist(files):
        info_names = ("info.txt", "INFO.txt", "Info.txt")
        for name in info_names:
            if name in files:
                return True
        return False

    @staticmethod
    def is_image(file_name: str) -> bool:
        return (
            file_name.endswith(".jpg")
            or file_name.endswith(".jpeg")
            or file_name.endswith(".png")
        )

    @staticmethod
    def read_txt_file(screen) -> str | int:
        with open("info.txt", encoding='UTF-8') as text_info:
            category = text_info.readline().strip()
            product_number = text_info.readline().strip()
            screen.count_for_category(category)  # Count category of processed folder
            if product_number.isdigit():
                screen.count_unique_nums(product_number)
                return product_number
            else:
                return 0

    @staticmethod
    def run_thumbnails_creator(
        image, name: str | None = None, photo_num: int = 0, directory: str = "small"
    ):
        with Image.open(image) as img:
            names = image.split(".")
            img.thumbnail((1400, 1040))
            os.chdir(directory)
            random_num = Application.create_random_num(photo_num)
            if name:
                img.save(f"{name}_{random_num}_small.jpg")
            else:
                img.save(f"{names[0]}_small.jpg")
            os.chdir("..")

    @staticmethod
    def create_random_num(photo_num: int):
        return (
            str(photo_num) * 2
            + str(random.randint(10000, 99999))
            + random.choice("ABCDEFGabcdefg")
        )


if __name__ == "__main__":
    app = Application()
    app.main()
