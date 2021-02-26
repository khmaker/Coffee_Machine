class CoffeeMachine:
    # TODO: Docstring
    ingredients = {
            'water': {
                    'order': 1,
                    'unit': 'ml',
                    },
            'milk': {
                    'order': 2,
                    'unit': 'ml',
                    },
            'coffee_beans': {
                    'order': 3,
                    'unit': 'grams',
                    },
            'disposable_cups': {
                    'order': 4,
                    'unit': '',
                    },
            }
    drinks_menu = {
            1: {
                    'name': 'espresso',
                    'ingredients': {
                            'water': 250,
                            'milk': 0,
                            'coffee_beans': 16,
                            'disposable_cups': 1
                            },
                    'money': 4,
                    },
            2: {
                    'name': 'latte',
                    'ingredients': {
                            'water': 350,
                            'milk': 75,
                            'coffee_beans': 20,
                            'disposable_cups': 1
                            },
                    'money': 7,
                    },
            3: {
                    'name': 'cappuccino',
                    'ingredients': {
                            'water': 200,
                            'milk': 100,
                            'coffee_beans': 12,
                            'disposable_cups': 1
                            },
                    'money': 6,
                    },
            }
    
    def __init__(self,
                 water: int,
                 milk: int,
                 coffee_beans: int,
                 disposable_cups: int,
                 money: int):
        self.water = water
        self.milk = milk
        self.coffee_beans = coffee_beans
        self.disposable_cups = disposable_cups
        self.money = money
    
    def action(self):
        # TODO: Docstring
        command = input('Write action (buy, fill, take, remaining, exit):\n')
        return self.dispatcher(command)
    
    def dispatcher(self, command: str):
        # TODO: Docstring
        commands = {
                'take': self.take,
                'buy': self.buy,
                'fill': self.fill,
                'remaining': self.remaining,
                'exit': self.exit,
                }
        if command not in commands:
            print('No such action\n')
            return self.action()
        return commands.get(command)()
    
    def take(self):
        # TODO: Docstring
        print(f'I gave you ${self.money}\n')
        self.money = 0
        return self.action()
    
    def buy(self):
        # TODO: Docstring
        menu = self.drinks_menu
        menu_items = ', '.join(f'{n} - {menu[n].get("name")}' for n in menu)
        message = ('What do you want to buy? '
                   f'{menu_items}, back - to main menu:\n')
        choice = input(message)
        if choice == 'back':
            return self.action()
        if choice in (str(item) for item in menu):
            return self.check_ingredients(choice)
        print('No such item in menu')
        return self.buy()
    
    def check_ingredients(self, choice: str):
        # TODO: Docstring
        choice = int(choice)
        drink_ingredients = self.drinks_menu[choice].get('ingredients')
        if drink_ingredients is None:
            print('No ingredients for this item\n')
            return self.buy()
        ingredients = self.ingredients
        for ingredient in sorted(ingredients,
                                 key=lambda y: ingredients[y].get('order')):
            need_ingredient = drink_ingredients.get(ingredient)
            have_ingredient = self.__getattribute__(ingredient)
            if need_ingredient is not None and have_ingredient is not None:
                if need_ingredient > have_ingredient:
                    print(f'Sorry, not enough {ingredient}!')
                    return self.action()
        
        print('I have enough resources, making you a coffee!\n')
        return self.make_drink(ingredients, drink_ingredients, choice)
    
    def make_drink(self,
                   ingredients: dict,
                   drink_ingredients: dict,
                   choice: int):
        # TODO: Docstring
        for ingredient in sorted(ingredients,
                                 key=lambda y: ingredients[y].get('order')):
            need_ingredient = drink_ingredients.get(ingredient)
            have_ingredient = self.__getattribute__(ingredient)
            self.__setattr__(ingredient,
                             have_ingredient - need_ingredient)
        have_money = self.__getattribute__('money')
        drink_price = self.drinks_menu[choice].get('money')
        self.__setattr__('money', have_money + drink_price)
        return self.action()
    
    def fill(self):
        # TODO: Docstring
        ingredients = self.ingredients
        for ingredient in sorted(ingredients,
                                 key=lambda y: ingredients[y].get('order')):
            unit = self.ingredients[ingredient].get('unit')
            self.filling_process(ingredient, unit)
        print()
        return self.action()
    
    def filling_process(self, ingredient: str, unit: str):
        # TODO: Docstring
        name = ingredient.replace('_', ' ')
        message = f'Write how many {unit} of {name} do you want to add:\n'
        amount_of_ingredient = input(message)
        try:
            amount_of_ingredient = int(amount_of_ingredient)
            if amount_of_ingredient < 0:
                raise ValueError
        except ValueError:
            print('Only positive integers allowed')
            return self.filling_process(ingredient, unit)
        
        current_amount_of_ingredient = self.__getattribute__(ingredient)
        self.__setattr__(ingredient,
                         current_amount_of_ingredient + amount_of_ingredient)
    
    def remaining(self):
        # TODO: Docstring
        print(f'The coffee machine has:')
        ingredients = self.ingredients
        for ingredient in sorted(ingredients,
                                 key=lambda y: ingredients[y].get('order')):
            print(f'{self.__getattribute__(ingredient)} of {ingredient}')
        print(f'${self.__getattribute__("money")} of money')
        print()
        return self.action()
    
    @staticmethod
    def exit():
        pass


if __name__ == '__main__':

    a = CoffeeMachine(400, 540, 120, 9, 550)
    a.action()
