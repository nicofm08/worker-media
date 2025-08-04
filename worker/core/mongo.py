"""This module contains the class MongoClient"""

import motor.motor_asyncio
from worker.core.logger_custom import log
from worker.core.constants import LOG_CORE, MONGO_URI



class MongoClient:
    """MongoClient class to interact with MongoDB"""

    _client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

    def __init__(self, db: str, collection: str) -> None:

        self.db = self._client[db]
        self.collection = self.db[collection]

    async def find_one(self, query, sort=None):
        """Find one document in the collection"""
        results = await self.collection.find_one(query)
        if sort and results and len(results) > 1:
            results = sorted(results, key=lambda x: x[sort[0]], reverse=sort[1])
        log.info(f"{LOG_CORE} The query find_one was executed successfully")
        return results

    async def find_all(self, query, sort=None, limit=None):
        """Find all documents in the collection"""
        results = await self.collection.find(query).to_list(length=limit)
        if sort and results:
            results = sorted(results, key=lambda x: x[sort[0]], reverse=sort[1])
        log.info(f"{LOG_CORE} The query find_all was executed successfully")
        return results

    async def insert_one(self, document):
        """Insert one document in the collection"""
        try:
            result = await self.collection.insert_one(document)
        except Exception as e:
            if "duplicate key error" in str(e):
                log.warning(
                    f"{LOG_CORE} Error inserting document - Duplicate key error"
                )
                raise Exception("Duplicate key error")
            else:
                log.error(f"{LOG_CORE} Error inserting document: {str(e)}")
                raise e
        log.info(f"{LOG_CORE} The query insert_one was executed successfully")
        return result

    async def insert_many(self, documents):
        """Insert many documents in the collection"""
        result = await self.collection.insert_many(documents)
        log.info(f"{LOG_CORE} The query insert_many was executed successfully")
        return result

    async def update_one(self, query, update):
        """Update one document in the collection"""
        log.info(f"{LOG_CORE} The query update_one was executed with query: {query} and update: {update}")
        result = await self.collection.update_one(query, update)
        log.info(f"{LOG_CORE} The query update_one was executed successfully")
        return result.modified_count

    async def update_many(self, query, update):
        """Update many documents in the collection"""
        result = await self.collection.update_many(query, update)
        log.info(f"{LOG_CORE} The query update_many was executed successfully")
        return result.modified_count

    async def delete_one(self, query):
        """Delete one document in the collection"""
        result = await self.collection.delete_one(query)
        log.info(f"{LOG_CORE} The query delete_one was executed successfully")
        return result

    async def delete_many(self, query):
        """Delete many documents in the collection"""
        result = await self.collection.delete_many(query)
        log.info(f"{LOG_CORE} The query delete_many was executed successfully")
        return result.deleted_count

    async def aggregate(self, query, sort=None):
        """Aggregate documents in the collection"""
        pipeline = query
        if sort:
            pipeline.append({"$sort": {sort[0]: sort[1]}})
        results = []
        async for document in self.collection.aggregate(pipeline):
            results.append(document)
        log.info(f"{LOG_CORE} The query aggregate was executed successfully")
        return results

    async def find_one_specific(
        self,
        query,
        sort_field: str,
        order: int = 1,
        limit: int = 1,
        length: int = 1,
    ):
        """Find the first document in the collection ordered by sort_field in descending order"""

        # Ejecutar la consulta con o sin ordenamiento según se proporcione sort_field
        cursor = self.collection.find(query)

        if sort_field:
            cursor = cursor.sort(sort_field, order)

        # Limitar los resultados a la cantidad especificada
        cursor = cursor.limit(limit)

        # Convertir el cursor a una lista y obtener el primer documento
        result = await cursor.to_list(length)

        # Retornar el primer documento si existe, de lo contrario, None
        if result:
            log.info(
                f"{LOG_CORE} The query find_one_specific was executed successfully"
            )
            return result[0]
        else:
            return None
