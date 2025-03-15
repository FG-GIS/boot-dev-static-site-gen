import textnode as tn
def main():
    node = tn.TextNode("test",tn.TextType.BOLD)
    node2 = tn.TextNode("second test: link",tn.TextType.LINK,"https://www.boot.dev")

    print("Test 1:\n")
    print(node)
    print("-----------------------\nTest 2:\n")
    print(node2)
    print("\n")


main()