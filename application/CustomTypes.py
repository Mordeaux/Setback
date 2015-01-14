from sqlalchemy.ext.mutable import MutableComposite

class Hand(MutableComposite):
    def __init__(self, hand0, hand1, hand2, hand3, hand4, hand5):
        self.hand0 = hand0
        self.hand1 = hand1
        self.hand2 = hand2
        self.hand3 = hand3
        self.hand4 = hand4
        self.hand5 = hand5

    def __setattr__(self, key, value):
        "Intercept set events"

        # set the attribute
        object.__setattr__(self, key, value)

        # alert all parents to the change
        self.changed()

    def __composite_values__(self):
        return [self.hand0, self.hand1, self.hand2, self.hand3, self.hand4, self.hand5] 

    def __eq__(self, other):
        return isinstance(other, Hand) and \
            other.hand0 == self.hand0 and \
            other.hand1 == self.hand1 and \
            other.hand2 == self.hand2 and \
            other.hand3 == self.hand3 and \
            other.hand4 == self.hand4 and \
            other.hand5 == self.hand5

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(self.__composite_values__())

    def __iter__(self):
        yield self.hand0
        yield self.hand1
        yield self.hand2
        yield self.hand3
        yield self.hand4
        yield self.hand5

    def pop(self, card):
        if card in self.__composite_values__():
            if card == self.hand0:
                self.hand0 = None
                return card
            elif card == self.hand1:
                self.hand1 = None
                return card
            elif card == self.hand2:
                self.hand2 = None
                return card
            elif card == self.hand3:
                self.hand3 = None
                return card
            elif card == self.hand4:
                self.hand4 = None
                return card
            elif card == self.hand5:
                self.hand5 = None
                return card
