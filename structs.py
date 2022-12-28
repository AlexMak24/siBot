########################################################################################################################
# IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT #
########################################################################################################################

# importing libraries
from dataclasses import dataclass


########################################################################################################################
# PURCHASE ## PURCHASE ## PURCHASE ## PURCHASE ## PURCHASE ## PURCHASE ## PURCHASE ## PURCHASE ## PURCHASE ## PURCHASE #
########################################################################################################################

# Purchase Class
@dataclass
class Purchase:
    ticker: str     # ticker of purchased coin
    price: float    # purchased price
    amount: float   # received amount (coin)
    total: float    # expended money (USD)
    fee: float      # fees (coin)
    date: str       # purchase date
    pair: str       # transaction pair

    # operator <
    def __lt__(self, other):
        return self.price < other.price


########################################################################################################################
# SALE ## SALE ## SALE ## SALE ## SALE ## SALE ## SALE ## SALE ## SALE ## SALE ## SALE ## SALE ## SALE ## SALE ## SALE #
########################################################################################################################

# Sale Class
@dataclass
class Sale:
    ticker: str     # ticker of sold coin
    price: float    # sold price
    amount: float   # sold amount (coin)
    total: float    # received money (USD)
    fee: float      # fees (coin)
    date: str       # sale date
    pair: str       # transaction pair

########################################################################################################################
# END ## END ## END ## END ## END ## END ## END ## END ### END ## END ## END ## END ## END ## END ## END ## END ## END #
########################################################################################################################
