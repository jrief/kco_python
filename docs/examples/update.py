'''Update example

This file demonstrates the use of the Klarna library to update an order.
'''
# Copyright 2013 Klarna AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# [[examples-update]]
import klarnacheckout

# Dictionary containing the cart items
cart = (
    {
        'quantity': 1,
        'reference': '123456789',
        'name': 'Klarna t-shirt',
        'unit_price': 12300,
        'discount_rate': 1000,
        'tax_rate': 2500
    }, {
        'quantity': 1,
        'type': 'shipping_fee',
        'reference': 'SHIPPING',
        'name': 'Shipping Fee',
        'unit_price': 4900,
        'tax_rate': 2500
    }
)

# Merchant ID
eid = "0"

# Shared Secret
shared_secret = 'shared_secret'

klarnacheckout.Order.content_type = \
    'application/vnd.klarna.checkout.aggregated-order-v2+json'
klarnacheckout.Order.base_uri = \
    'https://checkout.testdrive.klarna.com/checkout/orders'

connector = klarnacheckout.create_connector(shared_secret)

resource_location = \
    'https://checkout.testdrive.klarna.com/checkout/orders/ABC123'

order = klarnacheckout.Order(connector, resource_location)

# Reset cart
data = {'cart': []}
data["cart"] = {"items": []}

for item in cart:
    data["cart"]["items"].append(item)

order.update(data)
# [[examples-update]]
