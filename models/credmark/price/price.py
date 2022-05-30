# pylint: disable=locally-disabled, unused-import
from typing import List, Union
import pandas as pd

from credmark.cmf.model import Model, ModelDataErrorDesc
from credmark.cmf.model.errors import ModelDataError, ModelRunError
from credmark.cmf.types import (
    Account,
    Address,
    Token,
    Tokens,
    Price,
    Contract,
    Accounts,
    Contracts,
)

from credmark.dto import DTO, IterableListGenericDTO, DTOField

from models.dtos.price import PriceInput, TokenOrCode


@Model.describe(slug='price.oracle-chainlink',
                version='1.0',
                display_name='Token Price - from Oracle',
                description='Get token\'s price from Oracle',
                input=PriceInput,
                output=Price)
class PriceOracle(Model):

    NATIVE_TOKEN = {
        1: Address('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'),
    }

    # TODO: need to find the address to find the feed in registry
    OVERRIDE_FEED = {
        1: {
            # WAVAX: avax-usd.data.eth
            Address('0x85f138bfEE4ef8e540890CFb48F620571d67Eda3'):
            ('0xFF3EEb22B5E3dE6e705b44749C2559d704923FD7', 'USD'),
            # WSOL: sol-usd.data.eth
            Address('0xD31a59c85aE9D8edEFeC411D448f90841571b89c'):
            ('0x4ffc43a60e009b551865a93d232e33fce9f01507', 'USD'),
            # BNB: bnb-usd.data.eth
            Address('0xB8c77482e45F1F44dE1745F52C74426C631bDD52'):
            ('0x14e613ac84a31f709eadbdf89c6cc390fdc9540a', 'USD'),
            # WBTC:
            Address('0x2260fac5e5542a773aa44fbcfedf7c193bc2c599'):
            ('0xf4030086522a5beea4988f8ca5b36dbc97bee88c', 'USD'),
            # WETH:
            Address('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'):
            ('0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419', 'USD')
        }
    }

    # ilv-eth.data.eth
    # Address('0x767FE9EDC9E0dF98E07454847909b5E959D7ca0E')
    # bit-usd.data.eth
    # Address('0x1a4b46696b2bb4794eb3d4c26f1c55f9170fa4c5')
    # ohm-eth.data.eth
    # Address('0x64aa3364F17a4D01c6f1751Fd97C2BD3D7e7f1D5')
    # tribe-eth.data.eth
    # Address('0xc7283b66Eb1EB5FB86327f08e1B5816b0720212B'):

    CONVERT_FOR_TOKEN_PRICE = {
        1: {
            Address('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'):
            Address('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'),
            Address('0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB'):
            Address('0x2260fac5e5542a773aa44fbcfedf7c193bc2c599'),
        }
    }

    ROUTING_TOKEN = [
        Token(address='0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'),  # ETH
        Token(address='0x0000000000000000000000000000000000000348')  # USD
    ]

    """
    Return the value of base token in amount of quote tokens
    """

    def cross_price(self, price0: Price, price1: Price) -> Price:
        return Price(price=price0.price * price1.price, src=f'{price0.src},{price1.src}')

    def run(self, _: PriceInput) -> Price:  # pylint: disable=too-many-return-statements)
        base = _.base
        if _.quote is None:
            quote = Token(address=self.NATIVE_TOKEN[self.context.chain_id])
        else:
            quote = _.quote

        if base == quote:
            return Price(price=1, src=f'{self.slug}|Equal')

        try:
            return self.context.run_model('chainlink.price-by-registry',
                                          input={'base': base, 'quote': quote},
                                          return_type=Price)
        except ModelRunError:
            try:
                p = self.context.run_model('chainlink.price-by-registry',
                                           input={'base': quote, 'quote': base},
                                           return_type=Price)
                p.price = 1 / p.price
                p.src = f'{p.src}|Inverse'
                return p
            except ModelRunError:
                override_base = self.OVERRIDE_FEED[self.context.chain_id].get(base.address, None)
                override_quote = self.OVERRIDE_FEED[self.context.chain_id].get(quote.address, None)

                if override_base is not None:
                    p0 = self.context.run_model('chainlink.price-by-feed',
                                                input=Account(address=Address(override_base[0])),
                                                return_type=Price)
                    if TokenOrCode.validate(override_base[-1]) == quote:
                        return p0
                    else:
                        p1 = self.context.run_model(
                            self.slug,
                            input={'base': override_base[-1], 'quote': quote},
                            return_type=Price)
                        return self.cross_price(p0, p1)

                if override_quote is not None:
                    p0 = self.context.run_model('chainlink.price-by-feed',
                                                input=Account(address=Address(override_quote[0])),
                                                return_type=Price)
                    p0.price = 1 / p0.price
                    p0.src = f'{p0.src}|Inverse'
                    if TokenOrCode.validate(override_quote[-1]) == base:
                        return p0
                    else:
                        p1 = self.context.run_model(
                            self.slug,
                            input={'base': override_quote[-1], 'quote': base},
                            return_type=Price)
                        p1.price = 1 / p1.price
                        p1.src = f'{p1.src}|Inverse'
                    return self.cross_price(p0, p1)

                for routing_token in self.ROUTING_TOKEN:
                    if routing_token not in [quote, base]:
                        try:
                            p0 = self.context.run_model(
                                self.slug,
                                input={'base': base, 'quote': routing_token},
                                return_type=Price)
                            p1 = self.context.run_model(
                                self.slug,
                                input={'base': routing_token, 'quote': quote},
                                return_type=Price)
                        except ModelRunError:
                            continue
                        return self.cross_price(p0, p1)

                raise ModelRunError(f'No possible routing for token pair {base}/{quote}')
