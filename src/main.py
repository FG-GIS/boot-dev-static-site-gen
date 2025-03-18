from file_handler import update_content,generate_page_recursive
import sys
def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    update_content()
    generate_page_recursive("./content","./template.html","./docs", basepath)
    return


main()