class TreasureHuntException(Exception):
    ...


class RepositoryException(TreasureHuntException):
    ...


class WinnerAlreadyExists(RepositoryException):
    ...


class MailGatewayException(TreasureHuntException):
    ...
