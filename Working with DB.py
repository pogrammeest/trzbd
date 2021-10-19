import psycopg2
import prettytable


class WorkingWithDataBase():
    def __init__(self):
        self.conn = psycopg2.connect(
            user='postgres',
            password='admin',
            port='5432',
            database='trzbd_DB'
        )
        self.cursor = self.conn.cursor()

    def select_many_rows(self, table, columns='*', key='true', key_value='true'):
        select_many_rows_command = f"select {columns} from {table} where {key} = '{key_value}' "
        self.cursor.execute(select_many_rows_command)

        return self.cursor.fetchall()

    def select_one_row(self, table, columns='*', key='true', key_value='true'):
        select_one_row_command = f"select {columns} from {table} where {key} = '{key_value}'"
        self.cursor.execute(select_one_row_command)

        return self.cursor.fetchone()

    def select_all_rows(self, columns='*', table='table'):
        try:
            select_many_rows_command = f"select {columns} from {table} "
            self.cursor.execute(select_many_rows_command)
            tuple_data = self.cursor.description
            name_columns = []
            for i in tuple_data:
                name_columns.append(i[0])
            temp_data = self.cursor.fetchall()

            lovely = prettytable.PrettyTable()
            lovely.field_names = name_columns
            for i in temp_data:
                lovely.add_row(i)
            return (lovely, temp_data)
        except Exception as exc:
            return exc

    def update(self, table, set_string="", condition=""):  # UPDATE weather SET temp_lo = temp_lo+1, temp_hi = temp_lo+15, prcp = DEFAULT WHERE city = 'San Francisco' AND date = '2003-07-03'

        update_command = f"UPDATE {table} SET {set_string} WHERE {condition}"
        try:
            self.cursor.execute(update_command)
            self.conn.commit()
        except Exception as e:
            print('Exception:', e)
            self.conn.rollback()

    def delete(self, table, condition=""):  # DELETE FROM films WHERE kind <> 'Musical';

        delete_command = f"DELETE FROM {table} WHERE {condition}"
        try:
            self.cursor.execute(delete_command)
            self.conn.commit()
        except Exception as e:
            print('Exception:', e)

    def insert(self, table, columns, values):
        insert_command_string = f"insert into {table} ({columns}) values (%s {', %s' * (len(values) - 1)})"
        insert_command = self.cursor.mogrify(insert_command_string, values)
        try:
            self.cursor.execute(insert_command)
            self.conn.commit()
        except Exception as e:
            print('Exception:', e)
            self.conn.rollback()


# a.insert('admins_commands', 'id_command, headline, description', (4, 'help', 'helping command 4'))
# print(a.select_many_rows(table='admins_commands', key='headline', key_value='help'))

if __name__ == '__main__':
    a = WorkingWithDataBase()

    output, data = a.select_all_rows(columns='*', table='admins_commands')
    print(output)
    print(data)

    # a.update(table='admins_commands',
    #          set_string="id_command = 5, headline = 'output', description = 'output command'",
    #          condition="id_command = 4 AND headline = 'help'")
    a.delete(table='admins_commands', condition="headline = 'output'")

    output, data = a.select_all_rows(columns='*', table='admins_commands')
    print(output)
    print(data)
