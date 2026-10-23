"""The CornerCart shop guide: four short pages of demo text (storage tips, delivery, returns, labels).

Written for the chunking lesson: long enough to split, short enough to read. Demo data, not real policy.
"""

GUIDE = {
    "01-storage-tips.md": """# Storing your groceries

*CornerCart demo data. This guide is invented for the lessons.*

Good storage keeps food fresh longer and wastes less money. These tips use metric units and Celsius.

## The fridge (1 to 5 degrees C)

Milk, yogurt, butter, cheese and eggs belong in the fridge. Keep milk on a middle shelf rather than in the door,
because the door is the warmest part. Once opened, fresh milk keeps for about 3 to 4 days, and plant drinks for
about 5 days. Eggs keep for roughly three weeks in the fridge; keep them in their box so they do not pick up
smells from other food.

Cooked rice must be cooled quickly and eaten within a day. Put it in a shallow box and refrigerate it within an
hour of cooking.

## The cupboard (cool, dry, dark)

Rice, pasta, flour, lentils, beans and oats keep for a year or more if they are sealed. Move them into airtight
jars after opening, which also keeps out pantry moths. Store oils away from the stove, because heat and light
turn oil bitter. Coffee tastes best within a month of opening; keep it in a sealed container, not in the fridge.

Tea bags and spices lose their flavour slowly. Write the opening date on the lid and replace spices every year.

## Fruit and vegetables

Bananas, mangoes and avocados ripen on the counter; once ripe, move them to the fridge to slow them down.
Apples keep best in the fridge. Potatoes, onions and garlic like a cool, dark, airy place but not the fridge, and
they should not be stored together: onions make potatoes sprout sooner. Leafy vegetables stay crisp when wrapped
in a slightly damp cloth inside a box in the fridge.

## The freezer (minus 18 degrees C)

Frozen peas, berries and fish fingers keep their quality for months. Freeze bread in slices so you can toast one
at a time. Label bags with the date. Never refreeze food that has fully thawed at room temperature.

## Cleaning supplies

Keep cleaning products in their original bottles, out of reach of children and pets, and never store them next to
food. Do not mix bleach with other cleaners.
""",
    "02-delivery.md": """# Delivery

*CornerCart demo data. Times are in UTC; your order page shows your local time.*

## How delivery works

CornerCart delivers from the corner shop to your door. After you place an order it moves through three steps:
placed, packed and invoiced. You can follow the steps on your order status page. Most orders are packed within two
hours of being placed during opening hours.

## Delivery slots and cut-off times

Orders placed before 14:00 UTC are delivered the same day in the evening slot. Orders placed after 14:00 UTC are
delivered the next morning. There are three slots: morning (08:00 to 12:00), afternoon (12:00 to 17:00) and
evening (17:00 to 21:00). Slots are shown in UTC and in your local time at checkout.

## Delivery charges

Orders of 30 US dollars or more are delivered free. Smaller orders pay a flat fee of 3.50 US dollars. Prices on
the demo shop are in US dollars; a real shop would show the price in your own currency, and what you pay depends
on your country, taxes and delivery distance.

## Cold items

Chilled and frozen items travel in insulated bags with ice packs. Please put them away within two hours of
delivery. If the bag feels warm when it arrives, tell us on the order page and we will refund the item.

## Substitutions

If something is out of stock, the picker may offer a similar product of the same pack size. You can turn
substitutions off in your basket. Products with allergen labels, such as gluten-free or nut-free items, are only
ever replaced by products with the same labels.

## Missed deliveries

If nobody is home, the driver leaves safe items with a neighbour or in a safe place you named. Chilled and frozen
items are never left unattended; the driver brings them back and we rebook the slot for free.
""",
    "03-returns-and-refunds.md": """# Returns and refunds

*CornerCart demo data. This is an invented policy for the lessons.*

## Something wrong with your order

If an item is damaged, spoiled, missing or not what you ordered, tell us within 48 hours of delivery from the
order status page. Choose the item, say what is wrong and, if you can, add a photo. You do not need to send the
item back. We refund the price of the item to the original payment method, normally within five working days.

## Fresh food and best-before dates

Fresh food (fruit, vegetables, dairy, eggs and bakery) is guaranteed to arrive with at least two days left before
its date. If it does not, you will be refunded in full. Packaged food is guaranteed to arrive with at least a month
left, unless the product page says otherwise.

## Changing your mind

Because food cannot be resold, we cannot take back opened or perishable items just because you changed your mind.
Unopened household items, such as sponges, bin bags or kitchen towels, can be returned within 14 days in their
original packaging. The return is free if you ask for it from the order page.

## Cancelling an order

You can cancel an order for free while it is still in the placed step. Once an order is packed we can no longer
cancel it, but you may refuse the delivery and receive a refund when the bags come back to the shop.

## Allergy and diet mistakes

If a product labelled gluten-free, vegan, sugar-free or nut-free turns out not to match its label, stop using it,
contact us at once and keep the packaging. We will refund the order, investigate with the supplier and tell you
what we find. Labels on this page and on the product pages are demo data and must never be used for real
allergy decisions.

## How refunds are shown

A refund appears on the order page as a line with a minus sign. It is calculated in US dollars. Your bank may show
the amount in your own currency, and the exchange rate used is your bank's, not ours.
""",
    "04-diet-and-labels.md": """# Diet tags and labels

*CornerCart demo data. Tags on this demo shop are invented and are not safe for real allergy decisions.*

Each product page shows small tags. This page explains what they mean in the shop.

## Gluten-free

A product tagged gluten-free contains no wheat, barley, rye or ordinary oats among its ingredients. Oats are only
tagged gluten-free when the pack says they were grown and milled separately from other grains.

## Vegan

Vegan means no meat, fish, eggs, milk, honey or any other ingredient from animals. Honey is not vegan on
CornerCart.

## Sugar-free

On CornerCart, sugar-free means no sugar has been added. Whole fruit and plain milk still contain natural sugars,
and are tagged sugar-free because nothing was added. Fruit juice is not tagged sugar-free.

## Nut-free

Nut-free means no tree nuts or peanuts among the ingredients. Many nut-free products are made in kitchens that
also handle nuts, so people with a severe allergy should read the full label on the pack.

## Asking the shop

On the storefront, the "Ask the shop" box understands these tags. Typing "something vegan for dinner under $8"
filters the catalogue by the vegan tag and the price, and then looks for dinner products. In keyword mode the shop
matches words; in AI mode the shop also understands meaning.

## Pack sizes

Every pack size is metric: grams (g), kilograms (kg), millilitres (mL), litres (L), or a count such as 12 eggs.
The price shown is the price of the whole pack.
""",
}
