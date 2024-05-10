from dishka import Provider, Scope, provide

from src.business_logic.user.main import UserBusinessLogicService
from src.db.dao.user_dao import UserDAO
from src.db.models.user import User
from src.smtp.main import SmtpServer

class Obj:
    a = 1

class DishkaProvider(Provider):

    # @provide(scope=Scope.APP)
    # def get_user_service(self) -> UserBusinessLogicService:
    #     return UserBusinessLogicService(UserDAO())

    @provide(scope=Scope.APP)
    def get_object(self) -> Obj:
        return Obj()

    @provide(scope=Scope.APP)
    def get_smtp(self) -> SmtpServer:
        return SmtpServer()


provider = DishkaProvider()
