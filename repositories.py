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

    def save(self, counter):
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
