from file_handler import update_content,generate_page_recursive
def main():
    update_content()
    generate_page_recursive("./content","./template.html","./public")
    return


main()