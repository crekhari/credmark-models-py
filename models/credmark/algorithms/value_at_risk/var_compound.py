from credmark.cmf.model import Model
from credmark.cmf.types import Portfolio, Position, Some
from credmark.dto import EmptyInput
from models.credmark.algorithms.value_at_risk.dto import (ContractVaRInput,
                                                          PortfolioVaRInput,
                                                          VaRHistoricalOutput)
from models.credmark.protocols.lending.compound.compound_v2 import \
    CompoundV2PoolInfo


@Model.describe(slug="finance.var-compound",
                version="1.4",
                display_name="Compound V2 VaR",
                description="Calcualte the VaR of Compound contract of its net asset",
                category='protocol',
                subcategory='compound',
                tags=['var'],
                input=ContractVaRInput,
                output=VaRHistoricalOutput)
class CompoundGetVAR(Model):
    """
    VaR of Compound based on its inventory of tokens.
    The exposure of Compound is the number of tokens borrowed (totalLiability)
    less than it lends out (cToken.totalBorrows).

    - cash =  Liability + Reserve - Borrow
    - exposure = totalBorrows - totalLiability = - cash

    Reference:
    https://docs.credmark.com/risk-insights/research/aave-and-compound-historical-var
    """

    def run(self, input: ContractVaRInput) -> VaRHistoricalOutput:
        pools_info = self.context.run_model('compound-v2.all-pools-info',
                                            input=EmptyInput(),
                                            return_type=Some[CompoundV2PoolInfo])
        positions = []
        for pool_info in pools_info:
            # borrow: debt
            # liability: supply
            amount = - pool_info.cash
            positions.append(Position(amount=amount, asset=pool_info.token))

        portfolio = Portfolio(positions=positions)

        var_input = PortfolioVaRInput(portfolio=portfolio, **input.dict())
        return self.context.run_model(slug='finance.var-portfolio-historical',
                                      input=var_input,
                                      return_type=VaRHistoricalOutput)
