import pandas as pd
from typing import Optional

from credmark.cmf.model import Model
from credmark.cmf.model.errors import ModelDataError, ModelRunError
from credmark.cmf.types import (Account, Address, Contract, Contracts,
                                NativeToken, Network, Portfolio, Position,
                                PriceWithQuote, Some, Token)
from credmark.cmf.types.compose import MapInputsOutput
from credmark.dto import DTO, EmptyInput
from models.credmark.tokens.token import get_eip1967_proxy_err
from models.dtos.tvl import LendingPoolPortfolios
from models.tmp_abi_lookup import AAVE_STABLEDEBT_ABI
from web3.exceptions import ABIFunctionNotFound

@Model.describe(
    slug="aave-v2.reserve-config",
    version="0.1",
    display_name="Aave V2 reserve configuration data",
    description="Aave V2 metadata of the inputted reserve token",
    category="protocol",
    subcategory="aave-v2",
    input=Token,
    output=dict,
)

class AaveV2GetReserveConfigurationData(Model):
    def run(self, input: Token) -> dict:
        protocolDataProvider = self.context.run_model(
            "aave-v2.get-protocol-data-provider",
            input=EmptyInput(),
            return_type=Contract,
            local=True,
        )
        data = protocolDataProvider.functions.getReserveConfigurationData(input.address).call()
        reserveConfigDict = {
            'decimals': data[0],
            'ltv': data[1],
            'liquidationThreshold': data[2],
            'liquidationBonus': data[3],
            'reserveFactor': data[4],
            'usageAsCollateralEnabled': data[5],
            'borrowingEnabled': data[6],
            'stableBorrowRateEnabled': data[7],
            'isActive': data[8],
            'isFrozen': data[9]
        }
        return reserveConfigDict