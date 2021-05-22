from enum import Enum


class MessageType(Enum):
    Ok = "Ok"
    Total = "Total"
    UndoSuccess = "UndoSuccess"
    SameConfirm = "SameConfirm"
    EnergyQuery = "EnergyQuery"
    EnergyQueryRetry = "EnergyQueryRetry"
    AddingNotification = "AddingNotification"
    Math = "Math"
    BadInput = "BadInput"
    DbError = "DbError"
    SetUp = "SetUp"
    SetUpRetry = "SetUpRetry"
    Greet = "Greet"
