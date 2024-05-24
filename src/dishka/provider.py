from dishka import Provider, provide, Scope

from src.business_logic.user.main import UserBusinessLogicService
from src.db.dao.user_dao import UserDAO
from src.smtp.main import SmtpServer


class DishkaProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_user_dao(self) -> UserDAO:
        return UserDAO()

    @provide(scope=Scope.APP)
    def get_user_service(self, dao: UserDAO) -> UserBusinessLogicService:
        return UserBusinessLogicService(dao=dao)

    @provide(scope=Scope.APP)
    def get_smtp(self) -> SmtpServer:
        return SmtpServer()

    # @provide(scope=Scope.APP)
    # def get_db_user(self) -> BeanieUserDatabase:
    #     return BeanieUserDatabase(User)
    #
    # @provide(scope=Scope.APP)
    # def get_user_manager(self, user_db: BeanieUserDatabase, smtp: SmtpServer) -> UserManager:
    #     return UserManager(user_db, smtp)


provider = DishkaProvider()
