from django.test import TestCase

# Create your tests here.

id="kw"
name="input"
class_name="da"


def click(**kwargs):
    print(kwargs)
    # print(elem)
    # key = elem.split("=>")[0]
    # value = elem.split("=>")[1]
    #
    # if key == "id":
    #     driver.find_element_by_id(value)


click(id_="kw")
click(name="kw")
click(class_name="kw")





