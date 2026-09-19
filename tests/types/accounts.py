from enum import StrEnum


class AccountTestType(StrEnum):
    UNSPECIFIED = "UNSPECIFIED"
    DEBIT_CARD = "DEBIT_CARD"
    CREDIT_CARD = "CREDIT_CARD"
    DEPOSIT = "DEPOSIT"
    SAVINGS = "SAVINGS"


class AccountTestStatus(StrEnum):
    UNSPECIFIED = "UNSPECIFIED"
    ACTIVE = "ACTIVE"
    PENDING_CLOSURE = "PENDING_CLOSURE"
    CLOSED = "CLOSED"
