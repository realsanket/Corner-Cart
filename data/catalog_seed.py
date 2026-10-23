"""The vocabulary the generator builds the demo catalogue from. Everyday groceries, no real brand names.

One base item per line:  category | name | pack set | base price (US$, middle pack) | diet tags | meals | note
Diet tags:  g gluten-free  v vegan  s sugar-free (no sugar added)  n nut-free.   Meals:  b breakfast  l lunch  d dinner  s snack.
"""

PACKS = {
    "L": [("500 mL", 0.6), ("1 L", 1.0), ("2 L", 1.8)],
    "G": [("250 g", 0.55), ("500 g", 1.0), ("1 kg", 1.8)],
    "S": [("100 g", 0.5), ("200 g", 1.0)],
    "K": [("1 kg", 1.0), ("2 kg", 1.9), ("5 kg", 4.2)],
    "M": [("500 g", 1.0), ("1 kg", 1.8)],
    "BG": [("125 g", 0.55), ("250 g", 1.0)],
    "E": [("6 eggs", 0.55), ("12 eggs", 1.0), ("30 eggs", 2.3)],
    "TB": [("40 bags", 0.55), ("80 bags", 1.0), ("160 bags", 1.8)],
    "U4": [("4 pack", 1.0), ("8 pack", 1.9)],
    "U6": [("6 pack", 1.0), ("12 pack", 1.8)],
    "DR": [("330 mL", 0.5), ("1.5 L", 1.0), ("6 x 1.5 L", 5.0)],
    "TN": [("400 g", 1.0), ("800 g", 1.8)],
    "SP": [("50 g", 0.6), ("100 g", 1.0), ("250 g", 2.2)],
    "LOAF": [("400 g", 1.0), ("800 g", 1.7)],
    "TAB": [("30 tablets", 1.0), ("60 tablets", 1.8)],
    "WIPE": [("40 wipes", 0.6), ("80 wipes", 1.0)],
    "BAG": [("30 bags", 1.0), ("60 bags", 1.8)],
    "SPG": [("6 sponges", 1.0), ("12 sponges", 1.8)],
    "ROLL": [("6 rolls", 0.7), ("12 rolls", 1.3)],
    "FOIL": [("20 m", 1.0), ("50 m", 2.2)],
    "PR": [("200 g", 1.0), ("400 g", 1.8)],
}

BASES = """
Dairy & Eggs|Whole Milk|L|1.10|gsn|b|Fresh whole milk, lovely with breakfast cereal, tea or coffee.
Dairy & Eggs|Semi-Skimmed Milk|L|1.05|gsn|b|Lighter milk with less fat, good on cereal and in hot drinks.
Dairy & Eggs|Skimmed Milk|L|1.00|gsn|b|Fat-free milk for tea, coffee and breakfast bowls.
Dairy & Eggs|Lactose-Free Milk|L|1.60|gsn|b|Milk without lactose, for people who find ordinary milk hard to digest.
Dairy & Eggs|Oat Drink|L|1.50|vsn|b|A creamy plant drink made from oats, nice in coffee and porridge.
Dairy & Eggs|Soy Drink|L|1.30|gvsn|b|An unsweetened plant drink made from soya beans, a good all-rounder.
Dairy & Eggs|Almond Drink|L|1.70|gvs|b|A light, nutty plant drink for cereal and smoothies.
Dairy & Eggs|Plain Yogurt|G|1.50|gsn|b|Mild plain yogurt for breakfast bowls, dips and cooking.
Dairy & Eggs|Greek Yogurt|G|2.20|gsn|b|Thick, creamy strained yogurt that is high in protein.
Dairy & Eggs|Fruit Yogurt|G|1.80|gn|b|Yogurt swirled with fruit, an easy breakfast or snack.
Dairy & Eggs|Soy Yogurt|G|2.00|gvsn|b|A dairy-free yogurt made from soya, good with fruit at breakfast.
Dairy & Eggs|Salted Butter|S|2.60|gsn|b|Classic salted butter for toast, baking and cooking.
Dairy & Eggs|Cream Cheese|S|2.40|gsn|b|Soft, spreadable cheese for bagels, sandwiches and dips.
Dairy & Eggs|Mature Cheddar Cheese|S|3.80|gsn|l|A sharp, crumbly hard cheese for sandwiches and grating.
Dairy & Eggs|Mozzarella|S|2.50|gsn|d|Soft, stretchy cheese for pizza, salads and baked pasta.
Dairy & Eggs|Cottage Cheese|S|2.30|gsn|b|Fresh, lumpy cheese that is lovely on toast for breakfast or lunch.
Dairy & Eggs|Eggs|E|2.60|gsn|b|Hen's eggs for boiling, frying and baking; a classic breakfast food.
Dairy & Eggs|Paneer|S|2.80|gsn|d|Firm fresh cheese that holds its shape in curries and grills.
Dairy & Eggs|Ghee|S|4.50|gsn|d|Clarified butter with a rich, nutty flavour for cooking.
Bakery|Sliced White Bread|LOAF|1.50|n|b|A soft sandwich loaf, ready sliced for toast and lunch boxes.
Bakery|Wholemeal Bread|LOAF|1.90|n|b|A hearty loaf made with wholemeal flour for toast and sandwiches.
Bakery|Sourdough Loaf|LOAF|3.20|vn|b|A slow-fermented loaf with a chewy crust and a gentle tang.
Bakery|Seeded Bread|LOAF|2.60|vn|b|A loaf packed with sunflower and pumpkin seeds.
Bakery|Rye Bread|LOAF|2.60|vn|l|A dense, dark loaf that keeps well and suits open sandwiches.
Bakery|Pita Bread|U6|1.70|vn|l|Soft flatbread pockets for fillings, dips and falafel.
Bakery|Naan Bread|U4|2.20|n|d|Soft oven-baked flatbread to scoop up curries.
Bakery|Tortilla Wraps|U6|2.10|vn|l|Soft wraps for burritos, fajitas and packed lunches.
Bakery|Bagels|U4|2.40|vn|b|Dense, chewy rings that toast beautifully for breakfast.
Bakery|Croissants|U4|2.90|n|b|Buttery, flaky pastries for a weekend breakfast.
Bakery|Burger Buns|U6|1.80|n|d|Soft buns for burgers and veggie patties.
Bakery|Gluten-Free Bread|LOAF|3.90|gvn|b|A sliced loaf made without wheat, good toasted for breakfast.
Bakery|Gluten-Free Wraps|U6|3.50|gvn|l|Soft wraps without wheat for lunch fillings.
Bakery|Crispbread|S|2.00|vn|l|Crisp, dry crackerbread for cheese, hummus and soup.
Bakery|Blueberry Muffins|U4|3.00|n|b|Soft muffins dotted with blueberries, nice with a morning coffee.
Breakfast|Rolled Oats|G|1.80|vsn|b|Whole rolled oats for porridge, flapjacks and overnight oats at breakfast.
Breakfast|Gluten-Free Oats|G|3.20|gvsn|b|Oats grown and milled apart from other grains, for a gluten-free breakfast porridge.
Breakfast|Muesli|G|3.40|vn|b|A mix of oats, seeds and dried fruit; eat with milk or yogurt for breakfast.
Breakfast|Crunchy Granola|G|3.90|vn|b|Baked oat clusters to sprinkle over yogurt at breakfast.
Breakfast|Cornflakes|G|2.50|vn|b|Toasted corn flakes, a quick breakfast cereal.
Breakfast|Puffed Rice Cereal|G|2.80|gvn|b|Light puffed rice cereal that is gluten-free, an easy breakfast with milk.
Breakfast|Bran Flakes|G|2.70|vn|b|Wheat bran flakes for a high-fibre breakfast.
Breakfast|Buckwheat Porridge|G|3.10|gvsn|b|A warm gluten-free porridge made from buckwheat, ready in five minutes for breakfast.
Breakfast|Quinoa Flakes|G|4.00|gvsn|b|Fine quinoa flakes that cook into a gluten-free breakfast porridge.
Breakfast|Pancake Mix|G|2.20|vn|b|Just add milk or water for fluffy weekend pancakes.
Breakfast|Gluten-Free Pancake Mix|G|3.60|gvn|b|A gluten-free mix for fluffy pancakes at breakfast.
Breakfast|Maple-Style Syrup|S|4.20|gvn|b|A sweet syrup for pancakes, waffles and porridge.
Breakfast|Honey|G|4.50|gn|b|Runny golden honey for toast, porridge and tea.
Breakfast|Strawberry Jam|S|2.40|gvn|b|Fruity jam for toast and scones at breakfast.
Breakfast|Orange Marmalade|S|2.50|gvn|b|Bittersweet orange marmalade for breakfast toast.
Breakfast|Peanut Butter|S|3.00|gvs|b|Smooth peanut butter for toast, sandwiches and smoothies.
Breakfast|Almond Butter|S|6.50|gvs|b|A rich, smooth nut butter for toast and porridge.
Breakfast|Sunflower Seed Butter|S|5.50|gvsn|b|A nut-free spread made from sunflower seeds, for breakfast toast.
Breakfast|Breakfast Bars|U6|3.20|vn|b|Oat and fruit bars to grab on the way out of the door.
Breakfast|Chia Seeds|S|4.00|gvsn|b|Tiny seeds to stir into yogurt, porridge and breakfast puddings.
Fruit|Bananas|M|1.60|gvsn|b|Sweet, ready-to-eat bananas for breakfast, snacks and baking.
Fruit|Apples|M|2.40|gvsn|b|Crisp apples to eat fresh or bake.
Fruit|Pears|M|2.60|gvsn|s|Juicy, soft pears for lunch boxes.
Fruit|Oranges|M|2.80|gvsn|b|Juicy oranges for eating, squeezing and breakfast juice.
Fruit|Lemons|M|2.00|gvsn|d|Zesty lemons for drinks, dressings and cooking.
Fruit|Limes|BG|2.20|gvsn|d|Tangy limes for drinks, curries and salsa.
Fruit|Grapes|M|3.50|gvsn|s|Sweet seedless grapes, a handy snack.
Fruit|Strawberries|BG|3.50|gvsn|b|Ripe red strawberries, lovely on cereal or yogurt at breakfast.
Fruit|Blueberries|BG|3.80|gvsn|b|Plump blueberries for breakfast bowls and baking.
Fruit|Mangoes|M|2.90|gvsn|s|Sweet, juicy mangoes when in season.
Fruit|Pineapple|M|2.70|gvsn|s|Golden pineapple, sweet and tangy.
Fruit|Watermelon|K|3.00|gvsn|s|Cool, juicy watermelon for hot days.
Fruit|Kiwi Fruit|M|2.60|gvsn|b|Tangy green kiwi fruit, packed with vitamin C, nice at breakfast.
Fruit|Avocados|M|3.40|gvsn|l|Creamy avocados for toast, salads and guacamole.
Fruit|Peaches|M|3.10|gvsn|s|Soft, fragrant peaches in summer.
Fruit|Dried Dates|S|3.30|gvsn|s|Soft, sticky dates for snacks and baking.
Vegetables|Tomatoes|M|2.40|gvsn|l|Ripe tomatoes for salads, sauces and sandwiches.
Vegetables|Onions|K|1.60|gvsn|d|Everyday brown onions for the base of almost every dish.
Vegetables|Potatoes|K|2.20|gvsn|d|All-round potatoes for mashing, roasting and boiling.
Vegetables|Carrots|M|1.30|gvsn|l|Sweet, crunchy carrots to eat raw or cook.
Vegetables|Baby Spinach|BG|2.10|gvsn|l|Tender spinach leaves for salads and smoothies.
Vegetables|Broccoli|M|2.30|gvsn|d|Fresh green broccoli to steam or roast.
Vegetables|Cauliflower|M|2.50|gvsn|d|A whole white cauliflower for roasting and curries.
Vegetables|Cucumber|M|1.40|gvsn|l|Cool, crisp cucumber for salads and raita.
Vegetables|Bell Peppers|M|3.20|gvsn|d|Sweet red, yellow and green peppers.
Vegetables|Garlic|SP|1.80|gvsn|d|Fresh garlic bulbs for savoury cooking.
Vegetables|Ginger|S|1.90|gvsn|d|Fresh root ginger for teas, stir-fries and curries.
Vegetables|Lettuce|U4|1.70|gvsn|l|Crisp leaves for salads and sandwiches.
Vegetables|Cabbage|M|1.50|gvsn|d|A firm cabbage for slaw, soups and stir-fries.
Vegetables|Zucchini|M|2.20|gvsn|d|Mild courgettes to grill, fry or spiralise.
Vegetables|Eggplant|M|2.60|gvsn|d|Glossy aubergines for curries and bakes.
Vegetables|Sweet Potatoes|K|2.90|gvsn|d|Orange sweet potatoes for roasting and mash.
Vegetables|Mushrooms|BG|2.40|gvsn|d|Closed cap mushrooms for frying and soups.
Vegetables|Green Beans|M|2.80|gvsn|d|Fresh green beans to steam or stir-fry.
Vegetables|Sweetcorn Cobs|U4|2.50|gvsn|d|Sweet corn on the cob for grilling and boiling.
Vegetables|Pumpkin|K|2.40|gvsn|d|Orange pumpkin for soups and roasts.
Vegetables|Beetroot|M|1.90|gvsn|l|Earthy beetroot for salads and juices.
Vegetables|Spring Onions|U6|1.20|gvsn|l|Mild green onions for salads and noodles.
Vegetables|Chili Peppers|BG|1.80|gvsn|d|Fresh chillies to add heat to any dish.
Rice, Pasta & Grains|Basmati Rice|K|3.50|gvsn|d|Long, fragrant grains for biryani and everyday meals.
Rice, Pasta & Grains|Jasmine Rice|K|3.40|gvsn|d|Soft, slightly sticky rice that goes with stir-fries and curries.
Rice, Pasta & Grains|Brown Rice|K|3.10|gvsn|d|Wholegrain rice with a nutty bite.
Rice, Pasta & Grains|Short-Grain Rice|K|3.30|gvsn|d|Sticky rice for sushi, risotto and rice pudding.
Rice, Pasta & Grains|Spaghetti|G|1.40|vn|d|Classic long pasta for a quick dinner.
Rice, Pasta & Grains|Penne|G|1.40|vn|d|Tube-shaped pasta that holds thick sauces.
Rice, Pasta & Grains|Fusilli|G|1.50|vn|d|Twisty pasta for salads and bakes.
Rice, Pasta & Grains|Egg Noodles|G|2.10|n|d|Thin wheat noodles for soups and stir-fries.
Rice, Pasta & Grains|Rice Noodles|G|2.30|gvn|d|Thin rice noodles without wheat for soups and stir-fries.
Rice, Pasta & Grains|Gluten-Free Pasta|G|3.20|gvn|d|Pasta made from corn and rice, without wheat.
Rice, Pasta & Grains|Couscous|G|1.90|vn|d|Tiny grains of semolina that are ready in five minutes.
Rice, Pasta & Grains|Quinoa|G|4.20|gvsn|d|A protein-rich seed that cooks like a grain.
Rice, Pasta & Grains|Bulgur Wheat|G|2.20|vn|d|Cracked wheat for salads and pilafs.
Rice, Pasta & Grains|Red Lentils|G|2.40|gvsn|d|Quick-cooking lentils for dal and soups.
Rice, Pasta & Grains|Green Lentils|G|2.50|gvsn|d|Firm lentils that keep their shape in salads and stews.
Rice, Pasta & Grains|Dried Chickpeas|G|2.60|gvsn|d|Dried chickpeas for hummus, curries and stews; soak overnight.
Rice, Pasta & Grains|Dried Black Beans|G|2.50|gvsn|d|Dried black beans for chilli and rice dishes.
Rice, Pasta & Grains|Plain Flour|K|1.70|vn|d|All-purpose wheat flour for baking and sauces.
Rice, Pasta & Grains|Rice Flour|G|2.30|gvsn|d|Fine flour from rice for gluten-free baking and thickening.
Rice, Pasta & Grains|Polenta|G|2.10|gvsn|d|Coarse cornmeal for creamy polenta and baking.
Rice, Pasta & Grains|Pearl Barley|G|1.90|vn|d|Chewy grain for soups and stews.
Pantry|Olive Oil|L|7.00|gvsn|d|Fruity olive oil for dressings and gentle cooking.
Pantry|Sunflower Oil|L|3.00|gvsn|d|A light oil for frying and baking.
Pantry|Coconut Oil|S|4.80|gvsn|d|Solid coconut oil for baking and curries.
Pantry|White Vinegar|L|1.20|gvsn|d|Sharp vinegar for pickling, cleaning and dressings.
Pantry|Soy Sauce|L|2.60|vn|d|Salty fermented sauce for stir-fries and dipping.
Pantry|Tomato Passata|TN|1.60|gvsn|d|Smooth sieved tomatoes for pasta sauces and soups.
Pantry|Tomato Ketchup|TN|2.20|gvn|l|Sweet tomato sauce for chips and sandwiches.
Pantry|Pasta Sauce|TN|2.50|gvn|d|A ready-made tomato and herb sauce for pasta.
Pantry|Mild Curry Paste|S|2.70|gvn|d|A jar of spices for a quick, mild curry.
Pantry|Coconut Milk|TN|2.10|gvsn|d|Creamy coconut milk for curries and soups.
Pantry|Chopped Tomatoes|TN|1.10|gvsn|d|Tinned tomatoes, a pantry staple for sauces and stews.
Pantry|Canned Chickpeas|TN|1.20|gvsn|l|Ready-cooked chickpeas for salads, hummus and curries.
Pantry|Canned Sweetcorn|TN|1.00|gvsn|l|Sweet corn kernels for salads and sandwiches.
Pantry|Canned Tuna|PR|2.30|gsn|l|Tuna chunks in water for sandwiches and salads.
Pantry|Baked Beans|TN|1.20|gvn|b|Beans in tomato sauce, classic on toast for breakfast.
Pantry|White Sugar|K|1.80|gvn|b|Fine white sugar for tea and baking.
Pantry|Brown Sugar|G|2.00|gvn|d|Soft brown sugar with a molasses flavour.
Pantry|Sea Salt|G|1.30|gvsn|d|Flaky salt for cooking and the table.
Pantry|Black Pepper|SP|2.40|gvsn|d|Ground black pepper for seasoning.
Pantry|Ground Cumin|SP|2.20|gvsn|d|Warm, earthy spice for curries and stews.
Pantry|Turmeric Powder|SP|2.10|gvsn|d|Golden spice that colours curries and rice.
Pantry|Smoked Paprika|SP|2.50|gvsn|d|Smoky red spice for stews, eggs and roast vegetables.
Pantry|Vegetable Stock Cubes|U6|1.60|vn|d|Cubes to add savoury depth to soups and rice.
Coffee & Tea|Ground Coffee|G|5.00|gvsn|b|Medium roast ground coffee for the morning pot.
Coffee & Tea|Instant Coffee|S|4.50|gvsn|b|A jar of instant coffee, ready with hot water.
Coffee & Tea|Coffee Beans|G|6.00|gvsn|b|Whole roasted beans for grinding fresh.
Coffee & Tea|Decaf Coffee|S|4.80|gvsn|b|Ground coffee without most of the caffeine.
Coffee & Tea|Black Tea Bags|TB|2.50|gvsn|b|Strong everyday black tea bags.
Coffee & Tea|Green Tea Bags|TB|2.90|gvsn|b|Light, fresh green tea bags.
Coffee & Tea|Peppermint Tea|TB|2.70|gvsn|s|Caffeine-free minty tea.
Coffee & Tea|Chamomile Tea|TB|2.80|gvsn|s|A calming, caffeine-free tea for evenings.
Coffee & Tea|Masala Chai Tea|TB|3.10|gvsn|b|Black tea blended with ginger, cardamom and cinnamon.
Coffee & Tea|Hot Chocolate Powder|G|3.50|gn|s|Cocoa powder with sugar, whisk into hot milk.
Coffee & Tea|Matcha Powder|S|7.50|gvsn|b|Finely ground green tea for whisking or lattes.
Snacks|Salted Crisps|G|1.80|gvn|s|Thin, crispy potato crisps with a little salt.
Snacks|Tortilla Chips|G|2.20|gvn|s|Crunchy corn chips for dipping.
Snacks|Popcorn|S|1.50|gvn|s|Light, crunchy popcorn for the sofa.
Snacks|Salted Peanuts|S|2.00|gvs|s|Roasted, salted peanuts to nibble.
Snacks|Cashew Nuts|S|4.60|gvs|s|Buttery cashews for snacking and cooking.
Snacks|Whole Almonds|S|4.20|gvs|s|Crunchy almonds with their skins on.
Snacks|Pretzels|S|1.90|vn|s|Salty baked twists.
Snacks|Rice Cakes|S|1.70|gvsn|b|Light puffed rice rounds for toppings, a quick breakfast or snack.
Snacks|Oat Biscuits|S|1.90|vn|s|Crumbly oat biscuits for tea time.
Snacks|Dark Chocolate|S|2.60|gvn|s|Dark chocolate with a rich, bitter flavour.
Snacks|Milk Chocolate|S|2.20|gn|s|Smooth milk chocolate bar.
Snacks|Trail Mix|S|3.30|gvs|s|Nuts, seeds and dried fruit for hikes and desks.
Snacks|Raisins|S|2.00|gvsn|b|Sweet dried grapes for porridge, baking and snacking.
Snacks|Seaweed Snacks|S|2.40|gvsn|s|Thin, crisp, lightly salted seaweed sheets.
Snacks|Hummus|S|2.10|gvn|l|Chickpea dip for pita, carrots and sandwiches.
Snacks|Crackers|S|1.80|vn|s|Crisp savoury crackers for cheese.
Snacks|Fruit Gummies|S|1.60|gn|s|Chewy fruit-flavoured sweets.
Drinks|Still Water|DR|0.80|gvsn|d|Plain still drinking water.
Drinks|Sparkling Water|DR|0.90|gvsn|d|Fizzy water, plain and unsweetened.
Drinks|Orange Juice|L|2.60|gvn|b|Orange juice that goes well with breakfast.
Drinks|Apple Juice|L|2.20|gvn|b|Clear, sweet apple juice.
Drinks|Mango Juice|L|2.70|gvn|s|A thick, sweet tropical juice.
Drinks|Tomato Juice|L|2.30|gvn|d|Savoury juice, good chilled with a squeeze of lemon.
Drinks|Cola-Style Soda|DR|1.60|gvn|s|A classic fizzy cola-style soft drink.
Drinks|Lemonade|DR|1.30|gvn|s|Fizzy lemon drink.
Drinks|Zero Sugar Cola|DR|1.60|gvsn|s|Cola-style soda with no sugar.
Drinks|Coconut Water|L|2.90|gvsn|s|Light, naturally sweet water from young coconuts.
Drinks|Iced Tea|L|1.90|gvn|s|Lemon-flavoured iced black tea.
Drinks|Ginger Beer|DR|1.80|gvn|s|A spicy, fizzy ginger drink.
Frozen|Frozen Peas|G|1.80|gvsn|d|Garden peas frozen at their sweetest.
Frozen|Frozen Sweetcorn|G|1.70|gvsn|d|Frozen corn kernels, ready in minutes.
Frozen|Frozen Mixed Vegetables|G|2.00|gvsn|d|A colourful mix to add to rice and stir-fries.
Frozen|Frozen Berries|G|3.60|gvsn|b|A mix of berries for smoothies and breakfast porridge.
Frozen|Frozen Mango Chunks|G|3.40|gvsn|s|Ripe mango pieces for smoothies and desserts.
Frozen|Oven Chips|K|2.80|vn|d|Potato chips to bake in the oven.
Frozen|Veggie Burgers|U4|3.30|vn|d|Plant-based patties to grill or fry.
Frozen|Fish Fingers|U6|3.00|n|d|Breaded white fish fingers, quick for the family.
Frozen|Margherita Pizza|PR|3.20|n|d|A stone-baked pizza with tomato and cheese.
Frozen|Vanilla Ice Cream|L|3.50|gn|s|Creamy vanilla ice cream.
Frozen|Mango Sorbet|L|3.60|gvn|s|A dairy-free frozen dessert.
Frozen|Vegetable Dumplings|PR|3.40|n|d|Steamed or fried dumplings with a vegetable filling.
Frozen|Toaster Waffles|U6|2.60|vn|b|Waffles to pop in the toaster for a quick breakfast.
Cleaning & Household|Dish Soap|L|2.50| | |Gentle washing-up liquid that cuts through grease.
Cleaning & Household|Laundry Liquid|L|5.50| | |Liquid detergent for everyday washing.
Cleaning & Household|Laundry Powder|K|6.20| | |Powder detergent for whites and colours.
Cleaning & Household|Fabric Softener|L|3.20| | |Leaves clothes soft and fresh.
Cleaning & Household|All-Purpose Cleaner|L|2.80| | |A spray for worktops, tables and tiles.
Cleaning & Household|Glass Cleaner|L|2.40| | |Streak-free spray for windows and mirrors.
Cleaning & Household|Floor Cleaner|L|3.00| | |Concentrated cleaner for hard floors.
Cleaning & Household|Bleach|L|1.90| | |Thick bleach for toilets and drains; follow the label.
Cleaning & Household|Limescale Remover|L|3.10| | |Dissolves limescale in kettles, taps and showers.
Cleaning & Household|Dishwasher Tablets|TAB|5.60| | |All-in-one tablets for the dishwasher.
Cleaning & Household|Kitchen Sponges|SPG|2.20| | |Scrubbing sponges for pots and plates.
Cleaning & Household|Bin Bags|BAG|2.90| | |Strong bags for the kitchen bin.
Cleaning & Household|Kitchen Towels|ROLL|3.40| | |Absorbent paper towels for spills.
Cleaning & Household|Toilet Paper|ROLL|4.20| | |Soft, strong toilet paper.
Cleaning & Household|Hand Soap|L|2.20| | |Gentle liquid soap for the sink.
Cleaning & Household|Hand Sanitiser|S|2.80| | |A quick-drying gel for hands on the go.
Cleaning & Household|Surface Wipes|WIPE|2.60| | |Disposable wipes for quick clean-ups.
Cleaning & Household|Aluminium Foil|FOIL|2.70| | |Foil for roasting, wrapping and baking.
Cleaning & Household|Cling Film|FOIL|2.50| | |Film to keep food fresh in the fridge.
Cleaning & Household|Baking Paper|FOIL|2.60| | |Non-stick paper for trays and tins.
Cleaning & Household|Sandwich Bags|BAG|2.00| | |Resealable bags for lunch boxes.
Cleaning & Household|Washing-Up Gloves|U4|2.10| | |Durable rubber gloves for the sink.
Cleaning & Household|Air Freshener|S|2.90| | |A light scent for the living room.
Cleaning & Household|Scourer Pads|SPG|1.90| | |Tough pads for burnt-on food.
""".strip().splitlines()

# Qualifiers: plain descriptions only (a size, a way of growing it), never a line or brand name.
# (descriptor shown after the item name, price factor, pack choice, sentence added to the note)
FOOD_QUALIFIERS = [
    ("Organic", 1.25, "mid", "Made with organic ingredients."),
    ("Small Pack", 0.80, "small", "The smallest pack, good for one or two people."),
    ("Family Pack", 1.00, "large", "The big pack, sized for a busy household."),
    ("Bulk Pack", 0.95, "large", "A bulk pack that works out cheaper per gram or litre."),
    ("Regular Pack", 1.00, "mid", "A regular pack for the weekly shop."),
    ("Twin Pack", 1.10, "mid", "Two in one pack, so you always have a spare."),
    ("Imported", 1.20, "any", "Imported from a region known for growing it."),
    ("Locally Grown", 1.12, "any", "Grown or made as close to home as the season allows."),
    ("Trial Pack", 0.90, "small", "A small trial pack to try before you buy more."),
]
HOME_QUALIFIERS = [
    ("Eco-Friendly", 1.20, "mid", "A gentler formula in recycled packaging."),
    ("Small Pack", 0.80, "small", "The smallest pack, good for a small home."),
    ("Family Pack", 1.00, "large", "The big pack, sized for a busy household."),
    ("Bulk Pack", 0.95, "large", "A bulk pack that works out cheaper per use."),
    ("Regular Pack", 1.00, "mid", "A regular pack for the weekly shop."),
    ("Fragrance-Free", 1.15, "any", "Fragrance-free, kinder to sensitive skin."),
    ("Concentrated", 1.30, "small", "A concentrated formula: a little goes a long way."),
    ("Heavy-Duty", 1.25, "any", "Extra strength for the toughest jobs."),
    ("Twin Pack", 1.10, "mid", "Two in one pack, so you always have a spare."),
]
