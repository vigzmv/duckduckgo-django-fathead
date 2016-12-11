import argparse

from bs4 import BeautifulSoup

ARGUMENT_PARSER = argparse.ArgumentParser()
ARGUMENT_PARSER.add_argument('--django-version')

DJANGO_HOME = 'https://www.djangoproject.com/'
DJANGO_DOC_URL = 'https://docs.djangoproject.com/en/{}'


class DjangoData(object):
    """
    Object responsible for loading raw HTML data for Django Docs
    """
    def __init__(self, page_name):
        """
        Initialize DjangoData object. Load data from HTML.

        """
        self.DJANGO_HTML = ""
        self.load_data(page_name)

    def load_data(self, page_name):
        """
        Open the HTML file and load it into the object.

        """
        with open('download/' + page_name, 'r') as data_file:
            self.DJANGO_HTML = data_file.read()

    def get_raw_data(self):
        """
        Returns: The raw HTML that was loaded.

        """
        return self.DJANGO_HTML


class DjangoDataParser(object):
    """
    Object responsible for parsing the raw HTML that contains Django Docs data
    """
    def __init__(self, raw_data, section_name, page_url):
        """
        Given raw data, get the relevant sections
        Args:
            raw_data: HTML data
        """
        self.parsed_data = None
        self.url = page_url

        soup_data = BeautifulSoup(raw_data, 'html.parser')
        doc_content = soup_data.find('div', {'id': 'docs-content'})

        tags = doc_content.find('div', {'class': 'section', 'id': section_name})
        self.tag_sections = tags.find_all('div', {'class': 'section'})


    def parse_name_and_anchor_from_data(self, section):
        """
        Find the name and anchor for a given section
        Args:
            section: A section of parsed HTML that represents a section

        Returns:
            name: Name of the Element
            anchor: Anchor tag to use when linking back to docs (ie #autoescape)

        """
        name = ''
        anchor = ''
        h3 = section.find('h3')
        if h3:
            code = h3.find('code', {'class': 'docutils'})
            if code:
                name = code.find('span', {'class': 'pre'}).string
            a_tag = h3.find('a', {'class': 'headerlink'})
            if a_tag:
                anchor = a_tag['href']

        return name, anchor

    def parse_first_paragraph_from_data(self, section):
        """
        Get the first paragraph for display
        Args:
            section: A section of parsed HTML that represents a Element

        Returns:
            First paragraph in the HTML

        """
        return section.find('p').text.replace('\n', ' ')

    def parse_second_paragraph_from_data(self, section):
        """
        Get the second paragraph for display
        Args:
            section: A section of parsed HTML that represents a Element

        Returns:
            second paragraph in the HTML

        """

        try:
            para = section.find_all('p')[1]
            para = para.text.partition(".")
            return ''.join(para[:2]).replace('\n',' ')
        except:
            return ''

    def parse_code_from_data(self, section):
        """
        Look for an example code block to output
        Args:
            section: A section of parsed HTML that represents a section

        Returns:
            Formatted code string
        """
        code = section.find('div', {'class': 'highlight'})
        if code:
            return '<pre><code>{}</code></pre>'.format(code.text.replace('\n', '\\n'))
        return ''

    def parse_for_data(self, code_or_second_para):
        """
        Main gateway into parsing the data. Will retrieve all necessary data elements.
        """
        data = []

        for section in (self.tag_sections):
            name, anchor = self.parse_name_and_anchor_from_data(section)
            first_paragraph = self.parse_first_paragraph_from_data(section)

            if code_or_second_para == "code":
                code = self.parse_code_from_data(section)
                second_paragraph = ''
            elif code_or_second_para == "para":
                second_paragraph = self.parse_second_paragraph_from_data(section)
                code = ''

            data_elements = {
                'name': name,
                'anchor': anchor,
                'first_paragraph': first_paragraph,
                'second_paragraph': second_paragraph,
                'code': code,
                'url': self.url
            }

            data.append(data_elements)

        self.parsed_data = data

    def get_data(self):
        """
        Get the parsed data.
        Returns:
            self.parsed_data: Dict containing necessary data elements
        """
        return self.parsed_data


class DjangoDataOutput(object):
    """
    Object responsible for outputting data into the output.txt file
    """
    def __init__(self, data):
        self.data = data

    def create_file(self):
        """
        Iterate through the data and create the needed output.txt file.

        """
        with open('output.txt', 'a+') as output_file:
            for data_element in self.data:
                if data_element.get('name'):
                    name = data_element.get('name')
                    code = data_element.get('code')
                    first_paragraph = '<p>' + data_element.get('first_paragraph') + '</p>'
                    second_paragraph = '<p>' + data_element.get('second_paragraph') + '</p>'
                    abstract = '{}{}{}'.format(first_paragraph + second_paragraph, '', code)
                    abstract = '<section class="prog__container">' + abstract + '</section>'
                    url = '{}{}'.format(data_element.get('url'), data_element.get('anchor'))
                    list_of_data = [
                        name,       # unique name will be the name of the element
                        'A',        # type is article
                        '',         # no redirect data
                        '',         # ignore
                        '',         # no categories
                        '',         # ignore
                        '',         # no related topics
                        '',         # ignore
                        DJANGO_HOME,# add an external link back to Django home
                        '',         # no disambiguation
                        '',         # images
                        abstract,   # abstract
                        url         # url to doc
                    ]
                    output_file.write('{}\n'.format('\t'.join(list_of_data)))


if __name__ == "__main__":
    args = ARGUMENT_PARSER.parse_args()
    if args.django_version:
        DJANGO_DOC_URL = DJANGO_DOC_URL.format(args.django_version)
    else:
        DJANGO_DOC_URL = DJANGO_DOC_URL.format('1.10')


    """
    The Complete Page Structure to be scrapped
        name: Downloaded file name
        sections: Sections in page
        code_or_second_para: Whether to get code or second_paragraph
    """
    page_structure = [
    {"Name":'builtins.html', "Sections":['built-in-tag-reference','built-in-filter-reference'],
    "Url":'/ref/templates/builtins/',"code_or_second_para":"code"},

    {"Name":'settings.html', "Sections":['core-settings','auth','messages','sessions','sites','static-files'],
    "Url":'/ref/settings/',"code_or_second_para":"para"},

    ]

    for page in page_structure:
        data = DjangoData(page["Name"])

        page_url = '{}{}'.format(DJANGO_DOC_URL,page["Url"])

        parser = []
        for section_name in page["Sections"]:
            parser.append(DjangoDataParser(data.get_raw_data(), section_name, page_url))

            for parsed in parser:
                parsed.parse_for_data(page["code_or_second_para"])
                output = DjangoDataOutput(parsed.get_data())
                output.create_file()
