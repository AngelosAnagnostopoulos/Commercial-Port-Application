import asyncio
import threading
import mysql.connector


class DatabaseConnector:

    def __init__(self, config):
        self.config = config
        self.loop = asyncio.new_event_loop()
        self.executor_thread = threading.Thread(target=self.__executor)

    def start_executor(self):
        self.executor_thread.start()

    def __executor(self):
        self.conn  = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor(buffered=True)

        self.loop.run_forever()

        self.loop.close()
    
    def query_database(self, query, dispatcher=None, onerror=None):
        asyncio.run_coroutine_threadsafe(self.__inner_query_database(query, dispatcher, onerror), self.loop)

    async def __inner_query_database(self, query, dispatcher, onerror):
        try:
            self.cursor.execute(query)
            
            if dispatcher:
                for data in self.cursor:
                    dispatcher(data)

        except:
            if onerror:
                onerror()

        finally:
            self.cursor.commit()
            self.conn.commit()

    def close_connector(self):
        self.cursor.close()
        self.conn.close()
        
        self.loop.call_soon_threadsafe(self.loop.stop)

        self.executor_thread.join()






