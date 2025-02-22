# pylint:disable=locally-disabled,line-too-long

from cmf_test import CMFTest


class TestChainlink(CMFTest):
    block_number: int = 15000108

    def test_ens(self):
        self.title('Chainlink - ENS')

        self.run_model('chainlink.price-by-ens', {"domain": "eth-usd.data.eth"}, block_number=self.block_number)
        self.run_model('chainlink.price-by-ens', {"domain": "comp-eth.data.eth"}, block_number=self.block_number)
        self.run_model('chainlink.price-by-ens', {"domain": "avax-usd.data.eth"}, block_number=self.block_number)
        self.run_model('chainlink.price-by-ens', {"domain": "bnb-usd.data.eth"}, block_number=self.block_number)
        self.run_model('chainlink.price-by-ens', {"domain": "sol-usd.data.eth"}, block_number=self.block_number)

    def test_price_by_registry(self):
        self.title('Chainlink - registry')

        # AAVE 0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9
        self.run_model('chainlink.price-by-registry', {"base": {"address": "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9"},
                                                       "quote": {"address": "0x0000000000000000000000000000000000000348"}}, block_number=self.block_number)  # chainlink.get-feed-registry
        self.run_model('chainlink.price-by-registry', {"base": {"address": "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9"},
                                                       "quote": {"address": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"}}, block_number=self.block_number)
        self.run_model('chainlink.price-from-registry-maybe',
                       {"base": {"address": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"}}, block_number=self.block_number)

    def test_price_quote(self):
        self.title('Chainlink - price quote')

        self.run_model('price.cex', {"base": {"symbol": "AAVE"}}, block_number=self.block_number)
        self.run_model('price.cex', {"base": {"symbol": "WETH"}}, block_number=self.block_number)
        self.run_model('price.cex', {"base": {"symbol": "WBTC"}}, block_number=self.block_number)
        self.run_model('price.cex', {
                       "base": {"address": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"}}, block_number=self.block_number)
        self.run_model('price.cex', {
                       "base": {"address": "0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB"}}, block_number=self.block_number)
        self.run_model('price.cex', {
                       "base": {"address": "0xD31a59c85aE9D8edEFeC411D448f90841571b89c"}}, block_number=self.block_number)

        block_number = 15249443
        self.run_model('price.cex', {"base": {"symbol": "WBTC"}}, block_number=block_number)
        self.run_model('price.cex', {"base": {"symbol": "BTC"}}, block_number=block_number)
        self.run_model('price.cex', {"base": {"symbol": "WETH"}}, block_number=block_number)
        self.run_model('price.cex', {"base": {"symbol": "ETH"}}, block_number=block_number)
        self.run_model('price.cex', {"base": {"symbol": "AAVE"}}, block_number=block_number)
        self.run_model('price.cex', {"base": {"symbol": "USD"}}, block_number=block_number)

    def test_oracle_chainlink(self):
        self.title('Chainlink - Oracle')

        self.run_model('price.oracle-chainlink',
                       {"base": {"address": "0xD31a59c85aE9D8edEFeC411D448f90841571b89c"}}, block_number=self.block_number)
        self.run_model('price.oracle-chainlink',
                       {"base": {"address": "0x1a4b46696b2bb4794eb3d4c26f1c55f9170fa4c5"}}, block_number=self.block_number)
        self.run_model('price.oracle-chainlink',
                       {"base": {"address": "0x64aa3364F17a4D01c6f1751Fd97C2BD3D7e7f1D5"}}, block_number=self.block_number)
        self.run_model('price.oracle-chainlink',
                       {"base": {"address": "0x383518188C0C6d7730D91b2c03a03C837814a899"}}, block_number=self.block_number)
        self.run_model('price.oracle-chainlink', {"base": {"symbol": "AAVE"}}, block_number=self.block_number)
        self.run_model('price.oracle-chainlink', {"base": {"symbol": "WETH"}}, block_number=self.block_number)
        self.run_model('price.oracle-chainlink', {"base": {"symbol": "WBTC"}}, block_number=self.block_number)
        self.run_model('price.oracle-chainlink',
                       {"base": {"address": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"}}, block_number=self.block_number)
        self.run_model('price.oracle-chainlink',
                       {"base": {"address": "0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB"}}, block_number=self.block_number)

    def test_price_by_feed(self):
        self.title('Chainlink - Feed')

        self.run_model('chainlink.price-by-feed',
                       {"address": "0x37bC7498f4FF12C19678ee8fE19d713b87F6a9e6"}, block_number=self.block_number)  # simple feed
        self.run_model('chainlink.price-by-feed',
                       {"address": "0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419"}, block_number=self.block_number)  # aggregator
