import asyncio
import threading
import mysql.connector
import datetime

def escape_string(string):
    ESCAPED_CHARS = """%'"_\\"""
    str_buffer = list(string)

    for esc in ESCAPED_CHARS:
        for i, e in enumerate(str_buffer):
            if e == esc:
                str_buffer[i] = "\\" + e
    
    return ''.join(str_buffer)

def format_date_to_sql(date):
    return f"DATE '{datetime.date.strftime(date, '%Y-%m-%d')}'"


class DatabaseConnector:

    def __init__(self, config, default_error_handler=None):
        self.config = config
        self.deafult_error_handler = default_error_handler
        self.loop = asyncio.new_event_loop()
        self.executor_thread = threading.Thread(target=self.__executor)

    def start_executor(self):
        self.executor_thread.start()

    def __executor(self):
        self.conn  = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor(buffered=True)

        self.loop.run_forever()

        self.loop.close()
    
    def query_database(self, query, dispatcher=None, column_dispatcher=None, onerror=None, on_success=None):
        if onerror is None:
            onerror = self.deafult_error_handler
        
        asyncio.run_coroutine_threadsafe(self.__inner_query_database(query, dispatcher, column_dispatcher, onerror, on_success), self.loop)

    async def __inner_query_database(self, query, dispatcher, column_dispatcher, onerror, on_sucess):
        try:
            self.cursor.execute(query)
            
            if column_dispatcher:
                column_dispatcher(self.cursor.column_names)

            if dispatcher:
                for data in self.cursor:
                    dispatcher(data)

            if on_sucess:
                on_sucess()

        except Exception as e:
            if onerror:
                onerror()
        finally:
            self.conn.commit()

    def close_connector(self):
        self.cursor.close()
        self.conn.close()
        
        self.loop.call_soon_threadsafe(self.loop.stop)

        self.executor_thread.join()






