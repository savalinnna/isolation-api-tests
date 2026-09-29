import allure
import grpc

from contracts.services.gateway.gateway_service_pb2_grpc import GatewayServiceStub
from contracts.services.gateway.rpc_get_account_details_pb2 import (
    GetAccountDetailsRequest,
    GetAccountDetailsResponse,
)
from contracts.services.gateway.rpc_get_user_details_pb2 import (
    GetUserDetailsRequest,
    GetUserDetailsResponse,
)
from tests.clients.grpc.client import GRPCTestClient, build_grpc_test_channel
from tests.config import test_settings
from tests.context.base import RequestContext, build_grpc_test_metadata
from tests.tools.fakers import fake
from tests.tools.logger import get_test_logger


class GatewayGRPCTestClient(GRPCTestClient):
    """
    gRPC API-клиент тестового слоя для gateway-service.

    Это специализированный клиент, построенный поверх базового
    GRPCTestClient. Он знает gRPC-контракт gateway-service и
    protobuf-сообщения, но остаётся тестовым инструментом,
    а не частью бизнес-логики системы.

    Ключевой смысл этого клиента в курсе:
    тест обращается к gateway-service, а gateway-service "под капотом"
    обращается к внешним интеграциям (users / cards / accounts),
    которые в изоляционном контуре подменены мок-сервисами.

    Поэтому входные идентификаторы (user_id / account_id)
    не являются управляющим параметром поведения.
    Управляющая переменная — это сценарий, передаваемый
    через RequestContext и gRPC metadata.
    """

    def __init__(self, channel: grpc.Channel):
        # Базовый gRPC-клиент хранит channel как инфраструктурную зависимость.
        super().__init__(channel)

        # Stub создаётся поверх channel и является прямым отражением
        # protobuf-контракта gateway-service.
        #
        # Важно: stub не знает о сценариях, тестах или моках.
        # Он просто реализует gRPC-интерфейс сервиса.
        self.stub = GatewayServiceStub(channel)

    @allure.step("Get user details")
    def get_user_details_api(
        self,
        request: GetUserDetailsRequest,
        context: RequestContext,
    ) -> GetUserDetailsResponse:
        # Низкоуровневый API-метод.
        #
        # Он напрямую вызывает gRPC-метод stub'а и возвращает
        # protobuf-ответ без дополнительной интерпретации.
        #
        # Здесь явно передаётся metadata, сформированная из RequestContext.
        # Это ключевая архитектурная точка:
        # - транспорт (channel) остаётся чистым;
        # - сценарий применяется только там, где он нужен по смыслу.
        return self.stub.GetUserDetails(
            request,
            metadata=build_grpc_test_metadata(context),
        )

    @allure.step("Get account details")
    def get_account_details_api(
        self,
        request: GetAccountDetailsRequest,
        context: RequestContext,
    ) -> GetAccountDetailsResponse:
        return self.stub.GetAccountDetails(
            request,
            metadata=build_grpc_test_metadata(context),
        )

    def get_user_details(self, context: RequestContext) -> GetUserDetailsResponse:
        # Фасадный метод для тестов.
        #
        # Мы сознательно генерируем произвольный, но валидный user_id.
        # Почему это корректно:
        # - gateway-service требует id по контракту;
        # - но в изоляционном контуре внешний мир моделируется сценарием;
        # - значит, поведение определяется metadata, а не значением id.
        request = GetUserDetailsRequest(id=str(fake.uuid()))
        return self.get_user_details_api(request, context)

    def get_account_details(self, context: RequestContext) -> GetAccountDetailsResponse:
        request = GetAccountDetailsRequest(id=str(fake.uuid()))
        return self.get_account_details_api(request, context)


def build_gateway_grpc_test_client() -> GatewayGRPCTestClient:
    # Фабрика создания специализированного gRPC-клиента gateway-service.
    #
    # Здесь соблюдается тот же архитектурный паттерн,
    # что и в HTTP-части курса:
    # - конфигурация берётся из test_settings;
    # - логгер создаётся единым способом;
    # - channel настраивается централизованно.
    channel = build_grpc_test_channel(
        logger=get_test_logger("GATEWAY_GRPC_TEST_CLIENT"),
        config=test_settings.gateway_grpc_client,
    )
    return GatewayGRPCTestClient(channel=channel)
