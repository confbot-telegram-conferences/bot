def message_recieved(sender, **kwargs):
    print("\n---------- Message in ----------")
    print(kwargs)


def message_sent(sender, **kwargs):
    print("\n---------- Message out ----------")
    print(kwargs)
