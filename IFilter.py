

# email -> bool
class IFilter:
    def filter(self, mail) -> bool:
        """
        mail is a mail object parsed by email.parser.BytesParser
        read object mail and return whether or not it is what you need
        (like curse forge update mail)
        """
        pass
