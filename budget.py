class Category:
    def __init__(self, category_name):
        self.category_name = category_name
        self.ledger = list()

    def deposit(self, amount, description=""):
        # add a record to the ledger list with an income
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        # make a negative deposit
        is_ok = self.check_funds(amount)
        if is_ok:
            amount *= -1
            self.deposit(amount, description)
            return True
        return False

    def get_balance(self):
        # return the balance of all movements
        amount_list = [movement["amount"] for movement in self.ledger]
        return sum(amount_list)

    def transfer(self, amount, budget):
        # return true if the transfer is done between to budget categories
        is_ok = self.check_funds(amount)

        if is_ok:
            self.withdraw(amount, f"Transfer to {budget.category_name}")
            budget.deposit(amount, f"Transfer from {self.category_name}")
            return True
        return False

    def check_funds(self, amount):
        # return true if the balance is bigger than the ammount
        current_balance = self.get_balance()
        if current_balance >= amount:
            return True
        return False

    def __str__(self):
        # print list of movements
        dot_numbers = (30 - len(self.category_name)) // 2
        title_decor = "*" * dot_numbers
        title = f"{title_decor}{self.category_name}{title_decor}\n"
        # description
        description = ""
        # define: description witdh 23 amount width 7
        for movement in self.ledger:
            des = movement["description"]
            if len(des) >= 23:
                des = des[:23]
            else:
                des = des.ljust(23)
            amnt = movement["amount"]
            amnt = "%.2f" % amnt  # add two decimals
            amnt = amnt.rjust(7)
            description += f"{des}{amnt}\n"
        # add the balance to the end of the println
        description += f"Total: {self.get_balance()}"

        return title + description


def create_spend_chart(categories):
    """print a spend chart based on the total spend in
    the categories list
    """
    # all of the variables will have the same order than the categories
    categ_spent = list()  # total spent for each category
    category_names = list()
    percent_display = list()  # percents rounded to the nearesth 10th

    # get the total spend from each category
    # and get the category names
    for category in categories:
        categ_spent.append(
            sum([mov["amount"] for mov in category.ledger if mov["amount"] < 0])
        )
        category_names.append(category.category_name)

    # get the total sum spent from all the categories
    total_spent = sum(categ_spent)
    # get percentage spent and round it to the nearesth 10th
    for spent in categ_spent:
        percent = (spent / total_spent) * 100
        # rount to the nearest then
        percent = round(percent // 10) * 10
        percent_display.append(percent)

    # ######## draw the bar chart ########

    # pencil is the line which will be draw depending de data
    # default is white space line
    pencil = list()
    for i in range(len(categories)):
        pencil.append("   ")

    string = "Percentage spent by category\n"  # this will be the final string

    # display the percentage numbers
    for i in reversed(range(0, 110, 10)):
        string += f"{i}".rjust(3) + "| "

        # edit pencil to display percents
        if i in percent_display:
            idx = percent_display.index(i)
            pencil[idx] = "o".ljust(3)

        string += "".join(pencil)
        string += "\n"

    # add the x axis
    string += "    -" + "---" * len(categories)

    # ##### display categories names #######

    # get the larger lenght word
    larger_w = len(max(category_names, key=len))
    i = 0
    while larger_w > i:
        for word in category_names:
            # get current  word indice
            idx = category_names.index(word)
            try:
                # add a letter to the current line
                pencil[idx] = word[i].ljust(3)
            except:
                # all word done, just add spaces
                pencil[idx] = "   "

        pencil_join = "".join(pencil)
        # the string adds spaces because there are no
        # percent numbers displaying
        string += f"\n     {pencil_join}"
        i += 1
    return string
