import sqlite3


class EntryRepository:
    """ handles database queries
    that enter data into the entry table
    """
    def get_by_name(self, category_name):
        """ fetches data for a specific category
        based on the submitted category name
        """
        with sqlite3.connect('library.db') as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT `id`, `name` from `category` WHERE `name`=?', (category_name, ))
            return cursor.fetchall()[0][0]

    def get_unique_numbers(self):
        with sqlite3.connect('library.db') as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT `unique_number` from `unique_product_numbers`')
            return cursor.fetchall()
    def save(self, counter: dict, unique_numbers: list):
        """ writes data to the entry table
        based on the data retrieved from the counter
        """
        with sqlite3.connect('library.db') as connection:
            cursor = connection.cursor()
            for category in counter:
                if counter[category] > 0:
                    category_id = self.get_by_name(category)
                    cursor.execute(
                        'INSERT INTO entry(`category_id`, `amount`) VALUES(?, ?)', (
                            category_id,
                            counter[category]
                    ))
            list_of_unique_numbers = [element[0] for element in self.get_unique_numbers()]
            for number in unique_numbers:
                if number not in list_of_unique_numbers:
                    cursor.execute(
                        'INSERT INTO unique_product_numbers(`unique_number`) VALUES(?)', (
                            number,
                        ))
            connection.commit()


class ReportRepository:
    """ handles database queries that
    retrieve data to create reports
    """
    def get_summary(self, year: str, month: str):
        date = year + month.zfill(2)
        with sqlite3.connect('library.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT category_id, amount FROM entry WHERE strftime('%Y%m', created_at) = (?)''', (
                date,))
            return cursor.fetchall()

    def get_categories(self):
        """ fetches detailed data on each
        category from the database
        """
        with sqlite3.connect('library.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT id, name FROM category''')
            return cursor.fetchall()
