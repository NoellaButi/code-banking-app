# schemas.py (Marshmallow schemas for API)
from __future__ import annotations

from decimal import Decimal
from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError, pre_load

ACCOUNT_TYPES = ("Checking", "Savings")
TX_KINDS = ("deposit", "withdraw", "transfer")


# ---------- Accounts ----------
class AccountCreateSchema(Schema):
    name = fields.Str(required=True)
    type = fields.Str(required=True, validate=validate.OneOf(ACCOUNT_TYPES))
    opening = fields.Decimal(as_string=True, places=2, default=Decimal("0.00"))

    @pre_load
    def strip_strings(self, data, **kwargs):
        for k in ("name", "type"):
            if k in data and isinstance(data[k], str):
                data[k] = data[k].strip()
        return data

    @validates("opening")
    def validate_opening(self, value: Decimal):
        if value < Decimal("0.00"):
            raise ValidationError("Opening balance cannot be negative.")


class AccountSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    type = fields.Str(required=True, validate=validate.OneOf(ACCOUNT_TYPES))
    balance = fields.Decimal(as_string=True, places=2, dump_only=True)
    created_at = fields.DateTime(format="iso", dump_only=True)


# ---------- Transactions ----------
class TransactionCreateSchema(Schema):
    account_id = fields.Int(required=True)
    kind = fields.Str(required=True, validate=validate.OneOf(TX_KINDS))
    amount = fields.Decimal(as_string=True, places=2, required=True)
    description = fields.Str(load_default="")
    related_account_id = fields.Int(allow_none=True, load_default=None)

    @pre_load
    def strip_strings(self, data, **kwargs):
        if "description" in data and isinstance(data["description"], str):
            data["description"] = data["description"].strip()
        return data

    @validates("amount")
    def validate_amount(self, value: Decimal):
        if value <= Decimal("0.00"):
            raise ValidationError("Amount must be greater than 0.")

    @validates_schema
    def validate_transfer_fields(self, data, **kwargs):
        kind = data.get("kind")
        related = data.get("related_account_id")
        if kind == "transfer" and not related:
            raise ValidationError({"related_account_id": "required for transfers"})
        if kind in {"deposit", "withdraw"} and related:
            raise ValidationError({"related_account_id": "should be empty for deposits/withdrawals"})


class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    account_id = fields.Int()
    kind = fields.Str(validate=validate.OneOf(TX_KINDS))
    amount = fields.Decimal(as_string=True, places=2)
    description = fields.Str()
    related_account_id = fields.Int(allow_none=True)
    created_at = fields.DateTime(format="iso", dump_only=True)


# Optional singletons
account_create_schema = AccountCreateSchema()
account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)

transaction_create_schema = TransactionCreateSchema()
transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)