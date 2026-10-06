import allure
import pytest

from tests.assertions.http.gateway import (
    assert_get_user_details_response_user_with_active_credit_card_account,
    assert_get_account_details_response_user_with_active_debit_card_account
)
from tests.clients.http.gateway.client import GatewayHTTPTestClient
from tests.context.base import RequestContext
from tests.context.scenario import Scenario
from tests.tools.allure import AllureTag, AllureStory, AllureFeature


@pytest.mark.gateway
@pytest.mark.regression
@allure.tag(AllureTag.HTTP, AllureTag.GATEWAY_SERVICE)
@allure.feature(AllureFeature.GATEWAY_SERVICE)
class TestGatewayHTTP:
    """
        Сценарные HTTP тесты gateway-service.

        Этот тестовый класс:
        - не подготавливает данные;
        - не управляет моками напрямую;
        - не содержит логики маршрутизации или агрегации.

        Он описывает сценарии взаимодействия с gateway
        в условиях полностью детерминированного внешнего мира.
        """
    @allure.story(AllureStory.GET_USER_DETAILS)
    @allure.title("[HTTP] Get user details. User with active credit card account")
    def test_get_user_details_user_with_active_credit_card_account(
            self,
            gateway_http_test_client: GatewayHTTPTestClient
    ):
        response = gateway_http_test_client.get_user_details(
            RequestContext(scenario=Scenario.USER_WITH_ACTIVE_CREDIT_CARD_ACCOUNT)
        )
        assert_get_user_details_response_user_with_active_credit_card_account(response)

    @allure.story(AllureStory.GET_ACCOUNT_DETAILS)
    @allure.title("[HTTP] Get account details. User with active debit card account")
    def test_get_account_details_user_with_active_debit_card_account(
            self,
            gateway_http_test_client: GatewayHTTPTestClient
    ):
        response = gateway_http_test_client.get_account_details(
            RequestContext(scenario=Scenario.USER_WITH_ACTIVE_DEBIT_CARD_ACCOUNT)
        )
        assert_get_account_details_response_user_with_active_debit_card_account(response)

