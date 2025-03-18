from file_handler import update_content,generate_page
def main():
    update_content()
    generate_page("./content/index.md","./template.html","./public/index.html")
    return


main()