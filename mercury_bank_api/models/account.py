"""Account model for Mercury Bank API."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal, Dict, Any
from dateutil.parser import parse as parse_date # type: ignore[import]


@dataclass
class Account:
    """Represents a Mercury bank account."""

    accountNumber: str
    availableBalance: float
    createdAt: datetime
    currentBalance: float
    id: str
    kind: str
    name: str
    routingNumber: str
    status: Literal["active", "deleted", "pending", "archived"]
    type: Literal["mercury", "external", "recipient"]
    legalBusinessName: str
    canReceiveTransactions: Optional[bool] = None
    nickname: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Account":
        """Create an Account from a dictionary."""
        # Parse datetime
        created_at = data["createdAt"]
        if isinstance(created_at, str):
            created_at = parse_date(created_at)

        return cls(
            accountNumber=data["accountNumber"],
            availableBalance=float(data["availableBalance"]),
            createdAt=created_at,
            currentBalance=float(data["currentBalance"]),
            id=data["id"],
            kind=data["kind"],
            name=data["name"],
            routingNumber=data["routingNumber"],
            status=data["status"],
            type=data["type"],
            legalBusinessName=data["legalBusinessName"],
            canReceiveTransactions=data.get("canReceiveTransactions"),
            nickname=data.get("nickname"),
        )
