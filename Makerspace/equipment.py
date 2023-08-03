########################################################################
# Equipment
#
# The Equipment class is used to store relevant information about makerspace
# equipment from the database table called equipment. Additional functions
# convert this information into html. Use the function create_parameters()
# to create all necessary parameters needed in the render_template function
# to display the equipment html on the index.html page.
########################################################################
import database


# equipment class stores information about equipment from database table called equipment
class Equipment:
    def __init__(self, equipment_id, category, subcategory, equipment_name, quantity, description_file_name, image_file_name, is_visible):
        self._equipment_id = equipment_id
        self._category = category
        self._subcategory = subcategory
        self._equipment_name = equipment_name
        self._quantity = quantity
        self._description_file_name = description_file_name
        self._image_file_name = image_file_name
        self._is_visible = is_visible

    @property
    def equipment_id(self):
        return self._equipment_id

    @equipment_id.setter
    def equipment_id(self, equipment_id):
        self._equipment_id = equipment_id

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    @property
    def subcategory(self):
        return self._subcategory

    @subcategory.setter
    def subcategory(self, subcategory):
        self._subcategory = subcategory

    @property
    def equipment_name(self):
        return self._equipment_name

    @equipment_name.setter
    def equipment_name(self, equipment_name):
        self._equipment_name = equipment_name

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        self._quantity = quantity

    @property
    def description_file_name(self):
        return self._description_file_name

    @description_file_name.setter
    def description_file_name(self, description_file_name):
        self._description_file_name = description_file_name

    @property
    def image_file_name(self):
        return self._image_file_name

    @image_file_name.setter
    def image_file_name(self, image_file_name):
        self._image_file_name = image_file_name

    @property
    def is_visible(self):
        return self._is_visible

    @is_visible.setter
    def is_visible(self, is_visible):
        self._is_visible = is_visible

    def __str__(self):
        return f'id: {self.equipment_id}; category: {self.category}; subcategory: {self.subcategory}; equipment name: ' \
               f'{self.equipment_name}; quantity: {self.quantity}; description filename: {self.description_file_name}; ' \
               f'image filename: {self.image_file_name}; is_visible: {self.is_visible}'


# takes the name of a txt file
# open a file and read it as a string
def readFile(filename):
    with open(filename + '.txt') as file:
        text_list = [line.strip() for line in file.readlines()]
    text = ''
    for line in text_list:
        text = text + line
    return text


# connect to makerspace database and return all equipment
def connect_to_database():
    mydb, my_cursor = database.connect_to_database()
    my_cursor.execute("SELECT * FROM equipment")
    equipment = my_cursor.fetchall()

    return equipment


# fetch equipment from database and create a list of equipment objects populated with information from database
# [0] equipment_id, [1] category, [2] subcategory, [3] equipment_name, [4] quantity
# [5] description_file_name, [6] image_file_name, [7] created, [8] last_modified, [9] is_visible
# returns a list of equipment objects
def create_equipment():
    equipment = connect_to_database()
    equipment_objects = []
    for item in equipment:
        equipment_objects.append(Equipment(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[9]))

    return equipment_objects


# takes the equipment category and a list of equipment objects
# create and return html for images
def create_image_html(category, equipment_list):
    image_html = ''
    visibility = 'block'
    for equipment in equipment_list:
        if equipment.category == category:
            image_html = image_html + f'<img id="image_{equipment.equipment_id}" src="static/images/{equipment.image_file_name}.png" class="card-img-top" ' \
                                      f'style="display: {visibility};" alt="..." />'
            visibility = 'none'
    return image_html


# takes the equipment category and a list of equipment objects
# create and return html for titles
def create_title_html(category, equipment_list):
    title_html = ''
    visibility = 'block'
    for equipment in equipment_list:
        if equipment.category == category:
            title_html = title_html + f'<h5 class="card-title" style="display: {visibility};" id="title_{equipment.equipment_id}">' \
                                      f'{equipment.category} - {equipment.subcategory}</h5>'
            visibility = 'none'
    return title_html


# takes the equipment category and a list of equipment objects
# create and return html for descriptions
def create_description_html(category, equipment_list):
    description_html = ''
    visibility = 'block'
    for equipment in equipment_list:
        if equipment.category == category:
            filename = "static/equipment_descriptions/description_" + f"{equipment.equipment_id}"
            description_html = description_html + f'<p class="card-text" id="description_{equipment.equipment_id}" ' \
                                                  f'style="display: {visibility};">' \
                                                  f'{readFile(f"{filename}")}</p>'
            visibility = 'none'
    return description_html


# takes the equipment category and a list of equipment objects
# create and return html for radio buttons
def create_radio_btn_html(category, equipment_list):
    radio_buttons_html = ''
    checked = 'checked'
    if category == 'Design, Prototyping, and Testing':
        class_name = "DPT"
    elif category == 'Fabrication':
        class_name = "fabrication"
    elif category == 'Assembly':
        class_name = "assembly"
    elif category == 'Production':
        class_name = "production"
    else:
        class_name = "other"
    for equipment in equipment_list:
        if equipment.category == category:
            radio_buttons_html = radio_buttons_html + f'<input type="radio" class="btn-check {class_name}" ' \
                                                      f'name="vbtn-radio-{class_name}" ' \
                                                      f'onclick="showImage(this.id, this.className)" ' \
                                                      f'id="{equipment.equipment_id}" ' \
                                                      f'autocomplete="off" {checked}><label class="btn" ' \
                                                      f'for="{equipment.equipment_id}">' \
                                                      f'{equipment.subcategory}</label>'
            checked = ''
    return radio_buttons_html


# creates all html needed to display equipment
# returns a dictionary with all the parameters needed in the render_template function
def create_parameters():
    # create equipment class list
    database_equipment = create_equipment()

    ########## create 'Design, Prototyping, and Testing' html #########
    # create html to display images
    DPT_image_html = create_image_html('Design, Prototyping, and Testing', database_equipment)
    # create titles html
    DPT_title_html = create_title_html('Design, Prototyping, and Testing', database_equipment)
    # create description html
    DPT_descriptions_html = create_description_html('Design, Prototyping, and Testing', database_equipment)
    # create html for radio buttons
    DPT_radio_btn_html = create_radio_btn_html('Design, Prototyping, and Testing', database_equipment)

    ###################### create 'Fabrication' html ##################
    # create html to display images
    Fabrication_image_html = create_image_html('Fabrication', database_equipment)
    # create titles html
    Fabrication_title_html = create_title_html('Fabrication', database_equipment)
    # create description html
    Fabrication_descriptions_html = create_description_html('Fabrication', database_equipment)
    # create html for radio buttons
    Fabrication_radio_btn_html = create_radio_btn_html('Fabrication', database_equipment)

    #################### create 'Assembly' html #######################
    # create html to display images
    Assembly_image_html = create_image_html('Assembly', database_equipment)
    # create titles html
    Assembly_title_html = create_title_html('Assembly', database_equipment)
    # create description html
    Assembly_descriptions_html = create_description_html('Assembly', database_equipment)
    # create html for radio buttons
    Assembly_radio_btn_html = create_radio_btn_html('Assembly', database_equipment)

    ################# create 'Production' html ########################
    # create html to display images
    Production_image_html = create_image_html('Production', database_equipment)
    # create titles html
    Production_title_html = create_title_html('Production', database_equipment)
    # create description html
    Production_descriptions_html = create_description_html('Production', database_equipment)
    # create html for radio buttons
    Production_radio_btn_html = create_radio_btn_html('Production', database_equipment)

    ############### create dictionary of parameters ###################
    equipment_dictionary = {'DPT_image_html': DPT_image_html, 'DPT_radio_btn_html': DPT_radio_btn_html,
                            'DPT_title_html': DPT_title_html, 'DPT_descriptions_html': DPT_descriptions_html,
                            'Fabrication_image_html': Fabrication_image_html, 'Fabrication_title_html': Fabrication_title_html,
                            'Fabrication_descriptions_html': Fabrication_descriptions_html,
                            'Fabrication_radio_btn_html': Fabrication_radio_btn_html, 'Assembly_image_html': Assembly_image_html,
                            'Assembly_title_html': Assembly_title_html, 'Assembly_descriptions_html': Assembly_descriptions_html,
                            'Assembly_radio_btn_html': Assembly_radio_btn_html, 'Production_image_html': Production_image_html,
                            'Production_title_html': Production_title_html, 'Production_radio_btn_html': Production_radio_btn_html,
                            'Production_descriptions_html': Production_descriptions_html}
    return equipment_dictionary


if __name__ == '__main__':
    # EXAMPLE to create list of equipment objects
    equipment_objs = create_equipment()

    # EXAMPLE to show how the html is formatted
    print(f"example of image html:\n{create_image_html('Design, Prototyping, and Testing', equipment_objs)}\n")
    print(f"example of radio button html:\n{create_radio_btn_html('Design, Prototyping, and Testing', equipment_objs)}\n")
    print(f"example of title html:\n{create_title_html('Design, Prototyping, and Testing', equipment_objs)}\n")
    print(f"example of description html:\n{create_description_html('Design, Prototyping, and Testing', equipment_objs)}\n")

    # EXAMPLE to show the dictionary of parameters
    print(f"example of dictionary:\n{create_parameters()}\n")
