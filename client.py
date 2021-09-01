import motor.motor_asyncio as m_m_a


class SingletonClient:
    client = None
    db = None

    @staticmethod
    def get_client():
        if SingletonClient.client is None:
            MONGODB_HOSTNAME = 'localhost'
            MONGODB_PORT = '27017'

            SingletonClient.client = m_m_a.AsyncIOMotorClient("mongodb://{}:{}".format(
                MONGODB_HOSTNAME, str(MONGODB_PORT)))

        return SingletonClient.client

    @staticmethod
    def get_data_base():
        if SingletonClient.db is None:
            client = SingletonClient.get_client()
            MONGODB_DATABASE = 'shop'
            SingletonClient.db = client[MONGODB_DATABASE]

        return SingletonClient.db
