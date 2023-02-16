from repositories import ReportRepository
from terminaltables import AsciiTable


class CategoryCounter:
    """ counts the number of processed folders in a given category and summarizes the operations performed"""
    CATEGORIES_COUNTER = {
        'NAP': 0,
        'ENG': 0,
        'ARM': 0,
        'ECT': 0,
        'HCL': 0,
        'HYD': 0,
        'MB': 0,
        'OP': 0,
        'OS': 0,
        'PGI': 0,
        'NONE': 0
    }

    FOLDERS_DONE = 0 #total number of processed folders

    SHORTCUT = 'WM'
    LABEL = 'Wykonaj miniaturki'

    def count_for_category(self, cat):
        if cat.upper() in self.CATEGORIES_COUNTER:
            self.CATEGORIES_COUNTER[cat.upper()] += 1
        else:
            self.CATEGORIES_COUNTER['NONE'] += 1

    def show_result(self):
        for cat in self.CATEGORIES_COUNTER:
            if self.CATEGORIES_COUNTER[cat] > 0:
                print(f'W kategorii {cat} przetworzono {self.CATEGORIES_COUNTER[cat]} folderów')

    def count_folder(self):
        self.FOLDERS_DONE += 1

    def show_processed_folders(self):
        print(f'W sumie przetworzono: {self.FOLDERS_DONE} folderów')
        print('----------------------------------------------\n')

    @property
    def categories_counter(self):
        return self.CATEGORIES_COUNTER


class Progress:
    @staticmethod
    def welcome():
        print('rozpoczynam zmniejszanie zdjęć w folderach...')
        print('----------------------------------------------')

    @staticmethod
    def start_process(name):
        print(f'Przetwarzam folder {name}')

    @staticmethod
    def finish_folder(name):
        print(f'Ukończono zmniejszanie zdjęć w folderze {name}')
        print('----------------------------------------------')


class Statistics:
    """ generating statistics based on the date"""
    SHORTCUT = 'PS'
    LABEL = 'Pokaż statystyki'

    def get_date(self):
        year = input('Wybierz rok [rrrr]: ')
        month = input(('Wybierz miesiąc [mm]: '))
        return [year, month]

    def show_statistic(self):
        repo = self.get_repository()
        date = self.get_date()
        result = repo.get_summary(date[0], date[1])
        categories = dict(repo.get_categories())
        summary = {}
        for entry in result:
            if categories[entry[0]] in summary:
                summary[categories[entry[0]]] += entry[1]
            else:
                summary[categories[entry[0]]] = entry[1]
        summary['SUMA'] = sum(summary.values())
        table = [['KATEGORIA', 'ILOŚĆ']]
        for entry in summary:
            table.append([entry, summary[entry]])
        formated_table = AsciiTable(table)
        return print(formated_table.table)


    def get_repository(self):
        return ReportRepository()

class Quit():
    """ generating statistics based on the date"""
    SHORTCUT = 'EX'
    LABEL = 'Zakończ'


class MainMenu:
    OPTIONS = {
        CategoryCounter.SHORTCUT: CategoryCounter(),
        Statistics.SHORTCUT: Statistics(),
        Quit.SHORTCUT: Quit()
    }

    @staticmethod
    def draw():
        print('Powiedz co chcesz zrobić:')
        for shortcut, screen in MainMenu.OPTIONS.items():
            print(f'[{shortcut}] - {screen.LABEL}')

    @staticmethod
    def get_screen():
        option = None
        while option not in MainMenu.OPTIONS:
            option = input('Wybierz opcję: ')
            if option == 'ex':
                return 'end'
        return MainMenu.OPTIONS[option]
