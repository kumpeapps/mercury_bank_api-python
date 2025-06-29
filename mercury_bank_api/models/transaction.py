"""Transaction models for Mercury Bank API."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Literal, Dict, Any
from dateutil.parser import parse as parse_date  # type: ignore[import]


@dataclass
class Address:
    """Address information."""

    address1: str
    city: str
    postalCode: str
    address2: Optional[str] = None
    state: Optional[str] = None  # 2-letter US state code
    region: Optional[str] = None
    country: Optional[str] = None  # iso3166Alpha2

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Address":
        """Create an Address from a dictionary."""
        return cls(
            address1=data["address1"],
            city=data["city"],
            postalCode=data["postalCode"],
            address2=data.get("address2"),
            state=data.get("state"),
            region=data.get("region"),
            country=data.get("country"),
        )


@dataclass
class DomesticWireRoutingInfo:
    """Domestic wire routing information."""

    accountNumber: str
    routingNumber: str
    bankName: Optional[str] = None
    address: Optional[Address] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DomesticWireRoutingInfo":
        """Create a DomesticWireRoutingInfo from a dictionary."""
        address = Address.from_dict(data["address"]) if data.get("address") else None
        return cls(
            accountNumber=data["accountNumber"],
            routingNumber=data["routingNumber"],
            bankName=data.get("bankName"),
            address=address,
        )


@dataclass
class ElectronicRoutingInfo:
    """Electronic routing information."""

    accountNumber: str
    routingnumber: str
    bankName: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ElectronicRoutingInfo":
        """Create an ElectronicRoutingInfo from a dictionary."""
        return cls(
            accountNumber=data["accountNumber"],
            routingnumber=data["routingnumber"],
            bankName=data.get("bankName"),
        )


@dataclass
class CorrespondentInfo:
    """Correspondent bank information."""

    routingNumber: Optional[str] = None
    swiftCode: Optional[str] = None
    bankName: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CorrespondentInfo":
        """Create a CorrespondentInfo from a dictionary."""
        return cls(
            routingNumber=data.get("routingNumber"),
            swiftCode=data.get("swiftCode"),
            bankName=data.get("bankName"),
        )


@dataclass
class BankDetails:
    """Bank details for international wires."""

    bankName: str
    cityState: Optional[str] = None
    country: Optional[str] = None  # iso3166Alpha2

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BankDetails":
        """Create a BankDetails from a dictionary."""
        return cls(
            bankName=data["bankName"],
            cityState=data.get("cityState"),
            country=data.get("country"),
        )


@dataclass
class CountrySpecificDataCanada:
    """Country-specific data for Canada."""

    bankCode: str
    transitNumber: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CountrySpecificDataCanada":
        """Create a CountrySpecificDataCanada from a dictionary."""
        return cls(bankCode=data["bankCode"], transitNumber=data["transitNumber"])


@dataclass
class CountrySpecificDataAustralia:
    """Country-specific data for Australia."""

    bsbCode: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CountrySpecificDataAustralia":
        """Create a CountrySpecificDataAustralia from a dictionary."""
        return cls(bsbCode=data["bsbCode"])


@dataclass
class CountrySpecificDataIndia:
    """Country-specific data for India."""

    ifscCode: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CountrySpecificDataIndia":
        """Create a CountrySpecificDataIndia from a dictionary."""
        return cls(ifscCode=data["ifscCode"])


@dataclass
class CountrySpecificDataRussia:
    """Country-specific data for Russia."""

    inn: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CountrySpecificDataRussia":
        """Create a CountrySpecificDataRussia from a dictionary."""
        return cls(inn=data["inn"])


@dataclass
class CountrySpecificDataPhilippines:
    """Country-specific data for Philippines."""

    routingNumber: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CountrySpecificDataPhilippines":
        """Create a CountrySpecificDataPhilippines from a dictionary."""
        return cls(routingNumber=data["routingNumber"])


@dataclass
class CountrySpecificDataSouthAfrica:
    """Country-specific data for South Africa."""

    branchCode: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CountrySpecificDataSouthAfrica":
        """Create a CountrySpecificDataSouthAfrica from a dictionary."""
        return cls(branchCode=data["branchCode"])


@dataclass
class CountrySpecific:
    """Country-specific routing information."""

    countrySpecificDataCanada: Optional[CountrySpecificDataCanada] = None
    countrySpecificDataAustralia: Optional[CountrySpecificDataAustralia] = None
    countrySpecificDataIndia: Optional[CountrySpecificDataIndia] = None
    countrySpecificDataRussia: Optional[CountrySpecificDataRussia] = None
    countrySpecificDataPhilippines: Optional[CountrySpecificDataPhilippines] = None
    countrySpecificDataSouthAfrica: Optional[CountrySpecificDataSouthAfrica] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CountrySpecific":
        """Create a CountrySpecific from a dictionary."""
        canada = None
        if data.get("countrySpecificDataCanada"):
            canada = CountrySpecificDataCanada.from_dict(
                data["countrySpecificDataCanada"]
            )

        australia = None
        if data.get("countrySpecificDataAustralia"):
            australia = CountrySpecificDataAustralia.from_dict(
                data["countrySpecificDataAustralia"]
            )

        india = None
        if data.get("countrySpecificDataIndia"):
            india = CountrySpecificDataIndia.from_dict(data["countrySpecificDataIndia"])

        russia = None
        if data.get("countrySpecificDataRussia"):
            russia = CountrySpecificDataRussia.from_dict(
                data["countrySpecificDataRussia"]
            )

        philippines = None
        if data.get("countrySpecificDataPhilippines"):
            philippines = CountrySpecificDataPhilippines.from_dict(
                data["countrySpecificDataPhilippines"]
            )

        south_africa = None
        if data.get("countrySpecificDataSouthAfrica"):
            south_africa = CountrySpecificDataSouthAfrica.from_dict(
                data["countrySpecificDataSouthAfrica"]
            )

        return cls(
            countrySpecificDataCanada=canada,
            countrySpecificDataAustralia=australia,
            countrySpecificDataIndia=india,
            countrySpecificDataRussia=russia,
            countrySpecificDataPhilippines=philippines,
            countrySpecificDataSouthAfrica=south_africa,
        )


@dataclass
class InternationalWireRoutingInfo:
    """International wire routing information."""

    iban: str
    swiftCode: str
    correspondentInfo: Optional[CorrespondentInfo] = None
    bankDetails: Optional[BankDetails] = None
    address: Optional[Address] = None
    phoneNumber: Optional[str] = None
    countrySpecific: Optional[CountrySpecific] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InternationalWireRoutingInfo":
        """Create an InternationalWireRoutingInfo from a dictionary."""
        correspondent_info = None
        if data.get("correspondentInfo"):
            correspondent_info = CorrespondentInfo.from_dict(data["correspondentInfo"])

        bank_details = None
        if data.get("bankDetails"):
            bank_details = BankDetails.from_dict(data["bankDetails"])

        address = None
        if data.get("address"):
            address = Address.from_dict(data["address"])

        country_specific = None
        if data.get("countrySpecific"):
            country_specific = CountrySpecific.from_dict(data["countrySpecific"])

        return cls(
            iban=data["iban"],
            swiftCode=data["swiftCode"],
            correspondentInfo=correspondent_info,
            bankDetails=bank_details,
            address=address,
            phoneNumber=data.get("phoneNumber"),
            countrySpecific=country_specific,
        )


@dataclass
class DebitCardInfo:
    """Debit card information."""

    id: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DebitCardInfo":
        """Create a DebitCardInfo from a dictionary."""
        return cls(id=data["id"])


@dataclass
class CreditCardInfo:
    """Credit card information."""

    id: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CreditCardInfo":
        """Create a CreditCardInfo from a dictionary."""
        return cls(id=data["id"])


@dataclass
class TransactionDetails:
    """Transaction details including routing information."""

    address: Optional[Address] = None
    domesticWireRoutingInfo: Optional[DomesticWireRoutingInfo] = None
    electronicRoutingInfo: Optional[ElectronicRoutingInfo] = None
    internationalWireRoutingInfo: Optional[InternationalWireRoutingInfo] = None
    debitCardInfo: Optional[DebitCardInfo] = None
    creditCardInfo: Optional[CreditCardInfo] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TransactionDetails":
        """Create a TransactionDetails from a dictionary."""
        address = None
        if data.get("address"):
            address = Address.from_dict(data["address"])

        domestic_wire = None
        if data.get("domesticWireRoutingInfo"):
            domestic_wire = DomesticWireRoutingInfo.from_dict(
                data["domesticWireRoutingInfo"]
            )

        electronic = None
        if data.get("electronicRoutingInfo"):
            electronic = ElectronicRoutingInfo.from_dict(data["electronicRoutingInfo"])

        international_wire = None
        if data.get("internationalWireRoutingInfo"):
            international_wire = InternationalWireRoutingInfo.from_dict(
                data["internationalWireRoutingInfo"]
            )

        debit_card = None
        if data.get("debitCardInfo"):
            debit_card = DebitCardInfo.from_dict(data["debitCardInfo"])

        credit_card = None
        if data.get("creditCardInfo"):
            credit_card = CreditCardInfo.from_dict(data["creditCardInfo"])

        return cls(
            address=address,
            domesticWireRoutingInfo=domestic_wire,
            electronicRoutingInfo=electronic,
            internationalWireRoutingInfo=international_wire,
            debitCardInfo=debit_card,
            creditCardInfo=credit_card,
        )


@dataclass
class CurrencyExchangeInfo:
    """Currency exchange information."""

    convertedFromCurrency: str
    convertedToCurrency: str
    convertedFromAmount: float
    convertedToAmount: float
    feeAmount: float
    feePercentage: float
    exchangeRate: float
    feeTransactionId: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CurrencyExchangeInfo":
        """Create a CurrencyExchangeInfo from a dictionary."""
        return cls(
            convertedFromCurrency=data["convertedFromCurrency"],
            convertedToCurrency=data["convertedToCurrency"],
            convertedFromAmount=float(data["convertedFromAmount"]),
            convertedToAmount=float(data["convertedToAmount"]),
            feeAmount=float(data["feeAmount"]),
            feePercentage=float(data["feePercentage"]),
            exchangeRate=float(data["exchangeRate"]),
            feeTransactionId=data["feeTransactionId"],
        )


@dataclass
class Attachment:
    """Transaction attachment."""

    fileName: str
    url: str  # Note: URLs expire after 12 hours
    attachmentType: Literal["checkImage", "receipt", "other"]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Attachment":
        """Create an Attachment from a dictionary."""
        return cls(
            fileName=data["fileName"],
            url=data["url"],
            attachmentType=data["attachmentType"],
        )


@dataclass
class Transaction:
    """Represents a Mercury bank transaction."""

    amount: float
    counterpartyId: str
    counterpartyName: str
    createdAt: datetime
    dashboardLink: str
    estimatedDeliveryDate: datetime
    id: str
    kind: Literal[
        "externalTransfer",
        "internalTransfer",
        "outgoingPayment",
        "creditCardCredit",
        "creditCardTransaction",
        "debitCardTransaction",
        "incomingDomesticWire",
        "checkDeposit",
        "incomingInternationalWire",
        "treasuryTransfer",
        "wireFee",
        "cardInternationalTransactionFee",
        "other",
    ]
    status: Literal["pending", "sent", "cancelled", "failed"]
    attachments: List[Attachment]

    # Optional fields
    bankDescription: Optional[str] = None
    counterpartyNickname: Optional[str] = None
    details: Optional[TransactionDetails] = None
    failedAt: Optional[datetime] = None
    note: Optional[str] = None
    externalMemo: Optional[str] = None
    postedAt: Optional[datetime] = None
    reasonForFailure: Optional[str] = None
    feeId: Optional[str] = None
    currencyExchangeInfo: Optional[CurrencyExchangeInfo] = None
    compliantWithReceiptPolicy: Optional[bool] = None
    hasGeneratedReceipt: Optional[bool] = None
    creditAccountPeriodId: Optional[str] = None
    mercuryCategory: Optional[str] = None
    generalLedgerCodeName: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Transaction":
        """Create a Transaction from a dictionary."""
        # Parse datetime fields
        created_at = data["createdAt"]
        if isinstance(created_at, str):
            created_at = parse_date(created_at)

        estimated_delivery_date = data["estimatedDeliveryDate"]
        if isinstance(estimated_delivery_date, str):
            estimated_delivery_date = parse_date(estimated_delivery_date)

        failed_at = None
        if data.get("failedAt"):
            failed_at = data["failedAt"]
            if isinstance(failed_at, str):
                failed_at = parse_date(failed_at)

        posted_at = None
        if data.get("postedAt"):
            posted_at = data["postedAt"]
            if isinstance(posted_at, str):
                posted_at = parse_date(posted_at)

        # Parse complex objects
        details = None
        if data.get("details"):
            details = TransactionDetails.from_dict(data["details"])

        currency_exchange_info = None
        if data.get("currencyExchangeInfo"):
            currency_exchange_info = CurrencyExchangeInfo.from_dict(
                data["currencyExchangeInfo"]
            )

        attachments = []
        for attachment_data in data.get("attachments", []):
            attachments.append(Attachment.from_dict(attachment_data))

        return cls(
            amount=float(data["amount"]),
            counterpartyId=data["counterpartyId"],
            counterpartyName=data["counterpartyName"],
            createdAt=created_at,
            dashboardLink=data["dashboardLink"],
            estimatedDeliveryDate=estimated_delivery_date,
            id=data["id"],
            kind=data["kind"],
            status=data["status"],
            attachments=attachments,
            bankDescription=data.get("bankDescription"),
            counterpartyNickname=data.get("counterpartyNickname"),
            details=details,
            failedAt=failed_at,
            note=data.get("note"),
            externalMemo=data.get("externalMemo"),
            postedAt=posted_at,
            reasonForFailure=data.get("reasonForFailure"),
            feeId=data.get("feeId"),
            currencyExchangeInfo=currency_exchange_info,
            compliantWithReceiptPolicy=data.get("compliantWithReceiptPolicy"),
            hasGeneratedReceipt=data.get("hasGeneratedReceipt"),
            creditAccountPeriodId=data.get("creditAccountPeriodId"),
            mercuryCategory=data.get("mercuryCategory"),
            generalLedgerCodeName=data.get("generalLedgerCodeName"),
        )


@dataclass
class TransactionResponse:
    """Response from the transactions API endpoint."""

    total: int
    transactions: List[Transaction]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TransactionResponse":
        """Create a TransactionResponse from a dictionary."""
        transactions = []
        for transaction_data in data.get("transactions", []):
            transactions.append(Transaction.from_dict(transaction_data))

        return cls(total=int(data["total"]), transactions=transactions)
