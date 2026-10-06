import allure
import pytest

from tests.assertions.grpc.gateway import (
    assert_get_user_details_response_user_with_active_credit_card_account,
    assert_get_account_details_response_user_with_active_debit_card_account
)
from tests.clients.grpc.gateway.client import GatewayGRPCTestClient
from tests.context.base import RequestContext
from tests.context.scenario import Scenario
from tests.tools.allure import AllureTag, AllureFeature, AllureStory


@pytest.mark.gateway
@pytest.mark.regression
@allure.tag(AllureTag.GRPC, AllureTag.GATEWAY_SERVICE)
@allure.feature(AllureFeature.GATEWAY_SERVICE)
class TestGatewayGRPC:
    """
        Сценарные gRPC тесты gateway-service.

        Этот класс архитектурно симметричен HTTP-версии.
        Он описывает сценарии взаимодействия с gateway,
        не зная ничего о транспортной реализации.
        """
    @allure.story(AllureStory.GET_USER_DETAILS)
    @allure.title("[gRPC] Get user details. User with active credit card account")
    def test_get_user_details_user_with_active_credit_card_account(
            self,
            gateway_grpc_test_client: GatewayGRPCTestClient
    ):
        response = gateway_grpc_test_client.get_user_details(
            RequestContext(scenario=Scenario.USER_WITH_ACTIVE_CREDIT_CARD_ACCOUNT)
        )
        assert_get_user_details_response_user_with_active_credit_card_account(response)

    @allure.story(AllureStory.GET_ACCOUNT_DETAILS)
    @allure.title("[gRPC] Get account details. User with active debit card account")
    def test_get_account_details_user_with_active_debit_card_account(
            self,
            gateway_grpc_test_client: GatewayGRPCTestClient
    ):
        response = gateway_grpc_test_client.get_account_details(
            RequestContext(scenario=Scenario.USER_WITH_ACTIVE_DEBIT_CARD_ACCOUNT)
        )
        assert_get_account_details_response_user_with_active_debit_card_account(response)
