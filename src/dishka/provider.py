from dishka import Provider, Scope, provide

from src.business_logic.user.main import UserBusinessLogicService
from src.db.dao.user_dao import UserDAO
from src.smtp.main import SmtpServer


class DishkaProvider(Provider):

    @provide(scope=Scope.APP)
    def get_user_service(self) -> UserBusinessLogicService:
        return UserBusinessLogicService(UserDAO())

    @provide(scope=Scope.APP)
    def get_smtp(self) -> SmtpServer:
        return SmtpServer()


provider = DishkaProvider()
