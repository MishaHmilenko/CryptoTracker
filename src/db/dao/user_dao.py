from src.db.models.user import User


class UserDAO:
    def __init__(self):
        self.collection = User

    async def get_all_emails(self) -> list[str]:
        pipeline = [
            {
                '$project': {
                    '_id': 0,
                    'email': 1
                }
            },
            {
                '$group': {
                    '_id': None,
                    'emails': {'$push': '$email'}
                }
            }
        ]
        return (await self.collection.aggregate(pipeline).to_list(length=None))[0]['emails']
