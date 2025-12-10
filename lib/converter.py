import sys
import requests

API_conversions = "https://api.frankfurter.dev/v1/latest"
API_parms = {
    "base": "CAD",
    "symbols": "PHP,USD"
}

class Converter:
    base = "CAD"
    targets = "PHP,USD"
    rates = {}

    def __init__(self, base, targets):
        self.updateFactors(base, targets)

    # Get the current conversion rates
    def checkRates(self):
        API_parms["base"] = self.base
        API_parms["symbols"] = self.targets
        response = requests.get(API_conversions, params = API_parms)
        data = response.json()
        self.rates = data["rates"]

    def updateFactors(self, base, targets):
        if base:
            self.base = base
        if targets:
            self.targets = targets
        self.checkRates()

    # convert currency1 to currency2
    def convert(self, amt, toVal, reverse = False):
        result = 0
        factor = 1
        if toVal in self.rates.keys():
            factor = self.rates[toVal]
            if reverse:
                result = amt / factor
            else:
                result = amt * factor
        return result

# cli conversion
def cliConverter(args):
    isErr = False
    base = "CAD"
    target = "PHP"
    amount = 1
    reverse = False
    try:
        if args[1]:
            base = args[1]
        if args[2]:
            target = args[2]
        if args[3]:
            amount = args[3]
        if args[4]:
            reverse = args[4]
        con = Converter(base, target)
        result = con.convert(amount, target, reverse)
        print(result)
    except:
        print(f"Incorrect Params detected: {args}")

# only trigger this function if parameters are passed
if len(sys.argv) > 1: cliConverter(sys.argv)